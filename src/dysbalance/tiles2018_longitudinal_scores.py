from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.project_paths import DATA_DIR, REPORTS_DIR


INPUT_PATH = DATA_DIR / "interim" / "tiles2018" / "subject_day_features.csv"
OUTPUT_DIR = DATA_DIR / "processed" / "tiles2018" / "dysbalance"
REPORT_DIR = REPORTS_DIR / "tiles2018"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "tiles2018_longitudinal_scores.csv"
SUMMARY_JSON = REPORT_DIR / "tiles2018_longitudinal_score_summary.json"
DOC_PATH = Path("docs/results/tiles2018_longitudinal_score_summary.md")


BASE_SIGNAL_COLUMNS = [
    "hr_mean",
    "hr_std",
    "resting_hr",
    "activity_total",
    "sedentary_minutes",
    "sleep_duration",
    "sleep_quality",
]

REQUIRED_COLUMNS = [
    "dataset",
    "subject_id",
    "day_index",
    "timestamp_start",
    "timestamp_end",
    "source_level",
    "missingness_rate",
]


def robust_z_by_subject(df: pd.DataFrame, column: str) -> pd.Series:
    values = pd.to_numeric(df[column], errors="coerce")
    out = pd.Series(np.nan, index=df.index, dtype=float)

    for subject_id, idx in df.groupby("subject_id").groups.items():
        subject_values = values.loc[idx]
        median = subject_values.median(skipna=True)
        mad = (subject_values - median).abs().median(skipna=True)

        if pd.isna(median) or pd.isna(mad) or mad == 0:
            mean = subject_values.mean(skipna=True)
            std = subject_values.std(skipna=True)
            if pd.isna(mean) or pd.isna(std) or std == 0:
                out.loc[idx] = 0.0
            else:
                out.loc[idx] = (subject_values - mean) / std
        else:
            out.loc[idx] = 0.6745 * (subject_values - median) / mad

    return out


def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    available_signal_columns = [
        col for col in BASE_SIGNAL_COLUMNS
        if col in result.columns
    ]

    z_columns = []
    for col in available_signal_columns:
        z_col = f"z_{col}"
        result[z_col] = robust_z_by_subject(result, col)
        z_columns.append(z_col)

    if not z_columns:
        raise ValueError("No usable signal columns available for TILES longitudinal scoring.")

    z_matrix = result[z_columns].abs()
    result["longitudinal_deviation_strength"] = np.sqrt((z_matrix ** 2).mean(axis=1))

    result["domain"] = "longitudinal_real_world"
    result["primary_score_name"] = "longitudinal_deviation_strength"
    result["primary_score_value"] = result["longitudinal_deviation_strength"]
    result["evidence_scope"] = "longitudinal_real_world_sequence"
    result["is_true_longitudinal_evidence"] = True

    if "context_name" not in result.columns:
        result["context_name"] = "unknown"

    return result


def build_missing_summary() -> dict:
    return {
        "input_path": str(INPUT_PATH),
        "status": "missing_input",
        "scores_created": False,
        "reason": "No local subject-day feature table is available yet.",
        "required_input": "data/interim/tiles2018/subject_day_features.csv",
        "output_csv": str(OUTPUT_CSV),
    }


def build_summary(scored: pd.DataFrame, z_columns: list[str]) -> dict:
    subject_counts = scored.groupby("subject_id").size()

    return {
        "input_path": str(INPUT_PATH),
        "status": "completed",
        "scores_created": True,
        "n_rows": int(scored.shape[0]),
        "n_subjects": int(scored["subject_id"].nunique()),
        "min_days_per_subject": int(subject_counts.min()),
        "max_days_per_subject": int(subject_counts.max()),
        "median_days_per_subject": float(subject_counts.median()),
        "z_columns": z_columns,
        "score_column": "longitudinal_deviation_strength",
        "mean_score": float(scored["longitudinal_deviation_strength"].mean()),
        "median_score": float(scored["longitudinal_deviation_strength"].median()),
        "max_score": float(scored["longitudinal_deviation_strength"].max()),
        "output_csv": str(OUTPUT_CSV),
    }


def validate_required_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def write_doc(summary: dict) -> None:
    lines = []
    lines.append("# TILES-2018 Longitudinal Score Summary")
    lines.append("")
    lines.append("Dieses Dokument beschreibt den Status der vorbereiteten TILES-2018-Score-Schicht.")
    lines.append("")
    lines.append("## Ergebnis")
    lines.append("")
    lines.append(f"- Status: {summary['status']}")
    lines.append(f"- Scores created: {summary['scores_created']}")
    lines.append(f"- Input: `{summary['input_path']}`")
    lines.append(f"- Output: `{summary['output_csv']}`")
    lines.append("")

    if summary["status"] == "missing_input":
        lines.append("## Interpretation")
        lines.append("")
        lines.append("Aktuell liegt lokal noch keine kanonische TILES-subject-day-Tabelle vor.")
        lines.append("")
        lines.append("Die Score-Schicht ist daher vorbereitet, aber noch nicht datengetrieben ausgeführt.")
        lines.append("")
        lines.append("Sobald `data/interim/tiles2018/subject_day_features.csv` existiert, erzeugt das Skript subject-normalisierte longitudinale Dysbalance Scores.")
        lines.append("")
    elif summary["status"] == "schema_error":
        lines.append("## Schema Error")
        lines.append("")
        lines.append("Die vorhandene Tabelle erfüllt das kanonische Subject-Day-Schema noch nicht vollständig.")
        lines.append("")
        for col in summary["missing_required_columns"]:
            lines.append(f"- missing: `{col}`")
        lines.append("")
    else:
        lines.append("## Score Statistics")
        lines.append("")
        lines.append(f"- Rows: {summary['n_rows']}")
        lines.append(f"- Subjects: {summary['n_subjects']}")
        lines.append(f"- Min days per subject: {summary['min_days_per_subject']}")
        lines.append(f"- Max days per subject: {summary['max_days_per_subject']}")
        lines.append(f"- Median days per subject: {summary['median_days_per_subject']}")
        lines.append(f"- Mean score: {summary['mean_score']:.4f}")
        lines.append(f"- Median score: {summary['median_score']:.4f}")
        lines.append(f"- Max score: {summary['max_score']:.4f}")
        lines.append("")
        lines.append("## Z columns")
        lines.append("")
        for col in summary["z_columns"]:
            lines.append(f"- `{col}`")
        lines.append("")

    lines.append("## Methodische Einordnung")
    lines.append("")
    lines.append("Die TILES-Score-Schicht ist bewusst subject-normalisiert. Dadurch wird nicht ein globaler Normwert modelliert, sondern die Abweichung vom individuellen Referenzzustand.")
    lines.append("")
    lines.append("Für die Thesis ist diese Schicht der Übergang von kontrollierten Window-Sequenzen zu echter longitudinaler Realwelt-Evidenz.")
    lines.append("")

    DOC_PATH.write_text("\n".join(lines))


def main() -> None:
    if not INPUT_PATH.exists():
        summary = build_missing_summary()
        SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
        write_doc(summary)
        print("=== TILES-2018 Longitudinal Score Summary ===")
        print(json.dumps(summary, indent=2))
        print()
        print("Wrote:", DOC_PATH)
        return

    df = pd.read_csv(INPUT_PATH)
    missing = validate_required_columns(df)

    if missing:
        summary = {
            "input_path": str(INPUT_PATH),
            "status": "schema_error",
            "scores_created": False,
            "missing_required_columns": missing,
            "output_csv": str(OUTPUT_CSV),
        }
        SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
        write_doc(summary)
        print("=== TILES-2018 Longitudinal Score Summary ===")
        print(json.dumps(summary, indent=2))
        print()
        print("Wrote:", DOC_PATH)
        return

    scored = compute_scores(df)
    z_columns = [col for col in scored.columns if col.startswith("z_")]

    scored.to_csv(OUTPUT_CSV, index=False)
    summary = build_summary(scored, z_columns)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
    write_doc(summary)

    print("=== TILES-2018 Longitudinal Score Summary ===")
    print(json.dumps(summary, indent=2))
    print()
    print("Saved:", OUTPUT_CSV)
    print("Wrote:", DOC_PATH)


if __name__ == "__main__":
    main()
