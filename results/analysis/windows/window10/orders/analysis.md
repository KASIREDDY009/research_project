# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

26880 windows pooled (5225 positive, 1641 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9283 | 0.7382 | 0.8224 | 0.7930 |
| source_free_deeplog | 0.7905 | 0.8226 | 0.8062 | 0.7585 |
| transfer | 0.9991 | 0.6415 | 0.7814 | 0.7680 |
| transfer_openstack | 1.0000 | 0.2052 | 0.3405 | 0.4149 |
| transfer_similar | 1.0000 | 0.5759 | 0.7309 | 0.7228 |
| threshold | 1.0000 | 0.1055 | 0.1908 | 0.2945 |
| source_free_forest | 0.9113 | 0.5701 | 0.7014 | 0.6741 |
| novelty_gate | 0.9973 | 0.6415 | 0.7808 | 0.7670 |
| source_free_source_features | 0.9991 | 0.6415 | 0.7814 | 0.7680 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2544 of 2701 | 0.30 | 0.0 | 3.2 |
| source_free_deeplog | 2700 of 2701 | 0.33 | 0.0 | 3.6 |
| transfer | 2160 of 2701 | 0.26 | 0.0 | 2.5 |
| transfer_openstack | 539 of 2701 | 0.00 | 0.0 | 0.0 |
| transfer_similar | 2059 of 2701 | 0.32 | 0.0 | 3.9 |
| threshold | 551 of 2701 | 0.58 | 1.3 | 2.3 |
| source_free_forest | 2306 of 2701 | 0.43 | 0.0 | 5.1 |
| novelty_gate | 2160 of 2701 | 0.26 | 0.0 | 2.5 |
| source_free_source_features | 2160 of 2701 | 0.26 | 0.0 | 2.5 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0410 | [-0.0476, -0.0349] | 1.07e-13 | 3.22e-13 | True |
| H2 | -0.4819 | [-0.4964, -0.4669] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0915 | [-0.1000, -0.0830] | 1.38e-59 | 5.53e-59 | True |
| H6 | -0.0505 | [-0.0565, -0.0448] | 3.50e-67 | 1.75e-66 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2544 of 2701 | | 5.08e-116 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 539/source_free 2544 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2059/source_free 2544 of 2701 | | 1.82e-135 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.772, config 0.752, timeout 0.797, resource 0.962, latency 0.425 | | 1.38e-179 | 9.63e-179 | True |
| H5 | FAR source_free 0.1060, source_free_deeplog 0.1377, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.12e-205 | 1.70e-204 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0357 | True | True | True |
| transfer_openstack | -0.4694 | True | True | True |
| transfer_similar | -0.0844 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0249 | [-0.0338, -0.0156] | 3.40e-05 | 6.80e-05 | True |
| H2 | -0.4657 | [-0.4822, -0.4496] | 6.79e-228 | 6.11e-227 | True |
| H3 | -0.0754 | [-0.0863, -0.0643] | 0.003 | 0.003 | True |
| H6 | -0.0505 | [-0.0565, -0.0448] | 3.50e-67 | 1.75e-66 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2700 of 2701 | | 5.56e-163 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 539/source_free_deeplog 2700 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2059/source_free_deeplog 2700 of 2701 | | 2.19e-193 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.846, config 0.836, timeout 0.821, resource 0.960, latency 0.657 | | 2.80e-72 | 1.68e-71 | True |
| H5 | FAR source_free 0.1060, source_free_deeplog 0.1377, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 2.12e-205 | 1.70e-204 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0170 | True | True | True |
| transfer_openstack | -0.4524 | True | True | True |
| transfer_similar | -0.0659 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8224, source_free_forest 0.7014, novelty_gate 0.7808; of 4155 alarms of the combined detector, 886 come from the gate only, 794 from the forest only, 2475 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (90): false-alarm rate source_free 0.8556, source_free_deeplog 0.6333, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.8556, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (1551): false-alarm rate source_free 0.0625, source_free_deeplog 0.1090, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0625, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (540 fault windows): recall source_free 0.439, source_free_deeplog 0.665, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.043, threshold 0.000, source_free_forest 0.439, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (539 fault windows): recall source_free 0.412, source_free_deeplog 0.649, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.041, threshold 0.000, source_free_forest 0.412, novelty_gate 0.000, source_free_source_features 0.000
