# MultiRocket Error-Memory Link Summary

Dieses Dokument untersucht, ob falsch klassifizierte MultiRocket-Fenster häufiger in der Longitudinal Dysbalance Memory-Schicht erscheinen.

## Leitfrage

Die Auswertung erweitert die Error-Dysbalance-Frage um die temporale Memory-Ebene:

> Tauchen falsch klassifizierte Fenster häufiger als Events, Episoden oder Hypothesen im Dysbalance Memory auf?

## Cross-Dataset Ergebnisübersicht

| Dataset | Fehlerquote % | Memory Events korrekt % | Memory Events falsch % | Differenz | Event OR | Fisher p | Hypothesen korrekt % | Hypothesen falsch % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MHEALTH | 2.78 | 5.07 | 2.82 | -2.26 | 0.5424 | 5.811e-01 | 5.07 | 2.82 |
| PAMAP2 | 5.65 | 3.17 | 36.13 | 32.96 | 17.2723 | <1e-99 | 3.17 | 36.13 |
| WESAD | 22.70 | 8.85 | 3.99 | -4.86 | 0.4280 | 1.270e-05 | 8.85 | 3.99 |

## Dataset-spezifische Error-Memory-Struktur

### MHEALTH

Bei MHEALTH liegt die Memory-Event-Rate für korrekt klassifizierte Fenster bei 5.07 % und für falsch klassifizierte Fenster bei 2.82 %.

Die Event-Odds-Ratio falsch gegenüber korrekt beträgt 0.5424. Die Hypothesenrate verändert sich von 5.07 % auf 2.82 %.

| True | Predicted | Errors | Score | Memory Event % | Memory Hypothesis % | Event Types |
|---|---|---:|---:|---:|---:|---|
| jogging | 11 | 37 | 0.7559 | 5.41 | 5.41 | model_anomaly |
| running | 10 | 32 | 0.6956 | 0.00 | 0.00 |  |
| cycling | 8 | 1 | 1.0184 | 0.00 | 0.00 |  |
| sitting_relaxing | 1 | 1 | 0.5373 | 0.00 | 0.00 |  |

### PAMAP2

Bei PAMAP2 liegt die Memory-Event-Rate für korrekt klassifizierte Fenster bei 3.17 % und für falsch klassifizierte Fenster bei 36.13 %.

Die Event-Odds-Ratio falsch gegenüber korrekt beträgt 17.2723. Die Hypothesenrate verändert sich von 3.17 % auf 36.13 %.

| True | Predicted | Errors | Score | Memory Event % | Memory Hypothesis % | Event Types |
|---|---|---:|---:|---:|---:|---|
| standing | sitting | 66 | 0.5876 | 0.00 | 0.00 |  |
| sitting | standing | 52 | 0.7602 | 9.62 | 9.62 | combined_score_model_event;model_anomaly |
| standing | ironing | 37 | 1.2291 | 24.32 | 24.32 | combined_score_model_event;model_anomaly |
| vacuum cleaning | ironing | 22 | 1.0786 | 13.64 | 13.64 | combined_score_model_event;model_anomaly |
| ascending stairs | descending stairs | 17 | 1.0626 | 17.65 | 17.65 | combined_score_model_event;model_anomaly |
| sitting | lying | 15 | 0.7057 | 6.67 | 6.67 | combined_score_model_event |
| Nordic walking | walking | 14 | 0.5224 | 0.00 | 0.00 |  |
| lying | standing | 12 | 2.0993 | 75.00 | 75.00 | combined_score_model_event;model_anomaly |

### WESAD

Bei WESAD liegt die Memory-Event-Rate für korrekt klassifizierte Fenster bei 8.85 % und für falsch klassifizierte Fenster bei 3.99 %.

Die Event-Odds-Ratio falsch gegenüber korrekt beträgt 0.4280. Die Hypothesenrate verändert sich von 8.85 % auf 3.99 %.

| True | Predicted | Errors | Score | Memory Event % | Memory Hypothesis % | Event Types |
|---|---|---:|---:|---:|---:|---|
| amusement | stress | 183 | 0.5807 | 4.37 | 4.37 | autonomic_activation;combined_score_model_event;model_anomaly |
| meditation | baseline | 152 | 0.6942 | 3.95 | 3.95 | combined_score_model_event;model_anomaly |
| baseline | amusement | 71 | 0.6852 | 0.00 | 0.00 |  |
| amusement | baseline | 65 | 0.6106 | 3.08 | 3.08 | model_anomaly |
| meditation | amusement | 57 | 0.6829 | 5.26 | 5.26 | combined_score_model_event;model_anomaly |
| meditation | stress | 53 | 0.5543 | 9.43 | 9.43 | combined_score_model_event;model_anomaly |
| baseline | stress | 46 | 0.6542 | 0.00 | 0.00 |  |
| baseline | meditation | 29 | 0.7303 | 0.00 | 0.00 |  |

## Interpretation

Die Memory-Verknüpfung prüft, ob Modellfehler nur punktuelle Klassifikationsprobleme sind oder ob sie auch in der temporalen Hypothesenbildung des Frameworks sichtbar werden.

Ein hoher Error-Memory-Zusammenhang bedeutet nicht automatisch klinische Relevanz. Er zeigt aber, dass ein Fehlerfenster nicht isoliert steht, sondern mit Score-, Anomaly- oder Episodenstruktur verbunden ist.

Besonders wichtig ist die Trennung der Ebenen: Klassifikationsfehler, Dysbalance Score, Anomaly Detection und Memory markieren verwandte, aber nicht identische Phänomene.

## Methodische Vorsicht

- Das aktuelle Memory basiert auf kontrollierten Window-Sequenzen, nicht auf echter Langzeitbeobachtung.
- Memory-Hypothesen sind keine Diagnosen.
- Events entstehen aus Scores und Anomaly Detection; sie sind keine unabhängige Ground Truth.
- Ein fehlender Memory-Treffer bedeutet nicht, dass ein Fehler irrelevant ist.

## Zwischenfazit

Die Error-Memory-Verknüpfung erweitert die Arbeit um eine wichtige Frage: Werden Modellfehler auch temporal und hypothesenbezogen sichtbar? Diese Ebene verbindet starke Zeitreihenklassifikation mit erklärbarer, vorsichtig interpretierter Dysbalance-Hypothesenbildung.

## Abbildungen

Die folgenden Abbildungen wurden für den späteren Ergebnisteil erzeugt:

| Abbildung | Datei |
|---|---|
| Memory Event Rate korrekt vs. falsch | `reports/figures/multirocket_error_memory_link/memory_event_rate_correct_vs_incorrect.png` |
| Memory Hypothesis Rate korrekt vs. falsch | `reports/figures/multirocket_error_memory_link/memory_hypothesis_rate_correct_vs_incorrect.png` |
| Memory Event Odds Ratio | `reports/figures/multirocket_error_memory_link/memory_event_odds_ratio_incorrect_vs_correct.png` |
| Combined Score-Model Event Rate | `reports/figures/multirocket_error_memory_link/combined_score_model_event_rate_correct_vs_incorrect.png` |
