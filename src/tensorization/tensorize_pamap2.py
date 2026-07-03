import numpy as np
import pandas as pd

from src.project_paths import INTERIM_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR
from src.preprocessing.imputation import impute_tensor_channel_median
from src.tensorization.windowing import window_array, majority_labels, window_timestamps


VALID_SUBJECT_IDS = ["101", "102", "103", "104", "105", "106", "107", "108"]


SIGNAL_COLUMNS = [
    "heart_rate",

    "hand_acc16_x", "hand_acc16_y", "hand_acc16_z",
    "hand_gyro_x", "hand_gyro_y", "hand_gyro_z",

    "chest_acc16_x", "chest_acc16_y", "chest_acc16_z",
    "chest_gyro_x", "chest_gyro_y", "chest_gyro_z",

    "ankle_acc16_x", "ankle_acc16_y", "ankle_acc16_z",
    "ankle_gyro_x", "ankle_gyro_y", "ankle_gyro_z",
]


def load_clean_subject(subject_id: str) -> pd.DataFrame:
    """Load one cleaned PAMAP2 subject file."""
    path = (
        INTERIM_DATA_DIR
        / "pamap2"
        / "protocol_cleaned"
        / f"subject{subject_id}_cleaned.pkl.gz"
    )

    if not path.exists():
        raise FileNotFoundError(f"Cleaned subject file not found: {path}")

    return pd.read_pickle(path)


def add_contiguous_segment_ids(
    df: pd.DataFrame,
    max_time_gap_seconds: float = 0.05,
) -> pd.DataFrame:
    """
    Add segment IDs for contiguous PAMAP2 sequences.

    A new segment starts when:
    - the timestamp gap is larger than expected for 100 Hz data
    - the activity label changes
    """
    df = df.copy().reset_index(drop=True)

    time_gap = df["timestamp"].diff().fillna(0)
    activity_change = df["activity_id"].ne(df["activity_id"].shift()).fillna(False)

    new_segment = (time_gap > max_time_gap_seconds) | activity_change
    df["segment_id"] = new_segment.cumsum().astype(int)

    return df


def interpolate_heart_rate_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Interpolate heart rate inside each contiguous segment only.

    This avoids interpolating HR values across removed transient activity gaps.
    """
    df = df.copy()

    df["heart_rate"] = (
        df.groupby("segment_id", group_keys=False)["heart_rate"]
        .apply(lambda s: s.interpolate(method="linear", limit_direction="both").ffill().bfill())
    )

    return df


def tensorize_subject(
    subject_id: str,
    window_size: int = 500,
    step_size: int = 250,
    max_time_gap_seconds: float = 0.05,
) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """
    Tensorize one cleaned PAMAP2 subject using contiguous same-activity segments.

    Default setting assumes 100 Hz IMU data:
    - window_size=500 means approximately 5 seconds
    - step_size=250 means 50 percent overlap
    """
    df = load_clean_subject(subject_id)
    df = add_contiguous_segment_ids(
        df,
        max_time_gap_seconds=max_time_gap_seconds,
    )
    df = interpolate_heart_rate_by_segment(df)

    X_parts = []
    y_parts = []
    metadata_rows = []

    global_window_index = 0

    for segment_id, segment_df in df.groupby("segment_id", sort=True):
        if len(segment_df) < window_size:
            continue

        values = segment_df[SIGNAL_COLUMNS].to_numpy(dtype=float)
        labels = segment_df["activity_id"].to_numpy()
        timestamps = segment_df["timestamp"].to_numpy(dtype=float)

        X_segment, starts = window_array(
            values=values,
            window_size=window_size,
            step_size=step_size,
        )

        y_segment = majority_labels(labels, starts=starts, window_size=window_size)
        t_start, t_end = window_timestamps(
            timestamps=timestamps,
            starts=starts,
            window_size=window_size,
        )

        X_parts.append(X_segment)
        y_parts.append(y_segment)

        original_indices = segment_df.index.to_numpy()

        for local_i, start in enumerate(starts):
            metadata_rows.append(
                {
                    "subject_id": subject_id,
                    "window_index": global_window_index,
                    "segment_id": int(segment_id),
                    "segment_activity_id": int(segment_df["activity_id"].iloc[0]),
                    "start_row": int(original_indices[start]),
                    "end_row": int(original_indices[start + window_size - 1]),
                    "timestamp_start": float(t_start[local_i]),
                    "timestamp_end": float(t_end[local_i]),
                    "activity_id": int(y_segment[local_i]),
                }
            )
            global_window_index += 1

    if not X_parts:
        raise ValueError(f"No windows generated for subject {subject_id}")

    X = np.concatenate(X_parts, axis=0)
    y = np.concatenate(y_parts, axis=0)
    metadata = pd.DataFrame(metadata_rows)

    return X, y, metadata


def save_subject_tensor(
    subject_id: str,
    out_dir,
    window_size: int = 500,
    step_size: int = 250,
) -> dict:
    """Tensorize, impute and save one PAMAP2 subject."""
    X, y, metadata = tensorize_subject(
        subject_id=subject_id,
        window_size=window_size,
        step_size=step_size,
    )

    nan_before = int(np.isnan(X).sum())
    X, channel_medians = impute_tensor_channel_median(X)
    nan_after = int(np.isnan(X).sum())

    np.save(out_dir / f"X_subject{subject_id}.npy", X)
    np.save(out_dir / f"y_subject{subject_id}.npy", y)
    np.save(out_dir / f"channel_medians_subject{subject_id}.npy", channel_medians)
    metadata.to_csv(out_dir / f"metadata_subject{subject_id}.csv", index=False)

    durations = metadata["timestamp_end"] - metadata["timestamp_start"]
    label_counts = metadata["activity_id"].value_counts().sort_index()

    return {
        "subject_id": subject_id,
        "n_windows": int(X.shape[0]),
        "n_channels": int(X.shape[1]),
        "n_timepoints": int(X.shape[2]),
        "n_labels": int(label_counts.shape[0]),
        "nan_before_imputation": nan_before,
        "nan_after_imputation": nan_after,
        "windows_longer_than_5_2_seconds": int((durations > 5.2).sum()),
        "duration_min": float(durations.min()),
        "duration_mean": float(durations.mean()),
        "duration_max": float(durations.max()),
        "label_counts": dict(label_counts),
    }


def main() -> None:
    window_size = 500
    step_size = 250

    out_dir = PROCESSED_DATA_DIR / "pamap2" / "by_subject"
    out_dir.mkdir(parents=True, exist_ok=True)

    report_dir = REPORTS_DIR / "datasets"
    report_dir.mkdir(parents=True, exist_ok=True)

    rows = []

    for subject_id in VALID_SUBJECT_IDS:
        print(f"Tensorizing subject {subject_id} ...")
        row = save_subject_tensor(
            subject_id=subject_id,
            out_dir=out_dir,
            window_size=window_size,
            step_size=step_size,
        )
        rows.append(row)

        print(
            f"  X shape: ({row['n_windows']}, {row['n_channels']}, {row['n_timepoints']}) | "
            f"labels: {row['n_labels']} | "
            f"NaNs after: {row['nan_after_imputation']} | "
            f"long windows: {row['windows_longer_than_5_2_seconds']}"
        )

    summary = pd.DataFrame(rows)
    summary_path = report_dir / "pamap2_tensorization_by_subject_summary.csv"
    summary.to_csv(summary_path, index=False)

    print()
    print("Tensorization summary:")
    print(summary.drop(columns=["label_counts"]).to_string(index=False))
    print()
    print(f"Saved by-subject tensors to: {out_dir}")
    print(f"Saved summary to: {summary_path}")


if __name__ == "__main__":
    main()
