from pathlib import Path
import pandas as pd

from src.project_paths import RAW_DATA_DIR, REPORTS_DIR


IMU_CHANNELS = [
    "temperature",
    "acc16_x", "acc16_y", "acc16_z",
    "acc6_x", "acc6_y", "acc6_z",
    "gyro_x", "gyro_y", "gyro_z",
    "mag_x", "mag_y", "mag_z",
    "orientation_0", "orientation_1", "orientation_2", "orientation_3",
]


def build_pamap2_columns() -> list[str]:
    """Return the 54 official PAMAP2 column names."""
    columns = ["timestamp", "activity_id", "heart_rate"]

    for sensor_position in ["hand", "chest", "ankle"]:
        for channel in IMU_CHANNELS:
            columns.append(f"{sensor_position}_{channel}")

    if len(columns) != 54:
        raise ValueError(f"Expected 54 columns, got {len(columns)}")

    return columns


def load_subject_file(path: Path) -> pd.DataFrame:
    """Load one PAMAP2 subject file with named columns."""
    subject_id = path.stem.replace("subject", "")

    df = pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=build_pamap2_columns(),
        na_values=["NaN"],
    )

    df.insert(0, "subject_id", subject_id)
    return df


def summarize_protocol_files() -> pd.DataFrame:
    """Create a basic summary of all PAMAP2 protocol files."""
    protocol_dir = RAW_DATA_DIR / "pamap2" / "PAMAP2_Dataset" / "Protocol"
    files = sorted(protocol_dir.glob("subject*.dat"))

    if not files:
        raise FileNotFoundError(f"No PAMAP2 subject files found in {protocol_dir}")

    rows = []

    for file in files:
        df = load_subject_file(file)

        rows.append(
            {
                "file": file.name,
                "subject_id": df["subject_id"].iloc[0],
                "n_rows": len(df),
                "n_columns": df.shape[1],
                "n_activity_labels": df["activity_id"].nunique(dropna=True),
                "activity_labels": sorted(df["activity_id"].dropna().unique().tolist()),
                "heart_rate_missing_pct": round(df["heart_rate"].isna().mean() * 100, 2),
                "timestamp_start": df["timestamp"].min(),
                "timestamp_end": df["timestamp"].max(),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    out_dir = REPORTS_DIR / "datasets"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = summarize_protocol_files()

    out_csv = out_dir / "pamap2_protocol_summary.csv"
    summary.to_csv(out_csv, index=False)

    print(summary.to_string(index=False))
    print()
    print(f"Saved summary to: {out_csv}")


if __name__ == "__main__":
    main()
