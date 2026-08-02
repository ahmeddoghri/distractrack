"""Adversarial seeds for the label-free tracking fix.

TUNING_SEEDS: used to characterize the oracle leak and select the
ambiguity_gap hysteresis threshold in distractrack_v2.py.
HOLDOUT_SEEDS: disjoint, evaluated exactly once after the fix was finalized.
"""

TUNING_SEEDS = list(range(1, 61))
HOLDOUT_SEEDS = list(range(1000, 1030))
