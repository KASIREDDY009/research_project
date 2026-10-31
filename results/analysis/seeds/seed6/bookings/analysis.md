# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9750 | 0.7087 | 0.8208 | 0.7790 |
| source_free_deeplog | 0.8182 | 0.8391 | 0.8285 | 0.7556 |
| transfer | 0.9993 | 0.6835 | 0.8117 | 0.7764 |
| transfer_openstack | nan | 0.0000 | 0.0000 | nan |
| transfer_similar | 0.9993 | 0.7097 | 0.8300 | 0.7951 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9642 | 0.4346 | 0.5991 | 0.5746 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2240 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_deeplog | 2614 of 2697 | 0.19 | 0.0 | 2.5 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 0 of 2697 | n/a | n/a | n/a |
| transfer_similar | 2266 of 2697 | 0.16 | 0.0 | 2.1 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1680 of 2697 | 0.19 | 0.0 | 2.8 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0091 | [-0.0129, -0.0052] | 0.026 | 0.026 | True |
| H2 | -0.8208 | [-0.8309, -0.8106] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0092 | [+0.0034, +0.0142] | 1.53e-05 | 4.60e-05 | True |
| H6 | +0.0182 | [+0.0146, +0.0220] | 4.31e-22 | 2.16e-21 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2240 of 2697 | | 4.14e-25 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free 2240 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2266/source_free 2240 of 2697 | | 0.065 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.817, config 0.835, timeout 0.861, resource 0.963, latency 0.102 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0564, source_free_deeplog 0.1556, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.00e-106 | 1.40e-105 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0058 | True | True | True |
| transfer_openstack | -0.8124 | True | True | True |
| transfer_similar | +0.0134 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0168 | [-0.0270, -0.0073] | 0.001 | 0.002 | True |
| H2 | -0.8285 | [-0.8375, -0.8193] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0014 | [-0.0081, +0.0107] | 4.70e-10 | 1.88e-09 | True |
| H6 | +0.0182 | [+0.0146, +0.0220] | 4.31e-22 | 2.16e-21 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2614 of 2697 | | 1.07e-137 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free_deeplog 2614 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2266/source_free_deeplog 2614 of 2697 | | 1.96e-89 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.869, config 0.876, timeout 0.871, resource 0.962, latency 0.629 | | 5.95e-80 | 3.57e-79 | True |
| H5 | FAR source_free 0.0564, source_free_deeplog 0.1556, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.00e-106 | 1.40e-105 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0087 | True | True | True |
| transfer_openstack | -0.8208 | True | True | True |
| transfer_similar | +0.0091 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8208, source_free_forest 0.5991, novelty_gate 0.8114; of 2882 alarms of the combined detector, 1095 come from the gate only, 162 from the forest only, 1625 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features -0.0002 [-0.0006, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.4493, source_free_deeplog 0.7391, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.4493, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0201, source_free_deeplog 0.1017, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0187, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.104, source_free_deeplog 0.635, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.152, threshold 0.000, source_free_forest 0.104, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.100, source_free_deeplog 0.623, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.129, threshold 0.000, source_free_forest 0.097, novelty_gate 0.002, source_free_source_features 0.002
