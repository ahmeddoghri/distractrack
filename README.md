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

## Research basis

- [CVPR 2025's distractor-aware memory and introspective updates for SAM2 tracking](https://openaccess.thecvf.com/content/CVPR2025/html/Videnovic_A_Distractor-Aware_Memory_for_Visual_Object_Tracking_with_SAM2_CVPR_2025_paper.html)
- Original implementation and benchmark in this repository are MIT licensed.

## License

MIT
