# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings

4481 windows pooled (1329 positive, 271 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9802 | 0.7073 | 0.8217 | 0.7810 |
| source_free_deeplog | 0.8908 | 0.7547 | 0.8171 | 0.7536 |
| transfer | 1.0000 | 0.6795 | 0.8091 | 0.7737 |
| transfer_openstack | 1.0000 | 0.3303 | 0.4966 | 0.5075 |
| transfer_similar | 1.0000 | 0.6938 | 0.8192 | 0.7838 |
| threshold | 1.0000 | 0.2114 | 0.3491 | 0.3983 |
| source_free_forest | 0.9653 | 0.3770 | 0.5422 | 0.5299 |
| novelty_gate | 0.9989 | 0.6795 | 0.8088 | 0.7730 |
| source_free_source_features | 1.0000 | 0.6795 | 0.8091 | 0.7737 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 752 of 899 | 0.16 | 0.0 | 2.0 |
| source_free_deeplog | 783 of 899 | 0.18 | 0.0 | 2.3 |
| transfer | 720 of 899 | 0.16 | 0.0 | 2.0 |
| transfer_openstack | 360 of 899 | 0.19 | 0.0 | 1.3 |
| transfer_similar | 739 of 899 | 0.16 | 0.0 | 2.0 |
| threshold | 281 of 899 | 0.24 | 0.0 | 1.7 |
| source_free_forest | 490 of 899 | 0.25 | 0.0 | 3.6 |
| novelty_gate | 720 of 899 | 0.16 | 0.0 | 2.0 |
| source_free_source_features | 720 of 899 | 0.16 | 0.0 | 2.0 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0125 | [-0.0196, -0.0056] | 0.022 | 0.067 | False |
| H2 | -0.3251 | [-0.3501, -0.3000] | 1.43e-122 | 1.29e-121 | True |
| H3 | -0.0025 | [-0.0107, +0.0056] | 1.000 | 1.000 | False |
| H6 | +0.0101 | [+0.0059, +0.0147] | 3.81e-06 | 1.91e-05 | True |
| H1 (fault segments) | detected transfer 720/source_free 752 of 899 | | 4.66e-10 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 360/source_free 752 of 899 | | 1.98e-118 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 739/source_free 752 of 899 | | 0.092 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.805, config 0.828, timeout 0.863, resource 0.966, latency 0.118 | | 1.12e-131 | 1.12e-130 | True |
| H5 | FAR source_free 0.0627, source_free_deeplog 0.1476, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.22e-31 | 7.30e-31 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0067 | True | True | True |
| transfer_openstack | -0.3043 | True | True | True |
| transfer_similar | +0.0045 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0080 | [-0.0210, +0.0041] | 0.141 | 0.281 | False |
| H2 | -0.3205 | [-0.3490, -0.2923] | 2.56e-68 | 1.79e-67 | True |
| H3 | +0.0021 | [-0.0114, +0.0156] | 0.008 | 0.033 | True |
| H6 | +0.0101 | [+0.0059, +0.0147] | 3.81e-06 | 1.91e-05 | True |
| H1 (fault segments) | detected transfer 720/source_free_deeplog 783 of 899 | | 2.17e-19 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 360/source_free_deeplog 783 of 899 | | 9.23e-128 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 739/source_free_deeplog 783 of 899 | | 1.15e-06 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.839, config 0.868, timeout 0.871, resource 0.962, latency 0.268 | | 1.36e-99 | 1.09e-98 | True |
| H5 | FAR source_free 0.0627, source_free_deeplog 0.1476, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.22e-31 | 7.30e-31 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | +0.0026 | True | True | True |
| transfer_openstack | -0.2968 | True | True | True |
| transfer_similar | +0.0134 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8217, source_free_forest 0.5422, novelty_gate 0.8088; of 959 alarms of the combined detector, 440 come from the gate only, 55 from the forest only, 464 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (24): false-alarm rate source_free 0.5000, source_free_deeplog 0.7083, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.5000, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (247): false-alarm rate source_free 0.0202, source_free_deeplog 0.0931, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0202, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (144 fault windows): recall source_free 0.097, source_free_deeplog 0.264, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.083, threshold 0.000, source_free_forest 0.097, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (136 fault windows): recall source_free 0.140, source_free_deeplog 0.272, transfer 0.007, transfer_openstack 0.000, transfer_similar 0.059, threshold 0.000, source_free_forest 0.132, novelty_gate 0.007, source_free_source_features 0.007
