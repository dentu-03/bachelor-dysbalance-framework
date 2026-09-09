# TILES-2018 Memory Adapter Summary

Dieses Dokument beschreibt den Status des vorbereiteten TILES-2018-Memory-Adapters.

## Ergebnis

- Status: missing_input
- Input: `/home/dennis_preusch/Dokumente/UNI/6.Semester/Thesis/bachelor-dysbalance-framework/data/processed/tiles2018/dysbalance/tiles2018_longitudinal_scores.csv`
- Output: `/home/dennis_preusch/Dokumente/UNI/6.Semester/Thesis/bachelor-dysbalance-framework/reports/tiles2018/tiles2018_memory_events.csv`
- Events created: False

## Interpretation

Aktuell liegt noch keine verarbeitete TILES-Score-Tabelle vor.

Der Adapter ist vorbereitet, erzeugt aber noch keine datengetriebenen Memory-Events.

## Memory-Kompatibilität

Der Adapter erzeugt Events im bestehenden Memory-Schema mit:

- `dataset = tiles2018`
- `domain = longitudinal_real_world`
- `source_level = subject_day`
- `primary_score_name = longitudinal_deviation_strength`

Dadurch kann die bestehende Hypothesenlogik TILES später als echte longitudinale Evidenz behandeln.

## Methodische Vorsicht

Auch bei TILES bleiben Memory-Hypothesen Framework-Hypothesen und keine Diagnosen.
