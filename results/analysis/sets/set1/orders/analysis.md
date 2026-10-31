# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders

4483 windows pooled (1334 positive, 271 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9565 | 0.7256 | 0.8252 | 0.7783 |
| source_free_deeplog | 0.8510 | 0.8823 | 0.8664 | 0.8086 |
| transfer | 0.9989 | 0.6957 | 0.8202 | 0.7843 |
| transfer_openstack | 1.0000 | 0.3373 | 0.5045 | 0.5132 |
| transfer_similar | 0.9990 | 0.7459 | 0.8541 | 0.8200 |
| threshold | 1.0000 | 0.2039 | 0.3387 | 0.3905 |
| source_free_forest | 0.9245 | 0.3853 | 0.5439 | 0.5159 |
| novelty_gate | 0.9979 | 0.6972 | 0.8208 | 0.7847 |
| source_free_source_features | 0.9989 | 0.6957 | 0.8202 | 0.7843 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 756 of 901 | 0.15 | 0.0 | 1.7 |
| source_free_deeplog | 900 of 901 | 0.17 | 0.0 | 2.2 |
| transfer | 720 of 901 | 0.14 | 0.0 | 1.6 |
| transfer_openstack | 362 of 901 | 0.17 | 0.0 | 1.1 |
| transfer_similar | 787 of 901 | 0.14 | 0.0 | 1.5 |
| threshold | 272 of 901 | 0.22 | 0.0 | 1.4 |
| source_free_forest | 502 of 901 | 0.22 | 0.0 | 3.1 |
| novelty_gate | 720 of 901 | 0.14 | 0.0 | 1.6 |
| source_free_source_features | 720 of 901 | 0.14 | 0.0 | 1.6 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0051 | [-0.0129, +0.0025] | 0.826 | 0.826 | False |
| H2 | -0.3208 | [-0.3469, -0.2935] | 9.41e-104 | 8.47e-103 | True |
| H3 | +0.0288 | [+0.0180, +0.0404] | 1.22e-08 | 4.86e-08 | True |
| H6 | +0.0339 | [+0.0247, +0.0438] | 6.22e-13 | 3.73e-12 | True |
| H1 (fault segments) | detected transfer 720/source_free 756 of 901 | | 2.91e-11 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 362/source_free 756 of 901 | | 4.96e-119 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 787/source_free 756 of 901 | | 3.03e-04 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.812, config 0.838, timeout 0.872, resource 0.974, latency 0.135 | | 7.68e-130 | 7.68e-129 | True |
| H5 | FAR source_free 0.0664, source_free_deeplog 0.1771, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 3.54e-39 | 2.48e-38 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | +0.0015 | True | True | True |
| transfer_openstack | -0.2980 | True | True | True |
| transfer_similar | +0.0382 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0462 | [-0.0646, -0.0292] | 0.043 | 0.130 | False |
| H2 | -0.3619 | [-0.3911, -0.3331] | 9.76e-69 | 7.81e-68 | True |
| H3 | -0.0123 | [-0.0284, +0.0042] | 0.289 | 0.579 | False |
| H6 | +0.0339 | [+0.0247, +0.0438] | 6.22e-13 | 3.73e-12 | True |
| H1 (fault segments) | detected transfer 720/source_free_deeplog 900 of 901 | | 1.31e-54 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 362/source_free_deeplog 900 of 901 | | 2.22e-162 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 787/source_free_deeplog 900 of 901 | | 1.93e-34 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.879, config 0.902, timeout 0.888, resource 0.970, latency 0.772 | | 9.41e-11 | 4.71e-10 | True |
| H5 | FAR source_free 0.0664, source_free_deeplog 0.1771, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 3.54e-39 | 2.48e-38 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0316 | True | True | True |
| transfer_openstack | -0.3379 | True | True | True |
| transfer_similar | +0.0012 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8252, source_free_forest 0.5439, novelty_gate 0.8208; of 1012 alarms of the combined detector, 456 come from the gate only, 80 from the forest only, 476 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (26): false-alarm rate source_free 0.5000, source_free_deeplog 0.6923, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.5000, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (245): false-alarm rate source_free 0.0204, source_free_deeplog 0.1224, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0204, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (138 fault windows): recall source_free 0.116, source_free_deeplog 0.768, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.203, threshold 0.000, source_free_forest 0.116, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (129 fault windows): recall source_free 0.155, source_free_deeplog 0.775, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.302, threshold 0.000, source_free_forest 0.155, novelty_gate 0.000, source_free_source_features 0.000
