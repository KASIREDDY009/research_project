# Evaluation runs (9)

| Run | Injections per category | Fault episodes (silent) | Windows (fault windows) | F1 source_free | F1 source_free_deeplog | F1 transfer | F1 transfer_openstack | F1 transfer_similar | F1 threshold | F1 source_free_forest | F1 novelty_gate | F1 source_free_source_features | Forfeiture f1:transfer-source_free | Forfeiture f1:transfer-source_free_deeplog | Forfeiture mcc:transfer-source_free | Forfeiture mcc:transfer-source_free_deeplog | Forfeiture f1:transfer_openstack-source_free | Forfeiture f1:transfer_openstack-source_free_deeplog | Forfeiture mcc:transfer_openstack-source_free | Forfeiture mcc:transfer_openstack-source_free_deeplog | Forfeiture f1:transfer_similar-source_free | Forfeiture f1:transfer_similar-source_free_deeplog | Forfeiture mcc:transfer_similar-source_free | Forfeiture mcc:transfer_similar-source_free_deeplog | Forfeiture f1:transfer-source_free_source_features | Forfeiture mcc:transfer-source_free_source_features |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| run1/bookings | 60 | 300 (1) | 1494 (448) | 0.8255 | 0.8358 | 0.7892 | 0.4736 | 0.7892 | 0.3620 | 0.7353 | 0.7892 | 0.7892 | -0.0363 | -0.0466 | -0.0261 | -0.0124 | -0.3519 | -0.3622 | -0.2898 | -0.2761 | -0.0363 | -0.0466 | -0.0261 | -0.0124 | 0.0000 | 0.0000 |
| run2/bookings | 60 | 300 (0) | 1494 (439) | 0.8213 | 0.7943 | 0.8199 | 0.5068 | 0.8199 | 0.3496 | 0.2146 | 0.8188 | 0.8199 | -0.0014 | 0.0256 | 0.0012 | 0.0485 | -0.3145 | -0.2875 | -0.2680 | -0.2206 | -0.0014 | 0.0256 | 0.0012 | 0.0485 | 0.0000 | 0.0000 |
| run3/bookings | 60 | 300 (0) | 1493 (442) | 0.8181 | 0.8183 | 0.8182 | 0.5093 | 0.8475 | 0.3352 | 0.5760 | 0.8182 | 0.8182 | 0.0001 | -0.0001 | 0.0028 | 0.0177 | -0.3088 | -0.3090 | -0.2629 | -0.2480 | 0.0294 | 0.0292 | 0.0333 | 0.0481 | 0.0000 | 0.0000 |
| run4/bookings | 60 | 300 (1) | 1493 (445) | 0.8148 | 0.8210 | 0.8091 | 0.5067 | 0.8038 | 0.3457 | 0.3986 | 0.8096 | 0.8091 | -0.0057 | -0.0119 | -0.0040 | -0.0002 | -0.3081 | -0.3143 | -0.2616 | -0.2578 | -0.0111 | -0.0172 | -0.0084 | -0.0046 | 0.0000 | 0.0000 |
| run5/bookings | 60 | 300 (0) | 1492 (444) | 0.8223 | 0.7786 | 0.8022 | 0.4975 | 0.8005 | 0.3525 | 0.6889 | 0.8022 | 0.8022 | -0.0202 | 0.0235 | -0.0130 | 0.0452 | -0.3248 | -0.2812 | -0.2706 | -0.2124 | -0.0218 | 0.0219 | -0.0147 | 0.0436 | 0.0000 | 0.0000 |
| run6/bookings | 60 | 300 (1) | 1495 (435) | 0.8169 | 0.8729 | 0.8115 | 0.4974 | 0.8211 | 0.3647 | 0.4288 | 0.8093 | 0.8115 | -0.0054 | -0.0614 | 0.0062 | -0.0432 | -0.3195 | -0.3754 | -0.2614 | -0.3108 | 0.0043 | -0.0517 | 0.0160 | -0.0334 | 0.0000 | 0.0000 |
| run7/bookings | 60 | 300 (0) | 1493 (437) | 0.8528 | 0.8648 | 0.8253 | 0.5009 | 0.8560 | 0.3540 | 0.6891 | 0.8242 | 0.8253 | -0.0275 | -0.0395 | -0.0212 | -0.0165 | -0.3519 | -0.3639 | -0.3003 | -0.2957 | 0.0033 | -0.0088 | 0.0111 | 0.0158 | 0.0000 | 0.0000 |
| run8/bookings | 60 | 300 (0) | 1493 (438) | 0.8338 | 0.7979 | 0.8130 | 0.5051 | 0.8130 | 0.3626 | 0.6910 | 0.8130 | 0.8130 | -0.0208 | 0.0151 | -0.0127 | 0.0303 | -0.3286 | -0.2928 | -0.2762 | -0.2332 | -0.0208 | 0.0151 | -0.0127 | 0.0303 | 0.0000 | 0.0000 |
| run9/bookings | 60 | 300 (0) | 1495 (437) | 0.8391 | 0.8514 | 0.8189 | 0.5111 | 0.8347 | 0.3478 | 0.6823 | 0.8178 | 0.8189 | -0.0202 | -0.0325 | -0.0106 | -0.0039 | -0.3281 | -0.3403 | -0.2755 | -0.2688 | -0.0045 | -0.0167 | 0.0056 | 0.0123 | 0.0000 | 0.0000 |

## Over the runs

### source_free

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 0.9725 | 0.0140 | 0.9568 | 0.9904 | 9 | 0 |
| recall | 0.7201 | 0.0233 | 0.6921 | 0.7620 | 9 | 0 |
| f1 | 0.8272 | 0.0125 | 0.8148 | 0.8528 | 9 | 0 |
| mcc | 0.7853 | 0.0125 | 0.7711 | 0.8121 | 9 | 0 |
| false_alarm_rate | 0.0086 | 0.0045 | 0.0028 | 0.0132 | 9 | 0 |

### source_free_deeplog

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 0.8953 | 0.0492 | 0.8319 | 0.9525 | 9 | 0 |
| recall | 0.7756 | 0.0893 | 0.6734 | 0.8856 | 9 | 0 |
| f1 | 0.8261 | 0.0327 | 0.7786 | 0.8729 | 9 | 0 |
| mcc | 0.7694 | 0.0324 | 0.7203 | 0.8204 | 9 | 0 |
| false_alarm_rate | 0.0407 | 0.0247 | 0.0153 | 0.0728 | 9 | 0 |

### transfer

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 0.9993 | 0.0015 | 0.9967 | 1.0000 | 9 | 0 |
| recall | 0.6838 | 0.0151 | 0.6518 | 0.7025 | 9 | 0 |
| f1 | 0.8119 | 0.0109 | 0.7892 | 0.8253 | 9 | 0 |
| mcc | 0.7767 | 0.0116 | 0.7531 | 0.7909 | 9 | 0 |
| false_alarm_rate | 0.0002 | 0.0004 | 0.0000 | 0.0010 | 9 | 0 |

### transfer_openstack

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 9 | 0 |
| recall | 0.3342 | 0.0100 | 0.3103 | 0.3432 | 9 | 0 |
| f1 | 0.5009 | 0.0113 | 0.4736 | 0.5111 | 9 | 0 |
| mcc | 0.5112 | 0.0090 | 0.4894 | 0.5196 | 9 | 0 |
| false_alarm_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 9 | 0 |

### transfer_similar

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 0.9996 | 0.0011 | 0.9966 | 1.0000 | 9 | 0 |
| recall | 0.6965 | 0.0318 | 0.6518 | 0.7483 | 9 | 0 |
| f1 | 0.8206 | 0.0221 | 0.7892 | 0.8560 | 9 | 0 |
| mcc | 0.7859 | 0.0232 | 0.7531 | 0.8232 | 9 | 0 |
| false_alarm_rate | 0.0001 | 0.0003 | 0.0000 | 0.0010 | 9 | 0 |

### threshold

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 9 | 0 |
| recall | 0.2141 | 0.0070 | 0.2014 | 0.2230 | 9 | 0 |
| f1 | 0.3527 | 0.0095 | 0.3352 | 0.3647 | 9 | 0 |
| mcc | 0.4014 | 0.0072 | 0.3882 | 0.4112 | 9 | 0 |
| false_alarm_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 9 | 0 |

### source_free_forest

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 0.9587 | 0.0229 | 0.9104 | 0.9911 | 9 | 0 |
| recall | 0.4227 | 0.1676 | 0.1207 | 0.5982 | 9 | 0 |
| f1 | 0.5672 | 0.1798 | 0.2146 | 0.7353 | 9 | 0 |
| mcc | 0.5536 | 0.1387 | 0.2875 | 0.6868 | 9 | 0 |
| false_alarm_rate | 0.0078 | 0.0046 | 0.0010 | 0.0124 | 9 | 0 |

### novelty_gate

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 0.9971 | 0.0026 | 0.9933 | 1.0000 | 9 | 0 |
| recall | 0.6841 | 0.0151 | 0.6518 | 0.7025 | 9 | 0 |
| f1 | 0.8114 | 0.0106 | 0.7892 | 0.8242 | 9 | 0 |
| mcc | 0.7755 | 0.0110 | 0.7531 | 0.7889 | 9 | 0 |
| false_alarm_rate | 0.0008 | 0.0007 | 0.0000 | 0.0019 | 9 | 0 |

### source_free_source_features

| Metric | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| precision | 0.9993 | 0.0015 | 0.9967 | 1.0000 | 9 | 0 |
| recall | 0.6838 | 0.0151 | 0.6518 | 0.7025 | 9 | 0 |
| f1 | 0.8119 | 0.0109 | 0.7892 | 0.8253 | 9 | 0 |
| mcc | 0.7767 | 0.0116 | 0.7531 | 0.7909 | 9 | 0 |
| false_alarm_rate | 0.0002 | 0.0004 | 0.0000 | 0.0010 | 9 | 0 |

### Forfeiture (baseline minus source-free)

| Key | mean | std | min | max | n | undefined |
|---|---:|---:|---:|---:|---:|---:|
| f1:transfer-source_free | -0.0153 | 0.0127 | -0.0363 | 0.0001 | 9 | 0 |
| f1:transfer-source_free_deeplog | -0.0142 | 0.0322 | -0.0614 | 0.0256 | 9 | 0 |
| mcc:transfer-source_free | -0.0086 | 0.0110 | -0.0261 | 0.0062 | 9 | 0 |
| mcc:transfer-source_free_deeplog | 0.0073 | 0.0305 | -0.0432 | 0.0485 | 9 | 0 |
| f1:transfer_openstack-source_free | -0.3262 | 0.0164 | -0.3519 | -0.3081 | 9 | 0 |
| f1:transfer_openstack-source_free_deeplog | -0.3252 | 0.0361 | -0.3754 | -0.2812 | 9 | 0 |
| mcc:transfer_openstack-source_free | -0.2740 | 0.0134 | -0.3003 | -0.2614 | 9 | 0 |
| mcc:transfer_openstack-source_free_deeplog | -0.2581 | 0.0332 | -0.3108 | -0.2124 | 9 | 0 |
| f1:transfer_similar-source_free | -0.0065 | 0.0190 | -0.0363 | 0.0294 | 9 | 0 |
| f1:transfer_similar-source_free_deeplog | -0.0055 | 0.0305 | -0.0517 | 0.0292 | 9 | 0 |
| mcc:transfer_similar-source_free | 0.0006 | 0.0182 | -0.0261 | 0.0333 | 9 | 0 |
| mcc:transfer_similar-source_free_deeplog | 0.0165 | 0.0290 | -0.0334 | 0.0485 | 9 | 0 |
| f1:transfer-source_free_source_features | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 9 | 0 |
| mcc:transfer-source_free_source_features | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 9 | 0 |
