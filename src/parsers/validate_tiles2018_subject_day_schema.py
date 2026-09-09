from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.project_paths import DATA_DIR, REPORTS_DIR


INPUT_PATH = DATA_DIR / "interim" / "tiles2018" / "subject_day_features.csv"
OUTPUT_DIR = REPORTS_DIR / "tiles2018"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSON = OUTPUT_DIR / "tiles2018_subject_day_schema_validation.json"
DOC_PATH = Path("docs/results/tiles2018_subject_day_schema_validation.md")


REQUIRED_COLUMNS = [
    "dataset",
    "subject_id",
    "day_index",
    "timestamp_start",
    "timestamp_end",
    "source_level",
    "missingness_rate",
]

RECOMMENDED_SIGNAL_COLUMNS = [
    "hr_mean",
    "hr_std",
    "resting_hr",
    "activity_total",
    "sedentary_minutes",
    "sleep_duration",
    "sleep_quality",
    "stress_context",
    "affect_context",
]

DERIVED_COLUMNS = [
    "z_hr_mean",
    "z_hr_std",
    "z_activity_total",
    "z_sleep_duration",
    "z_sleep_quality",
    "longitudinal_deviation_strength",
]

SENSITIVE_COLUMN_HINTS = [
    "audio",
    "voice",
    "transcript",
    "free_text",
    "gps",
    "location",
    "latitude",
    "longitude",
    "bluetooth",
    "proximity",
    "name",
    "email",
]


def validate_existing_table(path: Path) -> dict:
    if not path.exists():
        return {
            "input_path": str(path),
            "exists": False,
            "is_schema_valid": False,
            "reason": "input file missing",
            "n_rows": 0,
            "n_columns": 0,
            "missing_required_columns": REQUIRED_COLUMNS,
            "available_recommended_signal_columns": [],
            "available_derived_columns": [],
            "sensitive_column_hints": [],
            "subjects": 0,
            "min_days_per_subject": None,
            "max_days_per_subject": None,
            "median_days_per_subject": None,
        }

    df = pd.read_csv(path)
    columns = df.columns.tolist()

    missing_required = [col for col in REQUIRED_COLUMNS if col not in columns]
    available_signal = [col for col in RECOMMENDED_SIGNAL_COLUMNS if col in columns]
    available_derived = [col for col in DERIVED_COLUMNS if col in columns]

    sensitive_hits = [
        col for col in columns
        if any(hint in col.lower() for hint in SENSITIVE_COLUMN_HINTS)
    ]

    if "subject_id" in df.columns:
        days_per_subject = df.groupby("subject_id").size()
        subjects = int(days_per_subject.shape[0])
        min_days = int(days_per_subject.min()) if len(days_per_subject) else None
        max_days = int(days_per_subject.max()) if len(days_per_subject) else None
        median_days = float(days_per_subject.median()) if len(days_per_subject) else None
    else:
        subjects = 0
        min_days = None
        max_days = None
        median_days = None

    is_schema_valid = (
        len(missing_required) == 0
        and len(available_signal) >= 1
        and subjects >= 1
        and (min_days is not None and min_days >= 2)
        and len(sensitive_hits) == 0
    )

    return {
        "input_path": str(path),
        "exists": True,
        "is_schema_valid": bool(is_schema_valid),
        "reason": "valid" if is_schema_valid else "schema incomplete or not longitudinally sufficient",
        "n_rows": int(df.shape[0]),
        "n_columns": int(df.shape[1]),
        "missing_required_columns": missing_required,
        "available_recommended_signal_columns": available_signal,
        "available_derived_columns": available_derived,
        "sensitive_column_hints": sensitive_hits,
        "subjects": subjects,
        "min_days_per_subject": min_days,
        "max_days_per_subject": max_days,
        "median_days_per_subject": median_days,
    }


def write_doc(result: dict) -> None:
    lines = []
    lines.append("# TILES-2018 Subject-Day Schema Validation")
    lines.append("")
    lines.append("Dieses Dokument prüft, ob lokal bereits eine kanonische TILES-subject-day-Tabelle vorliegt.")
    lines.append("")
    lines.append("## Ergebnis")
    lines.append("")
    lines.append(f"- Input: `{result['input_path']}`")
    lines.append(f"- Exists: {result['exists']}")
    lines.append(f"- Schema valid: {result['is_schema_valid']}")
    lines.append(f"- Reason: {result['reason']}")
    lines.append(f"- Rows: {result['n_rows']}")
    lines.append(f"- Columns: {result['n_columns']}")
    lines.append(f"- Subjects: {result['subjects']}")
    lines.append(f"- Min days per subject: {result['min_days_per_subject']}")
    lines.append(f"- Max days per subject: {result['max_days_per_subject']}")
    lines.append(f"- Median days per subject: {result['median_days_per_subject']}")
    lines.append("")
    lines.append("## Missing required columns")
    lines.append("")
    if result["missing_required_columns"]:
        for col in result["missing_required_columns"]:
            lines.append(f"- `{col}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Available recommended signal columns")
    lines.append("")
    if result["available_recommended_signal_columns"]:
        for col in result["available_recommended_signal_columns"]:
            lines.append(f"- `{col}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Sensitive column hints")
    lines.append("")
    if result["sensitive_column_hints"]:
        for col in result["sensitive_column_hints"]:
            lines.append(f"- `{col}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if result["is_schema_valid"]:
        lines.append("Die Tabelle ist grundsätzlich für eine fokussierte longitudinale TILES-Integration geeignet.")
    else:
        lines.append("Aktuell liegt noch keine nutzbare kanonische subject-day-Tabelle vor. Die TILES-Schicht bleibt daher vorbereitet, aber noch nicht datengetrieben integriert.")
    lines.append("")

    DOC_PATH.write_text("\n".join(lines))


def main() -> None:
    result = validate_existing_table(INPUT_PATH)
    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    write_doc(result)

    print("=== TILES-2018 Subject-Day Schema Validation ===")
    print(json.dumps(result, indent=2))
    print()
    print("Saved:", OUTPUT_JSON)
    print("Wrote:", DOC_PATH)


if __name__ == "__main__":
    main()
