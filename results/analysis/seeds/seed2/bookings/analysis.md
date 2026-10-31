# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9783 | 0.7049 | 0.8194 | 0.7785 |
| source_free_deeplog | 0.8413 | 0.8555 | 0.8483 | 0.7842 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.1201 | 0.2144 | 0.2962 |
| transfer_similar | 0.9996 | 0.7142 | 0.8332 | 0.7985 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9636 | 0.3604 | 0.5246 | 0.5163 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2226 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_deeplog | 2693 of 2697 | 0.20 | 0.0 | 2.6 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 239 of 2697 | 0.00 | 0.0 | 0.0 |
| transfer_similar | 2289 of 2697 | 0.17 | 0.0 | 2.1 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1389 of 2697 | 0.19 | 0.0 | 2.8 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0075 | [-0.0111, -0.0041] | 0.055 | 0.110 | False |
| H2 | -0.6050 | [-0.6226, -0.5884] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0138 | [+0.0081, +0.0190] | 1.01e-08 | 4.04e-08 | True |
| H6 | +0.0213 | [+0.0170, +0.0257] | 3.63e-23 | 1.82e-22 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2226 of 2697 | | 6.78e-21 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 239/source_free 2226 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2289/source_free 2226 of 2697 | | 4.76e-06 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.817, config 0.833, timeout 0.861, resource 0.963, latency 0.085 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0515, source_free_deeplog 0.1679, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 3.75e-117 | 2.62e-116 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0046 | True | True | True |
| transfer_openstack | -0.5911 | True | True | True |
| transfer_similar | +0.0181 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0364 | [-0.0467, -0.0266] | 0.247 | 0.247 | False |
| H2 | -0.6340 | [-0.6515, -0.6168] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0151 | [-0.0247, -0.0058] | 0.025 | 0.076 | False |
| H6 | +0.0213 | [+0.0170, +0.0257] | 3.63e-23 | 1.82e-22 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2693 of 2697 | | 1.78e-161 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 239/source_free_deeplog 2693 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2289/source_free_deeplog 2693 of 2697 | | 4.84e-122 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.850, config 0.870, timeout 0.869, resource 0.962, latency 0.735 | | 5.56e-36 | 3.34e-35 | True |
| H5 | FAR source_free 0.0515, source_free_deeplog 0.1679, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 3.75e-117 | 2.62e-116 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0283 | True | True | True |
| transfer_openstack | -0.6198 | True | True | True |
| transfer_similar | -0.0074 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8194, source_free_forest 0.5246, novelty_gate 0.8114; of 2857 alarms of the combined detector, 1374 come from the gate only, 137 from the forest only, 1346 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.3913, source_free_deeplog 0.8551, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.3913, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0201, source_free_deeplog 0.1044, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0187, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.080, source_free_deeplog 0.737, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.171, threshold 0.000, source_free_forest 0.080, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.090, source_free_deeplog 0.732, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.175, threshold 0.000, source_free_forest 0.088, novelty_gate 0.002, source_free_source_features 0.002
