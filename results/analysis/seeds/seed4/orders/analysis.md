# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9638 | 0.7236 | 0.8266 | 0.7821 |
| source_free_deeplog | 0.8608 | 0.8831 | 0.8718 | 0.8172 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.1335 | 0.2356 | 0.3130 |
| transfer_similar | 0.9970 | 0.7468 | 0.8539 | 0.8197 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9368 | 0.3774 | 0.5381 | 0.5168 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2250 of 2701 | 0.13 | 0.0 | 1.5 |
| source_free_deeplog | 2699 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 265 of 2701 | 0.00 | 0.0 | 0.0 |
| transfer_similar | 2353 of 2701 | 0.14 | 0.0 | 1.6 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1458 of 2701 | 0.20 | 0.0 | 2.8 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0047 | [-0.0087, -0.0007] | 0.834 | 1.000 | False |
| H2 | -0.5910 | [-0.6080, -0.5731] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0273 | [+0.0217, +0.0331] | 1.02e-25 | 4.07e-25 | True |
| H6 | +0.0320 | [+0.0272, +0.0369] | 3.33e-44 | 1.67e-43 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2250 of 2701 | | 1.62e-27 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 265/source_free 2250 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2353/source_free 2250 of 2701 | | 3.48e-12 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.836, config 0.838, timeout 0.879, resource 0.976, latency 0.110 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0674, source_free_deeplog 0.1728, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0086, threshold 0.0000 | | 5.26e-113 | 3.68e-112 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0014 | True | True | True |
| transfer_openstack | -0.5760 | True | True | True |
| transfer_similar | +0.0323 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0499 | [-0.0599, -0.0398] | 2.64e-06 | 7.91e-06 | True |
| H2 | -0.6362 | [-0.6537, -0.6182] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0178 | [-0.0271, -0.0088] | 0.634 | 1.000 | False |
| H6 | +0.0320 | [+0.0272, +0.0369] | 3.33e-44 | 1.67e-43 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2699 of 2701 | | 1.11e-162 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 265/source_free_deeplog 2699 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2353/source_free_deeplog 2699 of 2701 | | 1.40e-104 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.898, config 0.902, timeout 0.894, resource 0.975, latency 0.750 | | 1.43e-44 | 8.58e-44 | True |
| H5 | FAR source_free 0.0674, source_free_deeplog 0.1728, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0086, threshold 0.0000 | | 5.26e-113 | 3.68e-112 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0412 | True | True | True |
| transfer_openstack | -0.6212 | True | True | True |
| transfer_similar | -0.0101 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8266, source_free_forest 0.5381, novelty_gate 0.8218; of 2980 alarms of the combined detector, 1381 come from the gate only, 200 from the forest only, 1399 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.4615, source_free_deeplog 0.7949, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0769, threshold 0.0000, source_free_forest 0.4615, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0257, source_free_deeplog 0.1070, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0014, threshold 0.0000, source_free_forest 0.0257, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.116, source_free_deeplog 0.740, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.241, threshold 0.000, source_free_forest 0.116, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.105, source_free_deeplog 0.760, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.245, threshold 0.000, source_free_forest 0.105, novelty_gate 0.000, source_free_source_features 0.000
