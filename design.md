# Provenance Guard — Milestone 1 Design Notes

Written before any of `/submit` or `/appeal` is built. This is the plan the
rest of the code has to keep to.

---

## 1. The path a submission takes

1. **The writer's site sends `POST /submit`** (`app.py::submit`) with JSON:
   `text` and `creator_id`. *Adds:* nothing yet. It is just the request coming in.
2. **Input check** (`app.py::submit`). Rejects missing/non-string/empty `text`,
   missing `creator_id`, and text over the size cap with a `400`, and records
   the rejection with `audit.log_rejection`. *Adds:* a promise that every later
   step gets a real, non-empty string.
3. **A `content_id` is minted** (`uuid.uuid4()`). *Adds:* a stable handle the
   writer and the appeal endpoint can point at later.
4. **Signal one: the model signal** (`detector.py::model_signal`). gpt2 measures
   how predictable the text is, and the perplexity is squashed to 0–1.
   *Adds:* `model_score` (higher = more AI-like).
5. **Signal two: the style signal** (`stylometry.py::style_signal`). Measures
   the shape of the text: sentence-length spread, word variety, punctuation.
   *Adds:* `style_score` (higher = more AI-like).
6. **Combine and label** (`scoring.py::combine_signals` →
   `scoring.py::score_to_label`). The two scores become one `confidence`, and
   thresholds in `config.py` map that to a `guess` (`ai` / `unsure` / `human`)
   and a plain-English `label`. *Adds:* the decision and the sentence a person reads.
7. **Log and respond** (`audit.py::log_decision`, then `jsonify`). Every field,
   including both signal scores, goes to `logs/audit.jsonl` with
   `status: "decided"`, and the same fields go back to the caller. *Adds:* a
   permanent record, and the label the reader finally sees.

**Afterwards, the appeal path:** the writer sends `POST /appeal` with the
`content_id` and their reasoning → we check the id exists
(`audit.entries_for`) → `audit.log_appeal` appends an entry with
`status: "under_review"` next to the original decision → confirmation goes back.

---

## 2. The two signals

### Signal one: model signal (`detector.py`)

- **What it measures:** predictability. That is gpt2's perplexity on the text:
  how surprised a language model is by each next word.
- **Why it might differ:** a language model writes by picking likely next
  words, so its output is text a model finds easy to predict (low perplexity →
  high score). Human writing has more odd word choices and specific details, so
  it is more surprising.
- **What it can't see:** *who wrote it.* Predictable is not the same as
  machine-written. Plain writing with common words and short sentences
  scores as AI-like. That includes second-language writers, younger writers,
  and anyone writing simply on purpose. The other direction fails too: ornate
  prose full of rare words reads as human, so AI text asked to "use unusual
  vocabulary" can slip past. It also only sees the first 400 tokens, and it is
  unreliable on very short text.

### Signal two: style signal (`stylometry.py`)

- **What it measures:** the text's surface shape, with no understanding of meaning:
  - *sentence-length spread*: std dev / mean of sentence lengths (low = more AI-like)
  - *type-token ratio*: unique words / total words (low = more AI-like)
  - *punctuation density*: varied punctuation (`; : — ( ) ! ?`) per word
    (low = more AI-like)
- **Why it might differ:** "most likely next word" produces even, mid-length
  sentences, a safe vocabulary and plain commas and periods. Human writing is
  lumpier: a three-word sentence next to a forty-word one, a dash, a
  fragment.
- **What it can't see:** *anything the words say.* It can be gamed with
  changes to shape that leave the substance alone: add typos (raises word
  variety), chop or merge sentences (raises spread), sprinkle dashes and
  semicolons, paste in a quotation. It is also length-sensitive. Type-token
  ratio falls as text gets longer, and spread is meaningless with only one or
  two sentences. Finally, a human who writes in a deliberately even, tidy style
  (a technical writer, someone following a template) looks AI-like here too.

**Why these count as two different signals:** one is a model's judgement of
word choice in context. The other is counting that never reads a word. They
fail in different ways. Typos fool signal two but barely move signal one, and
plain vocabulary fools signal one but not necessarily signal two.

---

## 3. Tracing the false positive

**Who:** Ana, an ESL student, posts a short personal essay she wrote herself.
She uses words she is sure of and keeps sentences short and similar in length
so she won't make grammar mistakes.

**What happens in the service:**

1. Input check passes. She gets `content_id` `c-123…`.
2. **Signal one:** common words in ordinary order make perplexity low, around
   25, which gives `model_score ≈ 0.72`.
3. **Signal two:** sentences are all 10–14 words (low spread), the vocabulary
   repeats (low type-token ratio), and there are only periods and commas, so
   `style_score ≈ 0.65`.
4. **Combine:** both signals point the same wrong way, so there is no
   disagreement to soften it. 50/50 weighting gives `confidence ≈ 0.69`.
5. **Label:** with the starter's AI threshold of 0.65, she lands in
   **high-confidence AI**. The label tells her, in effect, that we think a
   machine wrote her essay.
6. **What she can do:** her only recourse is `POST /appeal` with her
   `content_id` and an explanation. Her item moves to `under_review` and the
   appeal sits in the log beside the original decision. Nothing re-checks it
   automatically. A person has to look.

**What this tells me about the design:**

- Both signals share a blind spot: plain, even writing. Agreement between
  them is **not** strong evidence on its own. The combining rule can't treat
  "both say AI" as certainty.
- The AI threshold needs to sit **high**, well above 0.65, so that a
  score like Ana's 0.69 lands in *unsure*, not *AI*. That widens the unsure
  band. More AI text gets labelled "unsure", and that is the cost I'm choosing
  to pay. A missed AI essay costs the site a little. A wrong accusation costs a
  real writer their reputation.
- The **AI label must name the appeal** and must not read as a verdict. The
  **unsure label must not read as an accusation**.
- The appeal response has to tell her what happens next, so she isn't left
  waiting on silence.
- Very short text should not get a confident label at all. With so little
  text, both signals are close to noise.

Thresholds are set for real in Milestones 4–5, after I see actual scores.
The decision made here is the *direction*: bias toward "unsure" over "AI".

---

## 4. Endpoint contracts

### `POST /submit`

**Request** (`Content-Type: application/json`)

| Field | Type | Required | Rules |
|---|---|---|---|
| `text` | string | yes | Not empty after trimming whitespace. At least 20 words. At most 20,000 characters. |
| `creator_id` | string | yes | Not empty after trimming whitespace. |

**Response `200`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string (UUID) | Handle for this submission. Needed for `/appeal`. |
| `creator_id` | string | Echoed back. |
| `guess` | string | One of `"ai"`, `"human"`, `"unsure"`. |
| `confidence` | float 0–1 | The combined score. **0 = confidently human, 1 = confidently AI.** |
| `label` | string | The full sentence shown to the reader. |
| `model_score` | float 0–1 | Signal one, higher = more AI-like. |
| `style_score` | float 0–1 | Signal two, higher = more AI-like. |
| `status` | string | `"decided"` on a new submission. |

```json
{
  "content_id": "3f2b9c1e-…",
  "creator_id": "ana_writes",
  "guess": "unsure",
  "confidence": 0.58,
  "label": "<full unsure label text>",
  "model_score": 0.72,
  "style_score": 0.44,
  "status": "decided"
}
```

**Errors.** All errors have the same shape: `{"error": "<code>", "message": "<human-readable>"}`

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | Body missing or not a JSON object |
| 400 | `missing_text` | `text` absent, not a string, or blank |
| 400 | `missing_creator_id` | `creator_id` absent, not a string, or blank |
| 400 | `text_too_short` | Fewer than 20 words, counted with `stylometry.words` |
| 413 | `text_too_long` | `text` over 20,000 characters |
| 503 | `detector_unavailable` | The model couldn't be loaded |

Every rejection is also written to the log with `audit.log_rejection`.

### `POST /appeal`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `content_id` | string | yes | Must match a `content_id` already in the log. |
| `reasoning` | string | yes | Not empty after trimming whitespace. The writer's explanation. |

**Response `200`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echoed back. |
| `status` | string | Always `"under_review"`. |
| `original_guess` | string | What we decided before the appeal. |
| `message` | string | Plain-English confirmation and what happens next. |
| `appealed_at` | string (ISO 8601 UTC) | When the appeal was recorded. |

```json
{
  "content_id": "3f2b9c1e-…",
  "status": "under_review",
  "original_guess": "ai",
  "message": "Thanks — your appeal is recorded and a person will review this piece. Until then it is marked as under review, not as AI-written.",
  "appealed_at": "2026-11-03T21:40:00+00:00"
}
```

**Errors** (same `{"error", "message"}` shape)

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | Body missing or not a JSON object |
| 400 | `missing_content_id` | Absent or blank |
| 400 | `missing_reasoning` | Absent or blank |
| 404 | `unknown_content_id` | No submission with that id in the log |
| 409 | `already_under_review` | That item already has an appeal on record |

**Log effect:** a new entry is appended with `event: "appeal"`,
`status: "under_review"` and the `reasoning`. The original decision entry
is never edited.
