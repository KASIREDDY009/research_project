# SFLAD evaluation artefact

This repository measures how much detection accuracy a **source-free** log anomaly detector loses, compared with a detector trained on a **labelled source**, on two AWS Lambda applications.

- **The applications.** Two small Lambda applications, `orders` and `bookings`, each with its own DynamoDB table and CloudWatch log group.
- **The faults.** The evaluation-run script injects five kinds of fault into the functions' configuration and restores each one straight after:
  - permission: an execution role that may only write logs;
  - config: a table name that does not exist;
  - timeout: an unreachable DynamoDB endpoint and a 3 s timeout;
  - resource: memory below the working set;
  - latency: the application waits 4 s or 6 s before handling each request (an environment variable), so calls succeed but slowly and log no error.
- **The labels.** A log line is a fault line when the call it belongs to was faulty: a Lambda error, a 5xx response, slower than the run's slow limit (the slowest call of the fault-free window plus 1 s), or an answer without the expected content. The request script measures each call; log text never decides a label.
- **The detectors.** Every detector is scored on the same 20-line windows of the logs. Every learned detector sets its alarm threshold at a 1% false-alarm target on the later half of the fault-free window; the source-free detectors train on its earlier half.

| Detector | Kind | What it learns from |
|---|---|---|
| Isolation Forest with a novelty gate | Source-free | Only a fault-free window of the application's own logs |
| DeepLog-style LSTM | Source-free | Only a fault-free window of the application's own logs |
| BGL-trained baseline (Random Forest) | Labelled source | The labelled LogHub BGL_2k sample |
| OpenStack-trained baseline (Random Forest) | Labelled source | The labelled LogHub OpenStack set |
| Similar-application baseline (Random Forest) | Labelled source | The other application's labelled logs, from another run of the same set |
| Threshold alarms | Reference | Nothing: a window alarms when at least two of its lines hold an error keyword |

Three ablations are scored beside them: the Isolation Forest without its gate, the gate alone, and the source-free detector on the BGL-trained baseline's feature space (no labels).

**Forfeiture** is a baseline's F1 minus a source-free detector's F1; a positive value means the source-free detector is less accurate.

## Folders

| Folder | What is in it |
|---|---|
| `src/apps/` | The two Lambda applications |
| `src/sflad/` | The evaluation run (`aws/`), the detectors, the log template parser, scoring and analysis |
| `configs/` | `aws.yaml`: region, run shape and slow-limit margin. `default.yaml`: detectors, windows, calibration split, analysis. `corpus.yaml`: checksums of the BGL and OpenStack sources |
| `infra/terraform/` | The AWS stack: both applications, an S3 bucket and the SageMaker role |
| `scripts/` | `setup/`: corpus downloads. `aws/`: deploy, evaluation run, SageMaker scoring. `scoring/`: labelling rebuild, scoring, re-scoring, calibration, demo |
| `notebooks/` | `evaluation.ipynb`, which rebuilds every figure and table |
| `tests/` | Unit tests |
| `data/` | Inputs only: the labelled BGL and OpenStack sources; `data/README.md` describes them |
| `results/` | Everything the evaluation produced; `results/README.md` explains each folder and file |

The run data (`results/runs/` and `results/rescoring/`) and the full LogHub logs (`data/public_corpus/full/`) ship in `ict_solution.zip`. The GitHub repository holds them too, except `BGL.log`, `HDFS.log` and `HDFS_v1.zip`, which are over GitHub's 100 MB file limit; `./scripts/setup/download_loghub_full.sh` downloads them. Check the run data with `cd results && shasum -a 256 -c SHA256SUMS` (the list leaves out the re-scorings' copies of `raw/`, each an exact copy of the matching run's `raw/`).

## 1. Set up (local)

Python 3.12, from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest tests -q
```

If a BGL file under `data/public_corpus/` is missing, run `./scripts/setup/download_loghub_corpus.sh`. If `data/public_corpus/OpenStack/source_events.jsonl` is missing, rebuild it from the full LogHub logs in `data/public_corpus/full/` (if a file there is missing, run `./scripts/setup/download_loghub_full.sh` first):

```bash
python scripts/setup/build_source.py OpenStack --input data/public_corpus/full \
    --out data/public_corpus/OpenStack/source_events.jsonl
```

## 2. Run the experiment (AWS)

This step needs the AWS CLI v2, Terraform 1.5 or later, and rights for Lambda, DynamoDB, CloudWatch Logs, IAM, S3 and SageMaker. Keep credentials out of the repository. Two account limits must be high enough: Lambda concurrent executions at least 10 (a run reaches 8), and the SageMaker quota "ml.t3.xlarge for processing job usage" at least 2 (each scoring command starts two jobs; while no slot is free, the launcher waits and tries again every 5 minutes). Both limits are per region; ask for an increase in the Service Quotas console if needed. One stack exists per account at a time: the S3 bucket and the IAM role names are account-wide, so a stack in a second region needs the first one removed.

The region is set once, in `configs/aws.yaml` (`region: eu-west-1`). The evaluation runs read it there, and `tf_apply.sh` and `tf_destroy.sh` pass it to Terraform. Export the same region for the AWS CLI commands below.

There are nine evaluation runs, `run1` to `run9`, in three sets: runs 1–3, 4–6 and 7–9. Run N uses fault-order seed N. Each run starts on a fresh deployment:

```bash
export AWS_DEFAULT_REGION=eu-west-1
./scripts/aws/tf_destroy.sh && ./scripts/aws/tf_apply.sh

# check that both functions answer 201, then wait five minutes
aws lambda invoke --function-name sflad-orders-api --cli-binary-format raw-in-base64-out \
  --payload '{"httpMethod":"POST","path":"/orders","body":"{\"sku\":\"SKU-000001\",\"quantity\":1}"}' /dev/stdout
aws lambda invoke --function-name sflad-bookings-api --cli-binary-format raw-in-base64-out \
  --payload '{"httpMethod":"POST","path":"/bookings","body":"{\"venue\":\"V000001\",\"slot\":0,\"guests\":1}"}' /dev/stdout

./scripts/aws/run_evaluation.sh run1 1
```

`run_evaluation.sh` drives both applications at the same time:

1. a fault-free window of 600 create-then-read cycles;
2. 300 fault episodes, 60 per category, in one shuffled order;
3. a fault-free elasticity window of concurrent bursts;
4. the export of the labelled logs to `results/runs/run1/<app>/raw/`.

An existing run folder is never overwritten. The shipped `run1` to `run9` already exist, so a repeat beside them takes new tags (for example `rerun1 1`) and the same tags in the commands below. A repeat with the same seed injects the faults in the same order (`episode_order` in `raw/run.json`), but AWS timing, request ids and cold starts differ, so it records new logs: its scores are a new sample of the same experiment, not a copy of the shipped runs. The shipped runs themselves are rebuilt locally from their raw files (Section 3).

After the third run of a set, score each run once. Each run is paired with a run of the other application from the same set, which is its similar-application source. Scoring runs on SageMaker and writes `processed/` beside `raw/`. For set 1:

```bash
./scripts/aws/score_pair.sh results/runs/run1/orders   results/runs/run2/bookings
./scripts/aws/score_pair.sh results/runs/run1/bookings results/runs/run3/orders
./scripts/aws/score_pair.sh results/runs/run2/orders   results/runs/run3/bookings
```

Sets 2 and 3 use runs 4–6 and 7–9 in the same pattern. `./scripts/aws/tf_destroy.sh` removes the stack at the end.

## 3. Analyse (local)

Each run's labelled log lines (`raw/events.jsonl`) and counts (`raw/export.json`) are built from its raw CloudWatch export and the request script's records. They can be rebuilt without AWS and compared with the shipped files:

```bash
python scripts/scoring/relabel_run.py results/runs/run1/orders/raw /tmp/relabel/run1/orders
cmp /tmp/relabel/run1/orders/events.jsonl results/runs/run1/orders/raw/events.jsonl
```

A run is scored locally with `python scripts/scoring/evaluate_run.py <copy of the run folder> --similar-source <partner run>/raw/events.jsonl`, the command the SageMaker jobs ran.

Run each command for `orders` and for `bookings`:

```bash
# main result: the nine runs pooled
python -m sflad.pipeline.analysis   results/analysis/pooled/orders     results/runs/run{1..9}/orders
# each set on its own (set2: runs 4..6, set3: runs 7..9)
python -m sflad.pipeline.analysis   results/analysis/sets/set1/orders  results/runs/run{1..3}/orders
# every run side by side
python -m sflad.pipeline.comparison results/analysis/comparison/orders results/runs/run{1..9}/orders
```

Supplementary re-scorings run locally on copies of each run's `raw/`. Each uses a copy of `configs/default.yaml` with one setting changed: the detector seed, the window size, or the share of the training part used. A run that already has `processed/results.json` is skipped, so to repeat the shipped re-scorings, first move `results/rescoring` aside (for example `mv results/rescoring results/rescoring_shipped`). `rescore.py` re-scores the runs `run1` to `run9` with the partners of Section 2.

```bash
python scripts/scoring/rescore.py seed 42,1,2,3,4,5,6,7,8,9,10    # -> results/rescoring/seeds/
python scripts/scoring/rescore.py window 10,50                    # -> results/rescoring/windows/
python scripts/scoring/rescore.py share 0.25,0.5,0.75             # -> results/rescoring/training-share/
python -m sflad.pipeline.analysis results/analysis/seeds/seed1/orders results/rescoring/seeds/seed1/run{1..9}/orders   # seeds 1..10
python -m sflad.pipeline.analysis results/analysis/windows/window10/orders results/rescoring/windows/window10/run{1..9}/orders
python -m sflad.pipeline.analysis results/analysis/training-share/share0.25/orders results/rescoring/training-share/share0.25/run{1..9}/orders
```

The benchmark calibration scores the BGL-trained baseline on the public LogHub logs (all of BGL and OpenStack, and the first 5,000,000 HDFS lines, the size of the HDFS set in the published ELFA-Log results), in `data/public_corpus/full/` (if a file there is missing, run `./scripts/setup/download_loghub_full.sh` first):

```bash
python scripts/scoring/calibrate_transfer_loghub.py               # -> results/calibration/
```

Checksums of the run data:

```bash
cd results && find runs rescoring -type f -not -path 'rescoring/*/*/run*/*/raw/*' -not -name README.md | sort | xargs shasum -a 256 > SHA256SUMS
```

## 4. Figures and tables

Install the notebook packages into the same environment (`.venv`):

```bash
pip install -r requirements-analysis.txt
```

Open `notebooks/evaluation.ipynb` in Visual Studio Code, select the `.venv` kernel and click Run All. Without Visual Studio Code:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/evaluation.ipynb
```

The figures are written to `notebooks/figures/` and the tables to `notebooks/tables/`.

## Settings and versions

- Windows: 20 lines, non-overlapping.
- Every learned detector's alarm level is set to a 1% false-alarm target on the later half of the fault-free window (the calibration part), without test labels; the source-free detectors train on its earlier half.
- A call is slow when it takes longer than the slowest call of the run's fault-free window plus 1 s (`configs/aws.yaml`).
- Detector seed: 42.
- Run shape: `configs/aws.yaml`. Detector and analysis settings: `configs/default.yaml`.
- Exact package versions: `requirements.txt`.
- Each run records its library versions (`processed/results.json`).
