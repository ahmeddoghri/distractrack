# distractrack

**A distractor-aware video memory that remembers motion, not just the last bright blob.**

distractrack is a compact, inspectable implementation inspired by [CVPR 2025's distractor-aware memory and introspective updates for SAM2 tracking.](https://openaccess.thecvf.com/content/CVPR2025/html/Videnovic_A_Distractor-Aware_Memory_for_Visual_Object_Tracking_with_SAM2_CVPR_2025_paper.html).
It turns the paper's core idea into a deterministic benchmark that runs on a laptop with Python's standard library.

## Run it

```bash
python distractrack.py
python -m unittest discover -s tests -v
```

The benchmark writes its result to stdout. Audio projects also write playable WAV files to `demo/`.

## What is tested

The test compares the research-inspired method with a deliberately legible baseline and requires
`tracking_gain_pct >= 20`. The data generator is seeded, so the number in this README,
CI, and the portfolio case study can be reproduced.

## Scope

This is an educational research reproduction on controlled synthetic data. It is not a clinical,
diagnostic, production genomics, copyright-authentication, or safety-critical system. The point is
to make one mechanism measurable without hiding it behind a checkpoint or API.

## Research basis

- [CVPR 2025's distractor-aware memory and introspective updates for SAM2 tracking.](https://openaccess.thecvf.com/content/CVPR2025/html/Videnovic_A_Distractor-Aware_Memory_for_Visual_Object_Tracking_with_SAM2_CVPR_2025_paper.html)
- Original implementation and benchmark in this repository are MIT licensed.

## License

MIT

## Reproduced result

| Metric | Value |
|---|---:|
| `recency_accuracy` | **0.738** |
| `distractor_aware_accuracy` | **1.0** |
| `tracking_gain_pct` | **26.2** |
