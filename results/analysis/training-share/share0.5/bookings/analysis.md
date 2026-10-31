# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9663 | 0.7301 | 0.8318 | 0.7884 |
| source_free_deeplog | 0.8779 | 0.8247 | 0.8505 | 0.7914 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.3342 | 0.5009 | 0.5112 |
| transfer_similar | 0.9996 | 0.6963 | 0.8209 | 0.7858 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9471 | 0.4199 | 0.5819 | 0.5547 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2318 of 2697 | 0.15 | 0.0 | 2.0 |
| source_free_deeplog | 2568 of 2697 | 0.18 | 0.0 | 2.4 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 1088 of 2697 | 0.17 | 0.0 | 1.2 |
| transfer_similar | 2215 of 2697 | 0.15 | 0.0 | 2.0 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1602 of 2697 | 0.22 | 0.0 | 2.9 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0199 | [-0.0252, -0.0150] | 4.91e-07 | 1.97e-06 | True |
| H2 | -0.3308 | [-0.3454, -0.3158] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0109 | [-0.0164, -0.0057] | 0.060 | 0.120 | False |
| H6 | +0.0090 | [+0.0062, +0.0119] | 4.64e-10 | 2.32e-09 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2318 of 2697 | | 1.37e-48 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free 2318 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2215/source_free 2318 of 2697 | | 4.71e-16 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.819, config 0.836, timeout 0.863, resource 0.964, latency 0.198 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0882, source_free_deeplog 0.1556, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 8.69e-108 | 5.21e-107 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0158 | True | True | True |
| transfer_openstack | -0.3180 | True | True | True |
| transfer_similar | -0.0067 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0385 | [-0.0475, -0.0298] | 9.55e-04 | 0.003 | True |
| H2 | -0.3495 | [-0.3659, -0.3334] | 2.66e-218 | 2.13e-217 | True |
| H3 | -0.0296 | [-0.0383, -0.0209] | 0.084 | 0.120 | False |
| H6 | +0.0090 | [+0.0062, +0.0119] | 4.64e-10 | 2.32e-09 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2568 of 2697 | | 7.56e-124 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free_deeplog 2568 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2215/source_free_deeplog 2568 of 2697 | | 4.35e-103 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.861, config 0.875, timeout 0.875, resource 0.962, latency 0.565 | | 1.74e-111 | 1.22e-110 | True |
| H5 | FAR source_free 0.0882, source_free_deeplog 0.1556, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 8.69e-108 | 5.21e-107 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0313 | True | True | True |
| transfer_openstack | -0.3364 | True | True | True |
| transfer_similar | -0.0221 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8318, source_free_forest 0.5819, novelty_gate 0.8114; of 2996 alarms of the combined detector, 1238 come from the gate only, 276 from the forest only, 1482 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.6087, source_free_deeplog 0.7971, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.6087, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0402, source_free_deeplog 0.0964, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0388, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.203, source_free_deeplog 0.572, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.085, threshold 0.000, source_free_forest 0.203, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.192, source_free_deeplog 0.557, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.063, threshold 0.000, source_free_forest 0.190, novelty_gate 0.002, source_free_source_features 0.002
