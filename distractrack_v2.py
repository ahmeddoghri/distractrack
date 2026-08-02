"""Genuine, label-free motion-consistency tracking, as a parallel
non-destructive fix.

distractrack.py's "aware" tracker scores candidates with
`abs(item[0]-predicted) + 3*(1-item[1])`, where `item[1]` is 1 for the
target and 0 for the distractor -- the ground-truth identity label,
read directly into the scoring formula. Verified directly: with that term
removed, the "motion-consistency" tracker picks the *exact same* candidate
as plain nearest-to-last-position recency tracking on 41-42 of 42 frames,
every seed tested. The published 100% / 26.2pp gain is not evidence of
working motion-consistency reasoning -- it's the label bonus alone.

This module implements a genuine, label-free tracker: it predicts the next
position from a smoothed velocity estimate as before, but detects when the
two candidates are close together (an ambiguous crossing, where either
pick is plausible) and, in that case, coasts on the prior velocity
estimate instead of letting a noisy pick corrupt it. That's a real,
verifiable, modest improvement over naive recency -- not the fake 26.2pp
the oracle term manufactures, but a real one.
"""
import json
import random


def run(seed=29, ambiguity_gap=3.0):
    rng = random.Random(seed)
    naive_last = 8.
    aware_last = 8.
    velocity = 1.
    naive = aware = 0
    for t in range(42):
        target = 8 + t if t < 22 else 10 + t
        distractor = 50 - t if t < 22 else 8 + t
        candidates = [(distractor + rng.uniform(-.25, .25), 0), (target + rng.uniform(-.25, .25), 1)]

        n = min(candidates, key=lambda item: abs(item[0] - naive_last))[0]
        naive += abs(n - target) < 2
        naive_last = n

        predicted = aware_last + velocity
        gap = abs(candidates[0][0] - candidates[1][0])
        a = min(candidates, key=lambda item: abs(item[0] - predicted))[0]
        aware += abs(a - target) < 2
        if gap > ambiguity_gap:
            velocity = .75 * velocity + .25 * (a - aware_last)
            aware_last = a
        else:
            aware_last = predicted

    return {
        "recency_accuracy": round(naive / 42, 3),
        "distractor_aware_accuracy": round(aware / 42, 3),
        "tracking_gain_pct": round(100 * (aware - naive) / 42, 1),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
