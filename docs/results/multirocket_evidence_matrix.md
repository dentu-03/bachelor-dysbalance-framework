# MultiRocket Evidence Matrix

Dieses Dokument verdichtet die MultiRocket-Experimentphase zu einer thesis-nahen Evidenzmatrix.

## Ziel

Die Matrix verbindet Modellleistung, erklärbare Dysbalance Scores, Anomaly Detection und Dysbalance Memory. Sie soll später helfen, die Ergebnisse nicht isoliert, sondern als mehrschichtiges Framework zu argumentieren.

## Evidenzmatrix

| Befund | Dataset | Modellschicht | Dysbalance-Schicht | Anomaly-Schicht | Memory-Schicht | Interpretation | Grenze |
|---|---|---|---|---|---|---|---|
| Sehr starke externe motorische Generalisierung | MHEALTH | MultiRocket LOSO Accuracy 0.9725, Macro-F1 0.9694 | funktionaler Score vorhanden, Fehler nicht erhöht | Fehlerfenster zeigen keine erhöhte Anomaly-Rate | Fehlerfenster erscheinen nicht häufiger im Memory | Fehler entstehen eher durch Klassenähnlichkeit, besonders jogging/running | ECG konservativ interpretieren; keine klinische Dysbalance-Validierung |
| Starke motorische Generalisierung | PAMAP2 | MultiRocket LOSO Accuracy 0.9443, fairer Macro-F1 0.9411 | Fehlerfenster zeigen stark erhöhte funktionale Dysbalance | Anomaly-Rate steigt bei Fehlern von 3.14 % auf 36.13 % | Memory-Rate steigt bei Fehlern von 3.17 % auf 36.13 % | stärkster Brückenbefund zwischen Modellunsicherheit, Dysbalance und Memory | kontrollierte Sequenz, keine echte Langzeitvalidierung |
| Schwierige autonom-affektive Zustandsmodellierung | WESAD | MultiRocket Accuracy 0.7730, Macro-F1 0.6981 | Fehlerfenster zeigen im Mittel keine erhöhte autonomic deviation | keine positive Error-Anomaly-Verstärkung | keine positive Error-Memory-Verstärkung | Fehler spiegeln eher Zustandsüberlappung, besonders amusement/stress/meditation | WESAD zeitlich reduziert, Subject-Split statt LOSO |
| Motorische Domäne stärker als autonom-affektive Domäne | Cross-Dataset | PAMAP2 + MHEALTH mittlere Accuracy 0.9584 | motorische Scores stabil interpretierbar | starke Übereinstimmung besonders in PAMAP2 | Memory verdichtet PAMAP2-Auffälligkeiten stark | funktional-motorische Biosignale generalisieren robuster | Domänen nicht direkt gleichsetzen |
| Fehler bedeutet nicht automatisch Dysbalance | Cross-Dataset | Fehlerprofile unterscheiden sich nach Dataset | Score-Effekt nur bei PAMAP2 stark positiv | Anomaly-Effekt nur bei PAMAP2 stark positiv | Memory-Effekt nur bei PAMAP2 stark positiv | schützt vor Überinterpretation und stärkt domänenspezifische Lesart | benötigt klare methodische Erklärung |
| MultiRocket als starke Referenzschicht | Cross-Dataset | robuste diskriminative Zeitreihenmodellierung | Scores liefern Erklärungsebene | Isolation Forest liefert unsupervised Bestätigung | Memory liefert temporale Hypothesenbildung | mehrschichtige Architektur ist wissenschaftlich begründet | MultiRocket selbst ist nicht erklärend |

## Wichtigster thesis-relevanter Befund

Der stärkste Einzelbefund ist PAMAP2.

Bei PAMAP2 fallen mehrere Ebenen zusammen:

1. Falsch klassifizierte MultiRocket-Fenster.
2. Erhöhte funktionale Dysbalance Scores.
3. Erhöhte Isolation-Forest-Anomaly-Treffer.
4. Erhöhte Memory-Events, Episoden und Hypothesen.

Diese Verbindung zeigt, dass Modellunsicherheit in bestimmten funktional-motorischen Kontexten mit erklärbarer Abweichung zusammenfallen kann.

## Wichtigste Gegenbefunde

MHEALTH und WESAD sind ebenso wichtig, weil sie zeigen, dass dieser Zusammenhang nicht pauschal gilt.

Bei MHEALTH sind Fehler selten und vor allem zwischen ähnlichen Aktivitäten konzentriert.

Bei WESAD sind Fehler häufiger und spiegeln physiologische Überlappung affektiver Zustände wider.

Damit entsteht keine vereinfachte Aussage wie:

> Klassifikationsfehler sind Dysbalance.

Sondern:

> Klassifikationsfehler können in bestimmten Domänen mit Dysbalance, Anomaly Detection und Memory zusammenfallen, müssen aber anhand der Signal- und Kontextdomäne interpretiert werden.

## Verwendung in der Thesis

Diese Matrix eignet sich für:

- Ergebniskapitel: kompakte Zusammenfassung der MultiRocket-Phase.
- Diskussion: Argument gegen naive Fehlerinterpretation.
- Methodik: Begründung der mehrschichtigen Architektur.
- Ausblick: Motivation für echte longitudinale Daten und eigene Wearable-Erhebung.

## Zwischenfazit

Die MultiRocket-Evidenzmatrix zeigt, dass die Arbeit nicht nur hohe Modellleistungen berichtet, sondern die Modellleistung in eine erklärbare und domänenspezifische Dysbalance-Architektur einordnet.
