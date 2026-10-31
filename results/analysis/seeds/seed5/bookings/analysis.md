# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9736 | 0.7074 | 0.8195 | 0.7773 |
| source_free_deeplog | 0.8439 | 0.8689 | 0.8562 | 0.7950 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.1190 | 0.2128 | 0.2949 |
| transfer_similar | 0.9989 | 0.7188 | 0.8360 | 0.8013 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9553 | 0.3667 | 0.5300 | 0.5174 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2235 of 2697 | 0.15 | 0.0 | 2.0 |
| source_free_deeplog | 2694 of 2697 | 0.19 | 0.0 | 2.5 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 236 of 2697 | 0.00 | 0.0 | 0.0 |
| transfer_similar | 2296 of 2697 | 0.16 | 0.0 | 2.1 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1404 of 2697 | 0.17 | 0.0 | 2.4 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0075 | [-0.0116, -0.0039] | 0.142 | 0.285 | False |
| H2 | -0.6067 | [-0.6239, -0.5903] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0166 | [+0.0111, +0.0219] | 2.03e-11 | 8.12e-11 | True |
| H6 | +0.0241 | [+0.0201, +0.0282] | 3.21e-36 | 1.93e-35 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2235 of 2697 | | 1.32e-23 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 236/source_free 2235 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2296/source_free 2235 of 2697 | | 2.94e-05 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.817, config 0.835, timeout 0.861, resource 0.963, latency 0.096 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0674, source_free_deeplog 0.1679, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.19e-114 | 1.53e-113 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0044 | True | True | True |
| transfer_openstack | -0.5928 | True | True | True |
| transfer_similar | +0.0210 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0443 | [-0.0548, -0.0344] | 0.008 | 0.024 | True |
| H2 | -0.6435 | [-0.6607, -0.6273] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0202 | [-0.0296, -0.0106] | 0.281 | 0.285 | False |
| H6 | +0.0241 | [+0.0201, +0.0282] | 3.21e-36 | 1.93e-35 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2694 of 2697 | | 8.89e-162 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 236/source_free_deeplog 2694 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2296/source_free_deeplog 2694 of 2697 | | 3.10e-120 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.882, config 0.890, timeout 0.866, resource 0.962, latency 0.750 | | 1.19e-34 | 5.96e-34 | True |
| H5 | FAR source_free 0.0674, source_free_deeplog 0.1679, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.19e-114 | 1.53e-113 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0360 | True | True | True |
| transfer_openstack | -0.6297 | True | True | True |
| transfer_similar | -0.0123 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8195, source_free_forest 0.5300, novelty_gate 0.8114; of 2881 alarms of the combined detector, 1359 come from the gate only, 161 from the forest only, 1361 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.4928, source_free_deeplog 0.8116, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.4928, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0281, source_free_deeplog 0.1084, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0268, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.094, source_free_deeplog 0.758, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.176, threshold 0.000, source_free_forest 0.094, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.097, source_free_deeplog 0.742, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.170, threshold 0.000, source_free_forest 0.095, novelty_gate 0.002, source_free_source_features 0.002
