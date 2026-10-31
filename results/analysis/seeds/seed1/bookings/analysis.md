# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9681 | 0.7269 | 0.8303 | 0.7873 |
| source_free_deeplog | 0.8848 | 0.8194 | 0.8509 | 0.7929 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.3342 | 0.5009 | 0.5112 |
| transfer_similar | 0.9996 | 0.7067 | 0.8280 | 0.7931 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9538 | 0.4530 | 0.6142 | 0.5831 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2307 of 2697 | 0.16 | 0.0 | 2.0 |
| source_free_deeplog | 2562 of 2697 | 0.19 | 0.0 | 2.4 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 1088 of 2697 | 0.17 | 0.0 | 1.2 |
| transfer_similar | 2275 of 2697 | 0.16 | 0.0 | 2.1 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1718 of 2697 | 0.21 | 0.0 | 2.8 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0184 | [-0.0233, -0.0136] | 1.82e-06 | 7.29e-06 | True |
| H2 | -0.3294 | [-0.3443, -0.3143] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0023 | [-0.0081, +0.0034] | 0.493 | 0.858 | False |
| H6 | +0.0161 | [+0.0121, +0.0205] | 1.46e-14 | 7.31e-14 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2307 of 2697 | | 2.80e-45 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free 2307 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2275/source_free 2307 of 2697 | | 0.032 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.817, config 0.835, timeout 0.862, resource 0.964, latency 0.187 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0735, source_free_deeplog 0.1495, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.80e-101 | 1.68e-100 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0143 | True | True | True |
| transfer_openstack | -0.3168 | True | True | True |
| transfer_similar | +0.0025 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0389 | [-0.0479, -0.0300] | 1.77e-04 | 5.30e-04 | True |
| H2 | -0.3499 | [-0.3671, -0.3342] | 1.16e-227 | 9.27e-227 | True |
| H3 | -0.0228 | [-0.0314, -0.0145] | 0.429 | 0.858 | False |
| H6 | +0.0161 | [+0.0121, +0.0205] | 1.46e-14 | 7.31e-14 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2562 of 2697 | | 4.84e-122 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 1088/source_free_deeplog 2562 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2275/source_free_deeplog 2562 of 2697 | | 5.85e-66 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.862, config 0.880, timeout 0.879, resource 0.962, latency 0.530 | | 1.94e-133 | 1.36e-132 | True |
| H5 | FAR source_free 0.0735, source_free_deeplog 0.1495, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.80e-101 | 1.68e-100 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0315 | True | True | True |
| transfer_openstack | -0.3368 | True | True | True |
| transfer_similar | -0.0156 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8303, source_free_forest 0.6142, novelty_gate 0.8114; of 2977 alarms of the combined detector, 1094 come from the gate only, 257 from the forest only, 1626 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.6087, source_free_deeplog 0.7391, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.6087, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0241, source_free_deeplog 0.0950, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0228, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.191, source_free_deeplog 0.536, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.164, threshold 0.000, source_free_forest 0.191, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.182, source_free_deeplog 0.523, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.129, threshold 0.000, source_free_forest 0.180, novelty_gate 0.002, source_free_source_features 0.002
