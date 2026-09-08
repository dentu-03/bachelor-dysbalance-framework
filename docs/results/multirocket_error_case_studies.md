# MultiRocket Error Case Studies

Dieses Dokument sammelt qualitative Fallbeispiele aus der MultiRocket-Experimentphase.

## Ziel

Die Case Studies sollen später im Ergebnisteil helfen, abstrakte Tabellenbefunde an konkreten Fenstern zu erklären.

Im Vordergrund steht die Frage, wann ein MultiRocket-Fehler nur eine plausible Klassenverwechslung ist und wann er zugleich mit Dysbalance Score, Anomaly Detection und Memory zusammenfällt.

## Auswahlprinzip

Für jeden Datensatz werden drei Typen von Fehlerfenstern gesammelt:

| Typ | Bedeutung |
|---|---|
| High-memory errors | Fehler mit Memory-Event, häufig thesis-relevant |
| High-score errors without memory | hohe Score-Auffälligkeit, aber nicht im Memory verdichtet |
| Low-score errors | eher Klassenähnlichkeit oder Modellgrenze statt Dysbalance |

## MHEALTH

Score-Spalte: `functional_deviation_strength`

### High-memory errors

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| jogging | 11 | 1.6301 | 0.0319 | subject_id=6; start_sample=53188; end_sample=53437 | ecg_signal_deviation_strength=1.224; combined_movement_ecg_deviation_strength=1.569; dominant_functional_component=log_extremity_chest_acc_ratio | model_anomaly | EP_000073 | HYP_000057 |
| jogging | 11 | 1.5118 | 0.0201 | subject_id=6; start_sample=50688; end_sample=50937 | ecg_signal_deviation_strength=0.772; combined_movement_ecg_deviation_strength=1.401; dominant_functional_component=log_arm_ankle_acc_ratio | model_anomaly | EP_000072 | HYP_000057 |

### High-score errors without memory

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| running | 10 | 1.3287 | -0.0278 | subject_id=2; start_sample=104680; end_sample=104929 | ecg_signal_deviation_strength=0.639; combined_movement_ecg_deviation_strength=1.225; dominant_functional_component=log_extremity_chest_acc_ratio | nan | nan | nan |
| jogging | 11 | 1.2449 | -0.0143 | subject_id=6; start_sample=52938; end_sample=53187 | ecg_signal_deviation_strength=0.728; combined_movement_ecg_deviation_strength=1.167; dominant_functional_component=log_arm_ankle_gyro_ratio | nan | nan | nan |
| jogging | 11 | 1.2074 | -0.0563 | subject_id=6; start_sample=53313; end_sample=53562 | ecg_signal_deviation_strength=2.752; combined_movement_ecg_deviation_strength=1.439; dominant_functional_component=total_acc_rms | nan | nan | nan |
| running | 10 | 1.1745 | -0.0545 | subject_id=2; start_sample=104305; end_sample=104554 | ecg_signal_deviation_strength=0.867; combined_movement_ecg_deviation_strength=1.128; dominant_functional_component=log_arm_ankle_gyro_ratio | nan | nan | nan |
| jogging | 11 | 1.1719 | -0.0469 | subject_id=1; start_sample=88314; end_sample=88563 | ecg_signal_deviation_strength=1.552; combined_movement_ecg_deviation_strength=1.229; dominant_functional_component=log_arm_ankle_gyro_ratio | nan | nan | nan |
| jogging | 11 | 1.1609 | -0.0730 | subject_id=6; start_sample=53063; end_sample=53312 | ecg_signal_deviation_strength=0.030; combined_movement_ecg_deviation_strength=0.991; dominant_functional_component=log_arm_ankle_gyro_ratio | nan | nan | nan |
| jogging | 11 | 1.0949 | -0.0868 | subject_id=1; start_sample=89689; end_sample=89938 | ecg_signal_deviation_strength=0.365; combined_movement_ecg_deviation_strength=0.985; dominant_functional_component=log_arm_ankle_acc_ratio | nan | nan | nan |
| running | 10 | 1.0939 | -0.0951 | subject_id=2; start_sample=104805; end_sample=105054 | ecg_signal_deviation_strength=0.729; combined_movement_ecg_deviation_strength=1.039; dominant_functional_component=total_acc_rms | nan | nan | nan |

### Low-score errors

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| running | 10 | 0.2102 | -0.1698 | subject_id=4; start_sample=108407; end_sample=108656 | ecg_signal_deviation_strength=0.759; combined_movement_ecg_deviation_strength=0.292; dominant_functional_component=total_acc_rms | nan | nan | nan |
| jogging | 11 | 0.2127 | -0.1694 | subject_id=1; start_sample=88689; end_sample=88938 | ecg_signal_deviation_strength=0.636; combined_movement_ecg_deviation_strength=0.276; dominant_functional_component=log_arm_ankle_gyro_ratio | nan | nan | nan |
| jogging | 11 | 0.2469 | -0.1632 | subject_id=6; start_sample=51438; end_sample=51687 | ecg_signal_deviation_strength=0.035; combined_movement_ecg_deviation_strength=0.215; dominant_functional_component=log_extremity_chest_acc_ratio | nan | nan | nan |
| jogging | 11 | 0.2662 | -0.1642 | subject_id=1; start_sample=88939; end_sample=89188 | ecg_signal_deviation_strength=0.830; combined_movement_ecg_deviation_strength=0.351; dominant_functional_component=log_extremity_chest_acc_ratio | nan | nan | nan |
| jogging | 11 | 0.2743 | -0.1619 | subject_id=1; start_sample=90689; end_sample=90938 | ecg_signal_deviation_strength=0.213; combined_movement_ecg_deviation_strength=0.265; dominant_functional_component=log_arm_ankle_acc_ratio | nan | nan | nan |
| jogging | 11 | 0.2997 | -0.1587 | subject_id=1; start_sample=89439; end_sample=89688 | ecg_signal_deviation_strength=0.306; combined_movement_ecg_deviation_strength=0.301; dominant_functional_component=log_arm_ankle_gyro_ratio | nan | nan | nan |
| running | 10 | 0.3458 | -0.1487 | subject_id=4; start_sample=108782; end_sample=109031 | ecg_signal_deviation_strength=1.368; combined_movement_ecg_deviation_strength=0.499; dominant_functional_component=log_arm_ankle_gyro_ratio | nan | nan | nan |
| running | 10 | 0.3714 | -0.1609 | subject_id=2; start_sample=103680; end_sample=103929 | ecg_signal_deviation_strength=0.804; combined_movement_ecg_deviation_strength=0.436; dominant_functional_component=log_arm_ankle_acc_ratio | nan | nan | nan |

## PAMAP2

Score-Spalte: `functional_deviation_strength`

### High-memory errors

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| walking | standing | 7.0692 | 0.7844 | subject_id=107; window_index=564; timestamp_start=2050.92; timestamp_end=2055.91 | z_total_acc_rms=-6.543; z_log_extremity_chest_acc_ratio=-7.385; z_log_hand_ankle_acc_ratio=7.280 | combined_score_model_event | EP_000309 | HYP_000201 |
| walking | sitting | 6.3029 | 0.7814 | subject_id=104; window_index=583; timestamp_start=2186.89; timestamp_end=2191.88 | z_total_acc_rms=-6.327; z_log_extremity_chest_acc_ratio=-6.610; z_log_hand_ankle_acc_ratio=5.972 | combined_score_model_event | EP_000217 | HYP_000149 |
| sitting | vacuum cleaning | 6.0468 | 0.7824 | subject_id=102; window_index=173; timestamp_start=554.66; timestamp_end=559.65 | z_total_acc_rms=5.772; z_log_extremity_chest_acc_ratio=6.062; z_log_hand_ankle_acc_ratio=6.306 | combined_score_model_event | EP_000163 | HYP_000119 |
| sitting | vacuum cleaning | 5.9980 | 0.7807 | subject_id=106; window_index=94; timestamp_start=393.64; timestamp_end=398.63 | z_total_acc_rms=6.605; z_log_extremity_chest_acc_ratio=6.309; z_log_hand_ankle_acc_ratio=-5.080 | combined_score_model_event | EP_000277 | HYP_000181 |
| lying | ascending stairs | 5.9611 | 0.7800 | subject_id=102; window_index=3; timestamp_start=62.7; timestamp_end=67.69 | z_total_acc_rms=6.294; z_log_extremity_chest_acc_ratio=6.381; z_log_hand_ankle_acc_ratio=-5.208 | combined_score_model_event | EP_000158 | HYP_000116 |
| Nordic walking | sitting | 5.8420 | 0.7738 | subject_id=106; window_index=704; timestamp_start=2646.3; timestamp_end=2651.29 | z_total_acc_rms=-5.821; z_log_extremity_chest_acc_ratio=-7.254; z_log_hand_ankle_acc_ratio=4.452 | combined_score_model_event | EP_000263 | HYP_000174 |
| walking | vacuum cleaning | 5.5688 | 0.7657 | subject_id=102; window_index=600; timestamp_start=2780.72; timestamp_end=2785.71 | z_total_acc_rms=-6.257; z_log_extremity_chest_acc_ratio=-6.757; z_log_hand_ankle_acc_ratio=3.693 | combined_score_model_event | EP_000167 | HYP_000122 |
| ironing | vacuum cleaning | 5.4627 | 0.7769 | subject_id=102; window_index=345; timestamp_start=1068.08; timestamp_end=1073.07 | z_total_acc_rms=5.276; z_log_extremity_chest_acc_ratio=5.552; z_log_hand_ankle_acc_ratio=5.560 | combined_score_model_event | EP_000157 | HYP_000115 |

### High-score errors without memory

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| vacuum cleaning | ironing | 1.9224 | 0.5754 | subject_id=103; window_index=466; timestamp_start=1488.02; timestamp_end=1493.01 | z_total_acc_rms=1.899; z_log_extremity_chest_acc_ratio=1.535; z_log_hand_ankle_acc_ratio=2.334 | nan | nan | nan |
| descending stairs | ascending stairs | 1.9035 | 0.5883 | subject_id=105; window_index=593; timestamp_start=1960.44; timestamp_end=1965.43 | z_total_acc_rms=-2.050; z_log_extremity_chest_acc_ratio=-1.907; z_log_hand_ankle_acc_ratio=1.753 | nan | nan | nan |
| standing | ironing | 1.8928 | 0.5771 | subject_id=106; window_index=227; timestamp_start=729.05; timestamp_end=734.04 | z_total_acc_rms=1.048; z_log_extremity_chest_acc_ratio=1.604; z_log_hand_ankle_acc_ratio=3.027 | nan | nan | nan |
| standing | sitting | 1.8633 | 0.5806 | subject_id=101; window_index=225; timestamp_start=609.33; timestamp_end=614.32 | z_total_acc_rms=1.955; z_log_extremity_chest_acc_ratio=2.276; z_log_hand_ankle_acc_ratio=1.359 | nan | nan | nan |
| sitting | ironing | 1.8343 | 0.5584 | subject_id=102; window_index=172; timestamp_start=552.16; timestamp_end=557.15 | z_total_acc_rms=1.478; z_log_extremity_chest_acc_ratio=1.977; z_log_hand_ankle_acc_ratio=2.048 | nan | nan | nan |
| descending stairs | walking | 1.7969 | 0.5821 | subject_id=102; window_index=510; timestamp_start=1923.75; timestamp_end=1928.74 | z_total_acc_rms=-2.080; z_log_extremity_chest_acc_ratio=-1.643; z_log_hand_ankle_acc_ratio=1.667 | nan | nan | nan |
| ascending stairs | descending stairs | 1.7570 | 0.5766 | subject_id=106; window_index=511; timestamp_start=1658.59; timestamp_end=1663.58 | z_total_acc_rms=-2.069; z_log_extremity_chest_acc_ratio=-1.448; z_log_hand_ankle_acc_ratio=1.755 | nan | nan | nan |
| ascending stairs | ironing | 1.7272 | 0.5746 | subject_id=103; window_index=549; timestamp_start=1896.2; timestamp_end=1901.19 | z_total_acc_rms=-2.014; z_log_extremity_chest_acc_ratio=-1.758; z_log_hand_ankle_acc_ratio=1.410 | nan | nan | nan |

### Low-score errors

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| standing | sitting | 0.0269 | 0.3576 | subject_id=103; window_index=226; timestamp_start=831.72; timestamp_end=836.71 | z_total_acc_rms=-0.015; z_log_extremity_chest_acc_ratio=0.060; z_log_hand_ankle_acc_ratio=0.006 | nan | nan | nan |
| Nordic walking | walking | 0.0397 | 0.3575 | subject_id=102; window_index=806; timestamp_start=3422.2; timestamp_end=3427.19 | z_total_acc_rms=-0.060; z_log_extremity_chest_acc_ratio=0.038; z_log_hand_ankle_acc_ratio=0.021 | nan | nan | nan |
| sitting | standing | 0.1163 | 0.3675 | subject_id=105; window_index=154; timestamp_start=563.53; timestamp_end=568.52 | z_total_acc_rms=0.259; z_log_extremity_chest_acc_ratio=-0.032; z_log_hand_ankle_acc_ratio=0.058 | nan | nan | nan |
| standing | sitting | 0.1228 | 0.3632 | subject_id=103; window_index=279; timestamp_start=964.22; timestamp_end=969.21 | z_total_acc_rms=0.188; z_log_extremity_chest_acc_ratio=0.140; z_log_hand_ankle_acc_ratio=0.040 | nan | nan | nan |
| standing | ironing | 0.1230 | 0.3549 | subject_id=105; window_index=219; timestamp_start=729.67; timestamp_end=734.66 | z_total_acc_rms=-0.211; z_log_extremity_chest_acc_ratio=-0.070; z_log_hand_ankle_acc_ratio=0.087 | nan | nan | nan |
| lying | standing | 0.1414 | 0.3619 | subject_id=104; window_index=90; timestamp_start=300.25; timestamp_end=305.24 | z_total_acc_rms=0.166; z_log_extremity_chest_acc_ratio=-0.166; z_log_hand_ankle_acc_ratio=-0.093 | nan | nan | nan |
| Nordic walking | walking | 0.1482 | 0.3623 | subject_id=102; window_index=812; timestamp_start=3437.2; timestamp_end=3442.19 | z_total_acc_rms=0.022; z_log_extremity_chest_acc_ratio=0.164; z_log_hand_ankle_acc_ratio=0.259 | nan | nan | nan |
| sitting | lying | 0.1548 | 0.3569 | subject_id=101; window_index=124; timestamp_start=352.03; timestamp_end=357.02 | z_total_acc_rms=-0.060; z_log_extremity_chest_acc_ratio=0.268; z_log_hand_ankle_acc_ratio=-0.137 | nan | nan | nan |

## WESAD

Score-Spalte: `autonomic_deviation_strength`

### High-memory errors

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| amusement | stress | 2.5707 | 0.6910 | subject_id=S14; window_index=462; start_sample=3069636; end_sample=3076635 | z_autonomic_activation=0.580; z_hr_bpm=0.764; z_eda_mean=1.007; z_resp_std=4.228; z_inverse_rmssd=-4.285 | combined_score_model_event | EP_000449 | HYP_000249 |
| meditation | baseline | 2.0649 | 0.6643 | subject_id=S17; window_index=517; start_sample=3681464; end_sample=3688463 | z_autonomic_activation=1.055; z_hr_bpm=-0.223; z_eda_mean=1.191; z_resp_std=4.297; z_inverse_rmssd=-2.549 | combined_score_model_event | EP_000545 | HYP_000274 |
| meditation | stress | 2.0080 | 0.6150 | subject_id=S15; window_index=521; start_sample=3278261; end_sample=3285260 | z_autonomic_activation=1.885; z_hr_bpm=1.531; z_eda_mean=1.493; z_resp_std=2.755; z_inverse_rmssd=-2.253 | combined_score_model_event | EP_000487 | HYP_000258 |
| meditation | baseline | 2.0001 | 0.6565 | subject_id=S17; window_index=518; start_sample=3684964; end_sample=3691963 | z_autonomic_activation=0.803; z_hr_bpm=0.342; z_eda_mean=1.240; z_resp_std=3.452; z_inverse_rmssd=-2.966 | combined_score_model_event | EP_000545 | HYP_000274 |
| meditation | baseline | 1.9329 | 0.6625 | subject_id=S15; window_index=594; start_sample=3533761; end_sample=3540760 | z_autonomic_activation=-2.405; z_hr_bpm=-2.131; z_eda_mean=1.617; z_resp_std=-0.364; z_inverse_rmssd=-3.620 | combined_score_model_event | EP_000491 | HYP_000258 |
| meditation | baseline | 1.6442 | 0.6116 | subject_id=S15; window_index=593; start_sample=3530261; end_sample=3537260 | z_autonomic_activation=-1.788; z_hr_bpm=-2.089; z_eda_mean=1.617; z_resp_std=-0.642; z_inverse_rmssd=-2.230 | combined_score_model_event | EP_000491 | HYP_000258 |
| amusement | stress | 1.6334 | 0.6195 | subject_id=S14; window_index=513; start_sample=3248136; end_sample=3255135 | z_autonomic_activation=2.072; z_hr_bpm=0.234; z_eda_mean=1.966; z_resp_std=4.127; z_inverse_rmssd=-0.207 | autonomic_activation;combined_score_model_event | EP_000429;EP_000450 | HYP_000246;HYP_000249 |
| meditation | amusement | 1.6089 | 0.6182 | subject_id=S13; window_index=586; start_sample=3698035; end_sample=3705034 | z_autonomic_activation=-1.726; z_hr_bpm=-1.086; z_eda_mean=0.455; z_resp_std=0.366; z_inverse_rmssd=-4.529 | combined_score_model_event | EP_000410 | HYP_000240 |

### High-score errors without memory

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| amusement | stress | 1.3056 | 0.5385 | subject_id=S13; window_index=260; start_sample=1252235; end_sample=1259234 | z_autonomic_activation=0.043; z_hr_bpm=0.663; z_eda_mean=-0.306; z_resp_std=2.008; z_inverse_rmssd=-2.246 | nan | nan | nan |
| baseline | stress | 1.2569 | 0.5610 | subject_id=S13; window_index=0; start_sample=61534; end_sample=68533 | z_autonomic_activation=-1.060; z_hr_bpm=0.821; z_eda_mean=-0.799; z_resp_std=0.221; z_inverse_rmssd=-3.187 | nan | nan | nan |
| amusement | stress | 1.2209 | 0.5584 | subject_id=S16; window_index=485; start_sample=3164259; end_sample=3171258 | z_autonomic_activation=1.613; z_hr_bpm=0.264; z_eda_mean=0.145; z_resp_std=3.600; z_inverse_rmssd=0.875 | nan | nan | nan |
| meditation | baseline | 1.2191 | 0.5557 | subject_id=S15; window_index=596; start_sample=3540761; end_sample=3547760 | z_autonomic_activation=-0.845; z_hr_bpm=-1.605; z_eda_mean=1.621; z_resp_std=0.027; z_inverse_rmssd=-1.623 | nan | nan | nan |
| amusement | stress | 1.2054 | 0.5430 | subject_id=S14; window_index=466; start_sample=3083636; end_sample=3090635 | z_autonomic_activation=1.476; z_hr_bpm=-0.231; z_eda_mean=1.056; z_resp_std=3.045; z_inverse_rmssd=0.490 | nan | nan | nan |
| baseline | meditation | 1.2025 | 0.5055 | subject_id=S14; window_index=127; start_sample=462837; end_sample=469836 | z_autonomic_activation=-1.629; z_hr_bpm=-0.783; z_eda_mean=-1.205; z_resp_std=-1.055; z_inverse_rmssd=-1.768 | nan | nan | nan |
| meditation | baseline | 1.2021 | 0.5387 | subject_id=S17; window_index=539; start_sample=3758464; end_sample=3765463 | z_autonomic_activation=1.064; z_hr_bpm=-0.418; z_eda_mean=1.121; z_resp_std=2.653; z_inverse_rmssd=-0.616 | nan | nan | nan |
| baseline | stress | 1.2016 | 0.5103 | subject_id=S13; window_index=2; start_sample=68534; end_sample=75533 | z_autonomic_activation=0.108; z_hr_bpm=0.924; z_eda_mean=-0.806; z_resp_std=1.629; z_inverse_rmssd=-1.448 | nan | nan | nan |

### Low-score errors

| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |
|---|---|---:|---:|---|---|---|---|---|
| amusement | stress | 0.0857 | 0.3856 | subject_id=S16; window_index=510; start_sample=3251759; end_sample=3258758 | z_autonomic_activation=0.104; z_hr_bpm=-0.001; z_eda_mean=0.130; z_resp_std=-0.012; z_inverse_rmssd=0.199 | nan | nan | nan |
| amusement | stress | 0.1283 | 0.3902 | subject_id=S16; window_index=448; start_sample=3034759; end_sample=3041758 | z_autonomic_activation=0.100; z_hr_bpm=-0.099; z_eda_mean=-0.007; z_resp_std=0.300; z_inverse_rmssd=0.108 | nan | nan | nan |
| meditation | stress | 0.1308 | 0.3822 | subject_id=S16; window_index=544; start_sample=3604559; end_sample=3611558 | z_autonomic_activation=-0.173; z_hr_bpm=-0.170; z_eda_mean=-0.050; z_resp_std=-0.271; z_inverse_rmssd=-0.032 | nan | nan | nan |
| meditation | stress | 0.1326 | 0.3826 | subject_id=S16; window_index=533; start_sample=3566059; end_sample=3573058 | z_autonomic_activation=-0.148; z_hr_bpm=-0.373; z_eda_mean=-0.015; z_resp_std=0.041; z_inverse_rmssd=-0.102 | nan | nan | nan |
| meditation | stress | 0.1459 | 0.3855 | subject_id=S16; window_index=528; start_sample=3548559; end_sample=3555558 | z_autonomic_activation=-0.193; z_hr_bpm=-0.155; z_eda_mean=-0.089; z_resp_std=-0.114; z_inverse_rmssd=-0.226 | nan | nan | nan |
| meditation | stress | 0.1520 | 0.3831 | subject_id=S16; window_index=529; start_sample=3552059; end_sample=3559058 | z_autonomic_activation=0.010; z_hr_bpm=-0.150; z_eda_mean=-0.094; z_resp_std=-0.045; z_inverse_rmssd=0.319 | nan | nan | nan |
| meditation | stress | 0.1545 | 0.3834 | subject_id=S16; window_index=370; start_sample=2606359; end_sample=2613358 | z_autonomic_activation=0.046; z_hr_bpm=-0.126; z_eda_mean=0.036; z_resp_std=-0.113; z_inverse_rmssd=0.343 | nan | nan | nan |
| amusement | stress | 0.1561 | 0.3811 | subject_id=S16; window_index=456; start_sample=3062759; end_sample=3069758 | z_autonomic_activation=-0.192; z_hr_bpm=-0.206; z_eda_mean=0.022; z_resp_std=-0.262; z_inverse_rmssd=-0.135 | nan | nan | nan |

## Interpretation

Die Case Studies unterstützen eine vorsichtige, domänenspezifische Lesart.

Bei PAMAP2 sind Fehler mit hoher funktionaler Dysbalance und Memory-Treffern besonders wichtig, weil sie zeigen, dass Modellunsicherheit, Score-Auffälligkeit und temporale Hypothesenbildung zusammenfallen können.

Bei MHEALTH und WESAD sind viele Fehler dagegen besser als Klassenähnlichkeit oder Zustandsüberlappung zu lesen. Das verhindert eine Überinterpretation von Modellfehlern.

## Thesis-Nutzung

Diese Fallbeispiele eignen sich später für:

- Ergebnisteil: exemplarische Fehleranalyse.
- Diskussion: Abgrenzung von Modellfehler, Dysbalance und physiologischer Interpretation.
- Methodik: Begründung der mehrschichtigen Framework-Architektur.

## Zwischenfazit

Die qualitative Fehleranalyse ergänzt die quantitativen MultiRocket-Ergebnisse. Sie macht sichtbar, dass der wissenschaftliche Mehrwert nicht allein in hoher Klassifikationsleistung liegt, sondern in der erklärbaren Einordnung von Modellunsicherheit.
