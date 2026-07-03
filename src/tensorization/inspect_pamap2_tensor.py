import numpy as np
import pandas as pd

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR
from src.tensorization.tensorize_pamap2 import SIGNAL_COLUMNS


def inspect_subject_tensor(subject_id: str = "101") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Inspect one processed PAMAP2 subject tensor."""
    tensor_dir = PROCESSED_DATA_DIR / "pamap2" / "single_subject"

    x_path = tensor_dir / f"X_subject{subject_id}.npy"
    y_path = tensor_dir / f"y_subject{subject_id}.npy"
    meta_path = tensor_dir / f"metadata_subject{subject_id}.csv"

    if not x_path.exists():
        raise FileNotFoundError(f"Missing X file: {x_path}")
    if not y_path.exists():
        raise FileNotFoundError(f"Missing y file: {y_path}")
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing metadata file: {meta_path}")

    X = np.load(x_path)
    y = np.load(y_path)
    metadata = pd.read_csv(meta_path)

    if X.ndim != 3:
        raise ValueError(f"Expected X to be 3D, got shape {X.shape}")

    if X.shape[0] != len(y):
        raise ValueError("X and y have different number of windows")

    if X.shape[0] != len(metadata):
        raise ValueError("X and metadata have different number of windows")

    if X.shape[1] != len(SIGNAL_COLUMNS):
        raise ValueError(
            f"Expected {len(SIGNAL_COLUMNS)} channels, got {X.shape[1]}"
        )

    durations = metadata["timestamp_end"] - metadata["timestamp_start"]

    summary = pd.DataFrame(
        [
            {
                "subject_id": subject_id,
                "n_windows": X.shape[0],
                "n_channels": X.shape[1],
                "n_timepoints": X.shape[2],
                "y_length": len(y),
                "metadata_rows": len(metadata),
                "overall_nan_pct": round(float(np.isnan(X).mean() * 100), 4),
                "windows_longer_than_5_2_seconds": int((durations > 5.2).sum()),
                "duration_min": float(durations.min()),
                "duration_mean": float(durations.mean()),
                "duration_max": float(durations.max()),
                "n_labels": int(pd.Series(y).nunique()),
            }
        ]
    )

    channel_nan = pd.DataFrame(
        {
            "channel": SIGNAL_COLUMNS,
            "nan_pct": [
                round(float(np.isnan(X[:, i, :]).mean() * 100), 4)
                for i in range(X.shape[1])
            ],
        }
    )

    return summary, channel_nan


def main() -> None:
    subject_id = "101"

    report_dir = REPORTS_DIR / "datasets"
    report_dir.mkdir(parents=True, exist_ok=True)

    summary, channel_nan = inspect_subject_tensor(subject_id)

    summary_path = report_dir / f"pamap2_subject{subject_id}_tensor_summary.csv"
    channel_nan_path = report_dir / f"pamap2_subject{subject_id}_channel_nan_report.csv"

    summary.to_csv(summary_path, index=False)
    channel_nan.to_csv(channel_nan_path, index=False)

    print("Tensor summary:")
    print(summary.to_string(index=False))
    print()
    print("Channel NaN report:")
    print(channel_nan.to_string(index=False))
    print()
    print(f"Saved summary to: {summary_path}")
    print(f"Saved channel NaN report to: {channel_nan_path}")


if __name__ == "__main__":
    main()
