# distractrack

**A distractor-aware video memory that remembers motion, not just the last bright blob.**

A tracker with no memory of *how* its target moves is one lookalike away from losing the plot entirely. It sees something bright and roughly where the target was last frame, and it locks on — even if the real target is somewhere else, doing something else, and a near-identical distractor just wandered across its path. distractrack keeps a running estimate of the target's velocity and uses it to break the tie: if a candidate matches where the target *should* be given its motion, it wins, distractor or not.

It's a compact, inspectable implementation inspired by [CVPR 2025's distractor-aware memory and introspective updates for SAM2 tracking](https://openaccess.thecvf.com/content/CVPR2025/html/Videnovic_A_Distractor-Aware_Memory_for_Visual_Object_Tracking_with_SAM2_CVPR_2025_paper.html), rebuilt small enough to read in one sitting and run without a GPU, a checkpoint, or an API key.

## The result

```bash
python distractrack.py
```
```json
{
  "recency_accuracy": 0.738,
  "distractor_aware_accuracy": 1.0,
  "tracking_gain_pct": 26.2
}
```

Track by nearest-to-last-position alone across a 42-frame sequence with a moving distractor crossing the target's path, and you land the target correctly 73.8% of the time — the rest of the time, the tracker calmly follows the wrong object. Add a velocity estimate and penalize candidates that don't fit the target's expected trajectory, and tracking hits 100% — a 26.2 percentage-point gain from remembering *how* the target moves, not just where it was a moment ago.

**Update:** the "penalize candidates that don't fit" step doesn't use
motion at all. Its scoring formula includes `3*(1-item[1])`, where
`item[1]` is `1` for the true target and `0` for the distractor — the
ground-truth identity label, read directly. With that term removed, the
"motion-consistency" tracker picks the exact same candidate as plain
nearest-to-last-position recency on 41–42 of every 42 frames, every seed
tested — mean gain over naive: exactly `0.0`. `distractrack_v2.py` removes
the oracle term and adds a genuine (label-free) fix — hysteresis through
ambiguous crossings — that recovers a real, modest, never-negative gain
(~1.7–2.8pp, nowhere near 26.2pp). Details below.

## How it works

A synthetic 42-frame sequence has a target on a piecewise-linear path and a distractor that crosses directly through the target's trajectory partway through. The naive tracker (`recency`) always picks whichever candidate is closest to its last known position — exactly the failure mode that lets a distractor hijack a track. The distractor-aware tracker maintains a smoothed velocity estimate, predicts where the target should be this frame, and picks the candidate closest to that *prediction* rather than the last position, with a penalty against non-target candidates. No neural memory bank — just motion-consistency scoring, made explicit.

## Run it

```bash
python distractrack.py
python -m unittest discover -s tests -v
```

## What is tested

The test compares distractor-aware tracking against the recency-only baseline and requires `tracking_gain_pct >= 20`. The data generator is seeded, so the number in this README, in CI, and in the portfolio case study are the same number, not three different ones that happen to rhyme.

## Scope

This is an educational research reproduction on a single controlled synthetic trajectory. It is not a clinical, diagnostic, production video-tracking, or safety-critical system, and it makes no claim about real SAM2 benchmark results. The point is to make one mechanism — motion-consistency scoring beats nearest-position matching under distraction — measurable without hiding it behind a checkpoint.

## The motion-consistency mechanism never ran

`distractrack.py`'s aware tracker scores candidates with
`abs(item[0]-predicted) + 3*(1-item[1])`. `item[1]` isn't a motion feature
— it's the exact target/distractor identity label the tracker is supposed
to be inferring. Checked directly across 60 seeds: `distractor_aware_accuracy`
is exactly `1.0` every time, zero variance, because a flat +3 penalty on
the distractor overwhelms any realistic distance difference.

```bash
python eval_v2.py
```
```
published seed=29:                          tracking_gain_pct=26.2
same seed, label-free (no hysteresis fix):   tracking_gain_pct=0.0
same seed, label-free + hysteresis fix:      tracking_gain_pct=11.9

tuning (60 seeds):  published_mean=24.53  label_free_mean=0.0  hysteresis_fix_mean=2.78  worst=0.0
holdout (30 seeds): published_mean=25.72  label_free_mean=0.0  hysteresis_fix_mean=1.66  worst=0.0
```

Removing the label bonus (no other change) makes the "aware" tracker pick
the *identical* candidate to plain nearest-to-last-position recency on
41–42 of every 42 frames — mean gain over naive is exactly `0.0` across
every seed tested. The velocity-extrapolation mechanism itself contributes
nothing; the entire published 26.2pp came from the oracle term.

`distractrack_v2.py` keeps the velocity model but adds a real, label-free
mechanism: when the two candidates are close together (an ambiguous
crossing, where either pick is plausible), it coasts on the prior velocity
estimate instead of letting a noisy pick corrupt it, rather than
committing hard every frame. That recovers a real gain — never negative on
any of 90 tuning+holdout seeds — but a modest one (mean 1.7–2.8pp), because
after the crossing the distractor moves in exact lockstep with the target
at a constant offset, which is genuinely, information-theoretically
indistinguishable from motion alone. `distractrack.py` is untouched and
the published 26.2pp number still reproduces exactly.

## Research basis

- [CVPR 2025's distractor-aware memory and introspective updates for SAM2 tracking](https://openaccess.thecvf.com/content/CVPR2025/html/Videnovic_A_Distractor-Aware_Memory_for_Visual_Object_Tracking_with_SAM2_CVPR_2025_paper.html)
- Original implementation and benchmark in this repository are MIT licensed.

## License

MIT
