# Re-scorings

The purpose of this folder is to show how much the results change when one scoring setting changes: the detector seed, the window size or the amount of fault-free training data.

No new evaluation runs were made. Each folder below holds the same nine runs as `results/runs/` (`run1` to `run9`, both applications), scored again with one setting changed.

| Folder | Setting changed | Used in the report |
|---|---|---|
| `seeds/seed1` … `seed10` | Detector seed (the evaluation runs use 42; `seed42` reproduces them) | Experiment 2 |
| `windows/window10`, `window50` | Windows of 10 or 50 lines (the evaluation runs use 20) | Experiment 5 |
| `training-share/share0.25`, `share0.5`, `share0.75` | Only the first 25%, 50% or 75% of the training part | Experiment 5 |
| `configs/` | The configuration used for each re-scoring | |

Each run folder holds `processed/` and `evaluate.log`. The analyses of these re-scorings are in `results/analysis/seeds/`, `windows/` and `training-share/`. To rebuild them, see Section 6.4 of the configuration manual.
