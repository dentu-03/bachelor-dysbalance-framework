# Cross-Dataset Framework Summary

Dieses Dokument fasst den aktuellen datensatzübergreifenden Stand des Dysbalance-Frameworks zusammen. Der Fokus liegt nicht auf einem einzelnen Datensatz, sondern auf der Frage, ob dieselbe methodische Grundstruktur über unterschiedliche multimodale Biosignal-Domänen hinweg tragfähig bleibt.

## Purpose

Die zentrale Funktion dieses Dokuments ist die Integration der bisherigen Ergebnisblöcke:

- PAMAP2 als funktional-motorische Entwicklungsebene
- WESAD als autonom-physiologische Entwicklungsebene
- MHEALTH als externe multimodale Transfer- und Validierungsebene
- Score-Level Anomaly Detection als modellbasierte Zusatzperspektive
- Longitudinal Dysbalance Memory als Ereignis-, Episoden- und Hypothesenebene

Damit dient diese Datei als übergeordnete Ergebnisbrücke für die spätere Thesis-Struktur.

## Central Research Connection

Die zentrale Forschungsfrage lautet:

> Inwiefern lassen sich personalisierte physiologische Abweichungsmuster mithilfe eines multimodalen Dysbalance-Frameworks über verschiedene Biosignal-Datensätze hinweg erkennen, erklären und longitudinal verfolgen?

Die bisherigen Ergebnisse adressieren diese Frage in drei Schichten:

1. Erkennung: Klassifikations- und Anomaly-Baselines zeigen, dass die Daten strukturierte Muster enthalten.
2. Erklärung: Dysbalance-Scores zerlegen Auffälligkeiten in interpretierbare Komponenten.
3. Verfolgung: Das Longitudinal Dysbalance Memory aggregiert Fensterereignisse zu Episoden und Hypothesen.

## Dataset Roles

| Dataset | Rolle im Framework | Hauptdomäne | Aktueller Status |
|---|---|---|---|
| PAMAP2 | Entwicklung funktionaler Bewegungs-Dysbalance | Bewegung, Aktivität, Körpersegmente | vollständig integriert |
| WESAD | Entwicklung autonomer Dysbalance | Stress, autonome Regulation, Biosignale | vollständig integriert |
| MHEALTH | externe multimodale Transferprüfung | Chest-, Arm-, Ankle- und ECG-Signale | vollständig integriert |
| TILES | geplante longitudinale Erweiterung | Alltag, Wearables, längerfristige Beobachtung | noch nicht integriert |

Diese Rollen sind bewusst unterschiedlich. Das Framework soll nicht zeigen, dass alle Datensätze identisch verarbeitet werden können, sondern dass dieselbe methodische Struktur domänenspezifisch angepasst werden kann.

## Shared Framework Pattern

Über PAMAP2, WESAD und MHEALTH hinweg ist inzwischen dasselbe Grundmuster umgesetzt:

| Stufe | Zweck |
|---|---|
| Datenimport | kontrollierte lokale Rohdatenbasis |
| Parsing | strukturierte Subject-/Signal-Tabellen |
| Tensorisierung | segment-sichere Fensterbildung |
| Baseline-Modellierung | Nachweis lernbarer Signalstruktur |
| Feature Extraction | interpretierbare Komponenten |
| Score-Bildung | personalisierte Abweichungsmodellierung |
| Threshold-Auswertung | explizite Auffälligkeitsraten |
| Anomaly Detection | modellbasierte Zusatzperspektive |
| Ergebnisdokumentation | thesis-nahe Interpretation |
| Visualisierung | erklärende Grafiken |
| Memory-Kompatibilität | Übergang zu Ereignissen, Episoden und Hypothesen |

Diese Struktur ist der methodische Kern des Frameworks.

## PAMAP2 Summary

PAMAP2 bildet die funktional-motorische Entwicklungsebene.

Wichtige Eigenschaften:

| Eigenschaft | Wert |
|---|---:|
| Subjects | 8 im primären Pipeline-Stand |
| Sensorik | Hand, Chest, Ankle |
| Sampling Rate | 100 Hz |
| Fenstergröße | 500 Samples / 5 Sekunden |
| Kanäle im Baseline-Tensor | 19 |
| Fenster | 7,587 |

Die PAMAP2-Pipeline umfasst:

- Parser
- Cleaning
- Tensorisierung
- MiniRocket Activity Baseline
- funktionale Bewegungsfeatures
- funktionale Dysbalance-Scores
- Threshold-Auswertung
- Isolation-Forest-Anomaly-Detection
- Memory-Anbindung

Der supervised Activity-Baseline-Stand zeigte eine hohe Testleistung:

| Modell | Split | Accuracy |
|---|---|---:|
| MiniRocket | Train Subjects 101–106, Test Subjects 107–108 | 0.9541 |

Die funktionale Dysbalance-Auswertung nutzt Bewegungsrelationen zwischen Körpersegmenten. Die Score-Logik modelliert Abweichungen relativ zum individuellen Referenzverhalten.

Im Anomaly-Block zeigte PAMAP2 eine sehr starke Übereinstimmung zwischen explizitem funktionalem Score und modellbasierter Anomaly Detection. Für `functional_strength` und `anomaly_score` wurden sehr hohe Korrelationen beobachtet:

| Zusammenhang | Pearson | Spearman |
|---|---:|---:|
| PAMAP2 functional strength vs. anomaly score | 0.9499 | 0.9480 |

PAMAP2 stützt damit besonders stark die funktional-motorische Score-Logik.

## WESAD Summary

WESAD bildet die autonom-physiologische Entwicklungsebene.

Wichtige Eigenschaften:

| Eigenschaft | Wert |
|---|---:|
| Subjects | 15 |
| Sensorik | Chest-Signale |
| Sampling Rate | 700 Hz |
| Fenstergröße | 7,000 Samples / 10 Sekunden |
| Kanäle | 8 |
| Fenster | 8,892 |

Die WESAD-Pipeline umfasst:

- Chest-Pickle-Parser
- segment-sichere Fensterbildung
- MiniRocket-Baseline
- standardisierte Baseline
- autonome Feature Extraction
- autonome Dysbalance-Scores
- Threshold-Auswertung
- Isolation-Forest-Anomaly-Detection
- Memory-Anbindung

Die standardisierte WESAD-Baseline erreichte:

| Modell | Split | Accuracy |
|---|---|---:|
| MiniRocket standardisiert | Train S2–S11, Test S13–S17 | 0.7167 |

Die autonome Score-Logik unterscheidet gerichtete Aktivierung von ungerichteter Auffälligkeit. Besonders wichtig ist der Unterschied zwischen:

- `z_autonomic_activation`
- `autonomic_deviation_strength`

Die Stress-Bedingung zeigte erhöhte autonome Aktivierung:

| Condition | Mean z activation | % z activation > 2 |
|---|---:|---:|
| baseline | -0.4932 | 0.6279 |
| stress | 1.3926 | 18.0668 |
| amusement | -0.2430 | 0.8230 |
| meditation | -0.3269 | 0.1290 |

Im Anomaly-Block zeigte WESAD eine besonders starke Übereinstimmung zwischen ungerichteter autonomer Abweichungsstärke und modellbasierter Anomaly Detection:

| Zusammenhang | Pearson | Spearman |
|---|---:|---:|
| WESAD deviation strength vs. anomaly score | 0.9034 | 0.8458 |
| WESAD z activation vs. anomaly score | 0.3955 | 0.3171 |

Damit differenziert WESAD zwischen gerichteter autonomer Aktivierung und allgemeiner autonomer Auffälligkeit.

## MHEALTH Summary

MHEALTH bildet die externe multimodale Transfer- und Validierungsebene.

Wichtige Eigenschaften:

| Eigenschaft | Wert |
|---|---:|
| Subjects | 10 |
| Aktivitäten | 12 |
| Sensorik | Chest, Arm, Ankle, ECG |
| Sampling Rate | 50 Hz |
| Fenstergröße | 250 Samples / 5 Sekunden |
| Kanäle | 23 |
| Fenster | 2,555 |

Die MHEALTH-Pipeline umfasst:

- Rohdatenimport
- Parser
- segment-sichere Tensorisierung
- MiniRocket Subject-Split Baseline
- MiniRocket Leave-One-Subject-Out Baseline
- MultiRocket Leave-One-Subject-Out Baseline
- Movement Feature Extraction
- Functional Dysbalance Scores
- Dysbalance-Plots
- Isolation-Forest-Anomaly-Detection
- Ergebnisdokumentation

Die supervised Baseline zeigte:

| Experiment | Accuracy | Macro F1 |
|---|---:|---:|
| Subject Split 1–8 vs. 9–10 | 1.0000 | 1.0000 |
| MiniRocket Leave-One-Subject-Out Mean | 0.9521 | 0.9433 |
| MultiRocket Leave-One-Subject-Out Mean | 0.9725 | 0.9694 |

Der perfekte Subject-Split wurde nicht isoliert überinterpretiert. Die LOSO-Ergebnisse liefern das robustere Bild: starke Generalisierung mit sichtbaren subject- und aktivitätsabhängigen Grenzen. MultiRocket verbessert die MHEALTH-LOSO-Leistung gegenüber MiniRocket zusätzlich von 0.9521 auf 0.9725 Accuracy und von 0.9433 auf 0.9694 Macro-F1.

Die funktionale MHEALTH-Dysbalance-Auswertung nutzt unter anderem:

- `total_acc_rms`
- `log_extremity_chest_acc_ratio`
- `log_arm_ankle_acc_ratio`
- `log_arm_ankle_gyro_ratio`
- `ecg_diff_rms` als konservatives Zusatzsignal

Die Score-Ergebnisse zeigten:

| Größe | Wert |
|---|---:|
| Mean functional deviation strength | 0.7953 |
| Std functional deviation strength | 0.3592 |
| Max functional deviation strength | 2.9800 |
| Max combined movement ECG deviation strength | 2.7190 |

Bei Threshold `2.0` traten funktionale Abweichungen selten und plausibel auf. Höhere Raten zeigten unter anderem:

| Activity | Abnormal rate at θ = 2.0 |
|---|---:|
| frontal_elevation_arms | 1.3575 % |
| running | 1.3043 % |
| knees_bending | 0.9132 % |
| climbing_stairs | 0.8929 % |

Die modellbasierte MHEALTH-Anomaly-Auswertung bestätigte die funktionale Score-Logik stark:

| Zusammenhang | Pearson | Spearman |
|---|---:|---:|
| MHEALTH functional deviation strength vs. anomaly score | 0.9384 | 0.9335 |
| MHEALTH combined movement ECG score vs. anomaly score | 0.9035 | 0.8967 |
| MHEALTH ECG signal deviation vs. anomaly score | 0.0577 | 0.0512 |

Die geringe ECG-Korrelation stützt die vorsichtige Interpretation: Die MHEALTH-Anomaly-Struktur ist funktional-motorisch geprägt, nicht ECG-dominiert.

## Cross-Dataset Comparison

| Aspekt | PAMAP2 | WESAD | MHEALTH |
|---|---|---|---|
| Primäre Domäne | Bewegung | autonome Regulation | Bewegung + multimodale Zusatzsignale |
| Hauptziel | funktionale Abweichung | autonome Abweichung | externe Transferprüfung |
| Baseline-Modell | MiniRocket | MiniRocket | MiniRocket + MultiRocket |
| Score-Normalisierung | subject-bezogen | subject-/condition-bezogen | subject-/activity-bezogen |
| Score-Typ | funktional-motorisch | autonom-physiologisch | funktional-motorisch mit ECG-Zusatzsicht |
| Anomaly-Ebene | Isolation Forest | Isolation Forest | Isolation Forest |
| Memory-Anbindung | ja | ja | noch nicht im Memory integriert |
| Klinische Interpretation | nein | nein | nein |

Die wichtigste gemeinsame Erkenntnis ist nicht, dass alle Datensätze denselben Score verwenden. Die Gemeinsamkeit liegt darin, dass alle Datensätze dieselbe methodische Idee umsetzen:

> Abweichung wird als personalisierte, kontextbezogene Entfernung vom individuellen Referenzzustand modelliert.

## Classification vs. Dysbalance Modeling

Die Klassifikationsmodelle beantworten primär:

> Enthalten die Fenster ausreichend Signalstruktur, um Aktivität oder Zustand zu unterscheiden?

Die Dysbalance-Scores beantworten dagegen:

> Welche Fenster weichen innerhalb eines personalisierten Kontextes interpretierbar vom Referenzzustand ab?

Diese Unterscheidung ist zentral für die Thesis. Klassifikation ist eine Validierungs- und Strukturprüfung. Der eigentliche Framework-Beitrag liegt in der erklärbaren Abweichungsmodellierung.

## Anomaly Detection Across Datasets

Die Score-Level-Anomaly-Detection hat inzwischen eine zentrale Brückenfunktion.

| Dataset | stärkster Score-Anomaly-Zusammenhang | Interpretation |
|---|---|---|
| PAMAP2 | functional strength vs. anomaly score | funktionaler Score und Modellperspektive stimmen nahezu direkt überein |
| WESAD | deviation strength vs. anomaly score | ungerichtete autonome Auffälligkeit passt stärker als gerichtete Aktivierung |
| MHEALTH | functional deviation strength vs. anomaly score | externe funktionale Score-Logik wird modellbasiert bestätigt |

Damit entsteht ein dreistufiges Evidenzmuster:

1. Der Score ist explizit und interpretierbar.
2. Der Threshold markiert seltene Auffälligkeiten.
3. Das Modell erkennt diese Auffälligkeiten ebenfalls als anomal.

Diese Kombination ist stärker als eine reine Klassifikations- oder reine Threshold-Analyse.

## Longitudinal Dysbalance Memory

Das Longitudinal Dysbalance Memory wurde als Framework-Schicht implementiert, die einzelne Fensterauffälligkeiten in eine höhere Interpretationsstruktur überführt.

Aktueller Memory-Stand:

| Größe | Wert |
|---|---:|
| Events | 1,316 |
| Episodes | 686 |
| Hypotheses | 249 |
| Evidence scope | controlled_window_sequence |
| True longitudinal hypotheses | 0 |

Wichtig ist die vorsichtige Interpretation: Die aktuellen PAMAP2- und WESAD-Daten erlauben kontrollierte Fenstersequenzen, aber noch keine echte Langzeitbeobachtung. Deshalb werden alle Memory-Hypothesen als kontrollierte Sequenzhypothesen verstanden, nicht als echte longitudinale Evidenz.

Das Memory ist methodisch trotzdem wichtig, weil es die spätere TILES-Integration vorbereitet.

## Evidence for Generalizability

Der aktuelle Stand unterstützt eine begrenzte, aber starke methodische Generalisierbarkeit.

Evidenz:

- Drei unterschiedliche Datensätze wurden integriert.
- Alle Datensätze verwenden multimodale Biosignale.
- Alle Pipelines nutzen segment-sichere Fensterbildung.
- Alle Datensätze besitzen supervised Baselines.
- Alle Datensätze besitzen interpretierbare Features.
- Alle Score-Systeme nutzen personalisierte Normalisierung.
- Alle Score-Systeme erzeugen Threshold-basierte Auffälligkeitsraten.
- Alle drei Kern-Datensätze sind an eine modellbasierte Anomaly-Perspektive anschließbar.
- PAMAP2 und WESAD sind bereits an das Memory-System angeschlossen.
- MHEALTH bestätigt die funktionale Score-Logik auf einem externen Sensorset.

Grenzen:

- Die Scores bleiben domänenspezifisch.
- Die Daten sind kontrollierte Forschungsdatensätze.
- Klinische Diagnose ist explizit außerhalb des Scopes.
- Echte longitudinale Evidenz steht noch aus.
- MHEALTH ist in das Longitudinal Memory integriert und erweitert die Memory-Schicht um eine externe funktional-motorische Transferprüfung.
- TILES ist als echte Longitudinal-Perspektive noch nicht umgesetzt.

## Current Scientific Interpretation

Der aktuelle Stand spricht dafür, dass das Framework auf methodischer Ebene generalisierbar ist.

Die zentrale Aussage lautet:

> Das Framework ist nicht deshalb generalisierbar, weil überall dieselbe Formel verwendet wird. Es ist generalisierbar, weil dieselben Modellierungsprinzipien über verschiedene Biosignal-Domänen hinweg wiederverwendet werden können.

Diese Prinzipien sind:

- multimodale Fenster
- kontextbezogene Segmentierung
- interpretierbare Feature-Komponenten
- personalisierte Normalisierung
- Abweichungsscores
- Threshold-Analyse
- modellbasierte Anomaly-Prüfung
- Visualisierung
- Ereignis- und Hypothesenbildung

## Updated Project State

Completed core result blocks:

- PAMAP2 activity baseline
- PAMAP2 functional dysbalance score
- PAMAP2 anomaly evaluation
- WESAD condition baselines
- WESAD autonomic dysbalance score
- WESAD anomaly evaluation
- MHEALTH import and tensorization
- MHEALTH activity baselines
- MHEALTH functional dysbalance score
- MHEALTH anomaly evaluation
- Longitudinal Dysbalance Memory
- dataset attribution notes
- cross-dataset framework summary

Open core result blocks:

- MHEALTH integration into Longitudinal Dysbalance Memory
- MHEALTH MultiRocket LOSO model layer
- TILES feasibility and import decision
- final cross-dataset evaluation tables
- thesis chapter drafts
- final literature and BibTeX cleanup
- final figure selection

## Next Work Package

Der nächste methodisch sinnvolle Schritt ist die Erweiterung der Rocket-basierten Modellschicht auf PAMAP2 und WESAD sowie die Vorbereitung der TILES-Integration als echte longitudinale Datensatzebene.

Eine finale Cross-Dataset-Evaluation-Tabelle bleibt thesis-nah, weil sie PAMAP2, WESAD, MHEALTH, Anomaly Detection, Memory und MultiRocket kompakt gegenüberstellt und direkt in den Ergebnisteil übernommen werden kann.



## Cross-Dataset MultiRocket Model Layer

Die MultiRocket-Auswertung ergänzt die bisherige Framework-Evaluation um eine starke diskriminative Zeitreihenmodellschicht. Diese Modellschicht ist bewusst von den erklärbaren Dysbalance Scores, der modellbasierten Anomaly Detection und dem longitudinalen Dysbalance Memory getrennt.

Aus Sicht der Arbeit übernimmt MultiRocket drei Funktionen:

1. Es prüft, ob die segment-sicheren multimodalen Fenster robuste, subject-übergreifend lernbare Zeitreihenstruktur enthalten.
2. Es liefert eine leistungsstarke Referenzschicht gegenüber den erklärbaren Dysbalance Scores.
3. Es macht sichtbar, welche Biosignal-Domänen stärker oder schwächer generalisieren.

| Dataset | Domäne | Validierung | MultiRocket-Variante | Accuracy | Macro-F1 | Weighted-F1 |
|---|---|---|---|---:|---:|---:|
| MHEALTH | funktional-motorisch + ECG | Leave-One-Subject-Out | 10,000 kernels | 0.9725 | 0.9694 | 0.9673 |
| PAMAP2 | funktional-motorisch | Leave-One-Subject-Out | 5,000 kernels | 0.9443 | 0.9411 | 0.9444 |
| WESAD | autonom-affektiv | Subject-wise Split | standardisiert, stride 10, 5,000 kernels | 0.7730 | 0.6981 | 0.7614 |

Die Ergebnisse zeigen eine klare Domänenstruktur. Die funktional-motorischen Datensätze PAMAP2 und MHEALTH erreichen gemeinsam eine mittlere Accuracy von 0.9584. WESAD liegt mit 0.7730 niedriger, verbessert aber die standardisierte MiniRocket-Baseline um 0.0563.

Diese Differenz ist für die Arbeit produktiv: Bewegungsnahe Aktivitätsmuster sind subject-übergreifend sehr robust modellierbar, während autonom-affektive Zustände stärker personenabhängig, überlappend und erklärungsbedürftig bleiben.

Damit wird MultiRocket nicht als alleinige Lösung interpretiert, sondern als leistungsstarke Modellschicht innerhalb des Frameworks. Die eigentliche Dysbalance-Interpretation entsteht weiterhin über Scores, Anomaly Detection und Memory.




## MultiRocket Error-Dysbalance Linking

Neben der reinen Klassifikationsleistung wurde eine zusätzliche Verknüpfung zwischen MultiRocket-Fehlern, erklärbaren Dysbalance Scores und modellbasierter Anomaly Detection ausgewertet.

Die Leitfrage lautet:

> Sind falsch klassifizierte MultiRocket-Fenster zugleich physiologisch oder funktional auffälliger?

Diese Frage ist für die Arbeit zentral, weil sie Modellfehler nicht nur als technische Fehlklassifikationen behandelt, sondern mit der erklärbaren Dysbalance-Ebene verbindet.

| Dataset | Fehlerquote | Score korrekt | Score falsch | Score-Differenz | Anomaly korrekt | Anomaly falsch | Interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| MHEALTH | 2.78 % | 0.7972 | 0.7293 | -0.0679 | 5.07 % | 2.82 % | Fehler eher durch Klassenähnlichkeit, besonders jogging/running |
| PAMAP2 | 5.65 % | 0.6021 | 1.5871 | +0.9850 | 3.14 % | 36.13 % | Fehler stark mit funktionaler Dysbalance und Anomaly Detection verbunden |
| WESAD | 22.70 % | 0.8246 | 0.6443 | -0.1803 | 5.12 % | 3.84 % | Fehler eher durch autonom-affektive Zustandsüberlappung |

Der wichtigste Befund liegt bei PAMAP2: Falsch klassifizierte Fenster weisen im Mittel einen mehr als doppelt so hohen funktionalen Dysbalance Score auf wie korrekt klassifizierte Fenster. Gleichzeitig steigt die Anomaly-Rate von 3.14 % auf 36.13 %. Damit markieren MultiRocket-Fehler in PAMAP2 häufig genau jene Fensterbereiche, die auch durch die erklärbaren und modellbasierten Dysbalance-Schichten auffällig werden.

MHEALTH und WESAD zeigen dagegen eine andere Struktur. Bei MHEALTH entstehen Fehler vor allem zwischen sehr ähnlichen Bewegungsaktivitäten wie jogging und running. Bei WESAD dominieren physiologisch plausible Überlappungen zwischen amusement, stress, meditation und baseline. In beiden Fällen sind Fehler im Mittel nicht stärker dysbalanced als korrekt klassifizierte Fenster.

Diese Differenzierung ist für die Thesis entscheidend: Modellunsicherheit, Dysbalance Score und Anomaly Detection können zusammenfallen, müssen es aber nicht. Dadurch wird das Framework nicht auf eine einfache Gleichung „Fehler = Dysbalance“ reduziert, sondern erlaubt eine domänenspezifische Interpretation.

## Statistical Error-Dysbalance Check

Die Error-Dysbalance-Verknüpfung wurde zusätzlich statistisch geprüft. Dafür wurden korrekt und falsch klassifizierte MultiRocket-Fenster hinsichtlich Score-Differenz, nichtparametrischem Mann-Whitney-Test, Cliff's delta und Anomaly-Odds-Ratio verglichen.

| Dataset | Score-Differenz falsch-korrekt | 95%-CI | Cliff's delta | Anomaly-Odds-Ratio | Interpretation |
|---|---:|---:|---:|---:|---|
| MHEALTH | -0.0679 | [-0.1392, 0.0075] | -0.1020 | 0.5424 | Fehler nicht dysbalance-getrieben |
| PAMAP2 | 0.9850 | [0.8573, 1.1167] | 0.5070 | 17.4309 | starker Fehler-Dysbalance-Zusammenhang |
| WESAD | -0.1803 | [-0.2088, -0.1534] | -0.3256 | 0.7406 | Fehler eher Zustandsüberlappung |

Der stärkste und methodisch wichtigste Befund bleibt PAMAP2: Falsch klassifizierte Fenster zeigen eine deutlich höhere funktionale Dysbalance, eine positive Effektgröße und eine stark erhöhte Anomaly-Odds-Ratio. MHEALTH und WESAD zeigen dagegen, dass Fehler nicht automatisch Dysbalance bedeuten. Diese Differenzierung verhindert eine Überinterpretation von Modellfehlern und stärkt die domänenspezifische Framework-Logik.

## MultiRocket Error-Memory Linking

Zusätzlich zur Error-Dysbalance-Auswertung wurde geprüft, ob falsch klassifizierte MultiRocket-Fenster häufiger in der Longitudinal Dysbalance Memory-Schicht erscheinen.

| Dataset | Memory Events korrekt | Memory Events falsch | Event-Odds-Ratio | Hypothesen korrekt | Hypothesen falsch |
|---|---:|---:|---:|---:|---:|
| MHEALTH | 5.07 % | 2.82 % | 0.5424 | 5.07 % | 2.82 % |
| PAMAP2 | 3.17 % | 36.13 % | 17.2723 | 3.17 % | 36.13 % |
| WESAD | 8.85 % | 3.99 % | 0.4280 | 8.85 % | 3.99 % |

Diese Auswertung verbindet Modellunsicherheit mit temporaler Event-, Episoden- und Hypothesenbildung. Sie bleibt vorsichtig zu interpretieren, weil das aktuelle Memory kontrollierte Window-Sequenzen und noch keine echte Langzeitvalidierung abbildet.
