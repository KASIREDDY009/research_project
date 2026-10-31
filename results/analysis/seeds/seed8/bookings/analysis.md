# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9764 | 0.7090 | 0.8214 | 0.7801 |
| source_free_deeplog | 0.8957 | 0.7750 | 0.8310 | 0.7711 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.3342 | 0.5009 | 0.5112 |
| transfer_similar | 0.9993 | 0.7201 | 0.8370 | 0.8024 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9612 | 0.3750 | 0.5396 | 0.5269 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2247 of 2697 | 0.15 | 0.0 | 2.0 |
| source_free_deeplog | 2455 of 2697 | 0.18 | 0.0 | 2.3 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 1088 of 2697 | 0.17 | 0.0 | 1.2 |
| transfer_similar | 2314 of 2697 | 0.17 | 0.0 | 2.2 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1452 of 2697 | 0.18 | 0.0 | 2.5 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0095 | [-0.0133, -0.0057] | 0.010 | 0.020 | True |
| H2 | -0.3205 | [-0.3352, -0.3057] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0155 | [+0.0098, +0.0210] | 3.45e-10 | 1.38e-09 | True |
| H6 | +0.0251 | [+0.0209, +0.0297] | 1.00e-29 | 5.00e-29 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2247 of 2697 | | 3.23e-27 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free 2247 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2314/source_free 2247 of 2697 | | 4.17e-06 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.813, config 0.832, timeout 0.858, resource 0.964, latency 0.110 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0625, source_free_deeplog 0.1422, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 9.39e-96 | 5.63e-95 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0063 | True | True | True |
| transfer_openstack | -0.3081 | True | True | True |
| transfer_similar | +0.0200 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0191 | [-0.0264, -0.0115] | 0.852 | 0.852 | False |
| H2 | -0.3300 | [-0.3465, -0.3144] | 5.58e-219 | 4.46e-218 | True |
| H3 | +0.0060 | [-0.0018, +0.0141] | 8.21e-07 | 2.46e-06 | True |
| H6 | +0.0251 | [+0.0209, +0.0297] | 1.00e-29 | 5.00e-29 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2455 of 2697 | | 7.85e-90 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free_deeplog 2455 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2314/source_free_deeplog 2455 of 2697 | | 8.10e-15 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.835, config 0.853, timeout 0.870, resource 0.962, latency 0.377 | | 6.69e-213 | 4.68e-212 | True |
| H5 | FAR source_free 0.0625, source_free_deeplog 0.1422, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 9.39e-96 | 5.63e-95 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0128 | True | True | True |
| transfer_openstack | -0.3168 | True | True | True |
| transfer_similar | +0.0125 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8214, source_free_forest 0.5396, novelty_gate 0.8114; of 2879 alarms of the combined detector, 1332 come from the gate only, 159 from the forest only, 1388 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.5362, source_free_deeplog 0.6377, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.5362, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0187, source_free_deeplog 0.0964, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0174, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.111, source_free_deeplog 0.379, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.193, threshold 0.000, source_free_forest 0.111, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.109, source_free_deeplog 0.375, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.204, threshold 0.000, source_free_forest 0.107, novelty_gate 0.002, source_free_source_features 0.002
