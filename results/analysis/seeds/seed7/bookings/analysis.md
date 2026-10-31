# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9728 | 0.7127 | 0.8227 | 0.7805 |
| source_free_deeplog | 0.8943 | 0.7914 | 0.8397 | 0.7811 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.1221 | 0.2176 | 0.2988 |
| transfer_similar | 0.9993 | 0.7163 | 0.8344 | 0.7997 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9539 | 0.3702 | 0.5334 | 0.5195 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2257 of 2697 | 0.15 | 0.0 | 2.0 |
| source_free_deeplog | 2462 of 2697 | 0.17 | 0.0 | 2.2 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 247 of 2697 | 0.00 | 0.0 | 0.2 |
| transfer_similar | 2282 of 2697 | 0.15 | 0.0 | 2.1 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1432 of 2697 | 0.20 | 0.0 | 2.9 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0108 | [-0.0149, -0.0068] | 0.007 | 0.022 | True |
| H2 | -0.6051 | [-0.6225, -0.5888] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0117 | [+0.0064, +0.0170] | 1.73e-07 | 6.93e-07 | True |
| H6 | +0.0225 | [+0.0181, +0.0268] | 9.27e-27 | 4.63e-26 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2257 of 2697 | | 3.16e-30 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 247/source_free 2257 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2282/source_free 2257 of 2697 | | 0.068 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.814, config 0.833, timeout 0.862, resource 0.963, latency 0.124 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0650, source_free_deeplog 0.1483, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 7.85e-100 | 4.71e-99 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0074 | True | True | True |
| transfer_openstack | -0.5913 | True | True | True |
| transfer_similar | +0.0162 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0278 | [-0.0357, -0.0199] | 0.043 | 0.043 | True |
| H2 | -0.6221 | [-0.6400, -0.6055] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0053 | [-0.0135, +0.0029] | 0.016 | 0.032 | True |
| H6 | +0.0225 | [+0.0181, +0.0268] | 9.27e-27 | 4.63e-26 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2462 of 2697 | | 6.14e-92 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 247/source_free_deeplog 2462 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2282/source_free_deeplog 2462 of 2697 | | 1.88e-27 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.845, config 0.863, timeout 0.887, resource 0.962, latency 0.421 | | 1.17e-194 | 8.18e-194 | True |
| H5 | FAR source_free 0.0650, source_free_deeplog 0.1483, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 7.85e-100 | 4.71e-99 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0216 | True | True | True |
| transfer_openstack | -0.6078 | True | True | True |
| transfer_similar | +0.0015 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8227, source_free_forest 0.5334, novelty_gate 0.8114; of 2905 alarms of the combined detector, 1366 come from the gate only, 185 from the forest only, 1354 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.5652, source_free_deeplog 0.6957, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.5652, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0187, source_free_deeplog 0.0977, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0174, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.128, source_free_deeplog 0.418, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.174, threshold 0.000, source_free_forest 0.128, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.119, source_free_deeplog 0.423, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.141, threshold 0.000, source_free_forest 0.117, novelty_gate 0.002, source_free_source_features 0.002
