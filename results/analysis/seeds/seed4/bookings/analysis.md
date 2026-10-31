# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

13442 windows pooled (3965 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9731 | 0.7198 | 0.8275 | 0.7855 |
| source_free_deeplog | 0.8579 | 0.8633 | 0.8606 | 0.8020 |
| transfer | 0.9993 | 0.6837 | 0.8119 | 0.7766 |
| transfer_openstack | 1.0000 | 0.1190 | 0.2128 | 0.2949 |
| transfer_similar | 0.9983 | 0.7299 | 0.8432 | 0.8087 |
| threshold | 1.0000 | 0.2141 | 0.3527 | 0.4014 |
| source_free_forest | 0.9600 | 0.4293 | 0.5932 | 0.5684 |
| novelty_gate | 0.9971 | 0.6840 | 0.8114 | 0.7754 |
| source_free_source_features | 0.9993 | 0.6837 | 0.8119 | 0.7766 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2281 of 2697 | 0.15 | 0.0 | 2.0 |
| source_free_deeplog | 2696 of 2697 | 0.19 | 0.0 | 2.5 |
| transfer | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| transfer_openstack | 236 of 2697 | 0.00 | 0.0 | 0.0 |
| transfer_similar | 2335 of 2697 | 0.16 | 0.0 | 2.2 |
| threshold | 849 of 2697 | 0.22 | 0.0 | 1.5 |
| source_free_forest | 1654 of 2697 | 0.21 | 0.0 | 2.8 |
| novelty_gate | 2158 of 2697 | 0.15 | 0.0 | 1.9 |
| source_free_source_features | 2158 of 2697 | 0.15 | 0.0 | 1.9 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0156 | [-0.0201, -0.0112] | 1.02e-05 | 3.05e-05 | True |
| H2 | -0.6147 | [-0.6319, -0.5985] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0158 | [+0.0096, +0.0219] | 3.21e-09 | 1.28e-08 | True |
| H6 | +0.0313 | [+0.0262, +0.0364] | 4.58e-38 | 2.75e-37 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2281 of 2697 | | 1.88e-37 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 236/source_free 2281 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2335/source_free 2281 of 2697 | | 4.24e-04 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.815, config 0.837, timeout 0.862, resource 0.963, latency 0.153 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0637, source_free_deeplog 0.1679, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0025, threshold 0.0000 | | 1.98e-113 | 1.38e-112 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0117 | True | True | True |
| transfer_openstack | -0.6010 | True | True | True |
| transfer_similar | +0.0207 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0487 | [-0.0588, -0.0390] | 4.32e-05 | 8.63e-05 | True |
| H2 | -0.6478 | [-0.6648, -0.6313] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0174 | [-0.0265, -0.0083] | 0.348 | 0.348 | False |
| H6 | +0.0313 | [+0.0262, +0.0364] | 4.58e-38 | 2.75e-37 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2696 of 2697 | | 2.22e-162 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 236/source_free_deeplog 2696 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2335/source_free_deeplog 2696 of 2697 | | 4.26e-109 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.862, config 0.878, timeout 0.871, resource 0.962, latency 0.749 | | 6.15e-33 | 3.07e-32 | True |
| H5 | FAR source_free 0.0637, source_free_deeplog 0.1679, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0025, threshold 0.0000 | | 1.98e-113 | 1.38e-112 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0405 | True | True | True |
| transfer_openstack | -0.6340 | True | True | True |
| transfer_similar | -0.0096 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8275, source_free_forest 0.5932, novelty_gate 0.8114; of 2933 alarms of the combined detector, 1160 come from the gate only, 213 from the forest only, 1560 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (69): false-alarm rate source_free 0.5362, source_free_deeplog 0.8116, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0145, threshold 0.0000, source_free_forest 0.5362, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (747): false-alarm rate source_free 0.0201, source_free_deeplog 0.1084, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0013, threshold 0.0000, source_free_forest 0.0187, novelty_gate 0.0013, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (414 fault windows): recall source_free 0.159, source_free_deeplog 0.751, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.220, threshold 0.000, source_free_forest 0.159, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (411 fault windows): recall source_free 0.146, source_free_deeplog 0.747, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.231, threshold 0.000, source_free_forest 0.144, novelty_gate 0.002, source_free_source_features 0.002
