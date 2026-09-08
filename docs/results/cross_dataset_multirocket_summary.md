# Cross-Dataset MultiRocket Summary

Dieses Dokument fasst die aktuelle MultiRocket-Auswertung über die drei bisher integrierten Datensätze zusammen.

## Rolle in meiner Arbeit

MultiRocket bildet in meiner Arbeit eine starke diskriminative Zeitreihenmodellschicht. Diese Modellschicht ist bewusst von den erklärbaren Dysbalance Scores, der Anomaly-Detection-Ebene und dem longitudinalen Dysbalance Memory getrennt.

Die zentrale Idee ist nicht, Dysbalance allein durch Klassifikation zu ersetzen. Stattdessen prüfe ich, ob die segment-sicheren multimodalen Fenster über verschiedene Biosignal-Domänen hinweg genug robuste Zeitreihenstruktur enthalten, um durch ein starkes Rocket-basiertes Modell subject-übergreifend gelernt zu werden.

## Ergebnisübersicht

| Dataset | Domäne | Validierung | Modellvariante | Windows | Accuracy | Macro F1 | Weighted F1 |
|---|---|---|---|---:|---:|---:|---:|
| MHEALTH | functional-motor + ECG | leave-one-subject-out | MultiRocket, 10000 kernels | 2555 | 0.9725 | 0.9694 | 0.9673 |
| PAMAP2 | functional-motor | leave-one-subject-out | MultiRocket, 5000 kernels | 7587 | 0.9443 | 0.9411 | 0.9444 |
| WESAD | autonomic-affective | subject-wise split | MultiRocket, standardized, stride10, 5000 kernels | 8892 | 0.7730 | 0.6981 | 0.7614 |

## Kernergebnisse

Über alle drei Datensätze ergibt sich eine ungewichtete mittlere Accuracy von 0.8966 und ein ungewichteter mittlerer Macro-F1 von 0.8695.

Die funktional-motorischen Datensätze PAMAP2 und MHEALTH erreichen gemeinsam eine mittlere Accuracy von 0.9584. WESAD liegt mit 0.7730 niedriger, verbessert aber die standardisierte MiniRocket-Baseline um 0.0563.

## Dataset-spezifische Interpretation

### MHEALTH

MHEALTH liefert das stärkste externe MultiRocket-Ergebnis. Das ist für meine Arbeit besonders wichtig, weil MHEALTH nicht aus der ursprünglichen PAMAP2/WESAD-Struktur stammt und damit als externe funktional-motorische Transferprüfung dient.

Die sehr hohe LOSO-Leistung spricht dafür, dass die MHEALTH-Tensorisierung robuste, subject-übergreifend lernbare Bewegungsstruktur enthält. Gleichzeitig bleibt die ECG-Komponente im Dysbalance-Framework konservativ zu interpretieren, weil die vorherige Anomaly-Auswertung gezeigt hat, dass ECG die modellbasierte Abweichungsstruktur nicht wesentlich treibt.

### PAMAP2

PAMAP2 bestätigt die funktional-motorische Kernannahme meiner Arbeit. Auch im strengen Leave-One-Subject-Out-Protokoll bleibt die Accuracy hoch.

Besonders wichtig ist die Metrik-Korrektur: Der faire Macro-F1 muss über die im jeweiligen Testsubject vorhandenen Klassen berechnet werden, weil nicht alle Subjects alle Aktivitäten enthalten. Dadurch ergibt sich ein stimmiges Bild aus Accuracy, Macro-F1 und Weighted-F1.

### WESAD

WESAD ist der schwierigste, aber wissenschaftlich produktivste MultiRocket-Fall. MultiRocket verbessert die MiniRocket-Baseline deutlich, erreicht aber nicht die Leistung der funktional-motorischen Datensätze.

Das Ergebnis passt zur physiologischen Rolle von WESAD: Stress ist stark modellierbar, während amusement und meditation stärker mit anderen Zuständen überlappen. Damit unterstützt WESAD die zentrale Trennung zwischen leistungsstarker Klassifikation und erklärbarer Dysbalance-Modellierung.

## Bedeutung für die Forschungsfrage

Die MultiRocket-Ergebnisse stärken die Forschungsfrage meiner Arbeit auf drei Ebenen:

1. Die segment-sicheren Biosignal-Fenster enthalten robuste, modellierbare Zeitreihenstruktur.
2. Die funktional-motorische Domäne generalisiert besonders stark über Subjects.
3. Die autonom-affektive Domäne ist schwieriger, aber gerade deshalb für erklärbare Abweichungsmodellierung relevant.

Damit entsteht ein belastbares Argument: Das Framework ist nicht nur eine Sammlung von Scores, sondern verbindet starke Zeitreihenmodellierung mit erklärbarer Dysbalance- und Memory-Struktur.

## Rolle gegenüber Dysbalance Scores und Memory

| Framework-Ebene | Funktion |
|---|---|
| MultiRocket | starke diskriminative Modellschicht für subject-übergreifende Zeitreihenstruktur |
| Dysbalance Scores | erklärbare physiologische und funktionale Abweichungsmaße |
| Isolation Forest | unsupervised Modellbestätigung auffälliger Score- und Komponentenstrukturen |
| Dysbalance Memory | temporale Verdichtung von Auffälligkeiten zu Events, Episoden und Hypothesen |

Diese Trennung ist für die Thesis zentral: Hohe Modellleistung allein wäre nicht erklärbar genug, während Scores allein ohne starke Modellreferenz weniger überzeugend wären. Die Kombination erzeugt den Mehrwert.

## Aktueller Forschungsstand im Projekt

| Dataset | MultiRocket-Status | Dokumentation |
|---|---|---|
| MHEALTH | abgeschlossen | `docs/results/mhealth_multirocket_loso_summary.md` |
| PAMAP2 | abgeschlossen | `docs/results/pamap2_multirocket_loso_summary.md` |
| WESAD | abgeschlossen | `docs/results/wesad_multirocket_standardized_split_summary.md` |

## Grenzen

- Die Validierungsprotokolle sind nicht vollständig identisch: MHEALTH und PAMAP2 verwenden LOSO, WESAD einen festen Subject-Split.
- WESAD verwendet aus Ressourcengründen eine zeitliche Reduktion von 7,000 auf 700 Timepoints.
- Die Ergebnisse sind starke methodische Evidenz, aber keine klinische Validierung.
- MultiRocket erklärt nicht selbst, warum ein Fenster auffällig ist; diese Rolle übernehmen Scores, Anomaly Detection und Memory.
- PAMAP2, WESAD und MHEALTH liefern kontrollierte Window-Sequenzen, aber noch keine echte Langzeitbeobachtung.

## Zwischenfazit

MultiRocket ist nun dataset-übergreifend als starke Modellschicht etabliert. Die Ergebnisse sind besonders wertvoll, weil sie nicht nur hohe Performance zeigen, sondern auch eine klare Domänenstruktur sichtbar machen: motorische Signale generalisieren stark, autonom-affektive Zustände bleiben schwieriger und erklärungsbedürftiger.

Aus meiner Sicht stärkt genau diese Kombination die Arbeit: Das Framework kann robuste Zeitreihenstruktur modellieren, aber seine wissenschaftliche Stärke liegt in der erklärbaren Verbindung von Modellleistung, physiologischen Scores, Anomalien und longitudinaler Hypothesenbildung.
