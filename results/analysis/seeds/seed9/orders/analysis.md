# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9672 | 0.7347 | 0.8351 | 0.7920 |
| source_free_deeplog | 0.8635 | 0.8833 | 0.8733 | 0.8195 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | nan | 0.0000 | 0.0000 | nan |
| transfer_similar | 0.9990 | 0.7397 | 0.8500 | 0.8160 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9415 | 0.3731 | 0.5345 | 0.5157 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2293 of 2701 | 0.13 | 0.0 | 1.6 |
| source_free_deeplog | 2700 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 0 of 2701 | n/a | n/a | n/a |
| transfer_similar | 2321 of 2701 | 0.14 | 0.0 | 1.6 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1438 of 2701 | 0.21 | 0.0 | 2.9 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0132 | [-0.0176, -0.0085] | 0.002 | 0.004 | True |
| H2 | -0.8351 | [-0.8439, -0.8255] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0150 | [+0.0095, +0.0205] | 4.92e-10 | 1.97e-09 | True |
| H6 | +0.0281 | [+0.0237, +0.0328] | 4.28e-37 | 2.14e-36 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2293 of 2701 | | 1.84e-40 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free 2293 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2321/source_free 2293 of 2701 | | 0.056 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.836, config 0.838, timeout 0.880, resource 0.976, latency 0.163 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0576, source_free_deeplog 0.1703, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0025, threshold 0.0000 | | 1.32e-114 | 9.27e-114 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0095 | True | True | True |
| transfer_openstack | -0.8270 | True | True | True |
| transfer_similar | +0.0198 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0514 | [-0.0614, -0.0412] | 3.20e-07 | 9.59e-07 | True |
| H2 | -0.8733 | [-0.8809, -0.8649] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0233 | [-0.0322, -0.0141] | 0.598 | 0.598 | False |
| H6 | +0.0281 | [+0.0237, +0.0328] | 4.28e-37 | 2.14e-36 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2700 of 2701 | | 5.56e-163 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free_deeplog 2700 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2321/source_free_deeplog 2700 of 2701 | | 1.62e-114 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.896, config 0.892, timeout 0.899, resource 0.975, latency 0.758 | | 1.52e-40 | 9.12e-40 | True |
| H5 | FAR source_free 0.0576, source_free_deeplog 0.1703, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0025, threshold 0.0000 | | 1.32e-114 | 9.27e-114 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0426 | True | True | True |
| transfer_openstack | -0.8660 | True | True | True |
| transfer_similar | -0.0159 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8351, source_free_forest 0.5345, novelty_gate 0.8218; of 3015 alarms of the combined detector, 1442 come from the gate only, 235 from the forest only, 1338 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.4744, source_free_deeplog 0.7179, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0256, threshold 0.0000, source_free_forest 0.4744, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0136, source_free_deeplog 0.1125, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0136, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.176, source_free_deeplog 0.754, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.193, threshold 0.000, source_free_forest 0.176, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.150, source_free_deeplog 0.762, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.212, threshold 0.000, source_free_forest 0.150, novelty_gate 0.000, source_free_source_features 0.000
