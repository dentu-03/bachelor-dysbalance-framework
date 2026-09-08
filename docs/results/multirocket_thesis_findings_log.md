# MultiRocket Thesis Findings Log

Dieses Dokument hält die zentralen Gedanken, Fragen und Befunde der MultiRocket-Experimentphase für die spätere Thesis-Ausarbeitung fest.

## Ausgangspunkt

MultiRocket wurde in meiner Arbeit nicht nur als weiteres Klassifikationsmodell eingesetzt, sondern als starke diskriminative Zeitreihenmodellschicht innerhalb eines erklärbaren Dysbalance-Frameworks.

Die zentrale Idee lautet:

> Ein starkes Zeitreihenmodell kann zeigen, ob robuste subject-übergreifende Signalstruktur vorhanden ist. Die eigentliche physiologische und funktionale Bedeutung entsteht aber erst durch die Verbindung mit Dysbalance Scores, Anomaly Detection und Dysbalance Memory.

## Zentrale Forschungsfragen aus der Experimentphase

### 1. Enthalten die multimodalen Fenster robuste subject-übergreifende Zeitreihenstruktur?

Diese Frage prüft, ob die segment-sicheren Fenster über verschiedene Datensätze hinweg nicht nur technisch korrekt erzeugt wurden, sondern tatsächlich modellierbare Signalstruktur enthalten.

MultiRocket dient dafür als starke Referenzschicht.

### 2. Generalisieren funktional-motorische Biosignale besser als autonom-affektive Biosignale?

Die bisherigen Ergebnisse sprechen klar dafür.

MHEALTH und PAMAP2 erreichen sehr hohe subject-wise Leistungen. WESAD bleibt schwieriger, verbessert sich aber gegenüber MiniRocket deutlich.

Diese Differenz ist wissenschaftlich wichtig, weil sie zeigt, dass das Framework domänenspezifisch gelesen werden muss.

### 3. Sind falsch klassifizierte MultiRocket-Fenster zugleich funktional oder physiologisch auffälliger?

Diese Frage ist für meine Arbeit entscheidend.

Klassifikationsfehler sollen nicht nur als technische Fehler verstanden werden. Stattdessen wird geprüft, ob sie mit erklärbaren Dysbalance Scores und modellbasierter Anomaly Detection zusammenfallen.

Die Antwort ist differenziert:

- Bei PAMAP2: ja, sehr deutlich.
- Bei MHEALTH: nein, Fehler entstehen eher durch Klassenähnlichkeit.
- Bei WESAD: nein, Fehler spiegeln eher autonom-affektive Zustandsüberlappung.

### 4. Tauchen falsch klassifizierte Fenster häufiger im Dysbalance Memory auf?

Diese Frage erweitert die Error-Dysbalance-Verknüpfung um eine temporale Ebene.

Auch hier zeigt PAMAP2 den stärksten Befund. Falsch klassifizierte PAMAP2-Fenster erscheinen deutlich häufiger als Memory Events, Episoden und Hypothesen.

MHEALTH und WESAD zeigen dagegen keinen positiven Error-Memory-Effekt.

## Cross-Dataset MultiRocket Ergebnisse

| Dataset | Domäne | Validierung | Accuracy | Macro-F1 | Interpretation |
|---|---|---|---:|---:|---|
| MHEALTH | funktional-motorisch + ECG | Leave-One-Subject-Out | 0.9725 | 0.9694 | sehr starke externe funktional-motorische Transferprüfung |
| PAMAP2 | funktional-motorisch | Leave-One-Subject-Out | 0.9443 | 0.9411 | starke subject-wise Bewegungsmodellierung |
| WESAD | autonom-affektiv | Subject-wise Split | 0.7730 | 0.6981 | schwieriger, aber gegenüber MiniRocket verbessert |

## Error-Dysbalance Befund

| Dataset | Score korrekt | Score falsch | Differenz | Anomaly korrekt | Anomaly falsch | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| MHEALTH | 0.7972 | 0.7293 | -0.0679 | 5.07 % | 2.82 % | Fehler nicht dysbalance-getrieben |
| PAMAP2 | 0.6021 | 1.5871 | +0.9850 | 3.14 % | 36.13 % | starker Fehler-Dysbalance-Zusammenhang |
| WESAD | 0.8246 | 0.6443 | -0.1803 | 5.12 % | 3.84 % | Fehler eher Zustandsüberlappung |

## Statistische Absicherung

| Dataset | Score-Differenz falsch-korrekt | 95%-CI | Cliff's delta | Anomaly-Odds-Ratio | Interpretation |
|---|---:|---:|---:|---:|---|
| MHEALTH | -0.0679 | [-0.1392, 0.0075] | -0.1020 | 0.5424 | kein positiver Fehler-Dysbalance-Effekt |
| PAMAP2 | +0.9850 | [0.8573, 1.1167] | 0.5070 | 17.4309 | starker positiver Zusammenhang |
| WESAD | -0.1803 | [-0.2088, -0.1534] | -0.3256 | 0.7406 | Fehler eher nicht dysbalance-getrieben |

## Error-Memory Befund

| Dataset | Memory Events korrekt | Memory Events falsch | Event-Odds-Ratio | Hypothesen korrekt | Hypothesen falsch | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| MHEALTH | 5.07 % | 2.82 % | 0.5424 | 5.07 % | 2.82 % | kein positiver Error-Memory-Effekt |
| PAMAP2 | 3.17 % | 36.13 % | 17.2723 | 3.17 % | 36.13 % | starke Verbindung von Fehler, Dysbalance und Memory |
| WESAD | 8.85 % | 3.99 % | 0.4280 | 8.85 % | 3.99 % | Fehler eher autonom-affektive Zustandsüberlappung |

## Wichtigster Befund

Der stärkste und thesis-relevanteste Befund ist PAMAP2.

Bei PAMAP2 fallen drei Ebenen zusammen:

1. MultiRocket-Fehler
2. erhöhte funktionale Dysbalance Scores
3. deutlich erhöhte Anomaly- und Memory-Treffer

Damit zeigt PAMAP2, dass Modellunsicherheit nicht nur technisch entsteht, sondern in bestimmten motorischen Kontexten mit erklärbarer funktionaler Abweichung zusammenfallen kann.

## Warum MHEALTH und WESAD genauso wichtig sind

MHEALTH und WESAD sind keine negativen Ergebnisse.

Sie verhindern eine zu einfache Interpretation.

Bei MHEALTH entstehen Fehler vor allem zwischen sehr ähnlichen Bewegungsaktivitäten, insbesondere jogging und running. Das spricht eher für Klassenähnlichkeit als für Dysbalance.

Bei WESAD entstehen Fehler vor allem in physiologisch überlappenden affektiven Zuständen, insbesondere amusement, stress, meditation und baseline. Das spricht eher für Zustandsüberlappung und subject-spezifische autonome Variation.

Dadurch wird das Framework wissenschaftlich stärker, weil es nicht behauptet:

> Fehler bedeutet Dysbalance.

Sondern:

> Fehler, Dysbalance Score, Anomaly Detection und Memory können zusammenfallen, müssen aber domänenspezifisch interpretiert werden.

## Rolle von MultiRocket in der finalen Thesis

MultiRocket sollte in der Thesis als leistungsstarke Modellschicht beschrieben werden, nicht als alleiniger Erklärungsmechanismus.

Die Architektur bleibt:

| Ebene | Funktion |
|---|---|
| MultiRocket | starke subject-übergreifende Zeitreihenklassifikation |
| Dysbalance Scores | erklärbare funktionale oder autonom-physiologische Abweichung |
| Isolation Forest | modellbasierte Anomaly-Bestätigung |
| Dysbalance Memory | temporale Verdichtung zu Events, Episoden und Hypothesen |

## Methodische Vorsicht

Die bisherigen Ergebnisse sind methodisch stark, aber nicht klinisch zu überinterpretieren.

Wichtige Einschränkungen:

- PAMAP2, WESAD und MHEALTH sind kontrollierte Datensätze.
- Das aktuelle Memory bildet kontrollierte Window-Sequenzen ab, keine echte Langzeitbeobachtung.
- Dysbalance-Hypothesen sind keine Diagnosen.
- WESAD verwendet für MultiRocket eine zeitliche Reduktion auf 700 Timepoints.
- PAMAP2 verwendet aus Ressourcengründen 5,000 MultiRocket-Kernels.
- Die Validierungsprotokolle sind nicht vollständig identisch.

## Bedeutung für den weiteren Projektverlauf

Die MultiRocket-Phase stärkt die Bachelorarbeit deutlich.

Sie zeigt:

1. Die Datenbasis ist modellierbar.
2. Die motorische Domäne generalisiert stark.
3. Die autonom-affektive Domäne ist schwieriger und erklärungsbedürftiger.
4. Modellfehler können mit Dysbalance und Memory zusammenfallen.
5. Diese Verbindung ist domänenspezifisch und darf nicht pauschal interpretiert werden.

## Nächster wissenschaftlicher Schritt

Der nächste große Schritt ist die Vorbereitung einer echten longitudinalen Ebene.

Dafür sind besonders relevant:

- TILES als externer longitudinaler Datensatz.
- Spätere eigene Wearable-Daten mit Garmin Forerunner 965 und Polar H10.
- Übertragung der bisherigen Score-, Anomaly-, MultiRocket- und Memory-Logik auf echte Zeitverläufe.

## Zwischenfazit

Die MultiRocket-Experimentphase liefert eine tragfähige Brücke zwischen moderner Zeitreihenklassifikation und erklärbarer Dysbalance-Modellierung.

Der wichtigste Mehrwert liegt nicht allein in hoher Accuracy, sondern in der Frage, wann Modellunsicherheit physiologisch oder funktional bedeutsam wird.

Genau diese Frage ist zentral für die Thesis.
