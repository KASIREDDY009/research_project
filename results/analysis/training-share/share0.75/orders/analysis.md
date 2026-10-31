# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9629 | 0.7450 | 0.8401 | 0.7964 |
| source_free_deeplog | 0.8409 | 0.8818 | 0.8609 | 0.8011 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.3406 | 0.5082 | 0.5166 |
| transfer_similar | 0.9990 | 0.7344 | 0.8465 | 0.8123 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9402 | 0.4238 | 0.5842 | 0.5539 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2329 of 2701 | 0.14 | 0.0 | 1.6 |
| source_free_deeplog | 2700 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 1087 of 2701 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 2304 of 2701 | 0.13 | 0.0 | 1.5 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1612 of 2701 | 0.23 | 0.0 | 3.0 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0182 | [-0.0231, -0.0129] | 1.59e-05 | 6.37e-05 | True |
| H2 | -0.3319 | [-0.3469, -0.3166] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0065 | [+0.0009, +0.0128] | 4.46e-04 | 0.001 | True |
| H6 | +0.0246 | [+0.0202, +0.0292] | 3.74e-30 | 1.87e-29 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2329 of 2701 | | 2.67e-51 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free 2329 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2304/source_free 2329 of 2701 | | 0.095 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.838, config 0.837, timeout 0.879, resource 0.976, latency 0.213 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0760, source_free_deeplog 0.1740, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 1.84e-117 | 1.28e-116 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0138 | True | True | True |
| transfer_openstack | -0.3190 | True | True | True |
| transfer_similar | +0.0114 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0390 | [-0.0491, -0.0281] | 0.064 | 0.085 | False |
| H2 | -0.3527 | [-0.3684, -0.3354] | 1.15e-181 | 9.24e-181 | True |
| H3 | -0.0144 | [-0.0241, -0.0048] | 0.043 | 0.085 | False |
| H6 | +0.0246 | [+0.0202, +0.0292] | 3.74e-30 | 1.87e-29 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2700 of 2701 | | 5.56e-163 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free_deeplog 2700 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2304/source_free_deeplog 2700 of 2701 | | 1.24e-119 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.885, config 0.895, timeout 0.899, resource 0.975, latency 0.758 | | 6.14e-40 | 3.68e-39 | True |
| H5 | FAR source_free 0.0760, source_free_deeplog 0.1740, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 1.84e-117 | 1.28e-116 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0300 | True | True | True |
| transfer_openstack | -0.3385 | True | True | True |
| transfer_similar | -0.0064 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8401, source_free_forest 0.5842, novelty_gate 0.8218; of 3071 alarms of the combined detector, 1282 come from the gate only, 291 from the forest only, 1498 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.4872, source_free_deeplog 0.7436, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0128, threshold 0.0000, source_free_forest 0.4872, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0325, source_free_deeplog 0.1138, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0325, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.207, source_free_deeplog 0.754, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.169, threshold 0.000, source_free_forest 0.207, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.220, source_free_deeplog 0.762, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.193, threshold 0.000, source_free_forest 0.220, novelty_gate 0.000, source_free_source_features 0.000
