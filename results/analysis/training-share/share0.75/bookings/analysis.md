# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9635 | 0.7266 | 0.8285 | 0.7841 |
| source_free_deeplog | 0.8863 | 0.7841 | 0.8321 | 0.7705 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.3342 | 0.5009 | 0.5112 |
| transfer_similar | 0.9996 | 0.6963 | 0.8209 | 0.7858 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9456 | 0.4426 | 0.6030 | 0.5710 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2306 of 2697 | 0.16 | 0.0 | 2.1 |
| source_free_deeplog | 2456 of 2697 | 0.17 | 0.0 | 2.3 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 1088 of 2697 | 0.17 | 0.0 | 1.2 |
| transfer_similar | 2215 of 2697 | 0.15 | 0.0 | 2.0 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1692 of 2697 | 0.22 | 0.0 | 2.9 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0165 | [-0.0216, -0.0115] | 1.84e-04 | 7.36e-04 | True |
| H2 | -0.3275 | [-0.3425, -0.3124] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0076 | [-0.0130, -0.0024] | 0.531 | 1.000 | False |
| H6 | +0.0090 | [+0.0062, +0.0119] | 4.64e-10 | 2.32e-09 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2306 of 2697 | | 5.61e-45 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free 2306 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2215/source_free 2306 of 2697 | | 4.23e-13 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.815, config 0.837, timeout 0.865, resource 0.963, latency 0.183 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0956, source_free_deeplog 0.1593, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.18e-110 | 1.31e-109 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0124 | True | True | True |
| transfer_openstack | -0.3149 | True | True | True |
| transfer_similar | -0.0033 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0201 | [-0.0281, -0.0123] | 1.000 | 1.000 | False |
| H2 | -0.3311 | [-0.3472, -0.3153] | 3.05e-208 | 2.44e-207 | True |
| H3 | -0.0112 | [-0.0194, -0.0033] | 0.082 | 0.247 | False |
| H6 | +0.0090 | [+0.0062, +0.0119] | 4.64e-10 | 2.32e-09 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2456 of 2697 | | 3.93e-90 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free_deeplog 2456 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2215/source_free_deeplog 2456 of 2697 | | 3.93e-54 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.838, config 0.853, timeout 0.871, resource 0.962, latency 0.417 | | 1.56e-187 | 1.09e-186 | True |
| H5 | FAR source_free 0.0956, source_free_deeplog 0.1593, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.18e-110 | 1.31e-109 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0134 | True | True | True |
| transfer_openstack | -0.3182 | True | True | True |
| transfer_similar | -0.0045 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8285, source_free_forest 0.6030, novelty_gate 0.8114; of 2990 alarms of the combined detector, 1134 come from the gate only, 270 from the forest only, 1586 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.7246, source_free_deeplog 0.8261, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.7246, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0375, source_free_deeplog 0.0977, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0361, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.188, source_free_deeplog 0.415, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.085, threshold 0.000, source_free_forest 0.188, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.178, source_free_deeplog 0.418, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.063, threshold 0.000, source_free_forest 0.175, novelty_gate 0.002, source_free_source_features 0.002
