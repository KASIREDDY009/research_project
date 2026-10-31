# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9750 | 0.7183 | 0.8272 | 0.7857 |
| source_free_deeplog | 0.8701 | 0.7907 | 0.8285 | 0.7632 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | nan | 0.0000 | 0.0000 | nan |
| transfer_similar | 0.9972 | 0.7256 | 0.8400 | 0.8050 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9644 | 0.4441 | 0.6082 | 0.5820 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2276 of 2697 | 0.15 | 0.0 | 2.0 |
| source_free_deeplog | 2452 of 2697 | 0.19 | 0.0 | 2.4 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 0 of 2697 | n/a | n/a | n/a |
| transfer_similar | 2320 of 2697 | 0.16 | 0.0 | 2.1 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1701 of 2697 | 0.19 | 0.0 | 2.6 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0153 | [-0.0198, -0.0110] | 5.54e-06 | 1.11e-05 | True |
| H2 | -0.8272 | [-0.8370, -0.8175] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0128 | [+0.0073, +0.0183] | 9.33e-08 | 2.80e-07 | True |
| H6 | +0.0281 | [+0.0239, +0.0325] | 2.22e-39 | 1.11e-38 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2276 of 2697 | | 6.02e-36 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free 2276 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2320/source_free 2276 of 2697 | | 0.003 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.815, config 0.836, timeout 0.859, resource 0.963, latency 0.149 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0650, source_free_deeplog 0.1422, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0049, threshold 0.0000 | | 5.36e-93 | 3.21e-92 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0117 | True | True | True |
| transfer_openstack | -0.8190 | True | True | True |
| transfer_similar | +0.0175 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0166 | [-0.0251, -0.0083] | 0.169 | 0.169 | False |
| H2 | -0.8285 | [-0.8372, -0.8193] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0115 | [+0.0038, +0.0197] | 6.84e-12 | 2.74e-11 | True |
| H6 | +0.0281 | [+0.0239, +0.0325] | 2.22e-39 | 1.11e-38 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2452 of 2697 | | 6.28e-89 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free_deeplog 2452 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2320/source_free_deeplog 2452 of 2697 | | 9.46e-17 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.872, config 0.886, timeout 0.866, resource 0.962, latency 0.388 | | 9.70e-226 | 6.79e-225 | True |
| H5 | FAR source_free 0.0650, source_free_deeplog 0.1422, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0049, threshold 0.0000 | | 5.36e-93 | 3.21e-92 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0098 | True | True | True |
| transfer_openstack | -0.8209 | True | True | True |
| transfer_similar | +0.0184 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8272, source_free_forest 0.6082, novelty_gate 0.8114; of 2921 alarms of the combined detector, 1095 come from the gate only, 201 from the forest only, 1625 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.5652, source_free_deeplog 0.6812, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0290, threshold 0.0000, source_free_forest 0.5652, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0187, source_free_deeplog 0.0924, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0027, threshold 0.0000, source_free_forest 0.0174, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.157, source_free_deeplog 0.399, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.213, threshold 0.000, source_free_forest 0.157, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.141, source_free_deeplog 0.377, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.200, threshold 0.000, source_free_forest 0.139, novelty_gate 0.002, source_free_source_features 0.002
