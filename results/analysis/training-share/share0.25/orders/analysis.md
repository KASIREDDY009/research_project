# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9651 | 0.7743 | 0.8592 | 0.8181 |
| source_free_deeplog | 0.8567 | 0.8826 | 0.8694 | 0.8137 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.3406 | 0.5082 | 0.5166 |
| transfer_similar | 0.9990 | 0.7344 | 0.8465 | 0.8123 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9475 | 0.4732 | 0.6312 | 0.5946 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2426 of 2701 | 0.14 | 0.0 | 1.7 |
| source_free_deeplog | 2700 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 1087 of 2701 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 2304 of 2701 | 0.13 | 0.0 | 1.5 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1788 of 2701 | 0.24 | 0.0 | 3.1 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0373 | [-0.0432, -0.0310] | 2.44e-22 | 9.78e-22 | True |
| H2 | -0.3510 | [-0.3665, -0.3347] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0127 | [-0.0194, -0.0062] | 0.022 | 0.044 | True |
| H6 | +0.0246 | [+0.0202, +0.0292] | 3.74e-30 | 1.87e-29 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2426 of 2701 | | 1.69e-80 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free 2426 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2304/source_free 2426 of 2701 | | 2.59e-14 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.845, config 0.842, timeout 0.889, resource 0.978, latency 0.334 | | 4.03e-257 | 3.63e-256 | True |
| H5 | FAR source_free 0.0919, source_free_deeplog 0.1789, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 1.90e-123 | 1.33e-122 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0321 | True | True | True |
| transfer_openstack | -0.3376 | True | True | True |
| transfer_similar | -0.0072 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0476 | [-0.0576, -0.0370] | 4.40e-05 | 1.32e-04 | True |
| H2 | -0.3613 | [-0.3770, -0.3439] | 1.30e-208 | 1.04e-207 | True |
| H3 | -0.0229 | [-0.0324, -0.0134] | 0.909 | 0.909 | False |
| H6 | +0.0246 | [+0.0202, +0.0292] | 3.74e-30 | 1.87e-29 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2700 of 2701 | | 5.56e-163 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free_deeplog 2700 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2304/source_free_deeplog 2700 of 2701 | | 1.24e-119 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.883, config 0.895, timeout 0.905, resource 0.975, latency 0.758 | | 1.73e-40 | 1.04e-39 | True |
| H5 | FAR source_free 0.0919, source_free_deeplog 0.1789, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 1.90e-123 | 1.33e-122 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0386 | True | True | True |
| transfer_openstack | -0.3474 | True | True | True |
| transfer_similar | -0.0151 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8592, source_free_forest 0.6312, novelty_gate 0.8218; of 3184 alarms of the combined detector, 1202 come from the gate only, 404 from the forest only, 1578 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.5641, source_free_deeplog 0.8590, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0128, threshold 0.0000, source_free_forest 0.5641, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0420, source_free_deeplog 0.1070, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0420, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.340, source_free_deeplog 0.754, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.169, threshold 0.000, source_free_forest 0.340, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.328, source_free_deeplog 0.762, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.193, threshold 0.000, source_free_forest 0.328, novelty_gate 0.000, source_free_source_features 0.000
