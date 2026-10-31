# Analysis of the pooled runs: run7/orders, run8/orders, run9/orders

4476 windows pooled (1307 positive, 273 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9566 | 0.7590 | 0.8464 | 0.8027 |
| source_free_deeplog | 0.8460 | 0.8914 | 0.8681 | 0.8122 |
| transfer | 0.9989 | 0.7070 | 0.8280 | 0.7935 |
| transfer_openstack | 1.0000 | 0.3412 | 0.5088 | 0.5180 |
| transfer_similar | 1.0000 | 0.7643 | 0.8664 | 0.8346 |
| threshold | 1.0000 | 0.2127 | 0.3508 | 0.4007 |
| source_free_forest | 0.9432 | 0.5340 | 0.6820 | 0.6374 |
| novelty_gate | 0.9968 | 0.7070 | 0.8272 | 0.7922 |
| source_free_source_features | 0.9989 | 0.7070 | 0.8280 | 0.7935 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 787 of 900 | 0.14 | 0.0 | 1.8 |
| source_free_deeplog | 900 of 900 | 0.16 | 0.0 | 2.1 |
| transfer | 720 of 900 | 0.11 | 0.0 | 1.4 |
| transfer_openstack | 362 of 900 | 0.14 | 0.0 | 0.9 |
| transfer_similar | 795 of 900 | 0.13 | 0.0 | 1.6 |
| threshold | 278 of 900 | 0.18 | 0.0 | 1.2 |
| source_free_forest | 684 of 900 | 0.25 | 0.0 | 3.7 |
| novelty_gate | 720 of 900 | 0.11 | 0.0 | 1.4 |
| source_free_source_features | 720 of 900 | 0.11 | 0.0 | 1.4 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0185 | [-0.0283, -0.0097] | 0.029 | 0.067 | False |
| H2 | -0.3376 | [-0.3657, -0.3113] | 2.12e-110 | 2.12e-109 | True |
| H3 | +0.0200 | [+0.0102, +0.0296] | 3.39e-06 | 1.36e-05 | True |
| H6 | +0.0385 | [+0.0298, +0.0474] | 5.23e-22 | 3.14e-21 | True |
| H1 (fault segments) | detected transfer 720/source_free 787 of 900 | | 1.36e-20 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 362/source_free 787 of 900 | | 2.31e-128 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 795/source_free 787 of 900 | | 0.428 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.845, config 0.841, timeout 0.902, resource 0.970, latency 0.251 | | 1.30e-104 | 1.17e-103 | True |
| H5 | FAR source_free 0.0806, source_free_deeplog 0.1795, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.26e-39 | 8.80e-39 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0110 | True | True | True |
| transfer_openstack | -0.3157 | True | True | True |
| transfer_similar | +0.0279 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.0402 | [-0.0574, -0.0231] | 0.172 | 0.172 | False |
| H2 | -0.3593 | [-0.3883, -0.3309] | 4.05e-65 | 3.24e-64 | True |
| H3 | -0.0017 | [-0.0176, +0.0136] | 0.022 | 0.067 | False |
| H6 | +0.0385 | [+0.0298, +0.0474] | 5.23e-22 | 3.14e-21 | True |
| H1 (fault segments) | detected transfer 720/source_free_deeplog 900 of 900 | | 1.31e-54 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 362/source_free_deeplog 900 of 900 | | 2.22e-162 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 795/source_free_deeplog 900 of 900 | | 4.93e-32 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.905, config 0.905, timeout 0.911, resource 0.970, latency 0.768 | | 1.74e-12 | 8.72e-12 | True |
| H5 | FAR source_free 0.0806, source_free_deeplog 0.1795, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 1.26e-39 | 8.80e-39 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.0256 | True | True | True |
| transfer_openstack | -0.3361 | True | True | True |
| transfer_similar | +0.0111 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8464, source_free_forest 0.6820, novelty_gate 0.8272; of 1037 alarms of the combined detector, 297 come from the gate only, 110 from the forest only, 630 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features +0.0000 [+0.0000, +0.0000].
- Elasticity windows with new environment (26): false-alarm rate source_free 0.6538, source_free_deeplog 0.7692, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.6538, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (247): false-alarm rate source_free 0.0202, source_free_deeplog 0.1174, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0202, novelty_gate 0.0000, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (133 fault windows): recall source_free 0.263, source_free_deeplog 0.767, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.301, threshold 0.000, source_free_forest 0.263, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (134 fault windows): recall source_free 0.239, source_free_deeplog 0.769, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.269, threshold 0.000, source_free_forest 0.239, novelty_gate 0.000, source_free_source_features 0.000
