from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.project_paths import INTERIM_DATA_DIR


INPUT_DIR = INTERIM_DATA_DIR / "mhealth" / "subjects"
OUTPUT_DIR = INTERIM_DATA_DIR / "mhealth" / "by_subject"

WINDOW_SIZE = 250
STEP_SIZE = 125
SAMPLING_RATE_HZ = 50

SIGNAL_COLUMNS = [
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
]


def contiguous_segments(df: pd.DataFrame) -> list[pd.DataFrame]:
    df = df.sort_values("sample_index").reset_index(drop=True).copy()

    label_change = df["label"].ne(df["label"].shift())
    sample_gap = df["sample_index"].diff().fillna(1).ne(1)
    segment_id = (label_change | sample_gap).cumsum()

    return [segment for _, segment in df.groupby(segment_id)]


def window_segment(segment: pd.DataFrame) -> tuple[list[np.ndarray], list[dict]]:
    windows = []
    metadata = []

    values = segment[SIGNAL_COLUMNS].to_numpy(dtype=np.float32)
    labels = segment["label"].to_numpy(dtype=np.int16)

    if len(segment) < WINDOW_SIZE:
        return windows, metadata

    label = int(labels[0])
    activity_name = str(segment["activity_name"].iloc[0])
    subject_id = int(segment["subject_id"].iloc[0])

    for start in range(0, len(segment) - WINDOW_SIZE + 1, STEP_SIZE):
        end = start + WINDOW_SIZE
        window_labels = labels[start:end]

        if not np.all(window_labels == label):
            continue

        original_start = int(segment["sample_index"].iloc[start])
        original_end = int(segment["sample_index"].iloc[end - 1])

        windows.append(values[start:end].T)

        metadata.append(
            {
                "subject_id": subject_id,
                "label": label,
                "activity_name": activity_name,
                "start_sample": original_start,
                "end_sample": original_end,
                "window_size": WINDOW_SIZE,
                "step_size": STEP_SIZE,
                "sampling_rate_hz": SAMPLING_RATE_HZ,
                "duration_seconds": WINDOW_SIZE / SAMPLING_RATE_HZ,
            }
        )

    return windows, metadata


def tensorize_subject(path: Path) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    df = pd.read_csv(path)

    required_columns = {"subject_id", "sample_index", "label", "activity_name", *SIGNAL_COLUMNS}
    missing = sorted(required_columns.difference(df.columns))

    if missing:
        raise ValueError(f"Missing columns in {path.name}: {missing}")

    df = df[df["label"] != 0].copy()

    all_windows = []
    all_metadata = []

    for segment in contiguous_segments(df):
        windows, metadata = window_segment(segment)
        all_windows.extend(windows)
        all_metadata.extend(metadata)

    if not all_windows:
        raise ValueError(f"No windows generated for {path.name}")

    X = np.stack(all_windows).astype(np.float32)
    metadata_df = pd.DataFrame(all_metadata)
    y = metadata_df["label"].to_numpy(dtype=np.int16)

    return X, y, metadata_df


def main() -> None:
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Missing MHEALTH subject directory: {INPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(INPUT_DIR.glob("subject_*.csv.gz"))

    if len(files) != 10:
        raise ValueError(f"Expected 10 parsed subject files, found {len(files)}")

    summaries = []

    for path in files:
        X, y, metadata = tensorize_subject(path)

        subject_id = int(metadata["subject_id"].iloc[0])

        np.save(OUTPUT_DIR / f"subject_{subject_id:02d}_X.npy", X)
        np.save(OUTPUT_DIR / f"subject_{subject_id:02d}_y.npy", y)
        metadata.to_csv(OUTPUT_DIR / f"subject_{subject_id:02d}_metadata.csv", index=False)

        label_counts = metadata["label"].value_counts().sort_index().to_dict()

        summaries.append(
            {
                "subject_id": subject_id,
                "n_windows": int(len(metadata)),
                "n_channels": int(X.shape[1]),
                "window_size": int(X.shape[2]),
                "step_size": STEP_SIZE,
                "sampling_rate_hz": SAMPLING_RATE_HZ,
                "contains_nan": bool(np.isnan(X).any()),
                "labels": ",".join(str(label) for label in sorted(label_counts)),
                "label_counts": ";".join(
                    f"{label}:{count}" for label, count in label_counts.items()
                ),
            }
        )

        print(
            f"subject_{subject_id:02d}: X={X.shape}, "
            f"y={y.shape}, labels={sorted(label_counts)}, "
            f"nan={bool(np.isnan(X).any())}"
        )

    summary = pd.DataFrame(summaries).sort_values("subject_id")
    summary_path = OUTPUT_DIR / "mhealth_tensor_summary.csv"
    summary.to_csv(summary_path, index=False)

    print()
    print("Tensor summary:")
    print(summary.to_string(index=False))

    print()
    print(f"Saved tensor summary to: {summary_path}")


if __name__ == "__main__":
    main()
