# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9585 | 0.7677 | 0.8525 | 0.8091 |
| source_free_deeplog | 0.8548 | 0.8778 | 0.8661 | 0.8091 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.3406 | 0.5082 | 0.5166 |
| transfer_similar | 0.9990 | 0.7344 | 0.8465 | 0.8123 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9354 | 0.4560 | 0.6131 | 0.5754 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2406 of 2701 | 0.14 | 0.0 | 1.7 |
| source_free_deeplog | 2700 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 1087 of 2701 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 2304 of 2701 | 0.13 | 0.0 | 1.5 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1748 of 2701 | 0.24 | 0.0 | 3.1 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0307 | [-0.0367, -0.0247] | 2.20e-13 | 8.82e-13 | True |
| H2 | -0.3444 | [-0.3598, -0.3286] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0060 | [-0.0125, +0.0005] | 0.927 | 1.000 | False |
| H6 | +0.0246 | [+0.0202, +0.0292] | 3.74e-30 | 1.87e-29 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2406 of 2701 | | 1.77e-74 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free 2406 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2304/source_free 2406 of 2701 | | 9.03e-10 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.842, config 0.843, timeout 0.882, resource 0.978, latency 0.310 | | 5.81e-271 | 5.23e-270 | True |
| H5 | FAR source_free 0.1029, source_free_deeplog 0.1752, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 2.08e-122 | 1.46e-121 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0257 | True | True | True |
| transfer_openstack | -0.3312 | True | True | True |
| transfer_similar | -0.0004 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0442 | [-0.0542, -0.0339] | 6.47e-04 | 0.002 | True |
| H2 | -0.3580 | [-0.3735, -0.3409] | 1.05e-202 | 8.37e-202 | True |
| H3 | -0.0196 | [-0.0292, -0.0102] | 0.585 | 1.000 | False |
| H6 | +0.0246 | [+0.0202, +0.0292] | 3.74e-30 | 1.87e-29 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2700 of 2701 | | 5.56e-163 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free_deeplog 2700 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2304/source_free_deeplog 2700 of 2701 | | 1.24e-119 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.876, config 0.887, timeout 0.897, resource 0.975, latency 0.758 | | 2.68e-38 | 1.61e-37 | True |
| H5 | FAR source_free 0.1029, source_free_deeplog 0.1752, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 2.08e-122 | 1.46e-121 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0353 | True | True | True |
| transfer_openstack | -0.3438 | True | True | True |
| transfer_similar | -0.0121 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8525, source_free_forest 0.6131, novelty_gate 0.8218; of 3179 alarms of the combined detector, 1244 come from the gate only, 399 from the forest only, 1536 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.6667, source_free_deeplog 0.7821, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0128, threshold 0.0000, source_free_forest 0.6667, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0434, source_free_deeplog 0.1111, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0434, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.320, source_free_deeplog 0.754, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.169, threshold 0.000, source_free_forest 0.320, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.300, source_free_deeplog 0.762, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.193, threshold 0.000, source_free_forest 0.300, novelty_gate 0.000, source_free_source_features 0.000
