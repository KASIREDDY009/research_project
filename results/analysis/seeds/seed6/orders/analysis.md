# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9593 | 0.7433 | 0.8376 | 0.7928 |
| source_free_deeplog | 0.8727 | 0.8705 | 0.8716 | 0.8179 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | nan | 0.0000 | 0.0000 | nan |
| transfer_similar | 0.9976 | 0.7337 | 0.8455 | 0.8109 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9401 | 0.4666 | 0.6237 | 0.5858 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2323 of 2701 | 0.14 | 0.0 | 1.6 |
| source_free_deeplog | 2700 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 0 of 2701 | n/a | n/a | n/a |
| transfer_similar | 2294 of 2701 | 0.13 | 0.0 | 1.5 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1798 of 2701 | 0.23 | 0.0 | 3.0 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0157 | [-0.0207, -0.0107] | 0.001 | 0.002 | True |
| H2 | -0.8376 | [-0.8463, -0.8281] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0079 | [+0.0019, +0.0139] | 8.07e-05 | 2.42e-04 | True |
| H6 | +0.0236 | [+0.0194, +0.0281] | 3.03e-29 | 1.52e-28 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2323 of 2701 | | 1.71e-49 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free 2323 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2294/source_free 2323 of 2701 | | 0.062 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.836, config 0.842, timeout 0.880, resource 0.978, latency 0.200 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0760, source_free_deeplog 0.1679, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0061, threshold 0.0000 | | 1.82e-107 | 1.27e-106 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0115 | True | True | True |
| transfer_openstack | -0.8299 | True | True | True |
| transfer_similar | +0.0131 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0497 | [-0.0592, -0.0396] | 1.18e-07 | 4.71e-07 | True |
| H2 | -0.8716 | [-0.8795, -0.8634] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0261 | [-0.0350, -0.0171] | 0.175 | 0.175 | False |
| H6 | +0.0236 | [+0.0194, +0.0281] | 3.03e-29 | 1.52e-28 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2700 of 2701 | | 5.56e-163 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free_deeplog 2700 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2294/source_free_deeplog 2700 of 2701 | | 1.21e-122 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.872, config 0.863, timeout 0.891, resource 0.975, latency 0.755 | | 2.15e-37 | 1.29e-36 | True |
| H5 | FAR source_free 0.0760, source_free_deeplog 0.1679, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0061, threshold 0.0000 | | 1.82e-107 | 1.27e-106 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0412 | True | True | True |
| transfer_openstack | -0.8647 | True | True | True |
| transfer_similar | -0.0187 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8376, source_free_forest 0.6237, novelty_gate 0.8218; of 3075 alarms of the combined detector, 1105 come from the gate only, 295 from the forest only, 1675 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.5641, source_free_deeplog 0.6667, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0641, threshold 0.0000, source_free_forest 0.5641, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0244, source_free_deeplog 0.1152, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0244, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.205, source_free_deeplog 0.749, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.173, threshold 0.000, source_free_forest 0.205, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.195, source_free_deeplog 0.760, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.168, threshold 0.000, source_free_forest 0.195, novelty_gate 0.000, source_free_source_features 0.000
