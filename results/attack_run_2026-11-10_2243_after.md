# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 22:43
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `1d8e98a7-570c-486c-a72c-cd1b34a97b93` | unsure | 0.541 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `fd526827-2450-408c-8122-cec62d2a574b` | unsure | 0.361 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `f57851da-7e4e-4239-b2f7-702e5acc7d8c` | unsure | 0.610 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c3446937-3e14-4f69-aa26-4c6f873c441e` | unsure | 0.653 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `18ccc17b-c252-4e2d-bc17-691b3581a648` | human | 0.318 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `3ffac87e-9746-48c1-95c3-cd7b5ae646c0` | unsure | 0.474 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `5d3ec2c0-1c08-4158-8c9a-3ad96c753501` | unsure | 0.449 |  |
| EV08 | evasion | signal one: text below the token window | 400 | `—` | — | — |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `3a074da9-2df0-41ed-b339-5d4079ef3528` | unsure | 0.685 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `4d962be2-64fc-4dca-8729-1d242f6303e8` | unsure | 0.868 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `438f4fbf-d559-4076-83f7-96861d489322` | unsure | 0.648 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `fe8bb63d-8bfb-46ba-b475-455b54ab99d2` | unsure | 0.844 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `e186f48c-054f-4779-bdda-f0e7bf939db2` | unsure | 0.823 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `1c78b5bd-8fc7-4166-bb54-14213f34c231` | unsure | 0.812 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c58baafd-ed1f-4ab0-819e-9406cb5d084c` | unsure | 0.852 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `f7fa3f61-7916-4b52-849e-37cf95133536` | unsure | 0.741 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `a34559bc-5a94-4609-8ef6-60f2762b76f3` | unsure | 0.564 |  |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `731f67ac-a716-427b-9618-9d551597dc9a` | unsure | 0.442 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `4a2ea5b0-d83b-48ca-9ff8-204d8c6768d6` | human | 0.236 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `ab5645dd-0f51-4fc2-886b-0deed236501b` | unsure | 0.520 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `d2732c87-e762-40b3-93ce-69bb3f8f31a1` | unsure | 0.480 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `fb7dabf7-412e-4746-a0bf-60302abb3628` | unsure | 0.476 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `a27e9237-20ca-437f-b615-5e4827893ae3` | unsure | 0.626 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "1d8e98a7-570c-486c-a72c-cd1b34a97b93",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5409,
  "model_score": 0.1635,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "fd526827-2450-408c-8122-cec62d2a574b",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.361,
  "model_score": 0.5943,
  "style_score": 0.1277,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "f57851da-7e4e-4239-b2f7-702e5acc7d8c",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.6102,
  "model_score": 0.6662,
  "style_score": 0.5543,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c3446937-3e14-4f69-aa26-4c6f873c441e",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6529,
  "model_score": 0.6114,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "18ccc17b-c252-4e2d-bc17-691b3581a648",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3178,
  "model_score": 0.3212,
  "style_score": 0.3145,
  "label": "We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "3ffac87e-9746-48c1-95c3-cd7b5ae646c0",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4738,
  "model_score": 0.5727,
  "style_score": 0.375,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "5d3ec2c0-1c08-4158-8c9a-3ad96c753501",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4494,
  "model_score": 0.5862,
  "style_score": 0.3125,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "3a074da9-2df0-41ed-b339-5d4079ef3528",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6849,
  "model_score": 0.7042,
  "style_score": 0.6656,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "4d962be2-64fc-4dca-8729-1d242f6303e8",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.8684,
  "model_score": 0.9792,
  "style_score": 0.7576,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "438f4fbf-d559-4076-83f7-96861d489322",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6478,
  "model_score": 0.6175,
  "style_score": 0.6781,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "fe8bb63d-8bfb-46ba-b475-455b54ab99d2",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.8441,
  "model_score": 0.7387,
  "style_score": 0.9496,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "e186f48c-054f-4779-bdda-f0e7bf939db2",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.8225,
  "model_score": 0.8051,
  "style_score": 0.8398,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "1c78b5bd-8fc7-4166-bb54-14213f34c231",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.8123,
  "model_score": 0.8329,
  "style_score": 0.7917,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c58baafd-ed1f-4ab0-819e-9406cb5d084c",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.8522,
  "model_score": 0.8005,
  "style_score": 0.9039,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "f7fa3f61-7916-4b52-849e-37cf95133536",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7412,
  "model_score": 0.8814,
  "style_score": 0.601,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "a34559bc-5a94-4609-8ef6-60f2762b76f3",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5642,
  "model_score": 0.8816,
  "style_score": 0.375,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "731f67ac-a716-427b-9618-9d551597dc9a",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4421,
  "model_score": 0.4625,
  "style_score": 0.4217,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "4a2ea5b0-d83b-48ca-9ff8-204d8c6768d6",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2364,
  "model_score": 0.2044,
  "style_score": 0.2685,
  "label": "We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "ab5645dd-0f51-4fc2-886b-0deed236501b",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5202,
  "model_score": 0.5943,
  "style_score": 0.4462,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "d2732c87-e762-40b3-93ce-69bb3f8f31a1",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4799,
  "model_score": 0.4998,
  "style_score": 0.46,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "fb7dabf7-412e-4746-a0bf-60302abb3628",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4763,
  "model_score": 0.6401,
  "style_score": 0.3125,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "a27e9237-20ca-437f-b615-5e4827893ae3",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6258,
  "model_score": 0.5583,
  "style_score": 0.6932,
  "label": "We can't tell whether this was written by a person or with AI, so we aren't making a call. Lots of writing by real people lands here, especially plain or formal writing. This is not a sign that anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
