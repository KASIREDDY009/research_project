# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9692 | 0.7362 | 0.8368 | 0.7944 |
| source_free_deeplog | 0.8381 | 0.8660 | 0.8518 | 0.7884 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | nan | 0.0000 | 0.0000 | nan |
| transfer_similar | 0.9973 | 0.7455 | 0.8532 | 0.8191 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9431 | 0.3590 | 0.5201 | 0.5054 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2295 of 2701 | 0.14 | 0.0 | 1.6 |
| source_free_deeplog | 2669 of 2701 | 0.18 | 0.0 | 2.2 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 0 of 2701 | n/a | n/a | n/a |
| transfer_similar | 2354 of 2701 | 0.15 | 0.0 | 1.9 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1368 of 2701 | 0.23 | 0.0 | 3.5 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0149 | [-0.0197, -0.0106] | 1.03e-04 | 2.06e-04 | True |
| H2 | -0.8368 | [-0.8453, -0.8273] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0165 | [+0.0108, +0.0225] | 1.54e-10 | 6.16e-10 | True |
| H6 | +0.0313 | [+0.0265, +0.0365] | 6.39e-42 | 3.20e-41 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2295 of 2701 | | 4.59e-41 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free 2295 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2354/source_free 2295 of 2701 | | 2.65e-04 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.838, config 0.837, timeout 0.879, resource 0.976, latency 0.171 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0527, source_free_deeplog 0.1581, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0074, threshold 0.0000 | | 1.41e-104 | 9.84e-104 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0112 | True | True | True |
| transfer_openstack | -0.8289 | True | True | True |
| transfer_similar | +0.0214 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0299 | [-0.0395, -0.0199] | 0.913 | 0.913 | False |
| H2 | -0.8518 | [-0.8599, -0.8429] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0014 | [-0.0075, +0.0099] | 2.12e-07 | 6.35e-07 | True |
| H6 | +0.0313 | [+0.0265, +0.0365] | 6.39e-42 | 3.20e-41 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2669 of 2701 | | 1.19e-153 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 0/source_free_deeplog 2669 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2354/source_free_deeplog 2669 of 2701 | | 1.00e-81 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.890, config 0.893, timeout 0.902, resource 0.975, latency 0.676 | | 5.40e-75 | 3.24e-74 | True |
| H5 | FAR source_free 0.0527, source_free_deeplog 0.1581, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0074, threshold 0.0000 | | 1.41e-104 | 9.84e-104 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0214 | True | True | True |
| transfer_openstack | -0.8444 | True | True | True |
| transfer_similar | +0.0087 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8368, source_free_forest 0.5201, novelty_gate 0.8218; of 3015 alarms of the combined detector, 1504 come from the gate only, 235 from the forest only, 1276 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.3974, source_free_deeplog 0.7051, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0641, threshold 0.0000, source_free_forest 0.3974, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0163, source_free_deeplog 0.1003, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0014, threshold 0.0000, source_free_forest 0.0163, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.181, source_free_deeplog 0.675, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.236, threshold 0.000, source_free_forest 0.181, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.160, source_free_deeplog 0.677, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.245, threshold 0.000, source_free_forest 0.160, novelty_gate 0.000, source_free_source_features 0.000
