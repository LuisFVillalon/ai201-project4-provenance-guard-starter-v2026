"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.

    My choice: the coefficient of variation (stdev / mean) of words per
    sentence. Roughly 0.2 is very even, 0.7+ is very lumpy. **Higher = more
    human.** Fewer than two sentences returns 0.0, but `style_signal` doesn't
    trust this measure below MIN_SENTENCES_FOR_SPREAD and scores it neutral
    instead — "no spread to measure" is not evidence of AI.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.

    My choice: a moving-average TTR — the plain ratio inside every
    TTR_WINDOW-word window, averaged. That keeps a 60-word piece and a
    600-word piece on the same scale. Texts shorter than the window fall back
    to the plain ratio. **Higher = more human.**
    """
    toks = words(text)
    if not toks:
        return 0.0
    if len(toks) <= TTR_WINDOW:
        return len(set(toks)) / len(toks)
    ratios = [
        len(set(toks[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(toks) - TTR_WINDOW + 1)
    ]
    return statistics.mean(ratios)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.

    My choice: only the "varied" marks — ; : — – ( ) ! ? and double hyphens —
    per word. Full stops and commas are left out because every writer uses
    them. **Higher = more human.**
    """
    toks = words(text)
    if not toks:
        return 0.0
    marks = len(re.findall(r"[;:!?()—–]|--", text))
    return marks / len(toks)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.

    My answers:

      1. All three measures run "higher = more human", so all three get
         flipped.
      2. Each is mapped linearly onto 0–1 between a "very AI" and a "very
         human" anchor (the *_RANGE constants below, set from my calibration
         runs) and clamped. Then a weighted average, spread counting most
         because it separated my calibration inputs best, and TTR least
         (see the note on the weights below).
    """
    def flip(value, ai_end, human_end):
        # 0.0 at the human end, 1.0 at the AI end, clamped.
        return min(max((human_end - value) / (human_end - ai_end), 0.0), 1.0)

    if len(sentences(text)) >= MIN_SENTENCES_FOR_SPREAD:
        spread_ai = flip(sentence_length_spread(text), *SPREAD_RANGE)
    else:
        spread_ai = 0.5  # too few sentences to say anything
    ttr_ai = flip(type_token_ratio(text), *TTR_RANGE)
    punct_ai = flip(punctuation_density(text), *PUNCT_RANGE)

    score = (
        WEIGHT_SPREAD * spread_ai
        + WEIGHT_TTR * ttr_ai
        + WEIGHT_PUNCT * punct_ai
    )
    return round(score, 4)


# ── Calibration ──────────────────────────────────────────────────────────────
# (ai_end, human_end) for each measure: the raw value that scores 1.0 (very AI)
# and the one that scores 0.0 (very human).

SPREAD_RANGE = (0.20, 0.70)
TTR_RANGE = (0.60, 0.85)
PUNCT_RANGE = (0.0, 0.05)

# TTR is weighted lowest on purpose. In calibration it ran the wrong way: the
# clearly-AI text had the MOST varied vocabulary (0.91) and the plain human
# text the least (0.77). All it reliably detects is plain writing, which is
# the false positive I most want to avoid.
#
# UNIT 8 IMPROVEMENT (the one change): TTR removed from the style signal.
# Before: spread 0.5 / TTR 0.2 / punct 0.3. AI prose has varied vocabulary
# (TTR 0.87–0.90, above the 0.85 "very human" anchor), so TTR contributed 0 on
# AI text and capped the style signal at 0.80. With style stuck at 0.80 the
# combined score could only reach AI_THRESHOLD (0.90) with model_score = 1.00,
# so the ai label was unreachable for ordinary AI text (criterion 3a miss).
# TTR's 0.2 is split between the other two in their existing 5:3 ratio.
WEIGHT_SPREAD = 0.625
WEIGHT_TTR = 0.0
WEIGHT_PUNCT = 0.375

TTR_WINDOW = 50
MIN_SENTENCES_FOR_SPREAD = 3


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
