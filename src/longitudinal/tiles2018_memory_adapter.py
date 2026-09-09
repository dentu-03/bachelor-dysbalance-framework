from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.project_paths import DATA_DIR, REPORTS_DIR


INPUT_PATH = DATA_DIR / "processed" / "tiles2018" / "dysbalance" / "tiles2018_longitudinal_scores.csv"
OUTPUT_DIR = REPORTS_DIR / "tiles2018"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EVENTS_CSV = OUTPUT_DIR / "tiles2018_memory_events.csv"
SUMMARY_JSON = OUTPUT_DIR / "tiles2018_memory_adapter_summary.json"
DOC_PATH = Path("docs/results/tiles2018_memory_adapter_summary.md")

SCORE_COLUMN = "longitudinal_deviation_strength"
THRESHOLD = 2.0
HIGH_RANK_PERCENT = 95.0


def safe_float(value) -> float | None:
    if pd.isna(value):
        return None
    return float(value)


def available_component_columns(df: pd.DataFrame) -> list[str]:
    preferred = [
        "z_hr_mean",
        "z_hr_std",
        "z_resting_hr",
        "z_activity_total",
        "z_sedentary_minutes",
        "z_sleep_duration",
        "z_sleep_quality",
    ]
    return [col for col in preferred if col in df.columns]


def component_summary(row: pd.Series, component_cols: list[str]) -> str:
    parts = []
    for col in component_cols:
        value = row.get(col, np.nan)
        if pd.notna(value):
            parts.append(f"{col}={float(value):.3f}")
    return "; ".join(parts)


def create_tiles_events(df: pd.DataFrame) -> pd.DataFrame:
    if SCORE_COLUMN not in df.columns:
        raise ValueError(f"Missing score column: {SCORE_COLUMN}")

    scored = df.copy()
    scored[SCORE_COLUMN] = pd.to_numeric(scored[SCORE_COLUMN], errors="coerce")
    scored["score_rank_percent"] = scored[SCORE_COLUMN].rank(pct=True) * 100.0

    component_cols = available_component_columns(scored)

    rows = []

    for _, row in scored.iterrows():
        strength = safe_float(row[SCORE_COLUMN])
        if strength is None:
            continue

        is_threshold_event = strength >= THRESHOLD
        is_high_rank_event = float(row["score_rank_percent"]) >= HIGH_RANK_PERCENT

        if not (is_threshold_event or is_high_rank_event):
            continue

        if is_threshold_event and is_high_rank_event:
            event_type = "longitudinal_score_high_rank_event"
        elif is_threshold_event:
            event_type = "longitudinal_day_deviation"
        else:
            event_type = "high_rank_longitudinal_deviation"

        context_name = row.get("context_name", "unknown")
        if pd.isna(context_name):
            context_name = "unknown"

        rows.append(
            {
                "dataset": "tiles2018",
                "domain": "longitudinal_real_world",
                "subject_id": str(row["subject_id"]),
                "session_id": f"subject_{row['subject_id']}",
                "source_level": "subject_day",
                "window_index": int(row["day_index"]),
                "start_position": row.get("timestamp_start"),
                "end_position": row.get("timestamp_end"),
                "context_label": row.get("context_label", context_name),
                "context_name": str(context_name),
                "primary_score_name": SCORE_COLUMN,
                "primary_score_value": strength,
                "secondary_score_name": None,
                "secondary_score_value": None,
                "anomaly_score": None,
                "anomaly_score_z": None,
                "anomaly_rank_percent": safe_float(row["score_rank_percent"]),
                "is_threshold_event": bool(is_threshold_event),
                "is_model_anomaly": False,
                "is_high_rank_event": bool(is_high_rank_event),
                "event_strength": strength,
                "event_type": event_type,
                "component_summary": component_summary(row, component_cols),
                "created_from": "tiles2018_subject_day_longitudinal_score",
            }
        )

    events = pd.DataFrame(rows)

    if events.empty:
        return events

    events.insert(0, "event_id", [f"EVT_TILES2018_{i:06d}" for i in range(1, len(events) + 1)])

    return events


def missing_summary() -> dict:
    return {
        "status": "missing_input",
        "input_path": str(INPUT_PATH),
        "events_created": False,
        "reason": "No processed TILES longitudinal score table is available yet.",
        "output_csv": str(EVENTS_CSV),
    }


def completed_summary(events: pd.DataFrame, source_rows: int) -> dict:
    if events.empty:
        return {
            "status": "completed_no_events",
            "input_path": str(INPUT_PATH),
            "events_created": False,
            "source_rows": int(source_rows),
            "n_events": 0,
            "output_csv": str(EVENTS_CSV),
        }

    return {
        "status": "completed",
        "input_path": str(INPUT_PATH),
        "events_created": True,
        "source_rows": int(source_rows),
        "n_events": int(len(events)),
        "n_subjects": int(events["subject_id"].nunique()),
        "event_types": events["event_type"].value_counts().to_dict(),
        "mean_event_strength": float(events["event_strength"].mean()),
        "max_event_strength": float(events["event_strength"].max()),
        "threshold": THRESHOLD,
        "high_rank_percent": HIGH_RANK_PERCENT,
        "output_csv": str(EVENTS_CSV),
    }


def write_doc(summary: dict) -> None:
    lines = []
    lines.append("# TILES-2018 Memory Adapter Summary")
    lines.append("")
    lines.append("Dieses Dokument beschreibt den Status des vorbereiteten TILES-2018-Memory-Adapters.")
    lines.append("")
    lines.append("## Ergebnis")
    lines.append("")
    lines.append(f"- Status: {summary['status']}")
    lines.append(f"- Input: `{summary['input_path']}`")
    lines.append(f"- Output: `{summary['output_csv']}`")
    lines.append(f"- Events created: {summary['events_created']}")
    lines.append("")

    if summary["status"] == "missing_input":
        lines.append("## Interpretation")
        lines.append("")
        lines.append("Aktuell liegt noch keine verarbeitete TILES-Score-Tabelle vor.")
        lines.append("")
        lines.append("Der Adapter ist vorbereitet, erzeugt aber noch keine datengetriebenen Memory-Events.")
        lines.append("")
    elif summary["status"] == "completed_no_events":
        lines.append("## Interpretation")
        lines.append("")
        lines.append("Die TILES-Score-Tabelle wurde gelesen, aber es wurden keine Events oberhalb der definierten Schwellen erzeugt.")
        lines.append("")
    else:
        lines.append("## Event Summary")
        lines.append("")
        lines.append(f"- Source rows: {summary['source_rows']}")
        lines.append(f"- Events: {summary['n_events']}")
        lines.append(f"- Subjects: {summary['n_subjects']}")
        lines.append(f"- Mean event strength: {summary['mean_event_strength']:.4f}")
        lines.append(f"- Max event strength: {summary['max_event_strength']:.4f}")
        lines.append("")
        lines.append("## Event Types")
        lines.append("")
        for event_type, count in summary["event_types"].items():
            lines.append(f"- `{event_type}`: {count}")
        lines.append("")

    lines.append("## Memory-Kompatibilität")
    lines.append("")
    lines.append("Der Adapter erzeugt Events im bestehenden Memory-Schema mit:")
    lines.append("")
    lines.append("- `dataset = tiles2018`")
    lines.append("- `domain = longitudinal_real_world`")
    lines.append("- `source_level = subject_day`")
    lines.append("- `primary_score_name = longitudinal_deviation_strength`")
    lines.append("")
    lines.append("Dadurch kann die bestehende Hypothesenlogik TILES später als echte longitudinale Evidenz behandeln.")
    lines.append("")
    lines.append("## Methodische Vorsicht")
    lines.append("")
    lines.append("Auch bei TILES bleiben Memory-Hypothesen Framework-Hypothesen und keine Diagnosen.")
    lines.append("")

    DOC_PATH.write_text("\n".join(lines))


def main() -> None:
    if not INPUT_PATH.exists():
        summary = missing_summary()
        SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
        write_doc(summary)
        print("=== TILES-2018 Memory Adapter Summary ===")
        print(json.dumps(summary, indent=2))
        print()
        print("Wrote:", DOC_PATH)
        return

    df = pd.read_csv(INPUT_PATH)
    events = create_tiles_events(df)

    if not events.empty:
        events.to_csv(EVENTS_CSV, index=False)

    summary = completed_summary(events, source_rows=len(df))
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
    write_doc(summary)

    print("=== TILES-2018 Memory Adapter Summary ===")
    print(json.dumps(summary, indent=2))
    print()
    if not events.empty:
        print("Saved:", EVENTS_CSV)
    print("Wrote:", DOC_PATH)


if __name__ == "__main__":
    main()
