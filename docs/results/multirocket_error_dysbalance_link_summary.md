# MultiRocket Error-Dysbalance Link Summary

Dieses Dokument hält eine zentrale Anschlussfrage für die Thesis fest: Sind falsch klassifizierte MultiRocket-Fenster zugleich physiologisch oder funktional auffälliger?

## Forschungsfrage der Auswertung

Die Auswertung verbindet drei Ebenen meines Frameworks:

| Ebene | Rolle |
|---|---|
| MultiRocket | diskriminative Zeitreihenklassifikation |
| Dysbalance Scores | erklärbare funktionale oder autonom-physiologische Abweichung |
| Isolation Forest | modellbasierte Anomaly-Schicht auf Score-/Komponentenebene |

Die Leitfrage lautet: Treten Klassifikationsfehler bevorzugt dort auf, wo die erklärbaren Dysbalance- oder Anomaly-Schichten bereits erhöhte Abweichungen anzeigen?

## Cross-Dataset Ergebnisübersicht

| Dataset | Fehlerquote % | Score correct | Score incorrect | Differenz | Ratio | Anomaly % correct | Anomaly % incorrect | Anomaly-Differenz |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MHEALTH | 2.78 | 0.7972 | 0.7293 | -0.0679 | 0.9149 | 5.07 | 2.82 | -2.26 |
| PAMAP2 | 5.65 | 0.6021 | 1.5871 | 0.9850 | 2.6358 | 3.14 | 36.13 | 32.99 |
| WESAD | 22.70 | 0.8246 | 0.6443 | -0.1803 | 0.7813 | 5.12 | 3.84 | -1.28 |

## Dataset-spezifische Lesart

### MHEALTH

Bei MHEALTH liegt die Fehlerquote bei 2.78 %. Der mittlere erklärbare Score beträgt 0.7972 für korrekt klassifizierte Fenster und 0.7293 für falsch klassifizierte Fenster.

Die mittlere Score-Differenz falsch minus korrekt beträgt -0.0679. Die Anomaly-Rate steigt von 5.07 % auf 2.82 %.

| True | Predicted | Errors | Mean score | Anomaly % |
|---|---|---:|---:|---:|
| jogging | 11 | 37 | 0.7559 | 5.41 |
| running | 10 | 32 | 0.6956 | 0.00 |
| cycling | 8 | 1 | 1.0184 | 0.00 |
| sitting_relaxing | 1 | 1 | 0.5373 | 0.00 |

### PAMAP2

Bei PAMAP2 liegt die Fehlerquote bei 5.65 %. Der mittlere erklärbare Score beträgt 0.6021 für korrekt klassifizierte Fenster und 1.5871 für falsch klassifizierte Fenster.

Die mittlere Score-Differenz falsch minus korrekt beträgt 0.9850. Die Anomaly-Rate steigt von 3.14 % auf 36.13 %.

| True | Predicted | Errors | Mean score | Anomaly % |
|---|---|---:|---:|---:|
| standing | sitting | 66 | 0.5876 | 0.00 |
| sitting | standing | 52 | 0.7602 | 9.62 |
| standing | ironing | 37 | 1.2291 | 24.32 |
| vacuum cleaning | ironing | 22 | 1.0786 | 13.64 |
| ascending stairs | descending stairs | 17 | 1.0626 | 17.65 |
| sitting | lying | 15 | 0.7057 | 6.67 |
| Nordic walking | walking | 14 | 0.5224 | 0.00 |
| lying | standing | 12 | 2.0993 | 75.00 |

### WESAD

Bei WESAD liegt die Fehlerquote bei 22.70 %. Der mittlere erklärbare Score beträgt 0.8246 für korrekt klassifizierte Fenster und 0.6443 für falsch klassifizierte Fenster.

Die mittlere Score-Differenz falsch minus korrekt beträgt -0.1803. Die Anomaly-Rate steigt von 5.12 % auf 3.84 %.

| True | Predicted | Errors | Mean score | Anomaly % |
|---|---|---:|---:|---:|
| amusement | stress | 183 | 0.5807 | 4.37 |
| meditation | baseline | 152 | 0.6942 | 3.95 |
| baseline | amusement | 71 | 0.6852 | 0.00 |
| amusement | baseline | 65 | 0.6106 | 3.08 |
| meditation | amusement | 57 | 0.6829 | 5.26 |
| meditation | stress | 53 | 0.5543 | 9.43 |
| baseline | stress | 46 | 0.6542 | 0.00 |
| baseline | meditation | 29 | 0.7303 | 0.00 |

## Bedeutung für die Thesis

Diese Auswertung ist besonders wichtig, weil sie Modellfehler nicht nur als technische Fehlklassifikationen behandelt. Stattdessen werden Fehler mit erklärbaren Score- und Anomaly-Strukturen verbunden.

Ein positiver Zusammenhang würde bedeuten: MultiRocket scheitert nicht zufällig, sondern häufiger an Fenstern, die im Framework ohnehin als funktional oder physiologisch auffällig erscheinen.

Ein schwacher Zusammenhang wäre ebenfalls relevant: Dann würden Klassifikationsfehler eher aus Klassenähnlichkeit, Sensorrauschen oder subject-spezifischer Variation entstehen und müssten getrennt von Dysbalance interpretiert werden.

## Aktuelle methodische Vorsicht

- Die Analyse zeigt Zusammenhänge, aber keine Kausalität.
- Die Anomaly-Schicht nutzt eigene Modelle und darf nicht als Ground Truth gelesen werden.
- Bei WESAD sind affektive Zustände physiologisch überlappend, besonders amusement, stress und meditation.
- Bei PAMAP2 und MHEALTH können Fehler aus ähnlichen Bewegungsabläufen entstehen, auch wenn keine physiologische Auffälligkeit vorliegt.

## Zwischenfazit

Die Error-Dysbalance-Verknüpfung ist eine zentrale Brücke zwischen starker Zeitreihenklassifikation und erklärbarer Dysbalance-Modellierung. Sie macht sichtbar, ob Modellunsicherheit, funktionale Abweichung und modellbasierte Anomalie dieselben Fensterbereiche markieren oder unterschiedliche Aspekte der Daten beschreiben.

## Statistische Zusatzprüfung

Zur Absicherung der Error-Dysbalance-Verknüpfung wurden zusätzlich nichtparametrische Tests und Effektgrößen berechnet.

| Dataset | Score-Diff | 95%-CI | Mann-Whitney p | Cliff's delta | Anomaly OR | Fisher p |
|---|---:|---:|---:|---:|---:|---:|
| MHEALTH | -0.0679 | [-0.1392, 0.0075] | 1.423e-01 | -0.1020 | 0.5424 | 5.811e-01 |
| PAMAP2 | 0.9850 | [0.8573, 1.1167] | 7.672e-70 | 0.5070 | 17.4309 | <1e-99 |
| WESAD | -0.1803 | [-0.2088, -0.1534] | 4.520e-38 | -0.3256 | 0.7406 | 1.859e-01 |

Die statistische Prüfung bestätigt die deskriptive Interpretation. Der starke positive Zusammenhang zwischen Fehlern und Dysbalance zeigt sich klar bei PAMAP2. Bei MHEALTH und WESAD ist der Effekt dagegen negativ oder schwach, was gegen eine einfache Gleichsetzung von Klassifikationsfehler und Dysbalance spricht.

Damit wird die zentrale methodische Aussage gestützt: Modellunsicherheit, erklärbare Dysbalance und modellbasierte Anomalie können zusammenfallen, müssen aber domänenspezifisch interpretiert werden.
