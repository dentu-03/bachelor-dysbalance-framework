# Legacy Code Review – KI-Studienprojekt

Dieses Dokument bewertet, welche Teile des alten Studienprojekts in die Bachelorarbeit übernommen werden sollen.

## Grundsatz

Es wird nicht blind kopiert. Alte Skripte dienen als Referenz und werden in saubere Framework-Module überführt.

## Erste Sichtung

### `src/analysis/phase2/windowing.py`

Status: Platzhalter

Bewertung:
Nicht direkt übernehmbar. Für die Bachelorarbeit muss eine allgemeine Windowing-Logik neu erstellt werden.

Geplante neue Position:
`src/preprocessing/windowing.py`

---

### `src/analysis/phase2/rms.py`

Status: einfache RMS-Hilfsfunktion

Bewertung:
Inhaltlich brauchbar. Kann als Grundlage für allgemeine Feature-Funktionen genutzt werden.

Geplante neue Position:
`src/preprocessing/features.py`

---

### `src/analysis/phase3/phase3_multimodal_score.py`

Status: Proof-of-Concept für Score-Fusion

Bewertung:
Wissenschaftlich wichtige Idee, aber technisch zu hardcoded. Die Logik soll verallgemeinert werden.

Geplante neue Position:
`src/dysbalance/fusion.py`

---

## Noch zu prüfen

Folgende Dateien müssen noch gesichtet werden, bevor Funktionen übernommen werden:

- `src/analysis/phase2/emg_dysbalance_poc.py`
- `src/analysis/phase2/stress_poc_wesad.py`
- `src/analysis/build_dataset_inventory.py`
- `src/analysis/sync_inventory_to_sqlite.py`
- Modelltrainingsskripte für MiniRocket/ROCKET

Besonders wichtig:

- Z-Normierung
- Log-Ratio-Berechnung
- Threshold-Sweep
- Report-Erstellung
- SQLite-/Inventory-Logik
