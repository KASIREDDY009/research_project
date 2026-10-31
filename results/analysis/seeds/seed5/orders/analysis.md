# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9620 | 0.7274 | 0.8284 | 0.7836 |
| source_free_deeplog | 0.8601 | 0.8770 | 0.8685 | 0.8127 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.1335 | 0.2356 | 0.3130 |
| transfer_similar | 0.9977 | 0.7516 | 0.8573 | 0.8235 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9357 | 0.3925 | 0.5531 | 0.5279 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2263 of 2701 | 0.13 | 0.0 | 1.5 |
| source_free_deeplog | 2699 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 265 of 2701 | 0.00 | 0.0 | 0.0 |
| transfer_similar | 2357 of 2701 | 0.14 | 0.0 | 1.7 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1508 of 2701 | 0.17 | 0.0 | 2.5 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0065 | [-0.0107, -0.0021] | 0.791 | 0.791 | False |
| H2 | -0.5928 | [-0.6098, -0.5746] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0289 | [+0.0232, +0.0349] | 1.77e-26 | 7.08e-26 | True |
| H6 | +0.0354 | [+0.0306, +0.0406] | 2.28e-51 | 1.37e-50 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2263 of 2701 | | 1.97e-31 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 265/source_free 2263 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2357/source_free 2263 of 2701 | | 1.01e-09 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.838, config 0.837, timeout 0.880, resource 0.976, latency 0.126 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0699, source_free_deeplog 0.1581, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0061, threshold 0.0000 | | 3.42e-102 | 2.39e-101 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0028 | True | True | True |
| transfer_openstack | -0.5776 | True | True | True |
| transfer_similar | +0.0340 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0466 | [-0.0566, -0.0370] | 4.20e-05 | 1.26e-04 | True |
| H2 | -0.6329 | [-0.6506, -0.6148] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0112 | [-0.0198, -0.0025] | 0.072 | 0.143 | False |
| H6 | +0.0354 | [+0.0306, +0.0406] | 2.28e-51 | 1.37e-50 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2699 of 2701 | | 1.11e-162 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 265/source_free_deeplog 2699 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2357/source_free_deeplog 2699 of 2701 | | 2.23e-103 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.876, config 0.887, timeout 0.898, resource 0.975, latency 0.753 | | 4.14e-40 | 2.07e-39 | True |
| H5 | FAR source_free 0.0699, source_free_deeplog 0.1581, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0061, threshold 0.0000 | | 3.42e-102 | 2.39e-101 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0382 | True | True | True |
| transfer_openstack | -0.6184 | True | True | True |
| transfer_similar | -0.0037 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8284, source_free_forest 0.5531, novelty_gate 0.8218; of 3001 alarms of the combined detector, 1336 come from the gate only, 221 from the forest only, 1444 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.4872, source_free_deeplog 0.6795, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0513, threshold 0.0000, source_free_forest 0.4872, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0257, source_free_deeplog 0.1030, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0014, threshold 0.0000, source_free_forest 0.0257, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.133, source_free_deeplog 0.749, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.241, threshold 0.000, source_free_forest 0.133, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.120, source_free_deeplog 0.757, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.260, threshold 0.000, source_free_forest 0.120, novelty_gate 0.000, source_free_source_features 0.000
