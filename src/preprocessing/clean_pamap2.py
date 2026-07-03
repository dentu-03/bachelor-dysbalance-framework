from pathlib import Path
import pandas as pd

from src.project_paths import RAW_DATA_DIR, REPORTS_DIR
from src.parsers.parse_pamap2 import load_subject_file


SELECTED_COLUMNS = [
    "subject_id",
    "timestamp",
    "activity_id",
    "heart_rate",

    "hand_acc16_x", "hand_acc16_y", "hand_acc16_z",
    "hand_gyro_x", "hand_gyro_y", "hand_gyro_z",

    "chest_acc16_x", "chest_acc16_y", "chest_acc16_z",
    "chest_gyro_x", "chest_gyro_y", "chest_gyro_z",

    "ankle_acc16_x", "ankle_acc16_y", "ankle_acc16_z",
    "ankle_gyro_x", "ankle_gyro_y", "ankle_gyro_z",
]


def select_initial_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select the initial explainable PAMAP2 signal subset."""
    missing = [column for column in SELECTED_COLUMNS if column not in df.columns]

    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    return df[SELECTED_COLUMNS].copy()


def filter_initial_pipeline_rows(
    df: pd.DataFrame,
    exclude_activity_zero: bool = True,
    exclude_subject_109: bool = True,
) -> pd.DataFrame:
    """Apply first-pass filtering decisions for the initial PAMAP2 pipeline."""
    filtered = df.copy()

    if exclude_activity_zero:
        filtered = filtered[filtered["activity_id"] != 0]

    if exclude_subject_109:
        filtered = filtered[filtered["subject_id"] != "109"]

    return filtered.reset_index(drop=True)


def summarize_initial_cleaning() -> pd.DataFrame:
    """Summarize row counts and missingness after first-pass cleaning."""
    protocol_dir = RAW_DATA_DIR / "pamap2" / "PAMAP2_Dataset" / "Protocol"
    files = sorted(protocol_dir.glob("subject*.dat"))

    if not files:
        raise FileNotFoundError(f"No PAMAP2 subject files found in {protocol_dir}")

    rows = []

    for file in files:
        raw_df = load_subject_file(file)
        selected_df = select_initial_columns(raw_df)
        clean_df = filter_initial_pipeline_rows(selected_df)

        rows.append(
            {
                "file": file.name,
                "subject_id": raw_df["subject_id"].iloc[0],
                "raw_rows": len(raw_df),
                "selected_columns": selected_df.shape[1],
                "clean_rows": len(clean_df),
                "removed_rows": len(raw_df) - len(clean_df),
                "remaining_activity_labels": sorted(
                    clean_df["activity_id"].dropna().unique().tolist()
                ),
                "heart_rate_missing_pct_after_cleaning": round(
                    clean_df["heart_rate"].isna().mean() * 100, 2
                ) if len(clean_df) > 0 else None,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    out_dir = REPORTS_DIR / "datasets"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = summarize_initial_cleaning()

    out_csv = out_dir / "pamap2_initial_cleaning_summary.csv"
    summary.to_csv(out_csv, index=False)

    print(summary.to_string(index=False))
    print()
    print(f"Saved summary to: {out_csv}")


if __name__ == "__main__":
    main()
