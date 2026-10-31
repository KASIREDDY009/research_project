# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9606 | 0.7440 | 0.8386 | 0.7942 |
| source_free_deeplog | 0.8543 | 0.8818 | 0.8678 | 0.8114 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.3406 | 0.5082 | 0.5166 |
| transfer_similar | 0.9990 | 0.7344 | 0.8465 | 0.8123 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9392 | 0.4434 | 0.6024 | 0.5681 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2330 of 2701 | 0.14 | 0.0 | 1.7 |
| source_free_deeplog | 2700 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 1087 of 2701 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 2304 of 2701 | 0.13 | 0.0 | 1.5 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1701 of 2701 | 0.23 | 0.0 | 3.3 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0167 | [-0.0217, -0.0115] | 2.62e-04 | 6.81e-04 | True |
| H2 | -0.3304 | [-0.3455, -0.3150] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0080 | [+0.0021, +0.0143] | 5.23e-05 | 2.09e-04 | True |
| H6 | +0.0246 | [+0.0202, +0.0292] | 3.74e-30 | 1.87e-29 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2330 of 2701 | | 1.34e-51 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free 2330 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2304/source_free 2330 of 2701 | | 0.092 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.836, config 0.838, timeout 0.879, resource 0.976, latency 0.210 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0748, source_free_deeplog 0.1765, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 9.64e-120 | 6.75e-119 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0123 | True | True | True |
| transfer_openstack | -0.3172 | True | True | True |
| transfer_similar | +0.0131 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0460 | [-0.0560, -0.0356] | 2.27e-04 | 6.81e-04 | True |
| H2 | -0.3597 | [-0.3755, -0.3423] | 5.17e-204 | 4.14e-203 | True |
| H3 | -0.0213 | [-0.0309, -0.0118] | 0.820 | 0.820 | False |
| H6 | +0.0246 | [+0.0202, +0.0292] | 3.74e-30 | 1.87e-29 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2700 of 2701 | | 5.56e-163 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free_deeplog 2700 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2304/source_free_deeplog 2700 of 2701 | | 1.24e-119 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.890, config 0.893, timeout 0.897, resource 0.975, latency 0.758 | | 8.64e-40 | 5.18e-39 | True |
| H5 | FAR source_free 0.0748, source_free_deeplog 0.1765, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 9.64e-120 | 6.75e-119 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0371 | True | True | True |
| transfer_openstack | -0.3456 | True | True | True |
| transfer_similar | -0.0133 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8386, source_free_forest 0.6024, novelty_gate 0.8218; of 3074 alarms of the combined detector, 1200 come from the gate only, 294 from the forest only, 1580 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.5769, source_free_deeplog 0.7564, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0128, threshold 0.0000, source_free_forest 0.5769, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0217, source_free_deeplog 0.1152, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0217, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.210, source_free_deeplog 0.754, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.169, threshold 0.000, source_free_forest 0.210, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.210, source_free_deeplog 0.762, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.193, threshold 0.000, source_free_forest 0.210, novelty_gate 0.000, source_free_source_features 0.000
