# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9721 | 0.7201 | 0.8273 | 0.7851 |
| source_free_deeplog | 0.8884 | 0.7753 | 0.8280 | 0.7662 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.3342 | 0.5009 | 0.5112 |
| transfer_similar | 0.9996 | 0.6963 | 0.8209 | 0.7858 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9577 | 0.4230 | 0.5868 | 0.5625 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2278 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_deeplog | 2405 of 2697 | 0.17 | 0.0 | 2.2 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 1088 of 2697 | 0.17 | 0.0 | 1.2 |
| transfer_similar | 2215 of 2697 | 0.15 | 0.0 | 2.0 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1628 of 2697 | 0.19 | 0.0 | 2.8 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0154 | [-0.0200, -0.0109] | 2.27e-05 | 9.09e-05 | True |
| H2 | -0.3264 | [-0.3409, -0.3117] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0064 | [-0.0116, -0.0013] | 0.471 | 0.929 | False |
| H6 | +0.0090 | [+0.0062, +0.0119] | 4.64e-10 | 2.32e-09 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2278 of 2697 | | 1.50e-36 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free 2278 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2215/source_free 2278 of 2697 | | 5.34e-07 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.817, config 0.838, timeout 0.865, resource 0.964, latency 0.148 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0735, source_free_deeplog 0.1446, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.98e-97 | 1.79e-96 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0116 | True | True | True |
| transfer_openstack | -0.3137 | True | True | True |
| transfer_similar | -0.0023 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0161 | [-0.0234, -0.0086] | 0.464 | 0.929 | False |
| H2 | -0.3271 | [-0.3433, -0.3114] | 1.83e-206 | 1.28e-205 | True |
| H3 | -0.0071 | [-0.0148, +0.0004] | 0.009 | 0.028 | True |
| H6 | +0.0090 | [+0.0062, +0.0119] | 4.64e-10 | 2.32e-09 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2405 of 2697 | | 8.84e-75 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free_deeplog 2405 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2215/source_free_deeplog 2405 of 2697 | | 1.17e-40 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.851, config 0.867, timeout 0.866, resource 0.962, latency 0.353 | | 2.50e-237 | 2.00e-236 | True |
| H5 | FAR source_free 0.0735, source_free_deeplog 0.1446, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.98e-97 | 1.79e-96 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0096 | True | True | True |
| transfer_openstack | -0.3142 | True | True | True |
| transfer_similar | -0.0007 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8273, source_free_forest 0.5868, novelty_gate 0.8114; of 2937 alarms of the combined detector, 1186 come from the gate only, 217 from the forest only, 1534 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.6087, source_free_deeplog 0.6812, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.6087, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0241, source_free_deeplog 0.0950, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0228, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.157, source_free_deeplog 0.355, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.085, threshold 0.000, source_free_forest 0.157, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.139, source_free_deeplog 0.350, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.063, threshold 0.000, source_free_forest 0.136, novelty_gate 0.002, source_free_source_features 0.002
