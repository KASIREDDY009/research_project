# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9610 | 0.7450 | 0.8393 | 0.7951 |
| source_free_deeplog | 0.9130 | 0.7931 | 0.8489 | 0.7954 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.3406 | 0.5082 | 0.5166 |
| transfer_similar | 0.9986 | 0.7249 | 0.8400 | 0.8053 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9436 | 0.4759 | 0.6327 | 0.5945 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2325 of 2701 | 0.14 | 0.0 | 1.6 |
| source_free_deeplog | 2455 of 2701 | 0.16 | 0.0 | 1.9 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 1087 of 2701 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 2250 of 2701 | 0.13 | 0.0 | 1.5 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1819 of 2701 | 0.21 | 0.0 | 2.9 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0175 | [-0.0226, -0.0123] | 8.78e-05 | 3.51e-04 | True |
| H2 | -0.3312 | [-0.3466, -0.3152] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0007 | [-0.0051, +0.0065] | 0.063 | 0.125 | False |
| H6 | +0.0181 | [+0.0146, +0.0219] | 3.98e-26 | 1.99e-25 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2325 of 2701 | | 4.28e-50 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free 2325 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2250/source_free 2325 of 2701 | | 5.86e-08 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.838, config 0.841, timeout 0.879, resource 0.978, latency 0.209 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0711, source_free_deeplog 0.1569, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0025, threshold 0.0000 | | 9.30e-103 | 5.58e-102 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0131 | True | True | True |
| transfer_openstack | -0.3182 | True | True | True |
| transfer_similar | +0.0055 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0270 | [-0.0346, -0.0195] | 0.002 | 0.007 | True |
| H2 | -0.3407 | [-0.3559, -0.3251] | 3.83e-259 | 3.06e-258 | True |
| H3 | -0.0089 | [-0.0162, -0.0016] | 0.356 | 0.356 | False |
| H6 | +0.0181 | [+0.0146, +0.0219] | 3.98e-26 | 1.99e-25 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2455 of 2701 | | 3.14e-89 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free_deeplog 2455 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2250/source_free_deeplog 2455 of 2701 | | 5.29e-41 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.859, config 0.864, timeout 0.883, resource 0.975, latency 0.398 | | 8.89e-220 | 6.22e-219 | True |
| H5 | FAR source_free 0.0711, source_free_deeplog 0.1569, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0025, threshold 0.0000 | | 9.30e-103 | 5.58e-102 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0203 | True | True | True |
| transfer_openstack | -0.3277 | True | True | True |
| transfer_similar | -0.0025 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8393, source_free_forest 0.6327, novelty_gate 0.8218; of 3077 alarms of the combined detector, 1075 come from the gate only, 297 from the forest only, 1705 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.5000, source_free_deeplog 0.6410, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0256, threshold 0.0000, source_free_forest 0.5000, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0257, source_free_deeplog 0.1057, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0257, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.212, source_free_deeplog 0.398, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.118, threshold 0.000, source_free_forest 0.212, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.205, source_free_deeplog 0.398, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.113, threshold 0.000, source_free_forest 0.205, novelty_gate 0.000, source_free_source_features 0.000
