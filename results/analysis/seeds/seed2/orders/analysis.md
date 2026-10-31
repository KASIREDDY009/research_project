# Analysis of the pooled runs: run1/orders, run2/orders, run3/orders, run4/orders, run5/orders, run6/orders, run7/orders, run8/orders, run9/orders

13438 windows pooled (3969 positive, 816 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9645 | 0.7392 | 0.8370 | 0.7934 |
| source_free_deeplog | 0.8572 | 0.8559 | 0.8565 | 0.7965 |
| transfer | 0.9989 | 0.6982 | 0.8219 | 0.7866 |
| transfer_openstack | 1.0000 | 0.1343 | 0.2368 | 0.3139 |
| transfer_similar | 0.9986 | 0.7279 | 0.8420 | 0.8074 |
| threshold | 1.0000 | 0.2063 | 0.3421 | 0.3935 |
| source_free_forest | 0.9415 | 0.4097 | 0.5709 | 0.5439 |
| novelty_gate | 0.9975 | 0.6987 | 0.8218 | 0.7860 |
| source_free_source_features | 0.9989 | 0.6982 | 0.8219 | 0.7866 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 2304 of 2701 | 0.14 | 0.0 | 1.6 |
| source_free_deeplog | 2642 of 2701 | 0.17 | 0.0 | 2.1 |
| transfer | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| transfer_openstack | 268 of 2701 | 0.00 | 0.0 | 0.0 |
| transfer_similar | 2286 of 2701 | 0.14 | 0.0 | 1.7 |
| threshold | 819 of 2701 | 0.20 | 0.0 | 1.3 |
| source_free_forest | 1566 of 2701 | 0.21 | 0.0 | 3.1 |
| novelty_gate | 2160 of 2701 | 0.13 | 0.0 | 1.4 |
| source_free_source_features | 2160 of 2701 | 0.13 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0151 | [-0.0201, -0.0102] | 4.76e-04 | 0.002 | True |
| H2 | -0.6002 | [-0.6175, -0.5820] | 0.00e+00 | 0.00e+00 | True |
| H3 | +0.0051 | [-0.0009, +0.0109] | 0.003 | 0.009 | True |
| H6 | +0.0201 | [+0.0161, +0.0242] | 1.90e-25 | 9.52e-25 | True |
| H1 (fault segments) | detected transfer 2160/source_free 2304 of 2701 | | 8.97e-44 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 268/source_free 2304 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2286/source_free 2304 of 2701 | | 0.274 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.836, config 0.838, timeout 0.879, resource 0.976, latency 0.187 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0662, source_free_deeplog 0.1630, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0025, threshold 0.0000 | | 1.23e-108 | 8.61e-108 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0110 | True | True | True |
| transfer_openstack | -0.5852 | True | True | True |
| transfer_similar | +0.0101 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0346 | [-0.0439, -0.0245] | 0.072 | 0.144 | False |
| H2 | -0.6197 | [-0.6372, -0.6022] | 0.00e+00 | 0.00e+00 | True |
| H3 | -0.0145 | [-0.0232, -0.0058] | 0.110 | 0.144 | False |
| H6 | +0.0201 | [+0.0161, +0.0242] | 1.90e-25 | 9.52e-25 | True |
| H1 (fault segments) | detected transfer 2160/source_free_deeplog 2642 of 2701 | | 1.60e-145 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 268/source_free_deeplog 2642 of 2701 | | 0.00e+00 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 2286/source_free_deeplog 2642 of 2701 | | 5.53e-104 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.876, config 0.887, timeout 0.889, resource 0.975, latency 0.659 | | 1.96e-77 | 1.18e-76 | True |
| H5 | FAR source_free 0.0662, source_free_deeplog 0.1630, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0025, threshold 0.0000 | | 1.23e-108 | 8.61e-108 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0261 | True | True | True |
| transfer_openstack | -0.6048 | True | True | True |
| transfer_similar | -0.0070 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8370, source_free_forest 0.5709, novelty_gate 0.8218; of 3042 alarms of the combined detector, 1315 come from the gate only, 262 from the forest only, 1465 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (78): false-alarm rate source_free 0.5000, source_free_deeplog 0.7051, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0256, threshold 0.0000, source_free_forest 0.5000, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (738): false-alarm rate source_free 0.0203, source_free_deeplog 0.1057, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0203, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (415 fault windows): recall source_free 0.178, source_free_deeplog 0.655, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.157, threshold 0.000, source_free_forest 0.178, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (400 fault windows): recall source_free 0.195, source_free_deeplog 0.662, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.158, threshold 0.000, source_free_forest 0.195, novelty_gate 0.000, source_free_source_features 0.000
