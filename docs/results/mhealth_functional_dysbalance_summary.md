# MHEALTH Functional Dysbalance Summary

Dieses Dokument fasst die MHEALTH-spezifische Erweiterung des Dysbalance-Frameworks zusammen. Ziel war es, MHEALTH nicht nur als zusätzlichen Activity-Recognition-Datensatz zu verwenden, sondern als externe multimodale Validierungsebene für erklärbare funktionale Dysbalance-Scores.

## Ausgangspunkt

MHEALTH wurde zuvor segment-sicher tensorisiert.

| Eigenschaft | Wert |
|---|---:|
| Subjects | 10 |
| Aktivitäten | 12 |
| Fenster | 2,555 |
| Kanäle | 23 |
| Sampling Rate | 50 Hz |
| Fensterlänge | 250 Samples / 5 Sekunden |
| Step Size | 125 Samples / 2.5 Sekunden |
| Missing Values | 0 |

Die Labels `1` bis `12` wurden verwendet. Label `0` wurde ausgeschlossen, da es nicht annotierte Übergangs- und Nullsegmente beschreibt.

## Feature Extraction

Für jedes Fenster wurden interpretierbare Bewegungsfeatures berechnet. Die Features orientieren sich an der bereits etablierten PAMAP2-Logik, sind jedoch an die Sensorstruktur von MHEALTH angepasst.

| Sensorgruppe | Kanäle |
|---|---:|
| Chest acceleration | 3 |
| Ankle acceleration | 3 |
| Ankle gyroscope | 3 |
| Ankle magnetometer | 3 |
| Arm acceleration | 3 |
| Arm gyroscope | 3 |
| Arm magnetometer | 3 |
| ECG lead 1 / lead 2 | 2 |

Die wichtigsten abgeleiteten Features sind:

| Feature | Interpretation |
|---|---|
| `chest_acc_rms` | mittlere Bewegungsenergie am Rumpf |
| `ankle_acc_rms` | mittlere Bewegungsenergie am Fußgelenk |
| `arm_acc_rms` | mittlere Bewegungsenergie am Arm |
| `total_acc_rms` | globale Beschleunigungsintensität |
| `log_extremity_chest_acc_ratio` | Verhältnis Extremitätenbewegung zu Rumpfbewegung |
| `log_arm_ankle_acc_ratio` | Verhältnis Arm- zu Beinbeschleunigung |
| `log_arm_ankle_gyro_ratio` | Verhältnis Arm- zu Beingyroskopie |
| `ecg_diff_rms` | konservative ECG-Signalabweichung zwischen beiden Leads |

ECG wird in diesem Abschnitt bewusst nicht klinisch interpretiert. Es dient nur als konservatives Zusatzsignal zur Charakterisierung von Signalabweichungen.

## Plausibilität der Movement Features

Die extrahierten Features zeigen erwartbare Aktivitätsunterschiede.

| Aktivität | Mean `total_acc_rms` |
|---|---:|
| standing_still | 5.6557 |
| sitting_relaxing | 5.6553 |
| lying_down | 5.6539 |
| walking | 6.7276 |
| jogging | 9.2130 |
| running | 10.8231 |
| jump_front_back | 9.0423 |

Die Werte zeigen, dass statische Aktivitäten niedrige globale Bewegungsintensitäten besitzen, während dynamische Aktivitäten wie `jogging`, `running` und `jump_front_back` deutlich höhere Werte erreichen.

Auch die Verhältnisfeatures sind plausibel:

- `running` zeigt den höchsten mittleren `log_extremity_chest_acc_ratio`.
- `walking` zeigt einen stark negativen mittleren `log_arm_ankle_acc_ratio`, was auf dominante Beinbewegung gegenüber Armbewegung hinweist.
- `cycling` zeigt einen erhöhten `log_arm_ankle_gyro_ratio`, was auf aktivitätsspezifische Rotationsmuster verweist.

Damit liefert MHEALTH nicht nur eine hohe Klassifikationsleistung, sondern auch erklärbare Bewegungsstruktur.

## Functional Dysbalance Score

Der MHEALTH Functional Dysbalance Score wurde analog zur bisherigen Framework-Logik berechnet.

Pipeline:

1. Feature Extraction pro Fenster
2. Z-Normalisierung pro `subject_id` und `label`
3. Berechnung absoluter Komponentenabweichungen
4. Aggregation zum funktionalen Abweichungsscore
5. optionale ergänzende ECG-Signalabweichung

Die Normalisierung pro Subject und Aktivität ist methodisch zentral. Der Score misst nicht, ob eine Aktivität allgemein intensiver ist als eine andere, sondern ob ein Fenster für dieselbe Person und dieselbe Aktivität ungewöhnlich ist.

Ein hoher Score bei `running` bedeutet nicht automatisch, dass Running intensiver als Standing ist. Er bedeutet, dass dieses Running-Fenster für diese Person im Kontext ihrer eigenen Running-Fenster auffällig ist.

## Verwendete Score-Komponenten

Die funktionale Score-Komponente basiert auf vier Bewegungsfeatures:

| Komponente |
|---|
| `total_acc_rms` |
| `log_extremity_chest_acc_ratio` |
| `log_arm_ankle_acc_ratio` |
| `log_arm_ankle_gyro_ratio` |

Zusätzlich wurde eine konservative ECG-Signalabweichung berechnet:

| Komponente |
|---|
| `ecg_diff_rms` |

Der kombinierte Score wurde als gewichtete Zusatzsicht berechnet:

    combined_movement_ecg_deviation_strength =
        0.85 * functional_deviation_strength
      + 0.15 * ecg_signal_deviation_strength

Die primäre Interpretation bleibt funktional-motorisch. ECG wird nur ergänzend betrachtet.

## Gesamtergebnisse

| Größe | Wert |
|---|---:|
| Scored windows | 2,555 |
| Score columns | 40 |
| Missing values | 0 |
| Mean functional deviation strength | 0.7953 |
| Std functional deviation strength | 0.3592 |
| Max functional deviation strength | 2.9800 |
| Mean combined movement ECG deviation strength | 0.7949 |
| Max combined movement ECG deviation strength | 2.7190 |

Die mittleren Scorewerte sind über Subjects und Aktivitäten ähnlich. Das ist erwartbar, da pro Subject und Aktivität z-normalisiert wurde. Die relevanten Informationen liegen daher vor allem in den oberen Abweichungsbereichen und in den Threshold-Raten.

## Subject-Level-Ergebnisse

| Subject | Windows | Mean functional strength | Max functional strength | % > 1.5 | % > 2.0 |
|---:|---:|---:|---:|---:|---:|
| 1 | 263 | 0.7933 | 2.7574 | 4.9430 | 0.7605 |
| 2 | 266 | 0.8081 | 1.9698 | 3.0075 | 0.0000 |
| 3 | 265 | 0.8006 | 2.1792 | 2.6415 | 0.3774 |
| 4 | 264 | 0.7854 | 2.7588 | 4.1667 | 0.7576 |
| 5 | 253 | 0.7890 | 2.3284 | 4.7431 | 0.3953 |
| 6 | 239 | 0.7798 | 2.1469 | 5.8577 | 1.2552 |
| 7 | 251 | 0.8080 | 1.9242 | 2.7888 | 0.0000 |
| 8 | 248 | 0.7863 | 2.9800 | 2.8226 | 1.2097 |
| 9 | 255 | 0.7988 | 2.3011 | 4.7059 | 0.3922 |
| 10 | 251 | 0.8028 | 1.9701 | 3.9841 | 0.0000 |

Besonders Subjects 6 und 8 zeigen bei Threshold `2.0` die höchsten funktionalen Abweichungsraten.

## Activity-Level-Ergebnisse

| Label | Activity | Windows | Mean functional strength | Max functional strength | % > 1.5 | % > 2.0 |
|---:|---|---:|---:|---:|---:|---:|
| 1 | standing_still | 230 | 0.7902 | 1.7955 | 3.4783 | 0.0000 |
| 2 | sitting_relaxing | 230 | 0.7942 | 1.8397 | 2.1739 | 0.0000 |
| 3 | lying_down | 230 | 0.8024 | 1.4594 | 0.0000 | 0.0000 |
| 4 | walking | 230 | 0.7987 | 2.3011 | 4.3478 | 0.4348 |
| 5 | climbing_stairs | 224 | 0.7886 | 2.7588 | 5.8036 | 0.8929 |
| 6 | waist_bends_forward | 211 | 0.8102 | 1.5271 | 0.4739 | 0.0000 |
| 7 | frontal_elevation_arms | 221 | 0.8034 | 2.1032 | 6.7873 | 1.3575 |
| 8 | knees_bending | 219 | 0.8057 | 2.3284 | 6.8493 | 0.9132 |
| 9 | cycling | 230 | 0.7907 | 2.1469 | 3.9130 | 0.4348 |
| 10 | jogging | 230 | 0.7771 | 2.9800 | 4.3478 | 0.4348 |
| 11 | running | 230 | 0.7915 | 2.1792 | 6.0870 | 1.3043 |
| 12 | jump_front_back | 70 | 0.7883 | 1.6063 | 1.4286 | 0.0000 |

Bei Threshold `2.0` treten funktionale Abweichungen nur selten auf. Die höchsten Raten zeigen `frontal_elevation_arms`, `running`, `knees_bending` und `climbing_stairs`.

## Dominante Komponenten

In den Top-50-Fenstern mit der höchsten funktionalen Abweichung verteilten sich die dominanten Komponenten wie folgt:

| Dominant component | Count |
|---|---:|
| `log_arm_ankle_acc_ratio` | 17 |
| `log_extremity_chest_acc_ratio` | 13 |
| `total_acc_rms` | 10 |
| `log_arm_ankle_gyro_ratio` | 10 |

Die Verteilung zeigt, dass der Score nicht nur globale Aktivitätsintensität misst. Stattdessen tragen mehrere erklärbare Bewegungsrelationen zur Abweichungsbewertung bei.

## Grafische Darstellung

Für die MHEALTH-Dysbalance-Auswertung wurden drei Abbildungen erzeugt:

| Datei | Inhalt |
|---|---|
| `reports/figures/mhealth_functional_deviation_by_activity.png` | Functional-Deviation-Verteilung je Aktivität |
| `reports/figures/mhealth_functional_deviation_by_subject.png` | Functional-Deviation-Verteilung je Subject |
| `reports/figures/mhealth_top_deviation_components.png` | dominante Komponenten der Top-Deviation-Fenster |

Diese Plots dienen als thesis-nahe Ergebnisgrafiken und unterstützen die Interpretation der Scoreverteilungen.

## Interpretation

MHEALTH erweitert das Dysbalance-Framework um eine externe multimodale Bewegungsvalidierung. Während PAMAP2 bereits eine funktional-motorische Dysbalance-Ebene etabliert und WESAD eine autonom-physiologische Ebene ergänzt, zeigt MHEALTH, dass die Score-Logik auch auf einem weiteren Sensorset mit Chest-, Arm-, Ankle- und ECG-Signalen funktioniert.

Die wichtigsten Befunde sind:

- Die Feature-Extraktion ist vollständig und frei von Missing Values.
- Die Bewegungsfeatures zeigen plausible Aktivitätsunterschiede.
- Die Dysbalance-Scores sind subject- und activity-normalisiert interpretierbar.
- Auffällige Fenster treten selten auf und konzentrieren sich auf plausible dynamische oder koordinativ anspruchsvolle Aktivitäten.
- Die dominanten Komponenten verteilen sich auf mehrere Bewegungsrelationen.

Damit unterstützt MHEALTH die Generalisierbarkeit des Frameworks über Datensätze hinweg.

## Grenzen

Die Ergebnisse müssen vorsichtig interpretiert werden:

- MHEALTH ist ein kontrollierter Activity-Recognition-Datensatz.
- Die Daten bilden keine klinischen Dysbalancen ab.
- ECG wird nur als Signalabweichung verwendet, nicht medizinisch interpretiert.
- Die Scores markieren relative Auffälligkeiten innerhalb von Subject-Activity-Kontexten.
- Label `12` besitzt mit 70 Fenstern deutlich weniger Samples als die übrigen Aktivitäten.
- Es handelt sich nicht um echte longitudinale Beobachtung.

## Zwischenfazit

MHEALTH bestätigt, dass das Dysbalance-Framework auf einen weiteren multimodalen Biosignal-Datensatz übertragbar ist. Die Kombination aus interpretierbaren Bewegungsfeatures, subject- und activity-normalisierten Scores, Threshold-Auswertung und grafischer Darstellung macht MHEALTH zu einer wichtigen externen Validierungsebene des Frameworks.

Im aktuellen Stand liefert MHEALTH keine klinische Dysbalance-Erkennung, aber eine robuste, erklärbare und datensatzübergreifend anschlussfähige Modellierung funktionaler Bewegungsabweichungen.

## Modellbasierte Anomaly-Detection-Erweiterung

Zusätzlich zur expliziten Threshold-Auswertung wurde eine Isolation-Forest-basierte Anomaly-Detection auf den MHEALTH-Dysbalance-Scores berechnet. Ziel war es zu prüfen, ob die erklärbaren funktionalen Score-Abweichungen auch durch ein unsupervised Modell als auffällige Fenster erkannt werden.

Verwendete Feature-Sets:

| Feature Set | Inhalt |
|---|---|
| `score_level` | aggregierte funktionale, ECG- und kombinierte Scorewerte |
| `movement_component_level` | z-normalisierte funktionale Bewegungskomponenten |
| `movement_ecg_component_level` | Bewegungskomponenten plus z-normalisierte ECG-Signalabweichung |

Für jedes Feature-Set wurden drei Contamination-Level geprüft:

| Contamination | Erwarteter Anteil Modell-Anomalien |
|---:|---:|
| 0.02 | ca. 2 % |
| 0.05 | ca. 5 % |
| 0.10 | ca. 10 % |

Für alle Feature-Sets ergaben sich die erwarteten Modell-Anomalieraten:

| Contamination | Anomalies | Anteil |
|---:|---:|---:|
| 0.02 | 52 / 2,555 | 2.035 % |
| 0.05 | 128 / 2,555 | 5.010 % |
| 0.10 | 256 / 2,555 | 10.020 % |

Die folgenden Detailwerte beziehen sich auf das zentrale Feature-Set `movement_component_level` bei `contamination = 0.05`.

## Activity-Level-Anomaly-Raten

| Activity | Anomaly rate |
|---|---:|
| knees_bending | 6.8493 % |
| climbing_stairs | 6.6964 % |
| walking | 5.6522 % |
| jogging | 5.6522 % |
| running | 5.6522 % |
| cycling | 5.6522 % |
| frontal_elevation_arms | 5.4299 % |
| standing_still | 4.3478 % |
| waist_bends_forward | 4.2654 % |
| sitting_relaxing | 3.9130 % |
| lying_down | 2.1739 % |
| jump_front_back | 1.4286 % |

Die höchsten modellbasierten Auffälligkeitsraten treten vor allem bei koordinativ oder dynamisch anspruchsvolleren Aktivitäten auf.

## Subject-Level-Anomaly-Raten

| Subject | Anomaly rate |
|---:|---:|
| 6 | 7.5314 % |
| 1 | 6.8441 % |
| 5 | 6.7194 % |
| 9 | 6.2745 % |
| 8 | 5.2419 % |
| 4 | 4.5455 % |
| 10 | 4.3825 % |
| 3 | 3.3962 % |
| 2 | 3.0075 % |
| 7 | 2.3904 % |

Die Subject-Level-Ergebnisse zeigen, dass das Modell nicht alle Personen gleich stark als auffällig bewertet.

## Threshold-Overlap

Der Vergleich zwischen explizitem Functional-Dysbalance-Threshold und Isolation Forest zeigt:

| Threshold | Model anomalies | Threshold anomalies | Overlap | Model overlap | Threshold overlap | Jaccard |
|---:|---:|---:|---:|---:|---:|---:|
| 1.5 | 128 | 101 | 94 | 73.4375 % | 93.0693 % | 0.6963 |
| 2.0 | 128 | 13 | 13 | 10.1563 % | 100.0000 % | 0.1016 |
| 2.5 | 128 | 3 | 3 | 2.3438 % | 100.0000 % | 0.0234 |
| 3.0 | 128 | 0 | 0 | 0.0000 % | 0.0000 % | 0.0000 |

Besonders relevant ist `θ = 2.0`: Alle 13 expliziten Functional-Dysbalance-Fenster werden vom Isolation Forest erkannt. Das bedeutet, dass die stärksten erklärbaren funktionalen Abweichungen auch modellbasiert als auffällig erscheinen.

## Korrelation zwischen Score und Anomaly Score

Für `movement_component_level` und `contamination = 0.05` ergaben sich folgende Korrelationen:

| Target | Pearson | Spearman |
|---|---:|---:|
| `functional_deviation_strength` | 0.9384 | 0.9335 |
| `ecg_signal_deviation_strength` | 0.0577 | 0.0512 |
| `combined_movement_ecg_deviation_strength` | 0.9035 | 0.8967 |

Die sehr hohe Korrelation zwischen `functional_deviation_strength` und modellbasiertem `anomaly_score` zeigt, dass die erklärbare funktionale Score-Logik stark mit der unsupervised Modellperspektive übereinstimmt.

Die sehr geringe Korrelation zur isolierten ECG-Signalabweichung ist ebenfalls plausibel: Die zentrale MHEALTH-Anomaly-Struktur ist hier funktional-motorisch geprägt, nicht ECG-dominiert. Das stützt die konservative Entscheidung, ECG nur als Zusatzsignal und nicht als klinische Bewertungsgrundlage zu verwenden.

## Interpretation der Anomaly-Erweiterung

Die MHEALTH-Anomaly-Erweiterung stärkt die Generalisierbarkeit des Frameworks. Sie zeigt, dass funktionale Dysbalance nicht nur durch explizite Thresholds beschrieben werden kann, sondern auch durch ein unsupervised Modell auf den z-normalisierten Bewegungskomponenten wiedergefunden wird.

Damit ergibt sich für MHEALTH eine ähnliche Struktur wie zuvor bei PAMAP2:

- erklärbare funktionale Score-Komponenten
- seltene, plausible Threshold-Auffälligkeiten
- starke Übereinstimmung mit modellbasierter Anomaly-Detection
- interpretierbare dominante Bewegungsrelationen

MHEALTH bestätigt damit die Übertragbarkeit der funktionalen Dysbalance-Logik auf ein weiteres multimodales Sensorset.
