# Analysis of the pooled runs: run1/bookings, run2/bookings, run3/bookings, run4/bookings, run5/bookings, run6/bookings, run7/bookings, run8/bookings, run9/bookings

5374 windows pooled (3224 positive, 322 fault-free elasticity windows).

| Detector | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| source_free | 0.9755 | 0.7655 | 0.8578 | 0.7230 |
| source_free_deeplog | 0.9329 | 0.8325 | 0.8799 | 0.7296 |
| transfer | 1.0000 | 0.3033 | 0.4655 | 0.3852 |
| transfer_openstack | 1.0000 | 0.3685 | 0.5385 | 0.4350 |
| transfer_similar | 1.0000 | 0.8756 | 0.9337 | 0.8591 |
| threshold | 1.0000 | 0.3058 | 0.4684 | 0.3871 |
| source_free_forest | 0.9203 | 0.2041 | 0.3341 | 0.2562 |
| novelty_gate | 0.9979 | 0.7419 | 0.8511 | 0.7289 |
| source_free_source_features | 0.9996 | 0.7419 | 0.8517 | 0.7309 |

Detection delay over the fault segments (consecutive fault windows); a segment with no alarm has no delay.

| Detector | Segments detected | Mean delay (windows) | Median delay (s) | Mean delay (s) |
|---|---:|---:|---:|---:|
| source_free | 1571 of 1818 | 0.07 | 0.0 | 0.9 |
| source_free_deeplog | 1667 of 1818 | 0.04 | 0.0 | 0.7 |
| transfer | 852 of 1818 | 0.45 | 0.0 | 4.9 |
| transfer_openstack | 893 of 1818 | 0.43 | 0.0 | 4.8 |
| transfer_similar | 1794 of 1818 | 0.00 | 0.0 | 0.0 |
| threshold | 858 of 1818 | 0.45 | 0.0 | 4.9 |
| source_free_forest | 521 of 1818 | 0.13 | 0.0 | 2.1 |
| novelty_gate | 1527 of 1818 | 0.08 | 0.0 | 1.1 |
| source_free_source_features | 1527 of 1818 | 0.08 | 0.0 | 1.1 |

## Against source_free

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.3923 | [-0.4096, -0.3753] | 0.00e+00 | 0.00e+00 | True |
| H2 | -0.3193 | [-0.3354, -0.3025] | 1.39e-296 | 8.31e-296 | True |
| H3 | +0.0758 | [+0.0679, +0.0840] | 4.36e-97 | 1.31e-96 | True |
| H6 | +0.4682 | [+0.4491, +0.4857] | 0.00e+00 | 0.00e+00 | True |
| H1 (fault segments) | detected transfer 852/source_free 1571 of 1818 | | 7.25e-217 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 893/source_free 1571 of 1818 | | 1.59e-204 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 1794/source_free 1571 of 1818 | | 2.40e-64 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.905, config 0.923, timeout 0.926, resource 0.989, latency 0.102 | | 0.00e+00 | 0.00e+00 | True |
| H5 | FAR source_free 0.0839, source_free_deeplog 0.2453, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 7.08e-66 | 1.42e-65 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.3779 | True | True | True |
| transfer_openstack | -0.3054 | True | True | True |
| transfer_similar | +0.0826 | True | True | True |

## Against source_free_deeplog

| Hypothesis | Effect | 95% interval | p | Holm-adjusted p | Rejected |
|---|---:|---|---:|---:|---|
| H1 | -0.4144 | [-0.4335, -0.3959] | 1.69e-302 | 1.18e-301 | True |
| H2 | -0.3413 | [-0.3582, -0.3253] | 1.15e-249 | 5.76e-249 | True |
| H3 | +0.0538 | [+0.0457, +0.0616] | 9.76e-48 | 9.76e-48 | True |
| H6 | +0.4682 | [+0.4491, +0.4857] | 0.00e+00 | 0.00e+00 | True |
| H1 (fault segments) | detected transfer 852/source_free_deeplog 1667 of 1818 | | 9.15e-246 | *(supplementary, not Holm-adjusted)* | |
| H2 (fault segments) | detected transfer_openstack 893/source_free_deeplog 1667 of 1818 | | 2.01e-233 | *(supplementary, not Holm-adjusted)* | |
| H3 (fault segments) | detected transfer_similar 1794/source_free_deeplog 1667 of 1818 | | 1.43e-31 | *(supplementary, not Holm-adjusted)* | |
| H4 | recall permission 0.929, config 0.938, timeout 0.931, resource 0.983, latency 0.394 | | 6.86e-248 | 2.74e-247 | True |
| H5 | FAR source_free 0.0839, source_free_deeplog 0.2453, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000 | | 7.08e-66 | 1.42e-65 | True |

Non-inferiority (upper one-sided 95% bound of the forfeiture below 0.1) and viability (also above the threshold alarms' F1):

| Baseline | Upper bound | Non-inferior | Above threshold alarms | Viable substitute |
|---|---:|---|---|---|
| transfer | -0.3987 | True | True | True |
| transfer_openstack | -0.3276 | True | True | True |
| transfer_similar | +0.0604 | True | True | True |

## Supplementary (not Holm-adjusted)

- Novelty gate: F1 source_free 0.8578, source_free_forest 0.3341, novelty_gate 0.8511; of 2530 alarms of the combined detector, 1815 come from the gate only, 133 from the forest only, 582 from both.
- Feature space: BGL-trained baseline minus the source-free detector on its features -0.3862 [-0.4030, -0.3694].
- Elasticity windows with new environment (64): false-alarm rate source_free 0.2969, source_free_deeplog 0.7656, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.2969, novelty_gate 0.0000, source_free_source_features 0.0000
- Elasticity windows without new environment (258): false-alarm rate source_free 0.0310, source_free_deeplog 0.1163, transfer 0.0000, transfer_openstack 0.0000, transfer_similar 0.0000, threshold 0.0000, source_free_forest 0.0271, novelty_gate 0.0039, source_free_source_features 0.0000
- Latency fault, 4000 ms delay (323 fault windows): recall source_free 0.099, source_free_deeplog 0.399, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.663, threshold 0.000, source_free_forest 0.099, novelty_gate 0.000, source_free_source_features 0.000
- Latency fault, 6000 ms delay (335 fault windows): recall source_free 0.104, source_free_deeplog 0.388, transfer 0.000, transfer_openstack 0.000, transfer_similar 0.609, threshold 0.000, source_free_forest 0.104, novelty_gate 0.003, source_free_source_features 0.003
