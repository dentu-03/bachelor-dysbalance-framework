# Thesis Consolidation Summary

Dieses Dokument konsolidiert den aktuellen Stand der Bachelorarbeit thesis-orientiert.

Es ordnet die bisher implementierten Pipeline-Bausteine, Datensätze, Modellschichten, Dysbalance-Auswertungen, Anomaly-Analysen, Memory-Strukturen, MultiRocket-Ergebnisse und TILES-Vorbereitung in eine zusammenhängende Argumentationslinie ein.

## Arbeitstitel

Entwicklung eines generalisierbaren multimodalen Dysbalance-Frameworks zur erklärbaren Modellierung, Anomalieerkennung und longitudinalen Verfolgung personalisierter physiologischer Abweichungen

## Zentrale Forschungsfrage

Inwiefern lassen sich personalisierte physiologische Abweichungsmuster mithilfe eines multimodalen Dysbalance-Frameworks über verschiedene Biosignal-Datensätze hinweg erkennen, erklären und longitudinal verfolgen?

## Arbeitsdefinition Dysbalance

Dysbalance bezeichnet in dieser Arbeit eine durch modellbasierte Analyse multimodaler Biosignale erkennbare, personalisierte und physiologisch interpretierbare Abweichung vom individuellen Referenzzustand.

## Zentrale Framework-Idee

Die Arbeit entwickelt kein einzelnes isoliertes Klassifikationsmodell.

Der Kernbeitrag liegt in einer mehrschichtigen Architektur:

| Ebene | Aufgabe |
|---|---|
| Datenimport und Tensorisierung | Biosignale in reproduzierbare Fenster- und Tensorform überführen |
| Dysbalance Scores | erklärbare funktionale oder autonom-physiologische Abweichungen berechnen |
| Anomaly Detection | auffällige Fenster modellbasiert und unsupervised markieren |
| MultiRocket | starke diskriminative Zeitreihenmodellierung als Referenzschicht |
| Error-Dysbalance-Linking | prüfen, ob Modellfehler mit erklärbaren Abweichungen zusammenfallen |
| Longitudinal Dysbalance Memory | auffällige Fenster zu Events, Episoden und Hypothesen verdichten |
| TILES-Vorbereitung | Übergang zu echter longitudinaler Realwelt-Evidenz vorbereiten |

## Integrierte Datensätze

| Dataset | Rolle in der Arbeit | Evidenztyp | Status |
|---|---|---|---|
| PAMAP2 | funktional-motorische Hauptentwicklungsebene | kontrollierte Window-Sequenz | integriert |
| WESAD | autonom-affektive Vergleichsdomäne | kontrollierte Window-Sequenz | integriert |
| MHEALTH | externe funktional-motorische Transferprüfung | kontrollierte Window-Sequenz | integriert |
| TILES-2018 | vorbereitete longitudinale Realwelt-Zielschicht | echte Langzeitsequenz, noch ohne lokale Daten | vorbereitet |

## Pipeline-Status

| Pipeline-Baustein | PAMAP2 | WESAD | MHEALTH | TILES-2018 |
|---|---|---|---|---|
| Rohdaten lokal vorhanden | ja | ja | ja | nein |
| Parser / Import | ja | ja | ja | Inventar vorbereitet |
| Tensorisierung | ja | ja | ja | subject-day-Schema vorbereitet |
| Dysbalance Scores | ja | ja | ja | Score-Adapter vorbereitet |
| Isolation Forest | ja | ja | ja | noch nicht datengetrieben |
| MultiRocket | ja | ja | ja | nicht Ziel der ersten TILES-Schicht |
| Memory | ja | ja | ja | optional angebunden |
| echte longitudinale Evidenz | nein | nein | nein | vorbereitet, aber noch nicht aktiv |

## Modellische Hauptergebnisse

| Dataset | Modell | Validierung | Accuracy | Macro-F1 | Kernaussage |
|---|---|---|---:|---:|---|
| MHEALTH | MultiRocket | Leave-One-Subject-Out | 0.9725 | 0.9694 | sehr starke externe funktional-motorische Transferprüfung |
| PAMAP2 | MultiRocket | Leave-One-Subject-Out | 0.9443 | 0.9411 | starke subject-wise Bewegungsmodellierung |
| WESAD | MultiRocket | standardisierter Subject-Split | 0.7730 | 0.6981 | schwierigere autonom-affektive Zustandsmodellierung, aber Verbesserung gegenüber MiniRocket |

## Dysbalance- und Anomaly-Kernaussagen

### PAMAP2

PAMAP2 stützt die funktional-motorische Score-Logik besonders stark.

Die funktionalen Dysbalance Scores stimmen sehr eng mit der modellbasierten Anomaly Detection überein. Zusätzlich zeigt die MultiRocket-Fehleranalyse, dass falsch klassifizierte Fenster im Mittel deutlich höhere funktionale Dysbalance Scores und deutlich höhere Anomaly-Raten aufweisen.

PAMAP2 ist damit der stärkste Brückenbefund der Arbeit.

### WESAD

WESAD bildet die autonom-affektive Vergleichsdomäne.

Die Domäne ist schwieriger, weil baseline, stress, amusement und meditation physiologisch überlappen können. MultiRocket verbessert die standardisierte MiniRocket-Baseline, aber Fehler sind nicht automatisch stärker dysbalanciert.

WESAD ist dadurch methodisch wichtig, weil es zeigt, dass Dysbalance und Klassifikationsfehler domänenspezifisch interpretiert werden müssen.

### MHEALTH

MHEALTH erweitert die Arbeit um eine externe funktional-motorische Transferprüfung.

MultiRocket erreicht hier die höchste subject-wise Leistung. Die Fehleranalyse zeigt jedoch keinen positiven Fehler-Dysbalance-Effekt. Fehler entstehen eher zwischen ähnlichen Bewegungsaktivitäten, insbesondere jogging und running.

MHEALTH verhindert damit ebenfalls eine naive Gleichsetzung von Klassifikationsfehler und Dysbalance.

## MultiRocket als Referenzschicht

MultiRocket ist in dieser Arbeit nicht die Erklärungsschicht.

Die Rolle von MultiRocket besteht darin, zu zeigen, ob robuste subject-übergreifende Zeitreihenstruktur in den Fenstern vorhanden ist.

Die Erklärung entsteht anschließend durch:

- Dysbalance Scores,
- Anomaly Detection,
- Error-Dysbalance-Linking,
- Error-Memory-Linking,
- qualitative Case Studies.

## Wichtigster MultiRocket-Befund

Der wichtigste Befund liegt bei PAMAP2.

Bei PAMAP2 fallen mehrere Ebenen zusammen:

1. Falsch klassifizierte MultiRocket-Fenster.
2. Stark erhöhte funktionale Dysbalance Scores.
3. Stark erhöhte Anomaly-Treffer.
4. Stark erhöhte Memory-Events und Hypothesen.

Damit zeigt PAMAP2, dass Modellunsicherheit in bestimmten funktional-motorischen Kontexten nicht nur ein technisches Problem ist, sondern mit erklärbarer funktionaler Abweichung zusammenfallen kann.

## Wichtigste Gegenbefunde

MHEALTH und WESAD sind genauso wichtig wie PAMAP2.

Sie zeigen:

- Klassifikationsfehler bedeuten nicht automatisch Dysbalance.
- Fehler können durch Klassenähnlichkeit entstehen.
- Fehler können durch physiologische Zustandsüberlappung entstehen.
- Score-, Anomaly-, Modell- und Memory-Ebene müssen getrennt interpretiert werden.

Die Arbeit argumentiert daher nicht:

Klassifikationsfehler sind Dysbalance.

Sondern:

Klassifikationsfehler können in bestimmten Domänen mit Dysbalance, Anomaly Detection und Memory zusammenfallen, müssen aber kontext- und domänenspezifisch interpretiert werden.

## Longitudinal Dysbalance Memory

Das Longitudinal Dysbalance Memory überführt Fensterauffälligkeiten in eine höhere Interpretationsstruktur:

| Struktur | Bedeutung |
|---|---|
| Event | einzelnes auffälliges Fenster oder subject-day |
| Episode | zeitlich benachbarte Events |
| Hypothese | wiederkehrendes oder starkes Muster je Subject, Kontext und Eventtyp |

Aktuell sind PAMAP2, WESAD und MHEALTH integriert.

Da diese Datensätze kontrollierte Sequenzdaten sind, werden die Hypothesen bewusst nicht als echte longitudinale Evidenz interpretiert.

## TILES-2018 Vorbereitung

TILES-2018 ist als echte longitudinale Zielschicht vorbereitet, aber noch nicht datengetrieben integriert.

Implementiert sind:

| Komponente | Status |
|---|---|
| Integrationsplan | vorbereitet |
| Subject-Day-Schema | vorbereitet |
| lokales Inventar | implementiert |
| Schema-Validator | implementiert |
| longitudinaler Score-Adapter | implementiert |
| Memory-Event-Adapter | implementiert |
| optionale Einbindung in das Memory | implementiert |

Aktuell bleibt `true_longitudinal_hypotheses = 0`, weil keine lokalen TILES-subject-day-Daten vorliegen.

Das ist methodisch korrekt: Das Framework ist longitudinal-ready, behauptet aber ohne echte Langzeitdaten keine longitudinale Validierung.

## Wissenschaftlicher Beitrag

Die Arbeit leistet aktuell vier Beiträge.

### 1. Generalisierbare Biosignal-Pipeline

Mehrere heterogene Biosignal-Datensätze werden in ein gemeinsames Verarbeitungsprinzip überführt.

### 2. Erklärbare Dysbalance-Scores

Die Arbeit entwickelt domänenspezifische Scores für funktional-motorische und autonom-physiologische Abweichungen.

### 3. Mehrschichtige Modellinterpretation

Klassifikation, Dysbalance Score, Anomaly Detection und Memory werden nicht vermischt, sondern kontrolliert miteinander verknüpft.

### 4. Longitudinal-ready Framework

Die Memory-Schicht und TILES-Vorbereitung schaffen eine klare Brücke von kontrollierten Datensätzen zu echter Langzeitbeobachtung.

## Ergebnisstruktur für die spätere Thesis

Eine sinnvolle Ergebnisreihenfolge wäre:

1. Datenbasis und Tensorisierung.
2. Dysbalance Score-Entwicklung.
3. Isolation-Forest-Anomaly-Analyse.
4. Longitudinal Dysbalance Memory auf kontrollierten Sequenzen.
5. MultiRocket als starke Zeitreihen-Referenz.
6. Cross-Dataset MultiRocket-Vergleich.
7. Error-Dysbalance- und Error-Memory-Linking.
8. Case Studies.
9. TILES-2018 als vorbereitete longitudinale Erweiterung.
10. Methodische Grenzen und Ausblick.

## Diskussionsstruktur

Die Diskussion sollte besonders folgende Punkte betonen:

| Thema | Argument |
|---|---|
| Generalisierbarkeit | Framework funktioniert über mehrere Biosignal-Domänen hinweg |
| Domänenspezifik | motorische und autonom-affektive Signale verhalten sich unterschiedlich |
| Erklärbarkeit | Scores und Memory verhindern reine Black-Box-Interpretation |
| Fehlerinterpretation | Modellfehler sind nicht automatisch Dysbalance |
| Longitudinalität | aktuelle Ergebnisse sind longitudinal-ready, aber noch nicht longitudinal validiert |
| Datenschutz | TILES und spätere Pilotdaten werden bewusst aggregiert und vorsichtig geplant |

## Grenzen

Wichtige Einschränkungen:

- PAMAP2, WESAD und MHEALTH sind keine echten Langzeitdatensätze.
- Memory-Hypothesen sind keine Diagnosen.
- TILES ist vorbereitet, aber ohne lokale Daten noch nicht datengetrieben integriert.
- Validierungsprotokolle unterscheiden sich zwischen den Datensätzen.
- WESAD wurde für MultiRocket zeitlich reduziert.
- PAMAP2 wurde aus Ressourcengründen mit 5,000 MultiRocket-Kernels ausgewertet.
- Die physiologische Interpretation bleibt dataset- und kontextabhängig.

## Ausblick

Der nächste größere wissenschaftliche Schritt ist echte Longitudinalität.

Dafür gibt es zwei Pfade:

| Pfad | Rolle |
|---|---|
| TILES-2018 | öffentliche longitudinale Realwelt-Ebene, falls Datenzugriff möglich |
| Garmin Forerunner 965 und Polar H10 | spätere eigene explorative Pilotdaten |

Beide Pfade sollen nicht als klinische Validierung verstanden werden, sondern als Prüfung, ob sich die entwickelte Dysbalance-Memory-Architektur auf echte Zeitverläufe übertragen lässt.

## Thesis-Kernsatz

Der Kern der Arbeit lässt sich so formulieren:

Diese Arbeit zeigt, dass multimodale Biosignal-Fenster über verschiedene Datensätze hinweg modellierbare Zeitreihenstruktur enthalten und dass erklärbare Dysbalance Scores, Anomaly Detection und Memory-Strukturen eine vorsichtige, domänenspezifische Interpretation personalisierter physiologischer Abweichungsmuster ermöglichen.

## Zwischenfazit

Die Arbeit steht aktuell an einem sehr guten Übergangspunkt.

Die kontrollierten Datensätze zeigen robuste Modellierbarkeit, erklärbare Score-Strukturen und eine differenzierte Verbindung zwischen Modellfehlern, Anomalien und Memory.

TILES-2018 ist vorbereitet, um die noch offene longitudinale Validierungsfrage später methodisch sauber zu adressieren.
