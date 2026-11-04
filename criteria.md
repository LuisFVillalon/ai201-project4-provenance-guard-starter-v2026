# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service. I wrote them in
unit 7, **before** building `/submit`, `/appeal`, the style signal, or the
scoring. The commit history shows that.

Scores run 0.0 (confidently human) to 1.0 (confidently AI). Each criterion is
checked across **three trials**, and it has to pass in **all three**. The model
signal can score the same text differently on different runs, so one lucky run
doesn't count.

Areas covered: false positives (1), score spread (2), label coverage (3), the
appeal path (4), bad input (5).

---

## 1. No real writer gets called AI: 0 of 10 of my own pieces labelled high-confidence AI

I submit 10 pieces I wrote myself. At least 4 are deliberately plain or
formal: a cover letter, a lab-report paragraph, a short how-to, and a
paragraph written in short, even sentences. **None of the 10 may get the
high-confidence AI label in any of the three trials.** Getting the unsure label
is allowed.

**Why this target:** A false positive is the expensive mistake. On a writing
site, the AI label accuses a real person of cheating, and my Milestone 1 trace
(Ana) showed the plain writers are the ones it lands on. I'm allowing zero, not
"1 in 10", because I already decided to make the unsure band wide to take this
risk. If even one of my own pieces still gets past it, the threshold is in the
wrong place. When I pictured being the "1" in "1 in 10", I couldn't defend that
rate. The formal pieces are there on purpose, because both of my signals share
that blind spot. A test that only used my casual writing would be too easy to pass.

---

## 2. Clearly-AI and clearly-human text score far apart: mean gap of at least 0.30

I submit 5 pieces that are clearly AI (unedited chatbot output on ordinary
prompts) and 5 that are clearly human (my own casual writing, with personal
details and uneven rhythm). **In every trial, the mean confidence of the AI set
minus the mean confidence of the human set must be ≥ 0.30.** Also, **no single
clearly-human piece may score higher than any clearly-AI piece.**

**Why this target:** If the two sets aren't far apart, the thresholds have
nothing to separate and the labels are a coin flip with nicer wording. I chose
0.30 because it is at least the width of my unsure band. A smaller gap means
easy cases could land on either side of the band. The "no overlap" rule is
there because an average can hide one bad outlier. If a clearly-human piece
outscores a clearly-AI piece, the system is ranking them wrong, not just
being cautious.

---

## 3. All three labels are reachable, and borderline text lands in unsure

Two parts, both checked in every trial:

- **(a)** Out of the 10 texts from criterion 2 plus 5 borderline texts, **each
  of the three labels (high-confidence AI, unsure, high-confidence human)
  appears at least once.**
- **(b)** The 5 borderline texts are 2 pieces of lightly-edited AI (a few
  sentences reworded by me) and 3 pieces of my own formal writing. **At least 3
  of the 5 must get the unsure label**, and **none of the 3 formal-human pieces
  may get the AI label.**

**Why this target:** The assignment requires that 0.51 and 0.95 get different
labels. A label nobody can reach is a gap in the ranges, and that is a bug, not
caution. The starter warns that a stub style signal makes the human label
unreachable. Part (b) is the actual reason for having an unsure band: hard
cases should end up there. I set it at 3 of 5, not 5 of 5, because lightly-edited
AI is supposed to be hard to catch. Missing it is the cheap error. Calling the formal
human pieces AI is the expensive error, so that part allows zero.

---

## 4. Every appeal is recorded and changes status: 10 of 10, with zero silent failures

I make 10 submissions, then appeal each one with its real `content_id` and a
sentence of reasoning. **All 10 must return `200` with `status:
"under_review"`.** For each one, `GET /log` must show a new entry with `event:
"appeal"`, the same `content_id`, the reasoning text word for word, and
`status: "under_review"`. The original decision entry must still be there,
unchanged. Also:

- An appeal with a made-up `content_id` returns `404` (`unknown_content_id`),
  and **no** appeal entry is written.
- A second appeal on the same `content_id` returns `409`
  (`already_under_review`).
- An appeal with blank `reasoning` returns `400` (`missing_reasoning`).

**Why this target:** The appeal is the only thing a wrongly accused writer can
do. An appeal that says "received" but never reaches the log is worse than
having no appeal button. The writer believes something is happening, and
nothing is. That's why the target is 10 of 10 and not "most". The 404 check
is there because a typo in the id must fail loudly. It must not look like
it worked.

---

## 5. Bad input is rejected cleanly: 8 of 8 malformed requests get a 4xx, never a 500

I send these 8 bodies to `/submit`: empty `text`, whitespace-only `text`, no
`text` field, `"text": null`, `"text": 12345`, no `creator_id`, a 10-word
`text`, and a 50,000-word `text`. **Each one must:**

- return the status and `error` code in my Milestone 1 contract (`400`
  `missing_text` / `missing_creator_id` / `text_too_short`, or `413`
  `text_too_long`), and **never a 500**;
- return no `content_id`, `guess`, or `label`;
- write one `log_rejection` entry to `logs/audit.jsonl`;
- respond in **under 2 seconds**, which proves the model was never run on it.

That is **8 of 8, in all three trials**.

**Why this target:** The service sits behind someone else's website. A 500 tells
the caller nothing and leaves the writer looking at a broken page. A confident
label on a 10-word text is a made-up verdict, since both signals are noise at
that length. The 2-second limit makes sure I reject before running the model:
a 50,000-word body sent to gpt2 is slow, and in unit 8 an attacker could use it
to tie up the service. Rejections are logged so that someone probing the input
rules leaves a record.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
