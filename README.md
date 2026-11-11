# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **`POST /submit` arrives** (`app.py::submit`) with `text` and `creator_id`.
2. **Input check.** Missing, blank, too-short or oversized text is refused
   with a `400`/`413`, and the refusal is logged.
3. **A `content_id` is minted.** This is the handle the writer uses later to appeal.
4. **Signal one** (`detector.py::model_signal`): how predictable gpt2 finds
   the text → `model_score`.
5. **Signal two** (`stylometry.py::style_signal`): the shape of the text
   (sentence-length spread, word variety, punctuation) → `style_score`.
6. **Combine and label** (`scoring.py::combine_signals`, `score_to_label`):
   one `confidence` score, mapped to a `guess` and a plain-English `label`.
7. **Log and respond.** Everything, including both signal scores, is written to
   `logs/audit.jsonl` and returned to the caller.

If the writer disagrees, `POST /appeal` with the `content_id` and their
reasoning appends an `under_review` entry next to the original decision.

Full design notes and endpoint contracts: [design.md](design.md).


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** predictability. That is gpt2's perplexity on the text,
squashed to 0–1 so that low perplexity gives a high (more AI-like) score.

**Why that might differ between human and AI writing:** a language model
writes by picking likely next words, so its output is text a model finds easy
to predict. Human writing has more odd word choices and specific details.

**What it can't see:** authorship. Predictable ≠ machine-written. Plain
writing with common words and short sentences (second-language writers,
younger writers, anyone writing simply) scores as AI-like. Ornate, rare-word
prose scores as human even when a model wrote it. It reads only the first 400
tokens and is noisy on short text.

### Signal two — the style signal

**What it measures:** the text's surface shape, without reading it:
sentence-length spread (std dev / mean), type-token ratio (unique / total
words), and density of varied punctuation (`; : — ( ) ! ?`).

**Why that might differ between human and AI writing:** generated prose
tends toward even, mid-length sentences, a safe vocabulary and plain
punctuation. Human writing is lumpier.

**What it can't see:** meaning. Changes to shape that leave the substance
alone move it: added typos, chopped or merged sentences, sprinkled dashes, a
pasted quotation. It is length-sensitive (type-token ratio falls on long
text, and spread means nothing with one or two sentences). It also reads a
human with a deliberately tidy, even style as AI-like.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**How the style signal is built** (`stylometry.py::style_signal`): each
measure is flipped so higher = more AI-like, then mapped linearly onto 0–1
between a "very AI" and a "very human" anchor and clamped:

| Measure | Raw value | Scores 1.0 (AI) at | Scores 0.0 (human) at | Weight |
|---|---|---|---|---|
| Sentence-length spread | stdev / mean of words per sentence | 0.20 | 0.70 | 0.5 |
| Type-token ratio | moving-average TTR, 50-word window | 0.60 | 0.85 | 0.2 |
| Punctuation density | `; : — – ( ) ! ? --` per word | 0.00 | 0.05 | 0.3 |

With fewer than 3 sentences, spread is scored neutral (0.5), because "no
spread to measure" is not evidence of AI. TTR is weighted lowest because it
ran the wrong way in calibration (see below).

**The rule:**

1. Take the weighted average of the two signals.
2. If the signals disagree, pull the average halfway back toward 0.5. Two
   methods disagreeing is uncertainty.
3. What counts as "disagree" is asymmetric. An AI-leaning average (above 0.5)
   is softened when the gap is over **0.30**. A human-leaning one is softened
   only when the gap is over **0.50**. Accusing someone takes more agreement
   than clearing them, because the false positive is the expensive error.
   The human side still has a limit, because sprinkling punctuation into AI
   text can push the style signal to 0 by itself.

**The numbers** (in `config.py`):

| Setting | Value |
|---|---|
| `WEIGHT_MODEL_SIGNAL` | 0.5 |
| `WEIGHT_STYLE_SIGNAL` | 0.5 |
| `DISAGREEMENT_GAP_AI` | 0.30 |
| `DISAGREEMENT_GAP_HUMAN` | 0.50 |
| `DISAGREEMENT_SHRINK` | 0.5 (distance from 0.5 is halved) |

Equal weights because neither signal earned more trust. The style signal
separated my calibration texts more widely, but it is also the cheapest to
game. The detector's perplexity midpoint (45) is unchanged.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**Calibration run** (both signals, then combined; scored through `POST /submit`):

| Input | Perplexity | model_score | spread | TTR | punct | style_score | confidence |
|---|---|---|---|---|---|---|---|
| Clearly AI (unedited chatbot-style paragraph) | 14.6 | 0.858 | 0.294 | 0.911 | 0.000 | 0.706 | **0.782** |
| Clearly human (my grandmother/buttons piece) | 45.5 | 0.496 | 0.903 | 0.892 | 0.030 | 0.118 | **0.307** |
| Plain human (short, even sentences, simple words) | 11.2 | 0.902 | 0.270 | 0.774 | 0.000 | 0.791 | **0.847** |
| Lightly-edited AI (the AI text, reworded casually) | 22.9 | 0.747 | 0.469 | 0.858 | 0.013 | 0.454 | **0.600** |
| Gamed AI (the AI text + `; ! ( ) -- :` sprinkled in) | — | 0.621 | — | — | — | 0.000 | **0.405** |

What I learned from it:

- **Clearly AI and clearly human separate by 0.475**, which is above my
  criterion-2 target of 0.30.
- **Plain human writing scores higher than clearly-AI text on both signals.**
  This is the Ana case from [design.md](design.md), confirmed. Both signals
  share the blind spot, so they *agree*, and no combining rule built from
  these two signals can pull it apart. That has to be handled by where the AI
  threshold sits and how the labels are worded (Milestone 5). Criterion 1
  would fail for that paragraph under the starter's 0.65 AI threshold, which
  is why Milestone 5 moved it to 0.90 (see Label Variants).
- **Type-token ratio ran backwards.** The AI text had the *most* varied
  vocabulary (0.911) and the plain human text the least (0.774). All it
  reliably detects is plain writing, so I cut its weight to 0.2.
- **Sentence-length spread did the real work.** It was 0.90 for the human
  piece vs 0.27–0.29 for the AI and plain pieces.

**A case where my two signals split, and what my rule does with it:**

*Gamed AI.* I took the clearly-AI paragraph and added semicolons, an
exclamation mark, a parenthetical, a dash and two fragments, without
changing what it says. The style signal dropped from 0.706 to **0.000**. The
model signal still read it as fairly predictable at **0.621**. The plain
average is 0.31, which would have been a confident "human" verdict on AI text.
My first version of the rule only softened AI-leaning scores, and it let
this through (that run is in the log at 0.310). With the human-side gap limit,
the 0.62 gap triggers the shrink: 0.5 + (0.31 − 0.5) × 0.5 = **0.405**, which
lands in unsure.

The real human piece also splits (0.496 vs 0.118, gap 0.38), but that gap is
under the 0.50 human-side limit, so it keeps its 0.307. Telling these two
apart is the whole reason the two limits differ.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

The text lives in `scoring.py` (`LABEL_HUMAN`, `LABEL_UNSURE`, `LABEL_AI`) and
`scoring.py::score_to_label` picks one. Thresholds are in `config.py`
(`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.90`). Every score from 0 to 1
maps to exactly one label: `≤ 0.35` is human, `≥ 0.90` is AI, everything
between is unsure.

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing. |
| unsure | 0.35 – 0.90 | We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong. |
| high-confidence AI | 0.90 – 1.00 | This writing closely matches patterns we often see in AI-generated text. Our check can be wrong, and simple, even writing by real people can look like this too. If you wrote it yourself, you can appeal and a person will review it. |

**Why the AI threshold is 0.90 and not 0.65:** in calibration, plain human
writing (short, even sentences, common words) scored **0.85–0.885**, as high
as ordinary chatbot paragraphs (**0.80–0.89**). My formal cover-letter paragraph
scored 0.72. Both signals share this blind spot, so the threshold is the only
place left to protect those writers, and criterion 1 allows zero of them to be
called AI. At 0.90 all of them land in unsure. The cost is real: most ordinary
AI text also lands in unsure, and only very formulaic output (0.93–0.96 in
calibration) reaches the AI label. That's the trade I chose in
[design.md](design.md): a missed AI essay costs the site a little, and a wrong
accusation costs a writer a lot. The margin is thin. 0.885 is close to 0.90,
so a slightly plainer human piece could still cross it.

**Reachability check** (all three through `POST /submit`, full responses under
Sample Run):

| Input | model_score | style_score | confidence | Label |
|---|---|---|---|---|
| My bus-stop paragraph (casual, uneven, dialogue) | 0.573 | 0.110 | 0.341 | human |
| Plain human paragraph (short, even sentences) | 0.861 | 0.909 | 0.885 | unsure |
| Formulaic AI paragraph about drinking water | 0.953 | 0.965 | 0.959 | AI |

**Why I worded the "unsure" one this way:** the person reading it may well
have written every word, and given my threshold, most people who see it *did*.
So it says plainly that we aren't making a call. It names the kinds of writing
that end up there (plain, formal), so a careful writer doesn't take it as a
judgement on their style. It ends with "not a sign that anything is wrong" so
it can't be read as a softer accusation. It doesn't mention the appeal, because
there is nothing to appeal: the item isn't marked as AI.

**Why the AI one names the appeal:** it's the only label that accuses anyone,
so it says the check can be wrong, names the exact kind of human writing that
trips it, and tells the writer what they can do.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

*Milestone 3 run: signal one only. `style_score`, `confidence` and `label`
are placeholders until Milestones 4–5.*

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "My grandmother kept a jar of buttons on the windowsill, and every Sunday I would tip it out onto the rug and sort them by color while she yelled at the Padres on the radio. There was one brass button shaped like an anchor. Nobody knew where it came from.", "creator_id": "luis_v"}'
```

```json
{"confidence":0.4661,"content_id":"e21fb289-49b3-4434-be24-62d55136835f","creator_id":"luis_v","guess":"unsure","label":"PLACEHOLDER: label text arrives in Milestone 5.","model_score":0.4661,"status":"decided","style_score":null}
```

**Bad input is refused, and the refusal is logged**

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "   ", "creator_id": "luis_v"}'
{"error":"missing_text","message":"'text' is required and can't be blank."}          # 400
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "Too short.", "creator_id": "luis_v"}'
{"error":"text_too_short","message":"'text' needs at least 20 words to judge fairly."} # 400
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "hello"}'
{"error":"missing_creator_id","message":"'creator_id' is required and can't be blank."} # 400
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '[1,2]'
{"error":"invalid_json","message":"Send a JSON object with 'text' and 'creator_id'."}  # 400
# 25,000 characters of text:
{"error":"text_too_long","message":"'text' can be at most 20,000 characters."}         # 413
```

**The log after that run**

```bash
$ curl "http://127.0.0.1:5000/log?limit=7"
```

```json
{"count":6,"entries":[
  {"combined_score":0.4661,"content_id":"e21fb289-49b3-4434-be24-62d55136835f","creator_id":"luis_v","guess":"unsure","label":"PLACEHOLDER: label text arrives in Milestone 5.","model_score":0.4661,"status":"decided","style_score":null,"timestamp":"2026-11-04T06:03:18+00:00"},
  {"creator_id":"luis_v","event":"rejected","reason":"missing_text","status":"rejected","timestamp":"2026-11-04T06:03:18+00:00"},
  {"creator_id":"luis_v","event":"rejected","reason":"text_too_short","status":"rejected","text_length":10,"timestamp":"2026-11-04T06:03:18+00:00"},
  {"creator_id":"unknown","event":"rejected","reason":"missing_creator_id","status":"rejected","timestamp":"2026-11-04T06:03:18+00:00"},
  {"creator_id":"unknown","event":"rejected","reason":"invalid_json","status":"rejected","timestamp":"2026-11-04T06:03:18+00:00"},
  {"creator_id":"luis_v","event":"rejected","reason":"text_too_long","status":"rejected","text_length":25000,"timestamp":"2026-11-04T06:03:18+00:00"}
]}
```

**Milestone 5 run: all three labels.** Each body was saved to a file and sent
with `--data-binary`, because the texts have quotes and dashes in them.

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" --data-binary @human.json
# {"text": "The 7 bus was late again — twenty minutes, in the rain, with no shelter. A guy next to me was eating sunflower seeds and spitting the shells into a Big Gulp cup. I asked him how long he'd been waiting. \"Since Tuesday,\" he said, deadpan. I laughed so hard I almost missed the bus when it finally showed up. Worth it? Honestly, yes.", "creator_id": "luis_v"}
```

```json
{"confidence":0.3414,"content_id":"a87470b4-42e0-4efc-8d2e-cb0b7cdeee36","creator_id":"luis_v","guess":"human","label":"We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing.","model_score":0.5732,"status":"decided","style_score":0.1095}
```

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" --data-binary @unsure.json
# {"text": "I live in San Diego with my family. I go to school every day. I like my classes a lot. My favorite class is math. I study at the library after school. Then I take the bus home. I help my mom make dinner. We eat together at the table. After dinner I do my homework. I go to bed at ten.", "creator_id": "luis_v"}
```

```json
{"confidence":0.8849,"content_id":"d1e64954-6ab1-4321-9b33-ff05fe2e2ceb","creator_id":"luis_v","guess":"unsure","label":"We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.","model_score":0.8609,"status":"decided","style_score":0.9089}
```

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" --data-binary @ai.json
# {"text": "Water is essential for all living things on the planet. It is important for people to drink enough water every day. Water helps the body to stay healthy and work properly. It also helps to regulate the temperature of the body. Many people do not drink enough water each day. It is important to make sure that you drink enough water every day. Drinking water is one of the best ways to stay healthy.", "creator_id": "luis_v"}
```

```json
{"confidence":0.9587,"content_id":"c2cd4ce5-79cb-4ce7-943e-dfefe0becbcf","creator_id":"luis_v","guess":"ai","label":"This writing closely matches patterns we often see in AI-generated text. Our check can be wrong, and simple, even writing by real people can look like this too. If you wrote it yourself, you can appeal and a person will review it.","model_score":0.9527,"status":"decided","style_score":0.9648}
```

**An appeal**

This appeals the AI-labelled submission above. The reasoning is a test
message, written the way a wrongly flagged writer might put it.

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c2cd4ce5-79cb-4ce7-943e-dfefe0becbcf", "reasoning": "I wrote this myself for a 5th-grade health class handout. It is simple on purpose because the readers are ten years old."}'
```

```json
{"appealed_at":"2026-11-04T06:25:49+00:00","content_id":"c2cd4ce5-79cb-4ce7-943e-dfefe0becbcf","message":"Thanks — your appeal is recorded and a person will review this piece. Until then it is marked as under review, not as AI-written.","original_guess":"ai","status":"under_review"}
```

**Appeals that should fail, and do**

```bash
# same content_id again
{"error":"already_under_review","message":"This piece already has an appeal on record, and a person will review it."}   # 409
# "content_id": "not-a-real-id"
{"error":"unknown_content_id","message":"No submission with content_id 'not-a-real-id'. Check the id from your submit response."}   # 404
# "reasoning": "   "
{"error":"missing_reasoning","message":"Tell us why you think we got it wrong."}   # 400
# no content_id
{"error":"missing_content_id","message":"'content_id' is required and can't be blank."}   # 400
# body is [1]
{"error":"invalid_json","message":"Send a JSON object with 'content_id' and 'reasoning'."}   # 400
```

None of the failed appeals wrote a log entry. The log below shows only the
one successful appeal.

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=4"
```

```json
{"count":4,"entries":[
  {"combined_score":0.3414,"content_id":"a87470b4-42e0-4efc-8d2e-cb0b7cdeee36","creator_id":"luis_v","guess":"human","label":"We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing.","model_score":0.5732,"status":"decided","style_score":0.1095,"timestamp":"2026-11-04T06:25:13+00:00"},
  {"combined_score":0.8849,"content_id":"d1e64954-6ab1-4321-9b33-ff05fe2e2ceb","creator_id":"luis_v","guess":"unsure","label":"We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.","model_score":0.8609,"status":"decided","style_score":0.9089,"timestamp":"2026-11-04T06:25:14+00:00"},
  {"combined_score":0.9587,"content_id":"c2cd4ce5-79cb-4ce7-943e-dfefe0becbcf","creator_id":"luis_v","guess":"ai","label":"This writing closely matches patterns we often see in AI-generated text. Our check can be wrong, and simple, even writing by real people can look like this too. If you wrote it yourself, you can appeal and a person will review it.","model_score":0.9527,"status":"decided","style_score":0.9648,"timestamp":"2026-11-04T06:25:14+00:00"},
  {"content_id":"c2cd4ce5-79cb-4ce7-943e-dfefe0becbcf","creator_id":"luis_v","event":"appeal","reasoning":"I wrote this myself for a 5th-grade health class handout. It is simple on purpose because the readers are ten years old.","status":"under_review","timestamp":"2026-11-04T06:25:49+00:00"}
]}
```

The original `ai` decision is still there, unchanged. The appeal sits after it
with the same `content_id` and `status: "under_review"`.

---

## How I Used AI

**Moment 1: naming the blind spots and tracing the false positive (Milestone 1)**

- *What I asked for:* help tracing a submission from `POST /submit` to the
  label, naming what each of my two signals measures and what it can't see,
  and drafting the endpoint contracts. That became [design.md](design.md).
- *What came back:* a step-by-step path through `app.py`, `detector.py`,
  `stylometry.py`, `scoring.py` and `audit.py`, a blind spot for each signal,
  and request/response tables for both endpoints.
- *What I changed:* I made the blind spots specific to the people they would
  hurt. "Predictable ≠ machine-written" became second-language and younger
  writers, and I wrote the Ana trace around that. Walking her through the
  starter's 0.65 AI threshold is what showed me that both signals share the
  plain-writing blind spot, so their agreement can't count as certainty. That
  set the direction for everything after it: a high AI threshold and a wide
  unsure band. I also added the error table (`400`/`404`/`409`/`413`) and the
  20-word minimum to the contract, so very short text never gets a confident
  label.

**Moment 2: the combining rule (Milestone 4)**

- *What I asked for:* help writing `scoring.py::combine_signals` from my
  written rule: a 50/50 weighted average, pulled back toward 0.5 when the
  signals disagree, with disagreement judged more strictly on the AI side.
- *What came back:* a version that only softened **AI-leaning** scores, which
  matched my "accusing takes more agreement" reasoning. Human-leaning scores
  were never touched.
- *What I changed:* I tested it against my "gamed AI" input, which is the AI
  paragraph with semicolons, an exclamation mark, a parenthetical and dashes
  sprinkled in. The style signal fell to 0.000, the model signal stayed at
  0.621, and the rule passed the 0.31 average straight through as a confident
  human verdict on AI text. You can see it in the log at 06:18:21
  (`combined_score: 0.3103`). I added a second, looser gap limit for the human
  side (`DISAGREEMENT_GAP_HUMAN = 0.50` next to `DISAGREEMENT_GAP_AI = 0.30`).
  The same input now lands in unsure at 0.405 (log, 06:19:27). My real human
  piece, with a 0.38 gap, still keeps its 0.307 human score.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
A writer revising a passage might resubmit every 15–20 seconds during a burst of small edits, so 5 per minute allows that without much waiting. 50 per day allows several rounds of revision across a few pieces of writing, which is more than I'd expect most writers to need. A script is limited to 50 submissions per day per `creator_id`, so testing 1,000 variations under one ID would take 20 days.

**What a caller counts as:** <!-- per address, or per creator_id? They fail differently — one script can look like a thousand callers, and one household can look like one. -->
A caller counts per `creator_id`, falling back to IP address when it's missing or blank. A script that changes its `creator_id` on each request gets around both limits.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

Run with `python run_attacks.py --set attack_set --label before` on 2026-11-10 against
`app.py::submit`, with rate limiting on (5/minute, 50/day) and thresholds at
`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.90`. Full output:
[results/attack_run_2026-11-10_2145_before.md](results/attack_run_2026-11-10_2145_before.md).
Audit log for the run: [results/audit_extract.json](results/audit_extract.json) and
`logs/audit.jsonl` (lines 42–97).

56 attacks sent. **No crashes and no 5xx.** Every request left exactly one audit
log entry (log went from 41 to 97 lines).

**How I marked them** — HELD/BROKE is judged against what each family was going for:

- **evasion** (AI text trying to pass): BROKE if labeled `human`.
- **false_positive** (human text trying to get flagged): BROKE if labeled `ai`.
- **prompt_injection**: BROKE if the instruction got the result it asked for
  (a `human` label, a changed label text, or a malformed log entry).
- **malformed**: BROKE on a 5xx, a crash, or no response.
- **flood_same_creator**: BROKE if the limiter let the flood through.

| ID | Family | Targeting | Status | Guess | Model | Style | Score | Verdict |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.164 | 0.800 | 0.491 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | **human** | 0.594 | 0.102 | 0.348 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.666 | 0.443 | 0.555 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.611 | 0.800 | 0.706 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | **human** | 0.321 | 0.252 | 0.286 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.573 | 0.301 | 0.437 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.586 | 0.254 | 0.420 | HELD |
| EV08 | evasion | signal one: text below the token window | 400 | — | — | — | — | HELD (rejected `text_too_short`) |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.704 | 0.533 | 0.618 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | unsure | 0.979 | 0.806 | 0.893 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.618 | 0.578 | 0.598 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.739 | 0.824 | 0.781 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.805 | 0.696 | 0.751 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.833 | 0.657 | 0.745 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.801 | 0.903 | 0.852 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.881 | 0.556 | 0.609 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.882 | 0.500 | 0.595 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 | — | — | — | — | HELD (rejected `text_too_short`) |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.463 | 0.337 | 0.400 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | **human** | 0.204 | 0.215 | 0.210 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.594 | 0.357 | 0.476 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.500 | 0.368 | 0.434 | HELD (label text unchanged) |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.640 | 0.250 | 0.445 | HELD (log entry well-formed; text is not logged) |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.558 | 0.585 | 0.572 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | HELD (`missing_text`) |
| MF02 | malformed | text is a single character | 400 | — | — | — | — | HELD (`text_too_short`) |
| MF03 | malformed | text is control characters | 400 | — | — | — | — | HELD (`text_too_short`) |
| MF04 | malformed | text is only punctuation | 400 | — | — | — | — | HELD (`text_too_short`) |
| MF05 | malformed | text is a very long single word | 400 | — | — | — | — | HELD (`text_too_short`, 4000 chars) |
| MF06 | malformed | text is emoji only | 400 | — | — | — | — | HELD (`text_too_short`) |
| MF07 | malformed | text is right-to-left script | 400 | — | — | — | — | HELD (`text_too_short`) |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | — | — | HELD (`text_too_long`) |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | HELD (`missing_text`) |
| RQ02 | malformed | no creator_id | 400 | — | — | — | — | HELD (`missing_creator_id`) |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | HELD (`missing_text`) |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | HELD (`missing_text`) |
| RQ05 | malformed | text is null | 400 | — | — | — | — | HELD (`missing_text`) |
| RQ06 | malformed | creator_id is an object | 400 | — | — | — | — | HELD (`missing_creator_id`) |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | HELD (`invalid_json`) |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | HELD (`invalid_json`) |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | HELD (`invalid_json`) |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | — | — | HELD* (rate-limited before the route) |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | — | — | HELD* (rate-limited before the route) |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | HELD (`missing_text`) |
| FL01_01–05 | flood_same_creator | rapid submissions from one creator | 400 ×5 | — | — | — | — | HELD (reached route, `text_too_short`) |
| FL01_06–12 | flood_same_creator | rapid submissions from one creator | 429 ×7 | — | — | — | — | HELD (`rate_limited`, 5 per 1 minute) |

**Count: 53 HELD, 3 BROKE** (EV02, EV05, PI02).

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| evasion | 10 | 8 | 2 |
| false_positive | 8 | 8 | 0 |
| prompt_injection | 6 | 5 | 1 |
| malformed | 20 | 20 | 0 |
| flood_same_creator | 12 | 12 | 0 |

**Things the HELD marks hide** (what I saw in the run, not the cause yet;
that goes in my diagnoses):

- **No input in the whole run got the `ai` label.** The highest score was EV10
  at 0.893, which is three copies of the same AI paragraph, and it still came
  back `unsure` because `AI_THRESHOLD` is 0.90. So "evasion HELD" only means
  "not called human". The detector didn't catch any AI text either.
- **The false-positive rows held, but some came close.** FP05 (a person's
  technical docs) scored 0.852 and FP02 (formal human writing) scored 0.781.
  Both scored higher than 8 of the 9 AI evasion texts that got a score.
- **FP08 is a real writer refused.** "Went for a run. Legs hurt. Worth it." got
  a 400 `text_too_short`. Nobody accused them, but they got no answer either.
- **RQ10 and RQ11 (\*) were never tested by my route.** They had no `creator_id`
  my code could read, so they counted against my IP. Five earlier no-creator
  rows (RQ02, RQ06–RQ09) had already used up that minute, so the limiter
  rejected them first. I don't yet know what my route does with a form-encoded
  body or a `text/plain` JSON body.
- **The flood family is 12 rows, not the 20 the `targets` column says.** The
  first 5 reached the route and were rejected for being too short (55
  characters). Those 400s still counted toward the limit, so rows 6–12 got 429.
- **MF05's rejection reason is wrong.** A 4,000-character single word was
  rejected as `text_too_short`. The outcome is right (400, no crash), but the
  reason in the log is misleading for anyone reading it back.

**Ten audit log entries from the run** (from `logs/audit.jsonl`, written by
`audit.py`. The rejection entries carry fewer fields, which is expected.)

```json
{"timestamp": "2026-11-11T05:45:24+00:00", "content_id": "8b2a9dd1-109f-4239-ac5d-a5b5001f17f6", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.2148, "combined_score": 0.2096, "label": "We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing.", "status": "decided"}
{"timestamp": "2026-11-11T05:45:17+00:00", "content_id": "c670729d-3eed-434d-a49d-02ff56cbd7ad", "creator_id": "attacker_EV02", "guess": "human", "model_score": 0.5943, "style_score": 0.1022, "combined_score": 0.3483, "label": "We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing.", "status": "decided"}
{"timestamp": "2026-11-11T05:45:18+00:00", "content_id": "2d45cd76-bb49-417b-a478-6eacf54f9a54", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.2516, "combined_score": 0.2864, "label": "We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing.", "status": "decided"}
{"timestamp": "2026-11-11T05:45:20+00:00", "content_id": "1d974340-f926-46d1-bd41-b37b1f5a8e94", "creator_id": "attacker_EV10", "guess": "unsure", "model_score": 0.9792, "style_score": 0.8061, "combined_score": 0.8926, "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.", "status": "decided"}
{"timestamp": "2026-11-11T05:45:23+00:00", "content_id": "0a892f69-55f2-44de-ab55-d3b3df8aa087", "creator_id": "attacker_FP05", "guess": "unsure", "model_score": 0.8005, "style_score": 0.9025, "combined_score": 0.8515, "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.", "status": "decided"}
{"timestamp": "2026-11-11T05:45:21+00:00", "content_id": "1a9580ef-d862-40f5-9d67-fd75967349ff", "creator_id": "attacker_FP02", "guess": "unsure", "model_score": 0.7387, "style_score": 0.8239, "combined_score": 0.7813, "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.", "status": "decided"}
{"timestamp": "2026-11-11T05:45:24+00:00", "creator_id": "attacker_FP08", "event": "rejected", "status": "rejected", "reason": "text_too_short", "text_length": 36}
{"timestamp": "2026-11-11T05:45:26+00:00", "creator_id": "attacker_MF05", "event": "rejected", "status": "rejected", "reason": "text_too_short", "text_length": 4000}
{"timestamp": "2026-11-11T05:45:26+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-11T05:45:26+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

(Entry 9 is RQ10, a form-encoded body rejected by the limiter under my IP.
Entry 10 is FL01_06, the first flood row past the 5-per-minute limit.)

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

No real writer was labeled AI in this run, so no writer got caught. The
outcome I'd least want to explain is **PI02**. It was AI-generated text with
one fake "SYSTEM:" line on top telling the checker to return `human`. My
service returned `human` with a combined score of **0.21**, the lowest
(most-human) score of any input in the whole run, below every genuine human
false-positive row. That makes an honest writer's "human" label worth less,
because one pasted line of fake instructions earns the same label with more
confidence. Closest call for
a real writer: FP05, a person's technical documentation, scored 0.852, which
is 0.05 below the `ai` label.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
