# BGL-trained baseline on public LogHub transfer pairs

Window 20, step 20; seed 42; the baseline as configured for the evaluation. Targets are split chronologically in half and the second half is scored; the later half of the first half's normal lines sets the alarm threshold, as in the evaluation. HDFS lines are grouped by block session; every line of openstack_abnormal.log counts as an anomaly.

| Corpus | Lines used | Anomalous lines | ELFA-Log messages | ELFA-Log anomalies |
|---|---:|---:|---:|---:|
| BGL | 4,747,963 | 348,460 | 4,747,963 | 348,460 |
| HDFS | 5,000,000 | 145,864 | 5,000,000 | 284,818 |
| OpenStack | 70,746 | 18,434 | 70,724 | 18,435 |

ELFA-Log is a deep model with domain-adversarial alignment, evaluated under its own protocol; its values
are shown for comparison of scale only.

| Pair | F1 (%) | MCC | AUC | Precision | Recall | FAR | ELFA-Log F1 (%) | ELFA-Log MCC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BGL->HDFS | 0.83 | -0.014 | 0.542 | 0.03 | 0.01 | 0.012 | 71.83 | 0.674 |
| BGL->OpenStack | 0.22 | 0.023 | 0.500 | 1.00 | 0.00 | 0.000 | 58.43 | 0.054 |

HDFS scored per block session (a block alarms when any of its windows alarms):

| Blocks | F1 (%) | MCC | AUC | Precision | Recall | FAR |
|---:|---:|---:|---:|---:|---:|---:|
| 137374 | 1.48 | 0.057 | 0.526 | 0.48 | 0.01 | 0.000 |

n/a marks an undefined value (for example precision when no alarm was raised).
