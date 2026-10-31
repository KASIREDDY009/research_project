# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9679 | 0.7294 | 0.8319 | 0.7888 |
| source_free_deeplog | 0.8666 | 0.8753 | 0.8709 | 0.8164 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.3406 | 0.5082 | 0.5166 |
| transfer_similar | 0.9997 | 0.7410 | 0.8511 | 0.8174 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9427 | 0.3686 | 0.5300 | 0.5127 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2274 of 2701 | 0.13 | 0.0 | 1.5 |
| source_free_deeplog | 2696 of 2701 | 0.18 | 0.0 | 2.2 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 1087 of 2701 | 0.15 | 0.0 | 1.0 |
| transfer_similar | 2330 of 2701 | 0.14 | 0.0 | 1.7 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1423 of 2701 | 0.19 | 0.0 | 2.8 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0100 | [-0.0143, -0.0059] | 0.041 | 0.083 | False |
| H2 | -0.3237 | [-0.3384, -0.3082] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0192 | [+0.0135, +0.0248] | 1.19e-14 | 4.76e-14 | True |
| H6 | +0.0292 | [+0.0251, +0.0339] | 1.46e-50 | 7.31e-50 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2274 of 2701 | | 9.63e-35 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free 2274 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2330/source_free 2274 of 2701 | | 2.70e-04 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.836, config 0.837, timeout 0.879, resource 0.976, latency 0.140 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0564, source_free_deeplog 0.1703, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.28e-117 | 8.98e-117 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0064 | True | True | True |
| transfer_openstack | -0.3106 | True | True | True |
| transfer_similar | +0.0240 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0490 | [-0.0586, -0.0390] | 1.27e-06 | 3.80e-06 | True |
| H2 | -0.3627 | [-0.3783, -0.3461] | 2.89e-222 | 2.31e-221 | True |
| H3 | -0.0198 | [-0.0288, -0.0113] | 1.000 | 1.000 | False |
| H6 | +0.0292 | [+0.0251, +0.0339] | 1.46e-50 | 7.31e-50 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2696 of 2701 | | 8.89e-162 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1087/source_free_deeplog 2696 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2330/source_free_deeplog 2696 of 2701 | | 1.33e-110 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.898, config 0.902, timeout 0.878, resource 0.975, latency 0.726 | | 2.30e-52 | 1.38e-51 | True |
| H5 | FAR source_free 0.0564, source_free_deeplog 0.1703, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.28e-117 | 8.98e-117 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0405 | True | True | True |
| transfer_openstack | -0.3487 | True | True | True |
| transfer_similar | -0.0127 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8319, source_free_forest 0.5300, novelty_gate 0.8218; of 2991 alarms of the combined detector, 1439 come from the gate only, 211 from the forest only, 1341 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.4615, source_free_deeplog 0.6923, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.4615, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0136, source_free_deeplog 0.1152, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0136, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.152, source_free_deeplog 0.723, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.200, threshold 0.000, source_free_forest 0.152, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.128, source_free_deeplog 0.730, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.220, threshold 0.000, source_free_forest 0.128, novelty_gate 0.000, source_free_source_features 0.000
