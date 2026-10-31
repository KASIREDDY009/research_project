# Results guide

Everything the evaluation produced. `runs/` and `rescoring/` ship in `ict_solution.zip` and in the GitHub repository. To check them, run `cd results && shasum -a 256 -c SHA256SUMS`. `<app>` is `orders` or `bookings`, the two Lambda applications.

## Layout

| Folder | What it holds |
|---|---|
| `runs/run1` … `runs/run9` | The nine evaluation runs, in three sets (runs 1–3, 4–6, 7–9): the primary results |
| `rescoring/README.md` | What the re-scorings are for |
| `rescoring/seeds/seed1` … `seed10`, `seed42` | The nine runs re-scored with other detector seeds; `seed42` reproduces the primary results |
| `rescoring/windows/window10`, `window50` | The nine runs re-scored with windows of 10 and 50 lines |
| `rescoring/training-share/share0.25` … `share0.75` | The nine runs re-scored with only the first 25%, 50% or 75% of the training part (the calibration part unchanged) |
| `rescoring/configs/` | The configuration copy used for each re-scoring (one setting changed) |
| `analysis/pooled/<app>/` | The main result: the nine runs pooled (`analysis.md` readable, `analysis.json`) |
| `analysis/sets/set1` … `set3` | Each set of three runs analysed on its own |
| `analysis/seeds/seed1` … `seed10` | The analysis with each other detector seed |
| `analysis/windows/`, `analysis/training-share/` | The analysis of each window size and each training share (supplementary) |
| `analysis/comparison/<app>/` | Every run side by side (`comparison.md`) |
| `calibration/` | The BGL-trained baseline scored on public LogHub benchmark pairs (`calibration.md`) |
| `sagemaker_jobs.json` | The 18 SageMaker scoring jobs: name, status, creation and end time, from `aws sagemaker list-processing-jobs` (the jobs named `sflad-eval-run<i>-run<j>-<app>-…`, with the set of each run pair added); read by the notebook's cost table |

The report's figures and tables are in `../notebooks/figures/` and `../notebooks/tables/`, rebuilt by `../notebooks/evaluation.ipynb`.

In every `raw/` file the AWS account id is replaced by `<ACCOUNT>`. In `rescoring/`, each re-scoring folder holds `raw/`, an exact copy of the matching run's `raw/` folder, beside its `processed/` and `evaluate.log`; `SHA256SUMS` leaves these copies out.

## Inside one run: `runs/runN/<app>/`

| File | What it holds |
|---|---|
| `raw/export.json` | Counts for the run: invocations, the slow limit, faulty calls per phase and per reason (failed, slow, incorrect), calls refused before they ran and sent again, log lines, blank lines, fault episodes and lines with no recorded invocation (`orphan_lines`) |
| `raw/events.jsonl` | Every exported log line, with its label (fault or normal), its fault category and delay, and whether it is in the fault-free window |
| `raw/invocations.jsonl` | Every request sent, with its AWS request id, start and end times, status, expected answer and outcome |
| `raw/episodes.jsonl` | Every injected fault: category, delay (latency fault), start and restore times, and how many calls were faulty |
| `raw/deployment.json` | The log group's creation time and the function's last-modified time |
| `raw/run.json` | The run's seed, episode order, slow limit, timings and configuration, and the deployed function settings |
| `raw/cloudwatch_events.jsonl` | The log lines as returned by CloudWatch |
| `processed/clean_window_certificate.json` | The check that the fault-free window holds no faulty call |
| `processed/results.json` | Every metric for every detector (including detection delay), plus each detector's settings, training and scoring times, and the library versions |
| `processed/window_predictions.json` | Each detector's alarm (1) or no alarm (0) on every 20-line window, with the true label, fault category, delay, end time, and whether the window is an elasticity window or holds a new execution environment's start |
| `processed/summary.txt` | A readable summary of the run's results |
| `processed/models/` | The trained detectors |
| `run.log`, `evaluate.log` | The run's log and its scoring log |

## The two kinds of seed

- **Fault-order seed:** run `runN` uses seed N (1 to 9). It sets the shuffled order of the run's 300 fault episodes (60 of each of the five categories).
- **Detector seed:** the primary results use seed 42. It fixes the random choices inside the Isolation Forest, the Random Forests and the DeepLog-style model, so the same seed always gives the same result. `rescoring/seeds/` repeats the scoring with seeds 1 to 10.

## The detectors (names used in the files)

Every learned detector sets its alarm threshold on the calibration part (the later half of the fault-free window); the source-free detectors train on its earlier half.

| Name in the files | Detector |
|---|---|
| `source_free` | Isolation Forest with novelty gate, trained only on the application's fault-free logs |
| `source_free_deeplog` | DeepLog-style model, trained only on the application's fault-free logs |
| `transfer` | Random Forest trained on the labelled BGL logs |
| `transfer_openstack` | Random Forest trained on the labelled OpenStack logs |
| `transfer_similar` | Random Forest trained on the other application's labelled logs, from another run of the same set |
| `threshold` | Keyword threshold alarms |
| `source_free_forest` | Ablation: the Isolation Forest without its novelty gate |
| `novelty_gate` | Ablation: the novelty gate alone |
| `source_free_source_features` | Ablation: the source-free detector on the BGL-trained baseline's feature space (no labels) |
