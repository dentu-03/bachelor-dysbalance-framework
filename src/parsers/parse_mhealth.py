from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.project_paths import INTERIM_DATA_DIR, RAW_DATA_DIR


RAW_DIR = RAW_DATA_DIR / "mhealth" / "MHEALTHDATASET"
OUTPUT_DIR = INTERIM_DATA_DIR / "mhealth"

COLUMN_NAMES = [
    "chest_acc_x",
    "chest_acc_y",
    "chest_acc_z",
    "ecg_lead_1",
    "ecg_lead_2",
    "ankle_acc_x",
    "ankle_acc_y",
    "ankle_acc_z",
    "ankle_gyro_x",
    "ankle_gyro_y",
    "ankle_gyro_z",
    "ankle_mag_x",
    "ankle_mag_y",
    "ankle_mag_z",
    "arm_acc_x",
    "arm_acc_y",
    "arm_acc_z",
    "arm_gyro_x",
    "arm_gyro_y",
    "arm_gyro_z",
    "arm_mag_x",
    "arm_mag_y",
    "arm_mag_z",
    "label",
]

ACTIVITY_LABELS = {
    0: "null",
    1: "standing_still",
    2: "sitting_relaxing",
    3: "lying_down",
    4: "walking",
    5: "climbing_stairs",
    6: "waist_bends_forward",
    7: "frontal_elevation_arms",
    8: "knees_bending",
    9: "cycling",
    10: "jogging",
    11: "running",
    12: "jump_front_back",
}


def subject_id_from_path(path: Path) -> int:
    stem = path.stem
    return int(stem.replace("mHealth_subject", ""))


def load_subject_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=r"\s+", header=None)

    if df.shape[1] != len(COLUMN_NAMES):
        raise ValueError(
            f"Expected {len(COLUMN_NAMES)} columns in {path.name}, got {df.shape[1]}"
        )

    df.columns = COLUMN_NAMES

    subject_id = subject_id_from_path(path)
    df.insert(0, "subject_id", subject_id)
    df.insert(1, "sample_index", range(len(df)))

    df["label"] = df["label"].astype(int)
    df["activity_name"] = df["label"].map(ACTIVITY_LABELS)

    if df["activity_name"].isna().any():
        unknown = sorted(df.loc[df["activity_name"].isna(), "label"].unique().tolist())
        raise ValueError(f"Unknown labels in {path.name}: {unknown}")

    return df


def summarize_subject(df: pd.DataFrame, source_file: str) -> dict:
    labels = sorted(df["label"].unique().tolist())

    return {
        "source_file": source_file,
        "subject_id": int(df["subject_id"].iloc[0]),
        "n_rows": int(len(df)),
        "n_columns_raw": len(COLUMN_NAMES),
        "n_columns_with_metadata": int(df.shape[1]),
        "labels": ",".join(str(label) for label in labels),
        "n_missing_values": int(df.isna().sum().sum()),
        "n_null_label_rows": int((df["label"] == 0).sum()),
        "n_activity_rows": int((df["label"] != 0).sum()),
    }


def build_label_summary(all_subjects: list[pd.DataFrame]) -> pd.DataFrame:
    combined = pd.concat(
        [df[["subject_id", "label", "activity_name"]] for df in all_subjects],
        ignore_index=True,
    )

    summary = (
        combined.groupby(["subject_id", "label", "activity_name"])
        .size()
        .reset_index(name="n_rows")
        .sort_values(["subject_id", "label"])
        .reset_index(drop=True)
    )

    return summary


def main() -> None:
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Missing raw MHEALTH directory: {RAW_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    subject_dir = OUTPUT_DIR / "subjects"
    subject_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(RAW_DIR.glob("mHealth_subject*.log"))

    if len(files) != 10:
        raise ValueError(f"Expected 10 subject files, found {len(files)}")

    subject_summaries = []
    all_subjects = []

    for path in files:
        df = load_subject_file(path)

        subject_id = int(df["subject_id"].iloc[0])
        output_path = subject_dir / f"subject_{subject_id:02d}.csv.gz"

        df.to_csv(output_path, index=False, compression="gzip")

        subject_summaries.append(summarize_subject(df, path.name))
        all_subjects.append(df)

        print(
            f"{path.name}: rows={len(df)}, "
            f"cols={df.shape[1]}, "
            f"labels={sorted(df['label'].unique().tolist())}, "
            f"missing={int(df.isna().sum().sum())}"
        )

    subject_summary = pd.DataFrame(subject_summaries).sort_values("subject_id")
    label_summary = build_label_summary(all_subjects)

    subject_summary_path = OUTPUT_DIR / "mhealth_subject_summary.csv"
    label_summary_path = OUTPUT_DIR / "mhealth_label_distribution.csv"

    subject_summary.to_csv(subject_summary_path, index=False)
    label_summary.to_csv(label_summary_path, index=False)

    print()
    print("Subject summary:")
    print(subject_summary.to_string(index=False))

    print()
    print("Label distribution preview:")
    print(label_summary.head(30).to_string(index=False))

    print()
    print(f"Saved subject files to: {subject_dir}")
    print(f"Saved subject summary to: {subject_summary_path}")
    print(f"Saved label distribution to: {label_summary_path}")


if __name__ == "__main__":
    main()
