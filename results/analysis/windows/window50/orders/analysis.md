# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

5372 windows pooled (3203 positive, 320 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9768 | 0.7768 | 0.8654 | 0.7365 |
| source_free_deeplog | 0.9130 | 0.9404 | 0.9265 | 0.8144 |
| transfer | 1.0000 | 0.3066 | 0.4693 | 0.3892 |
| transfer_openstack | 1.0000 | 0.3706 | 0.5408 | 0.4383 |
| transfer_similar | 0.9989 | 0.8695 | 0.9297 | 0.8525 |
| threshold | 1.0000 | 0.3072 | 0.4700 | 0.3897 |
| source_free_forest | 0.9469 | 0.3175 | 0.4756 | 0.3573 |
| novelty_gate | 0.9992 | 0.7484 | 0.8558 | 0.7377 |
| source_free_source_features | 1.0000 | 0.7474 | 0.8555 | 0.7378 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 1574 of 1842 | 0.05 | 0.0 | 0.5 |
| source_free_deeplog | 1842 of 1842 | 0.00 | 0.0 | 0.0 |
| transfer | 853 of 1842 | 0.43 | 0.0 | 4.9 |
| transfer_openstack | 885 of 1842 | 0.38 | 0.0 | 4.5 |
| transfer_similar | 1800 of 1842 | 0.01 | 0.0 | 0.1 |
| threshold | 855 of 1842 | 0.42 | 0.0 | 4.9 |
| source_free_forest | 805 of 1842 | 0.20 | 0.0 | 3.7 |
| novelty_gate | 1514 of 1842 | 0.06 | 0.0 | 0.7 |
| source_free_source_features | 1513 of 1842 | 0.06 | 0.0 | 0.7 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.3961 | [-0.4148, -0.3786] | 0.00e+00 | 0.00e+00 | True |
| H2 | -0.3246 | [-0.3411, -0.3082] | 1.27e-305 | 7.60e-305 | True |
| H3 | +0.0643 | [+0.0571, +0.0718] | 1.93e-76 | 5.79e-76 | True |
| H6 | +0.4604 | [+0.4425, +0.4790] | 0.00e+00 | 0.00e+00 | True |
| H1 (fault segments) | detected transfer 853/source_free 1574 of 1842 | | 1.81e-217 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 885/source_free 1574 of 1842 | | 7.79e-208 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 1800/source_free 1574 of 1842 | | 2.72e-54 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.923, config 0.909, timeout 0.926, resource 0.991, latency 0.133 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.1094, source_free_deeplog 0.2969, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0063, threshold 0.0000 | | 4.73e-78 | 1.89e-77 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.3811 | True | True | True |
| transfer_openstack | -0.3102 | True | True | True |
| transfer_similar | +0.0707 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.4572 | [-0.4750, -0.4382] | 1.58e-322 | 1.11e-321 | True |
| H2 | -0.3857 | [-0.4047, -0.3677] | 3.47e-273 | 1.73e-272 | True |
| H3 | +0.0032 | [-0.0039, +0.0106] | 0.015 | 0.015 | True |
| H6 | +0.4604 | [+0.4425, +0.4790] | 0.00e+00 | 0.00e+00 | True |
| H1 (fault segments) | detected transfer 853/source_free_deeplog 1842 of 1842 | | 3.82e-298 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 885/source_free_deeplog 1842 of 1842 | | 1.64e-288 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 1800/source_free_deeplog 1842 of 1842 | | 4.55e-13 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.951, config 0.935, timeout 0.942, resource 0.989, latency 0.884 | | 2.66e-13 | 5.32e-13 | True |
| H5 | FAR source_free 0.1094, source_free_deeplog 0.2969, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0063, threshold 0.0000 | | 4.73e-78 | 1.89e-77 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.4415 | True | True | True |
| transfer_openstack | -0.3702 | True | True | True |
| transfer_similar | +0.0096 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8654, source_free_forest 0.4756, novelty_gate 0.8558; of 2547 alarms of the combined detector, 1473 come from the gate only, 148 from the forest only, 926 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features -0.3862 [-0.4038, -0.3680].
- Elasticity windows with new environment (67): false-alarm rate source_free 0.3582, source_free_deeplog 0.9254, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0299, threshold 0.0000, source_free_forest 0.3582, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (253): false-alarm rate source_free 0.0435, source_free_deeplog 0.1304, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0435, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (317 fault windows): recall source_free 0.129, source_free_deeplog 0.890, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.628, threshold 0.000, source_free_forest 0.129, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (322 fault windows): recall source_free 0.137, source_free_deeplog 0.879, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.575, threshold 0.000, source_free_forest 0.134, novelty_gate 0.003, source_free_source_features 0.000
