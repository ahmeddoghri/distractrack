"""Compare the published oracle-leaking tracker to a genuine, label-free
implementation, showing the published gain is almost entirely the oracle
term, not motion-consistency reasoning."""
import json
import statistics as st

import distractrack
import distractrack_v2
from adversarial import HOLDOUT_SEEDS, TUNING_SEEDS


def summarize(seeds):
    published = [distractrack.run(seed=seed)["tracking_gain_pct"] for seed in seeds]
    no_oracle_no_fix = [distractrack_v2.run(seed=seed, ambiguity_gap=0)["tracking_gain_pct"] for seed in seeds]
    genuine_fixed = [distractrack_v2.run(seed=seed)["tracking_gain_pct"] for seed in seeds]
    return {
        "n": len(seeds),
        "published_oracle_gain_mean_pct": round(st.mean(published), 2),
        "label_free_no_hysteresis_gain_mean_pct": round(st.mean(no_oracle_no_fix), 2),
        "label_free_with_hysteresis_gain_mean_pct": round(st.mean(genuine_fixed), 2),
        "label_free_with_hysteresis_worst_pct": min(genuine_fixed),
    }


def main():
    print("distractrack eval_v2: oracle-leaking tracker vs. genuine label-free tracker")
    print(f"published seed=29: {distractrack.run(seed=29)}")
    print(f"same seed, label-free (no hysteresis fix): {distractrack_v2.run(seed=29, ambiguity_gap=0)}")
    print(f"same seed, label-free + hysteresis fix:     {distractrack_v2.run(seed=29)}")
    for label, seeds in (("tuning", TUNING_SEEDS), ("holdout", HOLDOUT_SEEDS)):
        print(f"\n{label} ({len(seeds)} seeds):")
        print(json.dumps(summarize(seeds), indent=2))


if __name__ == "__main__":
    main()
