import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from src.project_paths import RAW_DATA_DIR, INTERIM_DATA_DIR, REPORTS_DIR
from src.tensorization.windowing import window_array, majority_labels


VALID_LABELS = {
    1: "baseline",
    2: "stress",
    3: "amusement",
    4: "meditation",
}

CHEST_CHANNELS = [
    "acc_x",
    "acc_y",
    "acc_z",
    "ecg",
    "emg",
    "eda",
    "temp",
    "resp",
]


def load_wesad_subject(subject_id: str) -> dict:
    """Load one WESAD subject pickle file."""
    path = RAW_DATA_DIR / "wesad" / subject_id / f"{subject_id}.pkl"

    if not path.exists():
        raise FileNotFoundError(f"Missing WESAD file: {path}")

    with open(path, "rb") as f:
        return pickle.load(f, encoding="latin1")


def chest_signal_matrix(data: dict) -> np.ndarray:
    """
    Build WESAD chest signal matrix.

    Channels:
    ACC(3), ECG, EMG, EDA, Temp, Resp

    Output shape:
        (n_samples, 8)
    """
    chest = data["signal"]["chest"]

    signal = np.hstack(
        [
            chest["ACC"],
            chest["ECG"],
            chest["EMG"],
            chest["EDA"],
            chest["Temp"],
            chest["Resp"],
        ]
    )

    if signal.shape[1] != len(CHEST_CHANNELS):
        raise ValueError(
            f"Expected {len(CHEST_CHANNELS)} chest channels, got {signal.shape[1]}"
        )

    return signal.astype(float)


def valid_label_segments(labels: np.ndarray) -> list[tuple[int, int, int]]:
    """
    Return contiguous segments with valid WESAD labels.

    Each segment is represented as:
        (start_index, end_index_exclusive, label)
    """
    labels = np.asarray(labels)

    is_valid = np.isin(labels, list(VALID_LABELS.keys()))
    segments = []

    start = None
    current_label = None

    for idx, label in enumerate(labels):
        if not is_valid[idx]:
            if start is not None:
                segments.append((start, idx, int(current_label)))
                start = None
                current_label = None
            continue

        if start is None:
            start = idx
            current_label = label
            continue

        if label != current_label:
            segments.append((start, idx, int(current_label)))
            start = idx
            current_label = label

    if start is not None:
        segments.append((start, len(labels), int(current_label)))

    return segments


def tensorize_subject_chest(
    subject_id: str,
    window_size: int = 7000,
    step_size: int = 3500,
) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """
    Tensorize one WESAD subject from chest signals only.

    Default:
    - 700 Hz chest signals
    - 7000 samples = 10 seconds
    - 3500 samples = 50 percent overlap
    """
    data = load_wesad_subject(subject_id)

    labels = np.asarray(data["label"])
    signal = chest_signal_matrix(data)

    n = min(len(labels), len(signal))
    labels = labels[:n]
    signal = signal[:n]

    X_parts = []
    y_parts = []
    metadata_rows = []

    global_window_index = 0

    for segment_index, (start, end, segment_label) in enumerate(valid_label_segments(labels)):
        segment_length = end - start

        if segment_length < window_size:
            continue

        segment_signal = signal[start:end]
        segment_labels = labels[start:end]

        X_segment, starts = window_array(
            values=segment_signal,
            window_size=window_size,
            step_size=step_size,
        )

        y_segment = majority_labels(
            labels=segment_labels,
            starts=starts,
            window_size=window_size,
        )

        X_parts.append(X_segment)
        y_parts.append(y_segment)

        for local_i, local_start in enumerate(starts):
            absolute_start = int(start + local_start)
            absolute_end = int(absolute_start + window_size - 1)

            metadata_rows.append(
                {
                    "subject_id": subject_id,
                    "window_index": global_window_index,
                    "segment_index": int(segment_index),
                    "label": int(y_segment[local_i]),
                    "label_name": VALID_LABELS[int(y_segment[local_i])],
                    "segment_label": int(segment_label),
                    "segment_label_name": VALID_LABELS[int(segment_label)],
                    "start_sample": absolute_start,
                    "end_sample": absolute_end,
                    "duration_seconds": window_size / 700.0,
                }
            )
            global_window_index += 1

    if not X_parts:
        raise ValueError(f"No WESAD windows generated for subject {subject_id}")

    X = np.concatenate(X_parts, axis=0)
    y = np.concatenate(y_parts, axis=0).astype(int)
    metadata = pd.DataFrame(metadata_rows)

    return X, y, metadata


def discover_subject_ids() -> list[str]:
    """Discover available WESAD subject IDs in raw data directory."""
    root = RAW_DATA_DIR / "wesad"
    subject_dirs = sorted(path.name for path in root.glob("S*") if path.is_dir())

    return subject_dirs


def main() -> None:
    window_size = 7000
    step_size = 3500

    out_dir = INTERIM_DATA_DIR / "wesad" / "chest_by_subject"
    out_dir.mkdir(parents=True, exist_ok=True)

    report_dir = REPORTS_DIR / "datasets"
    report_dir.mkdir(parents=True, exist_ok=True)

    rows = []

    for subject_id in discover_subject_ids():
        print(f"Tensorizing WESAD {subject_id} ...")

        X, y, metadata = tensorize_subject_chest(
            subject_id=subject_id,
            window_size=window_size,
            step_size=step_size,
        )

        np.save(out_dir / f"X_{subject_id}.npy", X)
        np.save(out_dir / f"y_{subject_id}.npy", y)
        metadata.to_csv(out_dir / f"metadata_{subject_id}.csv", index=False)

        label_counts = metadata["label"].value_counts().sort_index()

        rows.append(
            {
                "subject_id": subject_id,
                "n_windows": int(X.shape[0]),
                "n_channels": int(X.shape[1]),
                "n_timepoints": int(X.shape[2]),
                "n_labels": int(label_counts.shape[0]),
                "label_counts": dict(label_counts),
                "nan_count": int(np.isnan(X).sum()),
            }
        )

        print(
            f"  X shape: {X.shape} | labels: {dict(label_counts)} | "
            f"NaNs: {int(np.isnan(X).sum())}"
        )

    summary = pd.DataFrame(rows)
    summary_path = report_dir / "wesad_chest_tensorization_summary.csv"
    summary.to_csv(summary_path, index=False)

    print()
    print("WESAD chest tensorization summary:")
    print(summary.to_string(index=False))
    print()
    print(f"Saved WESAD chest tensors to: {out_dir}")
    print(f"Saved summary to: {summary_path}")


if __name__ == "__main__":
    main()
