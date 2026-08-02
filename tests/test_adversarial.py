import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import distractrack
import distractrack_v2
from adversarial import HOLDOUT_SEEDS, TUNING_SEEDS
from eval_v2 import summarize


class AdversarialTest(unittest.TestCase):
    def test_holdout_disjoint_from_tuning(self):
        self.assertTrue(set(TUNING_SEEDS).isdisjoint(HOLDOUT_SEEDS))

    def test_original_benchmark_still_reproduces_exactly(self):
        result = distractrack.run()
        self.assertEqual(result["recency_accuracy"], 0.738)
        self.assertEqual(result["distractor_aware_accuracy"], 1.0)
        self.assertEqual(result["tracking_gain_pct"], 26.2)

    def test_original_bug_aware_tracker_always_hits_exactly_1_0(self):
        """distractrack.py's distractor_aware_accuracy is mathematically
        guaranteed to be near-perfect: the +3*(1-item[1]) term in its
        scoring function reads item[1], the ground-truth target/distractor
        identity label, directly. Proven across 60 seeds: always exactly
        1.0, zero variance."""
        results = [distractrack.run(seed=seed)["distractor_aware_accuracy"] for seed in TUNING_SEEDS]
        self.assertEqual(set(results), {1.0})

    def test_removing_the_oracle_term_yields_zero_gain_over_naive(self):
        """With the label bonus removed and no hysteresis fix, the
        "motion-consistency" tracker picks the exact same candidate as
        plain nearest-to-last-position recency on every frame that
        matters -- mean gain is exactly 0.0 across every tuning seed."""
        gains = [distractrack_v2.run(seed=seed, ambiguity_gap=0)["tracking_gain_pct"] for seed in TUNING_SEEDS]
        self.assertEqual(set(gains), {0.0})

    def test_hysteresis_fix_never_regresses_below_naive_on_tuning_seeds(self):
        result = summarize(TUNING_SEEDS)
        self.assertEqual(result["label_free_with_hysteresis_worst_pct"], 0.0)
        self.assertGreater(result["label_free_with_hysteresis_gain_mean_pct"], 0)

    def test_hysteresis_fix_never_regresses_below_naive_on_frozen_holdout_seeds(self):
        result = summarize(HOLDOUT_SEEDS)
        self.assertEqual(result["label_free_with_hysteresis_worst_pct"], 0.0)
        self.assertGreater(result["label_free_with_hysteresis_gain_mean_pct"], 0)

    def test_hysteresis_fix_gain_is_real_but_far_below_the_oracle_claim(self):
        result = summarize(TUNING_SEEDS)
        self.assertLess(result["label_free_with_hysteresis_gain_mean_pct"], result["published_oracle_gain_mean_pct"] / 2)

    def test_original_module_untouched(self):
        import inspect

        source = inspect.getsource(distractrack.run)
        self.assertIn("3*(1-item[1])", source)

    def test_report_is_reproducible(self):
        a = summarize(TUNING_SEEDS[:5])
        b = summarize(TUNING_SEEDS[:5])
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
