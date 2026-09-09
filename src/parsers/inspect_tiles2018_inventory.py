from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.project_paths import DATA_DIR, REPORTS_DIR


RAW_DIR = DATA_DIR / "raw" / "tiles2018"
OUTPUT_DIR = REPORTS_DIR / "tiles2018"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "tiles2018_local_inventory.csv"
OUTPUT_JSON = OUTPUT_DIR / "tiles2018_local_inventory_summary.json"
DOC_PATH = Path("docs/results/tiles2018_feasibility_inventory.md")


SENSITIVE_HINTS = [
    "audio",
    "voice",
    "transcript",
    "bluetooth",
    "proximity",
    "location",
    "gps",
    "survey_text",
    "free_text",
]


def classify_file(path: Path) -> dict:
    rel = path.relative_to(RAW_DIR)
    suffix = path.suffix.lower()
    name_lower = path.name.lower()
    rel_lower = str(rel).lower()

    sensitivity_hints = [
        hint for hint in SENSITIVE_HINTS
        if hint in name_lower or hint in rel_lower
    ]

    if suffix in {".csv", ".tsv"}:
        file_type = "tabular"
    elif suffix in {".json"}:
        file_type = "json"
    elif suffix in {".pkl", ".pickle"}:
        file_type = "pickle"
    elif suffix in {".zip", ".gz", ".tar"}:
        file_type = "archive"
    elif suffix in {".txt", ".md", ".pdf"}:
        file_type = "documentation"
    else:
        file_type = "other"

    return {
        "relative_path": str(rel),
        "file_name": path.name,
        "suffix": suffix,
        "file_type": file_type,
        "size_bytes": path.stat().st_size,
        "size_mb": path.stat().st_size / 1024 / 1024,
        "parent": str(rel.parent),
        "sensitivity_hints": ";".join(sensitivity_hints),
        "has_sensitivity_hint": bool(sensitivity_hints),
    }


def build_inventory() -> pd.DataFrame:
    if not RAW_DIR.exists():
        return pd.DataFrame()

    records = [
        classify_file(path)
        for path in sorted(RAW_DIR.rglob("*"))
        if path.is_file()
    ]

    return pd.DataFrame(records)


def write_doc(inventory: pd.DataFrame, summary: dict) -> None:
    lines = []
    lines.append("# TILES-2018 Feasibility Inventory")
    lines.append("")
    lines.append("Dieses Dokument beschreibt den lokalen TILES-2018-Inventarstatus.")
    lines.append("")
    lines.append("Das Inventar wertet keine Inhalte aus. Es prüft nur Dateipfade, Dateitypen und Größen.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Raw directory: `{RAW_DIR}`")
    lines.append(f"- Files found: {summary['n_files']}")
    lines.append(f"- Total size MB: {summary['total_size_mb']:.3f}")
    lines.append(f"- Files with sensitivity hints: {summary['n_files_with_sensitivity_hints']}")
    lines.append("")
    lines.append("## File types")
    lines.append("")
    lines.append("| File type | Count | Size MB |")
    lines.append("|---|---:|---:|")

    for item in summary["file_type_summary"]:
        lines.append(f"| {item['file_type']} | {item['count']} | {item['size_mb']:.3f} |")

    lines.append("")
    lines.append("## Sensitivity handling")
    lines.append("")
    lines.append("Dateien mit möglichen Sensitivitätshinweisen sollen nicht automatisch in die Dysbalance-Pipeline übernommen werden.")
    lines.append("")
    lines.append("Für die Bachelorarbeit priorisiert die TILES-Integration aggregierte physiologische oder behaviorale Zeitreihen und vermeidet Audio-, Text-, Standort- oder Identifikationsinhalte.")
    lines.append("")
    lines.append("## Next decision")
    lines.append("")
    if summary["n_files"] == 0:
        lines.append("Aktuell sind lokal noch keine TILES-Dateien vorhanden. Die Integration bleibt daher eine vorbereitete Feasibility-Schicht.")
    else:
        lines.append("Als nächstes muss geprüft werden, ob mindestens eine nutzbare subject-day- oder subject-window-Tabelle mit physiologischen oder behavioralen Features vorhanden ist.")

    lines.append("")

    DOC_PATH.write_text("\n".join(lines))


def main() -> None:
    inventory = build_inventory()

    if inventory.empty:
        inventory = pd.DataFrame(
            columns=[
                "relative_path",
                "file_name",
                "suffix",
                "file_type",
                "size_bytes",
                "size_mb",
                "parent",
                "sensitivity_hints",
                "has_sensitivity_hint",
            ]
        )

    file_type_summary = (
        inventory.groupby("file_type", dropna=False)
        .agg(count=("relative_path", "size"), size_mb=("size_mb", "sum"))
        .reset_index()
        .sort_values(["count", "file_type"], ascending=[False, True])
        .to_dict(orient="records")
    )

    summary = {
        "raw_dir": str(RAW_DIR),
        "n_files": int(len(inventory)),
        "total_size_mb": float(inventory["size_mb"].sum()) if len(inventory) else 0.0,
        "n_files_with_sensitivity_hints": int(inventory["has_sensitivity_hint"].sum()) if len(inventory) else 0,
        "file_type_summary": file_type_summary,
    }

    inventory.to_csv(OUTPUT_CSV, index=False)
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2))
    write_doc(inventory, summary)

    print("=== TILES-2018 Local Inventory Summary ===")
    print(json.dumps(summary, indent=2))
    print()
    print("Saved:", OUTPUT_CSV)
    print("Saved:", OUTPUT_JSON)
    print("Wrote:", DOC_PATH)


if __name__ == "__main__":
    main()
