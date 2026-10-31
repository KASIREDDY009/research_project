# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9762 | 0.7150 | 0.8254 | 0.7842 |
| source_free_deeplog | 0.8698 | 0.8040 | 0.8356 | 0.7718 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.3342 | 0.5009 | 0.5112 |
| transfer_similar | 0.9989 | 0.7130 | 0.8321 | 0.7972 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9607 | 0.3763 | 0.5408 | 0.5276 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2272 of 2697 | 0.16 | 0.0 | 2.1 |
| source_free_deeplog | 2508 of 2697 | 0.18 | 0.0 | 2.4 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 1088 of 2697 | 0.17 | 0.0 | 1.2 |
| transfer_similar | 2276 of 2697 | 0.16 | 0.0 | 2.1 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1457 of 2697 | 0.24 | 0.0 | 3.4 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0135 | [-0.0179, -0.0095] | 4.50e-05 | 1.80e-04 | True |
| H2 | -0.3245 | [-0.3395, -0.3097] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0066 | [+0.0014, +0.0116] | 6.32e-04 | 0.001 | True |
| H6 | +0.0202 | [+0.0165, +0.0240] | 3.11e-28 | 1.56e-27 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2272 of 2697 | | 9.63e-35 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free 2272 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2276/source_free 2272 of 2697 | | 0.831 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.814, config 0.832, timeout 0.858, resource 0.963, latency 0.139 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0600, source_free_deeplog 0.1593, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 3.77e-107 | 2.26e-106 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0101 | True | True | True |
| transfer_openstack | -0.3118 | True | True | True |
| transfer_similar | +0.0109 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0237 | [-0.0322, -0.0154] | 0.974 | 0.974 | False |
| H2 | -0.3347 | [-0.3509, -0.3188] | 1.72e-192 | 1.38e-191 | True |
| H3 | -0.0036 | [-0.0117, +0.0048] | 2.20e-04 | 6.60e-04 | True |
| H6 | +0.0202 | [+0.0165, +0.0240] | 3.11e-28 | 1.56e-27 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2508 of 2697 | | 8.72e-106 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free_deeplog 2508 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2276/source_free_deeplog 2508 of 2697 | | 7.04e-43 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.850, config 0.870, timeout 0.865, resource 0.962, latency 0.491 | | 2.62e-147 | 1.83e-146 | True |
| H5 | FAR source_free 0.0600, source_free_deeplog 0.1593, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0012, threshold 0.0000 | | 3.77e-107 | 2.26e-106 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0167 | True | True | True |
| transfer_openstack | -0.3216 | True | True | True |
| transfer_similar | +0.0034 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8254, source_free_forest 0.5408, novelty_gate 0.8114; of 2904 alarms of the combined detector, 1351 come from the gate only, 184 from the forest only, 1369 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.4928, source_free_deeplog 0.7536, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.4928, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0201, source_free_deeplog 0.1044, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0013, threshold 0.0000, source_free_forest 0.0187, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.143, source_free_deeplog 0.498, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.152, threshold 0.000, source_free_forest 0.143, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.136, source_free_deeplog 0.484, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.144, threshold 0.000, source_free_forest 0.134, novelty_gate 0.002, source_free_source_features 0.002
