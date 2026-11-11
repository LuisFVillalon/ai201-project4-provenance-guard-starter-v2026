# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 21:45
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `392d00fb-3e06-46b5-bd26-314ff81e659b` | unsure | 0.491 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c670729d-3eed-434d-a49d-02ff56cbd7ad` | human | 0.348 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `703150c9-1abc-4851-a51b-060b57724af8` | unsure | 0.555 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `d3d863e7-53b5-41a2-b20e-8e45c70f3761` | unsure | 0.706 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `2d45cd76-bb49-417b-a478-6eacf54f9a54` | human | 0.286 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `5186ad4e-6ab7-4b84-9379-1d9c3d797595` | unsure | 0.437 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `9caf6df3-15dc-4a62-be1c-5b705b2ff32a` | unsure | 0.420 |  |
| EV08 | evasion | signal one: text below the token window | 400 | `—` | — | — |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `f2a3dc90-3f46-490f-8c3a-64fcac9beb90` | unsure | 0.618 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `1d974340-f926-46d1-bd41-b37b1f5a8e94` | unsure | 0.893 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c858d9d5-515e-4cae-9db1-c9c284bbcfad` | unsure | 0.598 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `1a9580ef-d862-40f5-9d67-fd75967349ff` | unsure | 0.781 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `cdea43d1-ad1c-497e-b230-f53e57b0b884` | unsure | 0.751 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `1cf40d9b-c1b5-4168-8aa4-19d8b13c1f44` | unsure | 0.745 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `0a892f69-55f2-44de-ab55-d3b3df8aa087` | unsure | 0.852 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `6a0757e2-db7b-4c5b-a511-5f26f320de8d` | unsure | 0.609 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `456351d6-a653-43cb-8445-db446c9a3df8` | unsure | 0.595 |  |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `b35c083f-2d70-4900-a9db-56409b1b6c4b` | unsure | 0.400 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `8b2a9dd1-109f-4239-ac5d-a5b5001f17f6` | human | 0.210 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `b49acccc-4178-41ff-9ea3-80b867b5a98e` | unsure | 0.476 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `9bf015ba-7c96-47a3-98c9-b1a32f209dbe` | unsure | 0.434 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `2c0e279b-3f1d-48bc-a3ed-4aa105657fb7` | unsure | 0.445 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `3710e189-58f5-44b6-8221-7ba4dff0a41a` | unsure | 0.572 |  |
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
  "content_id": "392d00fb-3e06-46b5-bd26-314ff81e659b",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4909,
  "model_score": 0.1635,
  "style_score": 0.8,
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
  "content_id": "c670729d-3eed-434d-a49d-02ff56cbd7ad",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.3483,
  "model_score": 0.5943,
  "style_score": 0.1022,
  "label": "We think this was written by a person. Our check found the kind of variety and detail we usually see in human writing.",
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
  "content_id": "703150c9-1abc-4851-a51b-060b57724af8",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5548,
  "model_score": 0.6662,
  "style_score": 0.4434,
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
  "content_id": "d3d863e7-53b5-41a2-b20e-8e45c70f3761",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.7057,
  "model_score": 0.6114,
  "style_score": 0.8,
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
  "content_id": "2d45cd76-bb49-417b-a478-6eacf54f9a54",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2864,
  "model_score": 0.3212,
  "style_score": 0.2516,
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
  "content_id": "5186ad4e-6ab7-4b84-9379-1d9c3d797595",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4368,
  "model_score": 0.5727,
  "style_score": 0.3009,
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
  "content_id": "9caf6df3-15dc-4a62-be1c-5b705b2ff32a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.42,
  "model_score": 0.5862,
  "style_score": 0.2537,
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
  "content_id": "f2a3dc90-3f46-490f-8c3a-64fcac9beb90",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6183,
  "model_score": 0.7042,
  "style_score": 0.5325,
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
  "content_id": "1d974340-f926-46d1-bd41-b37b1f5a8e94",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.8926,
  "model_score": 0.9792,
  "style_score": 0.8061,
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
  "content_id": "c858d9d5-515e-4cae-9db1-c9c284bbcfad",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5975,
  "model_score": 0.6175,
  "style_score": 0.5775,
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
  "content_id": "1a9580ef-d862-40f5-9d67-fd75967349ff",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7813,
  "model_score": 0.7387,
  "style_score": 0.8239,
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
  "content_id": "cdea43d1-ad1c-497e-b230-f53e57b0b884",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7507,
  "model_score": 0.8051,
  "style_score": 0.6963,
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
  "content_id": "1cf40d9b-c1b5-4168-8aa4-19d8b13c1f44",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7447,
  "model_score": 0.8329,
  "style_score": 0.6565,
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
  "content_id": "0a892f69-55f2-44de-ab55-d3b3df8aa087",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.8515,
  "model_score": 0.8005,
  "style_score": 0.9025,
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
  "content_id": "6a0757e2-db7b-4c5b-a511-5f26f320de8d",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6094,
  "model_score": 0.8814,
  "style_score": 0.556,
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
  "content_id": "456351d6-a653-43cb-8445-db446c9a3df8",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5954,
  "model_score": 0.8816,
  "style_score": 0.5,
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
  "content_id": "b35c083f-2d70-4900-a9db-56409b1b6c4b",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3999,
  "model_score": 0.4625,
  "style_score": 0.3373,
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
  "content_id": "8b2a9dd1-109f-4239-ac5d-a5b5001f17f6",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2096,
  "model_score": 0.2044,
  "style_score": 0.2148,
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
  "content_id": "b49acccc-4178-41ff-9ea3-80b867b5a98e",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4756,
  "model_score": 0.5943,
  "style_score": 0.3569,
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
  "content_id": "9bf015ba-7c96-47a3-98c9-b1a32f209dbe",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4339,
  "model_score": 0.4998,
  "style_score": 0.368,
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
  "content_id": "2c0e279b-3f1d-48bc-a3ed-4aa105657fb7",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4451,
  "model_score": 0.6401,
  "style_score": 0.25,
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
  "content_id": "3710e189-58f5-44b6-8221-7ba4dff0a41a",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5715,
  "model_score": 0.5583,
  "style_score": 0.5846,
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
