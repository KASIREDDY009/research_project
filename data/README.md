# Data

Inputs of the evaluation. Nothing in this folder is produced by the runs.

| File | What it holds |
|---|---|
| `public_corpus/BGL/BGL_2k.log` | The LogHub BGL_2k sample: 2,000 labelled log lines from the BlueGene/L supercomputer |
| `public_corpus/BGL/source_events.jsonl` | The same lines as labelled events, the source of the BGL-trained baseline |
| `public_corpus/OpenStack/source_events.jsonl` | The labelled LogHub OpenStack set (`openstack_normal1.log` and `openstack_abnormal.log`, labelled with `anomaly_labels.txt`) as 70,746 labelled events, 18,434 of them anomalous: the source of the OpenStack-trained baseline |
| `public_corpus/SHA256SUMS.txt` | Checksums of the three files, also pinned in `configs/corpus.yaml` with the checksums of the original LogHub files |

Both `source_events.jsonl` files are built by `scripts/setup/build_source.py` (`BGL` from the sample, `OpenStack` from the full LogHub OpenStack files). `scripts/setup/download_loghub_corpus.sh` downloads the BGL sample, rebuilds its source and checks both. The full LogHub logs, for the OpenStack source and the benchmark calibration, go to `public_corpus/full/` (shipped in `ict_solution.zip`; the GitHub repository leaves out `BGL.log`, `HDFS.log` and `HDFS_v1.zip`, which are over its 100 MB file limit, and `scripts/setup/download_loghub_full.sh` downloads them). `python scripts/setup/build_source.py OpenStack --input data/public_corpus/full --out data/public_corpus/OpenStack/source_events.jsonl` rebuilds the OpenStack source; it stops when one of the three LogHub files or the result differs from its pin in `configs/corpus.yaml`.

LogHub data is used under its licence for research (https://github.com/logpai/loghub#license); dataset DOI 10.5281/zenodo.8196385.
