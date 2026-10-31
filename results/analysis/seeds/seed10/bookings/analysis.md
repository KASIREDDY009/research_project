# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9733 | 0.7256 | 0.8314 | 0.7897 |
| source_free_deeplog | 0.8532 | 0.8252 | 0.8390 | 0.7734 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | nan | 0.0000 | 0.0000 | nan |
| transfer_similar | 0.9975 | 0.7150 | 0.8330 | 0.7977 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9598 | 0.4280 | 0.5920 | 0.5674 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2307 of 2697 | 0.16 | 0.0 | 2.0 |
| source_free_deeplog | 2560 of 2697 | 0.19 | 0.0 | 2.5 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 0 of 2697 | n/a | n/a | n/a |
| transfer_similar | 2296 of 2697 | 0.16 | 0.0 | 2.1 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1640 of 2697 | 0.19 | 0.0 | 2.7 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0195 | [-0.0242, -0.0148] | 1.14e-08 | 4.57e-08 | True |
| H2 | -0.8314 | [-0.8410, -0.8219] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0016 | [-0.0043, +0.0074] | 0.132 | 0.263 | False |
| H6 | +0.0210 | [+0.0169, +0.0255] | 8.05e-22 | 4.03e-21 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2307 of 2697 | | 2.80e-45 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free 2307 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2296/source_free 2307 of 2697 | | 0.525 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.815, config 0.835, timeout 0.859, resource 0.963, latency 0.185 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0699, source_free_deeplog 0.1532, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0061, threshold 0.0000 | | 5.34e-100 | 3.20e-99 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0155 | True | True | True |
| transfer_openstack | -0.8233 | True | True | True |
| transfer_similar | +0.0067 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0271 | [-0.0366, -0.0180] | 1.000 | 1.000 | False |
| H2 | -0.8390 | [-0.8477, -0.8295] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0060 | [-0.0154, +0.0032] | 4.30e-04 | 0.001 | True |
| H6 | +0.0210 | [+0.0169, +0.0255] | 8.05e-22 | 4.03e-21 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2560 of 2697 | | 1.94e-121 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free_deeplog 2560 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2296/source_free_deeplog 2560 of 2697 | | 6.60e-45 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.877, config 0.881, timeout 0.879, resource 0.962, latency 0.542 | | 3.22e-130 | 2.25e-129 | True |
| H5 | FAR source_free 0.0699, source_free_deeplog 0.1532, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0061, threshold 0.0000 | | 5.34e-100 | 3.20e-99 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0194 | True | True | True |
| transfer_openstack | -0.8313 | True | True | True |
| transfer_similar | +0.0017 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8314, source_free_forest 0.5920, novelty_gate 0.8114; of 2956 alarms of the combined detector, 1188 come from the gate only, 236 from the forest only, 1532 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.5652, source_free_deeplog 0.7101, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0580, threshold 0.0000, source_free_forest 0.5652, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0241, source_free_deeplog 0.1017, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0013, threshold 0.0000, source_free_forest 0.0228, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.188, source_free_deeplog 0.556, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.179, threshold 0.000, source_free_forest 0.188, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.182, source_free_deeplog 0.528, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.168, threshold 0.000, source_free_forest 0.180, novelty_gate 0.002, source_free_source_features 0.002
