# Analysis of the pooled runs: run7/bookings, run8/bookings, run9/bookings

4481 windows pooled (1312 positive, 272 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9646 | 0.7470 | 0.8419 | 0.7994 |
| source_free_deeplog | 0.8664 | 0.8155 | 0.8402 | 0.7775 |
| transfer | 1.0000 | 0.6936 | 0.8191 | 0.7845 |
| transfer_openstack | 1.0000 | 0.3384 | 0.5057 | 0.5154 |
| transfer_similar | 1.0000 | 0.7165 | 0.8348 | 0.8007 |
| threshold | 1.0000 | 0.2157 | 0.3549 | 0.4035 |
| source_free_forest | 0.9540 | 0.5373 | 0.6875 | 0.6457 |
| novelty_gate | 0.9978 | 0.6936 | 0.8183 | 0.7832 |
| source_free_source_features | 1.0000 | 0.6936 | 0.8191 | 0.7845 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 781 of 900 | 0.14 | 0.0 | 1.8 |
| source_free_deeplog | 842 of 900 | 0.17 | 0.0 | 2.2 |
| transfer | 720 of 900 | 0.14 | 0.0 | 1.8 |
| transfer_openstack | 364 of 900 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 750 of 900 | 0.14 | 0.0 | 1.8 |
| threshold | 283 of 900 | 0.19 | 0.0 | 1.3 |
| source_free_forest | 675 of 900 | 0.18 | 0.0 | 2.3 |
| novelty_gate | 720 of 900 | 0.14 | 0.0 | 1.8 |
| source_free_source_features | 720 of 900 | 0.14 | 0.0 | 1.8 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0228 | [-0.0323, -0.0131] | 0.001 | 0.005 | True |
| H2 | -0.3362 | [-0.3621, -0.3100] | 2.23e-115 | 2.23e-114 | True |
| H3 | -0.0071 | [-0.0177, +0.0036] | 0.797 | 1.000 | False |
| H6 | +0.0157 | [+0.0099, +0.0218] | 2.27e-07 | 1.14e-06 | True |
| H1 (fault segments) | detected transfer 720/source_free 781 of 900 | | 8.67e-19 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 364/source_free 781 of 900 | | 5.91e-126 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 750/source_free 781 of 900 | | 8.78e-04 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.853, config 0.839, timeout 0.865, resource 0.967, latency 0.229 | | 8.16e-107 | 7.35e-106 | True |
| H5 | FAR source_free 0.1103, source_free_deeplog 0.1581, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.07e-35 | 6.41e-35 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0148 | True | True | True |
| transfer_openstack | -0.3143 | True | True | True |
| transfer_similar | +0.0020 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0211 | [-0.0358, -0.0062] | 0.824 | 1.000 | False |
| H2 | -0.3345 | [-0.3638, -0.3063] | 6.00e-64 | 4.80e-63 | True |
| H3 | -0.0054 | [-0.0193, +0.0087] | 0.051 | 0.152 | False |
| H6 | +0.0157 | [+0.0099, +0.0218] | 2.27e-07 | 1.14e-06 | True |
| H1 (fault segments) | detected transfer 720/source_free_deeplog 842 of 900 | | 3.76e-37 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 364/source_free_deeplog 842 of 900 | | 2.56e-144 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 750/source_free_deeplog 842 of 900 | | 4.04e-28 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.868, config 0.870, timeout 0.869, resource 0.963, latency 0.517 | | 2.52e-45 | 1.77e-44 | True |
| H5 | FAR source_free 0.1103, source_free_deeplog 0.1581, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.07e-35 | 6.41e-35 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0088 | True | True | True |
| transfer_openstack | -0.3114 | True | True | True |
| transfer_similar | +0.0066 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8419, source_free_forest 0.6875, novelty_gate 0.8183; of 1016 alarms of the combined detector, 277 come from the gate only, 104 from the forest only, 635 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (23): false-alarm rate source_free 0.9130, source_free_deeplog 0.6957, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.9130, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (249): false-alarm rate source_free 0.0361, source_free_deeplog 0.1084, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0321, novelty_gate 0.0040, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (135 fault windows): recall source_free 0.259, source_free_deeplog 0.533, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.119, threshold 0.000, source_free_forest 0.259, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (136 fault windows): recall source_free 0.199, source_free_deeplog 0.500, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.125, threshold 0.000, source_free_forest 0.199, novelty_gate 0.000, source_free_source_features 0.000
