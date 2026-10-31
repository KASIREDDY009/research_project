# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9688 | 0.7342 | 0.8353 | 0.7927 |
| source_free_deeplog | 0.8874 | 0.8282 | 0.8568 | 0.8006 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.1353 | 0.2383 | 0.3151 |
| transfer_similar | 0.9983 | 0.7256 | 0.8404 | 0.8056 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9456 | 0.3812 | 0.5434 | 0.5240 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2285 of 2701 | 0.13 | 0.0 | 1.5 |
| source_free_deeplog | 2520 of 2701 | 0.15 | 0.0 | 1.9 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 272 of 2701 | 0.00 | 0.0 | 0.0 |
| transfer_similar | 2279 of 2701 | 0.14 | 0.0 | 1.7 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1461 of 2701 | 0.22 | 0.0 | 3.1 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0134 | [-0.0179, -0.0090] | 8.19e-04 | 0.003 | True |
| H2 | -0.5970 | [-0.6139, -0.5789] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0051 | [-0.0007, +0.0112] | 0.005 | 0.010 | True |
| H6 | +0.0185 | [+0.0144, +0.0230] | 4.87e-19 | 2.43e-18 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2285 of 2701 | | 4.70e-38 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 272/source_free 2285 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2279/source_free 2285 of 2701 | | 0.753 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.838, config 0.838, timeout 0.880, resource 0.976, latency 0.158 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0576, source_free_deeplog 0.1532, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0037, threshold 0.0000 | | 2.12e-101 | 1.27e-100 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0098 | True | True | True |
| transfer_openstack | -0.5818 | True | True | True |
| transfer_similar | +0.0102 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0349 | [-0.0429, -0.0259] | 9.17e-04 | 0.003 | True |
| H2 | -0.6184 | [-0.6362, -0.6004] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0164 | [-0.0243, -0.0087] | 0.892 | 0.892 | False |
| H6 | +0.0185 | [+0.0144, +0.0230] | 4.87e-19 | 2.43e-18 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2520 of 2701 | | 8.52e-109 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 272/source_free_deeplog 2520 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2279/source_free_deeplog 2520 of 2701 | | 1.54e-52 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.887, config 0.894, timeout 0.908, resource 0.975, latency 0.488 | | 9.07e-185 | 6.35e-184 | True |
| H5 | FAR source_free 0.0576, source_free_deeplog 0.1532, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0037, threshold 0.0000 | | 2.12e-101 | 1.27e-100 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0276 | True | True | True |
| transfer_openstack | -0.6034 | True | True | True |
| transfer_similar | -0.0098 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8353, source_free_forest 0.5434, novelty_gate 0.8218; of 3008 alarms of the combined detector, 1408 come from the gate only, 228 from the forest only, 1372 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.4359, source_free_deeplog 0.6538, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0385, threshold 0.0000, source_free_forest 0.4359, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0176, source_free_deeplog 0.1003, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0176, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.159, source_free_deeplog 0.489, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.137, threshold 0.000, source_free_forest 0.159, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.158, source_free_deeplog 0.487, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.180, threshold 0.000, source_free_forest 0.158, novelty_gate 0.000, source_free_source_features 0.000
