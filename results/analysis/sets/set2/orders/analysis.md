# Analysis of the pooled runs: run4/orders, run5/orders, run6/orders

4479 windows pooled (1328 positive, 272 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9688 | 0.7477 | 0.8440 | 0.8019 |
| source_free_deeplog | 0.8661 | 0.8720 | 0.8690 | 0.8136 |
| transfer | 0.9989 | 0.6920 | 0.8176 | 0.7820 |
| transfer_openstack | 1.0000 | 0.3434 | 0.5112 | 0.5186 |
| transfer_similar | 0.9978 | 0.6935 | 0.8183 | 0.7824 |
| threshold | 1.0000 | 0.2026 | 0.3369 | 0.3894 |
| source_free_forest | 0.9481 | 0.4127 | 0.5750 | 0.5492 |
| novelty_gate | 0.9978 | 0.6920 | 0.8173 | 0.7813 |
| source_free_source_features | 0.9989 | 0.6920 | 0.8176 | 0.7820 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 787 of 900 | 0.14 | 0.0 | 1.6 |
| source_free_deeplog | 900 of 900 | 0.17 | 0.0 | 2.1 |
| transfer | 720 of 900 | 0.12 | 0.0 | 1.3 |
| transfer_openstack | 363 of 900 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 722 of 900 | 0.12 | 0.0 | 1.3 |
| threshold | 269 of 900 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 515 of 900 | 0.21 | 0.0 | 3.0 |
| novelty_gate | 720 of 900 | 0.12 | 0.0 | 1.3 |
| source_free_source_features | 720 of 900 | 0.12 | 0.0 | 1.3 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0264 | [-0.0357, -0.0171] | 3.28e-05 | 1.64e-04 | True |
| H2 | -0.3328 | [-0.3589, -0.3063] | 2.51e-119 | 2.51e-118 | True |
| H3 | -0.0257 | [-0.0350, -0.0164] | 6.55e-05 | 2.62e-04 | True |
| H6 | +0.0007 | [-0.0021, +0.0036] | 1.000 | 1.000 | False |
| H1 (fault segments) | detected transfer 720/source_free 787 of 900 | | 1.36e-20 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 363/source_free 787 of 900 | | 4.62e-128 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 722/source_free 787 of 900 | | 5.06e-17 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.851, config 0.836, timeout 0.863, resource 0.985, latency 0.242 | | 1.48e-107 | 1.33e-106 | True |
| H5 | FAR source_free 0.0772, source_free_deeplog 0.1728, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0037, threshold 0.0000 | | 1.41e-37 | 9.90e-37 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0184 | True | True | True |
| transfer_openstack | -0.3106 | True | True | True |
| transfer_similar | -0.0179 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0514 | [-0.0682, -0.0346] | 0.003 | 0.010 | True |
| H2 | -0.3578 | [-0.3870, -0.3298] | 7.57e-74 | 6.05e-73 | True |
| H3 | -0.0507 | [-0.0673, -0.0349] | 0.004 | 0.010 | True |
| H6 | +0.0007 | [-0.0021, +0.0036] | 1.000 | 1.000 | False |
| H1 (fault segments) | detected transfer 720/source_free_deeplog 900 of 900 | | 1.31e-54 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 363/source_free_deeplog 900 of 900 | | 4.45e-162 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 722/source_free_deeplog 900 of 900 | | 5.22e-54 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.885, config 0.872, timeout 0.892, resource 0.985, latency 0.737 | | 6.02e-16 | 3.61e-15 | True |
| H5 | FAR source_free 0.0772, source_free_deeplog 0.1728, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0037, threshold 0.0000 | | 1.41e-37 | 9.90e-37 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0372 | True | True | True |
| transfer_openstack | -0.3340 | True | True | True |
| transfer_similar | -0.0370 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8440, source_free_forest 0.5750, novelty_gate 0.8173; of 1025 alarms of the combined detector, 447 come from the gate only, 104 from the forest only, 474 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (26): false-alarm rate source_free 0.5769, source_free_deeplog 0.8077, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0385, threshold 0.0000, source_free_forest 0.5769, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (246): false-alarm rate source_free 0.0244, source_free_deeplog 0.1057, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0244, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (144 fault windows): recall source_free 0.250, source_free_deeplog 0.729, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.014, threshold 0.000, source_free_forest 0.250, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (137 fault windows): recall source_free 0.234, source_free_deeplog 0.745, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.015, threshold 0.000, source_free_forest 0.234, novelty_gate 0.000, source_free_source_features 0.000
