# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9652 | 0.7402 | 0.8379 | 0.7946 |
| source_free_deeplog | 0.8610 | 0.8846 | 0.8726 | 0.8184 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.3406 | 0.5082 | 0.5166 |
| transfer_similar | 0.9993 | 0.7234 | 0.8392 | 0.8047 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9458 | 0.4349 | 0.5958 | 0.5652 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2309 of 2701 | 0.14 | 0.0 | 1.6 |
| source_free_deeplog | 2700 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 1087 of 2701 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 2275 of 2701 | 0.14 | 0.0 | 1.6 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1667 of 2701 | 0.21 | 0.0 | 3.0 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0160 | [-0.0207, -0.0112] | 1.18e-04 | 3.53e-04 | True |
| H2 | -0.3297 | [-0.3452, -0.3142] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0014 | [-0.0042, +0.0070] | 0.057 | 0.068 | False |
| H6 | +0.0173 | [+0.0135, +0.0213] | 4.01e-19 | 2.01e-18 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2309 of 2701 | | 2.80e-45 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free 2309 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2275/source_free 2309 of 2701 | | 0.026 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.838, config 0.839, timeout 0.880, resource 0.976, latency 0.187 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0686, source_free_deeplog 0.1752, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 8.99e-118 | 6.29e-117 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0119 | True | True | True |
| transfer_openstack | -0.3165 | True | True | True |
| transfer_similar | +0.0062 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0507 | [-0.0604, -0.0403] | 1.21e-06 | 4.86e-06 | True |
| H2 | -0.3644 | [-0.3801, -0.3476] | 2.57e-217 | 2.06e-216 | True |
| H3 | -0.0334 | [-0.0430, -0.0239] | 0.034 | 0.068 | False |
| H6 | +0.0173 | [+0.0135, +0.0213] | 4.01e-19 | 2.01e-18 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2700 of 2701 | | 5.56e-163 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free_deeplog 2700 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2275/source_free_deeplog 2700 of 2701 | | 2.31e-128 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.898, config 0.902, timeout 0.893, resource 0.975, latency 0.758 | | 3.23e-41 | 1.94e-40 | True |
| H5 | FAR source_free 0.0686, source_free_deeplog 0.1752, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 8.99e-118 | 6.29e-117 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0419 | True | True | True |
| transfer_openstack | -0.3502 | True | True | True |
| transfer_similar | -0.0257 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8379, source_free_forest 0.5958, novelty_gate 0.8218; of 3044 alarms of the combined detector, 1219 come from the gate only, 264 from the forest only, 1561 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.5128, source_free_deeplog 0.7821, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0128, threshold 0.0000, source_free_forest 0.5128, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0217, source_free_deeplog 0.1111, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0217, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.190, source_free_deeplog 0.754, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.145, threshold 0.000, source_free_forest 0.190, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.182, source_free_deeplog 0.762, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.142, threshold 0.000, source_free_forest 0.182, novelty_gate 0.000, source_free_source_features 0.000
