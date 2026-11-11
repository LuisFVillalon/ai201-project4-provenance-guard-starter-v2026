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

Run with `python run_eval.py --label before` on 2026-11-10. Full output:
[results/run_2026-11-10_2227_before.md](results/run_2026-11-10_2227_before.md).
Scenarios are in [scenarios.py](scenarios.py), and same thresholds as the attack run
(`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.90`).

**How each criterion was tested**

- **Criteria 1–3** send text through `POST /submit`. The "my own writing"
  pieces are copied word for word from writing I already had before this
  unit: the TEKnuova cover letter, my STAT 550 Lab 6 report, my "How to Be
  an AI-Native Engineer" guide, my Kanso project description, and the two
  casual paragraphs from unit 7. The clearly-AI texts are unedited Claude
  output on ordinary prompts.
- **Criterion 4.** `run_eval.py` only ever called `/submit`, so I **extended
  it** with `run_eval.py::run_appeals` instead of testing by hand. Each trial
  does three things:
  - Submits 10 texts and appeals each one by its real `content_id`.
  - Re-reads `GET /log` to check the appeal entry (reasoning word for word,
    `under_review`) and that the original decision entry is unchanged.
  - Sends the three appeals that must fail: a made-up id, a second appeal,
    and blank reasoning on a fresh submission.
- **Criterion 5** sends the 8 bodies in criteria.md as raw bodies. For each,
  `run_eval.py::main` now also records the error code, the response time,
  and how many audit log entries it wrote.

**Gaps in my test set** (recorded, not filled with made-up writing):

| Criterion | Asks for | I had | Missing |
|---|---|---|---|
| 1 | 10 own pieces, incl. cover letter, lab report, how-to, **short-even-sentences** | 10 pieces (2 casual, 8 formal), 3 of the 4 named types | the short-even-sentences paragraph |
| 2 | 5 clearly-human casual pieces | 2 | 3 |
| 3(b) | 2 lightly-edited AI + 3 formal human | 3 formal human | both lightly-edited AI |

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | 0 of 10 | 0/10 | 0/10 | 0/10 | MET (on an incomplete set, see gaps) |
| 2. Clearly-AI minus clearly-human mean, and no overlap | gap ≥ 0.30, no human > any AI | gap 0.440, no overlap | gap 0.440, no overlap | gap 0.440, no overlap | MET (human set is 2 of 5) |
| 3a. All three labels reachable across c2 + c3 texts | 3 of 3 | 2/3 (no `ai`) | 2/3 | 2/3 | **MISSED** |
| 3b. Borderline texts unsure / formal human not AI | ≥ 3 of 5 unsure, 0 formal AI | 3/3 unsure, 0 AI | 3/3, 0 AI | 3/3, 0 AI | MET on 3 of 5 texts (lightly-edited AI not tested) |
| 4. Appeals recorded and change status, plus 404/409/400 | 10 of 10, 3 of 3 | 10/10, 3/3 | 10/10, 3/3 | 10/10, 3/3 | MET |
| 5. Malformed bodies get the contract's 4xx, no decision, logged, < 2 s | 8 of 8 | 8/8 (max 0.034 s) | 8/8 (max 0.032 s) | 8/8 (max 0.028 s) | MET |

**Criterion 3 overall: MISSED.** Part (a) failed in every trial.

**How I decided each verdict**

- **Criterion 1.** None of the 10 pieces got `ai` in any trial, which meets
  the target. The highest was my lab report at 0.807. I still don't count
  it as a clean pass, because the piece most likely to break it is missing.
  In unit 7 my short-even-sentences paragraph scored 0.885, only 0.015
  below the `ai` label.
- **Criterion 2.** In all three trials the gap was 0.802 − 0.362 = 0.440,
  above 0.30. The lowest AI piece (0.683) beat the highest human piece
  (0.383), so there was no overlap. Both parts hold, but only on 2 human
  pieces, so the "no overlap" half is a weak check.
- **Criterion 3(a).** The 10 texts from criterion 2 plus the borderline ones
  produced only `human` and `unsure`. Even the most AI-like chatbot
  paragraph (0.867) stayed under 0.90. Since part (a) has to hold in every
  trial, this is a miss.
- **Criteria 4 and 5.** Every check passed in every trial. These are
  mechanical pass/fail checks, so there is no generous reading to argue
  about.

**The three trials were identical** down to the fourth decimal on every
score. That's expected, because neither signal is random. It shows the
results hold rather than turning up once.

One thing I noticed: my grandmother/buttons paragraph scored **0.383
(unsure)**. My unit 7 calibration table has it at 0.307 (human), but that
run predates my final combining rule. Today it gets `unsure`, so only 1 of
my 10 pieces earns the `human` label.

**Real output from trial 1** (produced by `run_eval.py::main` and
`run_eval.py::run_appeals` calling `app.py::submit` / `app.py::appeal`;
label text cut to 60 characters here, full text in the results file):

*Criterion 1: the casual piece that got `human`, and the highest-scoring piece (my lab report):*

```json
[
  {"status": 200, "guess": "human", "confidence": 0.3414, "model_score": 0.5732, "style_score": 0.1095,
   "label": "We think this was written by a person. Our check found the k…",
   "sent": "The 7 bus was late again — twenty minutes, in the rain, with no shelte"},
  {"status": 200, "guess": "unsure", "confidence": 0.8074, "model_score": 0.6926, "style_score": 0.9221,
   "label": "We can't tell whether this was written by a person or with A…",
   "sent": "The true expected value of the hypotenuse is about 0.7071, and the tru"}
]
```

*Criterion 2: the lowest-scoring AI piece and the highest-scoring human piece (the closest pair):*

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.6832, "model_score": 0.773, "style_score": 0.5933,
   "label": "We can't tell whether this was written by a person or with A…",
   "sent": "Reading books provides numerous advantages that extend far beyond ente"},
  {"status": 200, "guess": "unsure", "confidence": 0.3831, "model_score": 0.4661, "style_score": 0.3,
   "label": "We can't tell whether this was written by a person or with A…",
   "sent": "My grandmother kept a jar of buttons on the windowsill, and every Sund"}
]
```

*Criterion 3: the highest-scoring AI piece in the whole run (still not `ai`), and a borderline formal piece:*

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.8674,
   "sent": "Regular exercise offers a wide range of benefits for both physical and"},
  {"status": 200, "guess": "unsure", "confidence": 0.8074, "model_score": 0.6926, "style_score": 0.9221,
   "label": "We can't tell whether this was written by a person or with A…",
   "sent": "The true expected value of the hypotenuse is about 0.7071, and the tru"}
]
```

*Criterion 4: one appeal, then the three that must fail:*

```json
[
  {"check": "appeal", "item": 1, "submit_status": 200,
   "content_id": "bf664648-b93e-45f6-bf7e-9e3d561b2f84", "guess": "unsure",
   "appeal_http": 200, "appeal_status": "under_review", "appeal_entries_in_log": 1,
   "reasoning_verbatim": true, "log_status": "under_review", "decision_unchanged": true,
   "appeal_log_entry": {"content_id": "bf664648-b93e-45f6-bf7e-9e3d561b2f84",
     "creator_id": "eval_c4_t1_1_222639", "event": "appeal",
     "reasoning": "I wrote this myself and I'd like a person to review it. (item 1, trial 1)",
     "status": "under_review", "timestamp": "2026-11-11T06:26:40+00:00"},
   "pass": true},
  {"check": "unknown id → 404", "expected": "404 unknown_content_id",
   "http": 404, "error": "unknown_content_id", "appeal_entries_in_log": 0, "pass": true},
  {"check": "second appeal → 409", "expected": "409 already_under_review",
   "http": 409, "error": "already_under_review", "appeal_entries_in_log": 1, "pass": true},
  {"check": "blank reasoning → 400", "expected": "400 missing_reasoning",
   "http": 400, "error": "missing_reasoning", "appeal_entries_in_log": 0, "pass": true}
]
```

*Criterion 5: empty text, no creator_id, and the 50,000-word body:*

```json
[
  {"status": 400, "guess": null, "label": null, "sent": "(empty text)",
   "expected": "400 missing_text", "error": "missing_text", "content_id": null,
   "elapsed_s": 0.034, "log_entries_written": 1,
   "log_entry": {"creator_id": "eval_c5_empty", "event": "rejected", "reason": "missing_text",
                 "status": "rejected", "timestamp": "2026-11-11T06:26:58+00:00"}},
  {"status": 400, "guess": null, "label": null,
   "expected": "400 missing_creator_id", "error": "missing_creator_id", "content_id": null,
   "elapsed_s": 0.018, "log_entries_written": 1,
   "log_entry": {"creator_id": "unknown", "event": "rejected", "reason": "missing_creator_id",
                 "status": "rejected", "timestamp": "2026-11-11T06:26:58+00:00"}},
  {"status": 413, "guess": null, "label": null, "sent": "word word word word word word ...",
   "expected": "413 text_too_long", "error": "text_too_long", "content_id": null,
   "elapsed_s": 0.015, "log_entries_written": 1,
   "log_entry": {"creator_id": "eval_c5_huge", "event": "rejected", "reason": "text_too_long",
                 "status": "rejected", "text_length": 250000, "timestamp": "2026-11-11T06:26:59+00:00"}}
]
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

How I got the evidence: I re-scored each failing input one stage at a time.
That means the raw measures inside `stylometry.py`, the perplexity inside
`detector.py`, then `scoring.py::combine_signals` and
`scoring.py::score_to_label`. Where an attack added something, I scored the
same text **without** the addition, which shows which stage the addition
moved. Weights: model 0.5 / style 0.5. Inside the style signal: spread 0.5,
TTR 0.2, punctuation 0.3. Disagreement gaps: 0.30 on the AI side and 0.50
on the human side.

**Miss 1: Criterion 3(a), the `ai` label is unreachable for ordinary AI text.**
*Stage: signal two and the label mapping together.*

| Input | ppl | model | spread | TTR | punct | style | combined | label |
|---|---|---|---|---|---|---|---|---|
| Exercise (clearly AI) | 8.5 | 0.935 | 0.159 | 0.867 | 0.000 | **0.800** | 0.867 | unsure |
| Technology (clearly AI) | 11.9 | 0.893 | 0.179 | 0.874 | 0.000 | **0.800** | 0.847 | unsure |
| Time management (clearly AI) | 17.1 | 0.824 | 0.171 | 0.899 | 0.000 | **0.800** | 0.812 | unsure |
| EV10 (same AI paragraph ×3) | 4.1 | 0.979 | 0.394 | 0.500 | 0.000 | 0.806 | 0.893 | unsure |

The style signal **tops out at 0.80** on normal AI prose, and that's the
mechanism.
- Even sentences max out the spread part (0.5 × 1.0) and zero punctuation
  maxes out the punctuation part (0.3 × 1.0).
- AI text has *varied* vocabulary (TTR 0.87–0.90). That sits above the 0.85
  "very human" end of `TTR_RANGE`, so the TTR part contributes 0.
- So style = 0.5 + 0.3 + 0 = **0.80**. This is the "TTR runs backwards"
  problem I noted in calibration, and it's now a hard ceiling.

From there:
- With style stuck at 0.80, an even average reaches `AI_THRESHOLD = 0.90`
  only if the model signal is **1.00**. No real text gets there; the most
  predictable chatbot paragraph got 0.935.
- The only way to reach `ai` is low TTR, meaning repeated vocabulary. That
  happened for my unit 7 "drinking water" paragraph (0.959). EV10 has
  repetition too (TTR 0.50), but repeating the paragraph raised its spread
  and it stalled at 0.893.

The AI label therefore fires only on *plain, repetitive* writing, which is
exactly the kind my criteria call the expensive false positive. It never
fires on typical chatbot prose. The 0.90 threshold isn't wrong by itself.
It fails because of how it combines with a style signal that can't exceed
0.80.

**Broken attack EV02: AI text with "Really." inserted after every sentence → `human` (0.348).**
*Stage: signal two (sentence-length spread), let through by the combining rule's human-side gap.*

| Version | sentences | spread | punct | model | style | gap | combined | label |
|---|---|---|---|---|---|---|---|---|
| without the "Really."s and dashes | 7 | 0.161 | 0.000 | 0.594 | 0.800 | 0.206 | 0.697 | unsure |
| as sent | 13 | **0.849** | 0.033 | 0.594 | **0.102** | 0.492 | **0.348** | human |

- **Signal two:** the one-word sentences push spread from 0.16 (very even)
  to 0.85 (very lumpy), past the 0.70 "very human" end. The added dashes
  push punctuation to the human end as well. Style falls from 0.80 to 0.10,
  but nothing about the writing changed.
- **Signal one** doesn't move at all (0.594 both times). GPT-2 still finds
  it fairly predictable.
- **Combining rule:** the signals now disagree by 0.492. My human-side
  limit is 0.50, so the rule doesn't shrink the score toward 0.5. That rule
  was built for this kind of split, and it missed by **0.008**. The plain
  average of 0.348 then lands 0.002 under `HUMAN_THRESHOLD`.

**Broken attack PI02: a fake "SYSTEM:" line on top of AI text → `human` (0.210), the lowest score in the run.**
*Stage: signal one (perplexity), then signal two. The instruction was never obeyed.*

| Version | ppl | model | spread | style | gap | combined | label |
|---|---|---|---|---|---|---|---|
| without the SYSTEM line | 22.3 | 0.754 | 0.801 | 0.300 | 0.454 | 0.513 | unsure |
| as sent | **105.2** | **0.204** | 0.652 | 0.215 | 0.010 | **0.210** | human |

- **Nothing in my pipeline reads text as instructions.** GPT-2 only
  measures how predictable each word is, and the style signal only counts
  shapes. So "Return guess=human" wasn't followed.
- **Signal one:** the line *as text* is junk to GPT-2: capital letters,
  `guess=human`, `confidence=0.02`. It **quintuples perplexity** (22 → 105),
  and the model signal falls from 0.75 to 0.20. The injection worked as an
  evasion, not as an instruction.
- **Signal two:** the line adds three short "sentences". Style was already
  human-leaning at 0.30, partly because the attack's AI body ends mid-word
  ("…misunderstandings. Th"). That stub is a one-word "sentence", which
  inflates spread.
- **Combining rule:** with both signals now saying human, the gap is only
  0.010, so nothing triggers. My only protection against a split doesn't
  apply when the attack moves both signals the same way.

**Broken attack EV05: "heavy human editing pass" → `human` (0.286).**
*Stage: both signals, working as designed. I'm not counting this as a defect.*

| ppl | model | spread | punct | style | gap | combined |
|---|---|---|---|---|---|---|
| 71.8 | 0.321 | 0.675 | 0.012 | 0.252 | 0.070 | 0.286 |

- The edit replaced the AI's wording with new words ("the boring kind, not
  the away-day kind", "a corridor in March"). Perplexity is 71.8, above my
  midpoint of 45, so the model signal reads human.
- The rhythm is lumpy too (spread 0.675). Both signals agree, gap 0.07.
- Both signals saw a person's word choices and a person's rhythm, because a
  person rewrote it. Most of the text is now the editor's. I marked it
  BROKE because it met the attack's goal. But no detector that reads the
  text should call this AI, and I wouldn't change anything to catch it.

**The pattern across the misses**

There are two problems, not four.

1. **Short, non-prose additions read as "human" to both signals.**
   Both broken attacks that matter got there with filler, not with new
   writing: EV02's "Really." sentences and PI02's SYSTEM line. Filler
   - raises **sentence-length spread**, because short sentences make the
     rhythm lumpy;
   - adds varied **punctuation**;
   - and, if it's odd enough, raises **perplexity**.

   All three are "more human" to my signals, and neither signal checks
   whether the added words carry any meaning. So one cheap trick can move
   both signals at once, and my disagreement rule only protects against a
   split. The thresholds then let a borderline 0.348 through as `human`.
   This is signal two's named blind spot ("anything that changes the shape
   without changing the substance"). PI02 shows it applies to signal one
   too.
2. **The scale is squeezed at the top.** The style signal can't go above
   0.80 for typical AI text (miss 1). The AI label never fires on chatbot
   prose, so every attack's "held" mark on the evasion side means only
   "not called human".

**Things that held, but only just** (not misses, but my targets hide them):

- **Criterion 1** passed, but my lab report scored 0.807 and two
  false-positive attacks scored 0.852 (FP05) and 0.781 (FP02). The only
  thing between them and an accusation is the 0.90 threshold. The same
  ceiling that makes `ai` unreachable for AI text is what's protecting
  these writers.
- **Criteria 1 and 2** were measured on incomplete sets (see the gaps table
  above). The missing short-even-sentences piece is the riskiest one for
  criterion 1. In unit 7 it scored 0.885, so I'd tighten criterion 1 by
  adding it before trusting the MET.

**No criterion revised.** Criterion 3 was measurable. I could reach a
verdict in every trial, and the verdict was a miss. That stays a miss,
not a revision.



---

## The Improvement

**What I changed:** I removed type-token ratio from the style signal. That's
one change, in `stylometry.py`:

| | `WEIGHT_SPREAD` | `WEIGHT_TTR` | `WEIGHT_PUNCT` |
|---|---|---|---|
| before | 0.5 | 0.2 | 0.3 |
| after | 0.625 | **0.0** | 0.375 |

TTR's 0.2 is split between the other two measures in their existing 5:3
ratio, so the style signal still runs 0–1. Nothing else changed: no
thresholds, no combining rule, no model signal, no route.

**Which diagnosis pointed at it:** Miss 1. TTR runs backwards on AI prose
(0.87–0.90, above its 0.85 "very human" anchor), so it contributed 0 on
every AI text. That capped the style signal at 0.80, and the `ai` label
(0.90) became unreachable unless the model signal hit 1.00. TTR was
already the measure I distrusted in unit 7 ("all it reliably detects is
plain writing"). Removing it targets the ceiling directly and doesn't
touch the threshold that protects writers.

I previewed the change on the before-run inputs (scored offline, no files
changed) before making it. The preview predicted the trade below, and the
re-runs confirmed it exactly.

### Attack Run — After

Run with `python run_attacks.py --set attack_set --label after` (full output:
[results/attack_run_2026-11-10_2243_after.md](results/attack_run_2026-11-10_2243_after.md)).
Same marking rule as the before run. All 26 malformed and flood rows came
back with identical status codes and reasons (no 5xx, same 429 pattern),
so only the scored rows are shown.

| ID | Targeting | Before: guess / score | After: guess / score | Verdict before → after |
|---|---|---|---|---|
| EV01 | typos raise word variety | unsure 0.491 | unsure 0.541 | HELD → HELD |
| EV02 | broken-up sentences raise length spread | **human 0.348** | unsure 0.361 | **BROKE → HELD** |
| EV03 | a pasted quotation | unsure 0.555 | unsure 0.610 | HELD → HELD |
| EV04 | unusual words raise perplexity | unsure 0.706 | unsure 0.653 | HELD → HELD |
| EV05 | heavy human editing pass | **human 0.286** | **human 0.318** | BROKE → BROKE |
| EV06 | one very long sentence, one very short | unsure 0.437 | unsure 0.474 | HELD → HELD |
| EV07 | padding with punctuation | unsure 0.420 | unsure 0.449 | HELD → HELD |
| EV08 | below the token window | 400 | 400 | HELD → HELD |
| EV09 | human opening bolted on | unsure 0.618 | unsure 0.685 | HELD → HELD |
| EV10 | repeated stanza structure | unsure 0.893 | unsure 0.868 | HELD → HELD |
| FP01 | plain human writing | unsure 0.598 | unsure 0.648 | HELD → HELD |
| FP02 | formal register | unsure 0.781 | unsure 0.844 | HELD → HELD |
| FP03 | non-native speaker, careful | unsure 0.751 | unsure 0.823 | HELD → HELD |
| FP04 | student essay to a rubric | unsure 0.745 | unsure 0.812 | HELD → HELD |
| FP05 | technical documentation | unsure 0.852 | unsure 0.852 | HELD → HELD |
| FP06 | imitating a formal template | unsure 0.609 | unsure 0.741 | HELD → HELD |
| FP07 | repeats a phrase deliberately | unsure 0.595 | unsure 0.564 | HELD → HELD |
| FP08 | very short human submission | 400 | 400 | HELD → HELD |
| PI01 | ignore the check | unsure 0.400 | unsure 0.442 | HELD → HELD |
| PI02 | fake system message | **human 0.210** | **human 0.236** | BROKE → BROKE |
| PI03 | instruction in the writer's voice | unsure 0.476 | unsure 0.520 | HELD → HELD |
| PI04 | hostile label text | unsure 0.434 | unsure 0.480 | HELD → HELD |
| PI05 | inject into the audit log | unsure 0.445 | unsure 0.476 | HELD → HELD |
| PI06 | instruction plus human text | unsure 0.572 | unsure 0.626 | HELD → HELD |
| MF01–RQ12, FL01 (32 rows) | malformed / flood | same codes | same codes | HELD → HELD |

**Count: before 53 HELD / 3 BROKE → after 54 HELD / 2 BROKE.**

### Run Log — After

Run with `python run_eval.py --label after` (full output:
[results/run_2026-11-10_2245_after.md](results/run_2026-11-10_2245_after.md)).
All three trials were identical again.

| Criterion | Target | Before (×3) | After Run 1 | After Run 2 | After Run 3 | Verdict after |
|---|---|---|---|---|---|---|
| 1. Own writing labelled AI | 0 of 10 | 0/10 | 0/10 | 0/10 | 0/10 | MET (incomplete set) |
| 2. AI − human gap, no overlap | ≥ 0.30, none | 0.440, none | 0.507, none | 0.507, none | 0.507, none | MET (2 of 5 human) |
| 3a. All three labels reachable | 3 of 3 | 2/3 (no `ai`) | 2/3 (no `human`) | 2/3 | 2/3 | **MISSED** |
| 3b. Borderline unsure / formal not AI | ≥ 3 unsure, 0 AI | 3/3, 0 | 3/3, 0 | 3/3, 0 | 3/3, 0 | MET (3 of 5 texts) |
| 4. Appeals + 404/409/400 | 10/10, 3/3 | 10/10, 3/3 | 10/10, 3/3 | 10/10, 3/3 | 10/10, 3/3 | MET |
| 5. Malformed bodies | 8 of 8 | 8/8 | 8/8 | 8/8 | 8/8 | MET |

What moved:
- **Criterion 2:** clearly-AI mean went 0.802 → **0.895**. Clearly-human
  mean went 0.362 → 0.388.
- **Criterion 1:** my highest own piece (the lab report) went 0.807 →
  **0.841**. That's still 0.059 under the `ai` label.
- **Criterion 3(a):** 3 of the 5 clearly-AI texts now get `ai` (0.967,
  0.946, 0.912). But my bus-stop paragraph went 0.341 → **0.355**, which is
  just over the human line, so `human` now never appears.

**Did it help, and how do I know:**

**Partly. It fixed what it targeted and broke something next to it, and
the criterion it was meant to fix is still MISSED.**

- **What it fixed.**
  - The `ai` label now fires on ordinary chatbot prose, where before it
    never did.
  - EV02 moved from human to unsure. The style signal gained weight on
    the AI side, so the same "Really." trick no longer pulls the average
    under 0.35.
  - Nothing got worse on the accusation side: 0 of 10 of my pieces and 0 of
    7 false-positive attacks were called AI. FP05, the closest, stayed at
    0.852.
- **What it cost.** Raising the spread and punctuation weights pushes
  *every* score up a little, human text included. My one casual piece that
  earned `human` (0.341) now gets `unsure` (0.355). **After the change, the
  only inputs labeled `human` in either run are EV05 and PI02, and both are
  AI text.** That's worse than before. When the system says "we think a
  person wrote this", it is now always wrong on my test set.
- **Criterion 3(a) is still MISSED.** Before, the missing label was `ai`.
  After, it's `human`. The criterion caught the trade, and it was right
  to.
- **Every human piece got closer to the line:** the lab report is now
  0.841, FP02 0.844, FP03 0.823. Before the change, the 0.80 cap on the
  style signal was quietly protecting formal writers. Taking it away
  shrank their margin from about 0.09 to about 0.06.

So the change helped on the AI side and cost real writers on the human
side. My bus-stop piece sits 0.005 over the human line. That tells me the
next problem is where `HUMAN_THRESHOLD` sits relative to casual human
writing, not the style weights. I didn't change it, because that would be
a second change measured in the same run.



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
