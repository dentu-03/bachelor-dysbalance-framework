# PAMAP2 MultiRocket LOSO Summary

Dieses Dokument fasst die MultiRocket-basierte Leave-One-Subject-Out-Auswertung auf PAMAP2 zusammen.

## Rolle im Framework

PAMAP2 bildet die zentrale funktional-motorische Bewegungsdomäne des Frameworks. Die MultiRocket-Auswertung ergänzt die bisherige MiniRocket-Subject-Split-Baseline durch ein strengeres subject-wise Validierungsprotokoll.

MultiRocket dient hier nicht als Ersatz für die erklärbaren Dysbalance Scores, sondern als starke Zeitreihenmodellschicht. Dadurch kann geprüft werden, ob die segment-sicheren Rohfenster subject-übergreifend lernbare Bewegungsstruktur enthalten.

## Datengrundlage

| Größe | Wert |
|---|---:|
| Dataset | PAMAP2 |
| Subjects | 8 |
| Windows | 7587 |
| Tensor shape | `(7587, 19, 500)` |
| Channels | 19 |
| Window length | 500 |
| Validation | Leave-One-Subject-Out |

## Modellkonfiguration

| Parameter | Wert |
|---|---:|
| Model | MultiRocketClassifier |
| n_kernels | 5000 |
| random_state | 42 |
| n_jobs | 4 |

Die ressourcenschonende Variante mit 5,000 Kernels wurde verwendet, weil die 10,000-Kernel-Variante auf PAMAP2 nach mehreren Folds vom System beendet wurde.

## Aggregierte Ergebnisse

| Metric | Mean | Std | Min | Max |
|---|---:|---:|---:|---:|
| Accuracy | 0.9443 | 0.0265 | 0.8887 | 0.9737 |
| Macro F1, present labels | 0.9411 | 0.0263 | 0.8962 | 0.9709 |
| Macro F1, all labels | 0.8614 | | 0.6324 | 0.9522 |
| Weighted F1 | 0.9444 | | 0.8887 | 0.9740 |

## Wichtige Metrik-Korrektur

Der ursprünglich gespeicherte Macro-F1 über alle Labels fällt niedriger aus, weil einzelne Testsubjects nicht alle Aktivitäten enthalten. Wenn Macro-F1 nur über die tatsächlich im jeweiligen Testsubject vorhandenen Klassen berechnet wird, ergibt sich ein deutlich faireres Bild.

| Metrik | Wert | Interpretation |
|---|---:|---|
| Macro F1 über alle Labels | 0.8614 | konservativ, bestraft fehlende Testklassen |
| Macro F1 über vorhandene Labels | 0.9411 | fairere subject-wise Bewertung |

Damit zeigt PAMAP2 eine starke subject-wise Generalisierung, obwohl das Protokoll strenger ist als der ursprüngliche feste Subject-Split.

## Fold-Ergebnisse

| Test Subject | Windows | Present Classes | Accuracy | Macro F1 Present Labels | Weighted F1 |
|---:|---:|---:|---:|---:|---:|
| 101 | 979 | 12 | 0.8887 | 0.8962 | 0.8887 |
| 102 | 1032 | 12 | 0.9496 | 0.9522 | 0.9496 |
| 103 | 682 | 8 | 0.9487 | 0.9485 | 0.9487 |
| 104 | 907 | 10 | 0.9724 | 0.9709 | 0.9727 |
| 105 | 1068 | 12 | 0.9354 | 0.9360 | 0.9358 |
| 106 | 979 | 11 | 0.9469 | 0.9485 | 0.9465 |
| 107 | 912 | 11 | 0.9737 | 0.9669 | 0.9740 |
| 108 | 1028 | 12 | 0.9387 | 0.9095 | 0.9395 |

## Stärkste Folds

| Test Subject | Accuracy | Macro F1 Present Labels |
|---:|---:|---:|
| 107 | 0.9737 | 0.9669 |
| 104 | 0.9724 | 0.9709 |
| 102 | 0.9496 | 0.9522 |

## Schwächste Folds

| Test Subject | Accuracy | Macro F1 Present Labels |
|---:|---:|---:|
| 101 | 0.8887 | 0.8962 |
| 105 | 0.9354 | 0.9360 |
| 108 | 0.9387 | 0.9095 |

## Häufigste Verwechslungen

| True Activity | Predicted Activity | Errors |
|---|---|---:|
| standing | sitting | 66 |
| sitting | standing | 52 |
| standing | ironing | 37 |
| vacuum cleaning | ironing | 22 |
| ascending stairs | descending stairs | 17 |
| sitting | lying | 15 |
| Nordic walking | walking | 14 |
| ironing | standing | 12 |
| lying | standing | 12 |
| vacuum cleaning | standing | 9 |
| descending stairs | standing | 9 |
| rope jumping | descending stairs | 8 |
| sitting | ironing | 8 |
| lying | ironing | 8 |
| ascending stairs | standing | 8 |

Die häufigsten Fehler betreffen vor allem nahe oder physiologisch plausible Bewegungskontexte, insbesondere sitting/standing, standing/ironing sowie ascending/descending stairs.

## Schwächste Klassenmetriken

| Test Subject | Label | Precision | Recall | F1 | Support |
|---:|---:|---:|---:|---:|---:|
| 101.0 | 2 | 0.7463 | 0.5435 | 0.6289 | 92 |
| 101.0 | 3 | 0.6988 | 0.6824 | 0.6905 | 85 |
| 108.0 | 13 | 0.5738 | 0.9722 | 0.7216 | 36 |
| 105.0 | 3 | 0.7191 | 0.7356 | 0.7273 | 87 |
| 108.0 | 12 | 0.9310 | 0.6136 | 0.7397 | 44 |
| 106.0 | 3 | 0.8481 | 0.6979 | 0.7657 | 96 |
| 108.0 | 24 | 1.0000 | 0.6471 | 0.7857 | 34 |
| 101.0 | 17 | 0.6549 | 1.0000 | 0.7915 | 93 |
| 105.0 | 2 | 0.8889 | 0.8302 | 0.8585 | 106 |
| 106.0 | 2 | 0.7719 | 0.9670 | 0.8585 | 91 |
| 103.0 | 3 | 0.9444 | 0.8395 | 0.8889 | 81 |
| 108.0 | 3 | 0.8455 | 0.9394 | 0.8900 | 99 |

## Interpretation

Die PAMAP2-MultiRocket-Ergebnisse sind stark, aber differenzierter als ein einfacher Subject-Split.

Zentrale Erkenntnisse:

- Leave-One-Subject-Out bleibt mit ungefähr 0.944 Accuracy hoch.
- Der faire Macro-F1 über vorhandene Klassen liegt mit ungefähr 0.941 nahe an Accuracy und Weighted F1.
- Die ursprüngliche all-label Macro-F1-Auswertung ist methodisch zu konservativ, weil einige Subjects nicht alle Aktivitäten enthalten.
- Die wichtigsten Fehler entstehen in plausiblen Grenzbereichen ähnlicher Körperhaltungen oder Bewegungsabläufe.
- MultiRocket bestätigt die hohe technische Qualität der segment-sicheren PAMAP2-Tensorisierung.

## Bedeutung für das Dysbalance-Framework

PAMAP2 zeigt nun zwei komplementäre Ebenen:

| Ebene | Aussage |
|---|---|
| MultiRocket LOSO | starke subject-wise Klassifizierbarkeit der Rohzeitreihen |
| Functional Dysbalance Score | erklärbare Abweichung von subject- und activity-spezifischen Bewegungsreferenzen |
| Isolation Forest | starke modellbasierte Bestätigung der funktionalen Score-Struktur |
| Dysbalance Memory | Überführung auffälliger Fenster in Events, Episoden und Hypothesen |

Damit wird PAMAP2 nicht nur als Activity-Recognition-Datensatz genutzt, sondern als funktional-motorischer Kernbaustein eines erklärbaren Dysbalance-Frameworks.

## Grenzen

- PAMAP2 ist kein echter Longitudinaldatensatz.
- Einige Subjects enthalten nicht alle Aktivitätsklassen.
- Die 5,000-Kernel-Variante wurde aus Ressourcengründen gewählt.
- Activity Classification ist keine klinische Dysbalance-Validierung.
- Die erklärbare Dysbalance-Ebene muss getrennt von der Klassifikationsleistung interpretiert werden.

## Zwischenfazit

MultiRocket wurde erfolgreich auf PAMAP2 im Leave-One-Subject-Out-Protokoll angewendet.

Die Ergebnisse stärken die Thesis, weil sie zeigen, dass die funktional-motorische Datengrundlage nicht nur erklärbare Dysbalance Scores ermöglicht, sondern auch unter einer starken Rocket-basierten Zeitreihenmodellschicht subject-übergreifend belastbare Signalstruktur enthält.
