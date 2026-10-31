# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

26887 windows pooled (5231 positive, 1642 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9273 | 0.7238 | 0.8130 | 0.7832 |
| source_free_deeplog | 0.8458 | 0.7259 | 0.7813 | 0.7366 |
| transfer | 0.9994 | 0.6310 | 0.7736 | 0.7609 |
| transfer_openstack | 1.0000 | 0.1910 | 0.3207 | 0.3997 |
| transfer_similar | 1.0000 | 0.5720 | 0.7277 | 0.7200 |
| threshold | 1.0000 | 0.1130 | 0.2030 | 0.3050 |
| source_free_forest | 0.9125 | 0.5720 | 0.7032 | 0.6759 |
| novelty_gate | 0.9970 | 0.6310 | 0.7729 | 0.7596 |
| source_free_source_features | 0.9994 | 0.6310 | 0.7736 | 0.7609 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2563 of 2697 | 0.33 | 0.0 | 3.5 |
| source_free_deeplog | 2405 of 2697 | 0.32 | 0.0 | 3.4 |
| transfer | 2158 of 2697 | 0.29 | 0.0 | 3.0 |
| transfer_openstack | 504 of 2697 | 0.01 | 0.0 | 0.2 |
| transfer_similar | 2000 of 2697 | 0.29 | 0.0 | 3.8 |
| threshold | 591 of 2697 | 0.61 | 1.6 | 2.6 |
| source_free_forest | 2383 of 2697 | 0.46 | 0.0 | 5.2 |
| novelty_gate | 2158 of 2697 | 0.29 | 0.0 | 3.0 |
| source_free_source_features | 2158 of 2697 | 0.29 | 0.0 | 3.0 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0394 | [-0.0460, -0.0330] | 1.04e-11 | 3.13e-11 | True |
| H2 | -0.4923 | [-0.5076, -0.4770] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0853 | [-0.0938, -0.0772] | 8.20e-53 | 3.28e-52 | True |
| H6 | -0.0459 | [-0.0514, -0.0410] | 2.33e-89 | 1.16e-88 | True |
| H1 (fault segments) | detected transfer 2158/source_free 2563 of 2697 | | 2.42e-122 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 504/source_free 2563 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2000/source_free 2563 of 2697 | | 6.62e-170 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.727, config 0.747, timeout 0.787, resource 0.957, latency 0.420 | | 6.11e-172 | 4.27e-171 | True |
| H5 | FAR source_free 0.1035, source_free_deeplog 0.1041, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.53e-169 | 9.15e-169 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0342 | True | True | True |
| transfer_openstack | -0.4800 | True | True | True |
| transfer_similar | -0.0784 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0077 | [-0.0151, -0.0003] | 1.95e-08 | 3.90e-08 | True |
| H2 | -0.4606 | [-0.4766, -0.4455] | 7.69e-298 | 6.92e-297 | True |
| H3 | -0.0536 | [-0.0623, -0.0444] | 0.004 | 0.004 | True |
| H6 | -0.0459 | [-0.0514, -0.0410] | 2.33e-89 | 1.16e-88 | True |
| H1 (fault segments) | detected transfer 2158/source_free_deeplog 2405 of 2697 | | 8.84e-75 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 504/source_free_deeplog 2405 of 2697 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2000/source_free_deeplog 2405 of 2697 | | 2.42e-122 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.792, config 0.802, timeout 0.798, resource 0.952, latency 0.304 | | 2.19e-282 | 1.75e-281 | True |
| H5 | FAR source_free 0.1035, source_free_deeplog 0.1041, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.53e-169 | 9.15e-169 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0014 | True | True | True |
| transfer_openstack | -0.4475 | True | True | True |
| transfer_similar | -0.0462 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8130, source_free_forest 0.7032, novelty_gate 0.7729; of 4083 alarms of the combined detector, 804 come from the gate only, 772 from the forest only, 2507 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.9359, source_free_deeplog 0.4359, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.9359, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (1564): false-alarm rate source_free 0.0620, source_free_deeplog 0.0876, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0614, novelty_gate 0.0006, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (541 fault windows): recall source_free 0.420, source_free_deeplog 0.314, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.000, threshold 0.000, source_free_forest 0.420, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (540 fault windows): recall source_free 0.420, source_free_deeplog 0.294, transfer 0.002, transfer_openstack 0.000, transfer_similar 0.002, threshold 0.000, source_free_forest 0.420, novelty_gate 0.002, source_free_source_features 0.002
