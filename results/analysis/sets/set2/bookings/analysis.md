# Analysis of the pooled runs: run4/bookings, run5/bookings, run6/bookings

4480 windows pooled (1324 positive, 273 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9719 | 0.7062 | 0.8180 | 0.7752 |
| source_free_deeplog | 0.9108 | 0.7560 | 0.8262 | 0.7688 |
| transfer | 0.9978 | 0.6782 | 0.8076 | 0.7717 |
| transfer_openstack | 1.0000 | 0.3338 | 0.5006 | 0.5108 |
| transfer_similar | 0.9989 | 0.6790 | 0.8085 | 0.7729 |
| threshold | 1.0000 | 0.2153 | 0.3543 | 0.4024 |
| source_free_forest | 0.9554 | 0.3557 | 0.5184 | 0.5085 |
| novelty_gate | 0.9945 | 0.6790 | 0.8070 | 0.7702 |
| source_free_source_features | 0.9978 | 0.6782 | 0.8076 | 0.7717 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 745 of 898 | 0.15 | 0.0 | 2.0 |
| source_free_deeplog | 780 of 898 | 0.16 | 0.0 | 2.1 |
| transfer | 718 of 898 | 0.15 | 0.0 | 2.0 |
| transfer_openstack | 364 of 898 | 0.17 | 0.0 | 1.3 |
| transfer_similar | 726 of 898 | 0.16 | 0.0 | 2.1 |
| threshold | 285 of 898 | 0.22 | 0.0 | 1.6 |
| source_free_forest | 463 of 898 | 0.16 | 0.0 | 2.6 |
| novelty_gate | 718 of 898 | 0.15 | 0.0 | 2.0 |
| source_free_source_features | 718 of 898 | 0.15 | 0.0 | 2.0 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0105 | [-0.0180, -0.0037] | 0.162 | 0.809 | False |
| H2 | -0.3175 | [-0.3426, -0.2907] | 6.12e-112 | 5.51e-111 | True |
| H3 | -0.0096 | [-0.0174, -0.0022] | 0.268 | 1.000 | False |
| H6 | +0.0009 | [-0.0032, +0.0051] | 0.804 | 1.000 | False |
| H1 (fault segments) | detected transfer 718/source_free 745 of 898 | | 1.49e-08 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 364/source_free 745 of 898 | | 4.06e-115 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 726/source_free 745 of 898 | | 6.60e-05 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.793, config 0.848, timeout 0.866, resource 0.960, latency 0.099 | | 1.16e-135 | 1.16e-134 | True |
| H5 | FAR source_free 0.0476, source_free_deeplog 0.1282, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.56e-28 | 9.37e-28 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0047 | True | True | True |
| transfer_openstack | -0.2956 | True | True | True |
| transfer_similar | -0.0032 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0187 | [-0.0307, -0.0069] | 0.671 | 1.000 | False |
| H2 | -0.3257 | [-0.3527, -0.2985] | 2.78e-79 | 1.95e-78 | True |
| H3 | -0.0178 | [-0.0301, -0.0056] | 0.779 | 1.000 | False |
| H6 | +0.0009 | [-0.0032, +0.0051] | 0.804 | 1.000 | False |
| H1 (fault segments) | detected transfer 718/source_free_deeplog 780 of 898 | | 4.34e-19 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 364/source_free_deeplog 780 of 898 | | 1.18e-125 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 726/source_free_deeplog 780 of 898 | | 1.19e-14 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.847, config 0.864, timeout 0.859, resource 0.960, latency 0.277 | | 5.11e-94 | 4.09e-93 | True |
| H5 | FAR source_free 0.0476, source_free_deeplog 0.1282, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.56e-28 | 9.37e-28 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0091 | True | True | True |
| transfer_openstack | -0.3030 | True | True | True |
| transfer_similar | -0.0076 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8180, source_free_forest 0.5184, novelty_gate 0.8070; of 962 alarms of the combined detector, 469 come from the gate only, 58 from the forest only, 435 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (22): false-alarm rate source_free 0.4091, source_free_deeplog 0.6364, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.4091, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (251): false-alarm rate source_free 0.0159, source_free_deeplog 0.0837, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0159, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (135 fault windows): recall source_free 0.119, source_free_deeplog 0.274, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.052, threshold 0.000, source_free_forest 0.119, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (139 fault windows): recall source_free 0.079, source_free_deeplog 0.281, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.007, threshold 0.000, source_free_forest 0.079, novelty_gate 0.000, source_free_source_features 0.000
