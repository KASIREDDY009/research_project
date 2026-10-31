# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9624 | 0.7233 | 0.8259 | 0.7811 |
| source_free_deeplog | 0.8893 | 0.7781 | 0.8300 | 0.7686 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.3342 | 0.5009 | 0.5112 |
| transfer_similar | 0.9996 | 0.6963 | 0.8209 | 0.7858 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9284 | 0.3334 | 0.4906 | 0.4781 |
| novelty_gate | 0.9963 | 0.6840 | 0.8111 | 0.7750 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2285 of 2697 | 0.15 | 0.0 | 2.0 |
| source_free_deeplog | 2440 of 2697 | 0.18 | 0.0 | 2.3 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 1088 of 2697 | 0.17 | 0.0 | 1.2 |
| transfer_similar | 2215 of 2697 | 0.15 | 0.0 | 2.0 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1275 of 2697 | 0.20 | 0.0 | 3.1 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0140 | [-0.0189, -0.0094] | 0.005 | 0.019 | True |
| H2 | -0.3250 | [-0.3395, -0.3100] | 4.64e-322 | 4.18e-321 | True |
| H3 | -0.0050 | [-0.0107, +0.0002] | 0.867 | 1.000 | False |
| H6 | +0.0090 | [+0.0062, +0.0119] | 4.64e-10 | 2.32e-09 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2285 of 2697 | | 1.18e-38 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free 2285 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2215/source_free 2285 of 2697 | | 2.98e-08 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.824, config 0.838, timeout 0.862, resource 0.964, latency 0.159 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0858, source_free_deeplog 0.1311, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 3.62e-90 | 2.17e-89 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0100 | True | True | True |
| transfer_openstack | -0.3125 | True | True | True |
| transfer_similar | -0.0007 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0181 | [-0.0259, -0.0105] | 0.799 | 1.000 | False |
| H2 | -0.3290 | [-0.3451, -0.3135] | 1.03e-209 | 7.19e-209 | True |
| H3 | -0.0091 | [-0.0167, -0.0014] | 0.034 | 0.103 | False |
| H6 | +0.0090 | [+0.0062, +0.0119] | 4.64e-10 | 2.32e-09 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2440 of 2697 | | 2.57e-85 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free_deeplog 2440 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2215/source_free_deeplog 2440 of 2697 | | 5.89e-51 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.836, config 0.860, timeout 0.879, resource 0.962, latency 0.376 | | 7.34e-219 | 5.87e-218 | True |
| H5 | FAR source_free 0.0858, source_free_deeplog 0.1311, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 3.62e-90 | 2.17e-89 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0117 | True | True | True |
| transfer_openstack | -0.3162 | True | True | True |
| transfer_similar | -0.0025 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8259, source_free_forest 0.4906, novelty_gate 0.8111; of 2980 alarms of the combined detector, 1556 come from the gate only, 258 from the forest only, 1166 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.6087, source_free_deeplog 0.6812, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.6087, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0375, source_free_deeplog 0.0803, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0361, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.162, source_free_deeplog 0.374, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.085, threshold 0.000, source_free_forest 0.162, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.156, source_free_deeplog 0.377, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.063, threshold 0.000, source_free_forest 0.153, novelty_gate 0.002, source_free_source_features 0.002
