import numpy as np
import pandas as pd

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR
from src.dysbalance.ratios import safe_log_ratio
from src.tensorization.tensorize_pamap2 import SIGNAL_COLUMNS, VALID_SUBJECT_IDS


ACC_CHANNELS = {
    "hand": ["hand_acc16_x", "hand_acc16_y", "hand_acc16_z"],
    "chest": ["chest_acc16_x", "chest_acc16_y", "chest_acc16_z"],
    "ankle": ["ankle_acc16_x", "ankle_acc16_y", "ankle_acc16_z"],
}

GYRO_CHANNELS = {
    "hand": ["hand_gyro_x", "hand_gyro_y", "hand_gyro_z"],
    "chest": ["chest_gyro_x", "chest_gyro_y", "chest_gyro_z"],
    "ankle": ["ankle_gyro_x", "ankle_gyro_y", "ankle_gyro_z"],
}


def channel_indices(channel_names: list[str]) -> list[int]:
    """Return indices of selected channels in the PAMAP2 tensor."""
    return [SIGNAL_COLUMNS.index(channel) for channel in channel_names]


def rms_over_channels_and_time(X: np.ndarray, channels: list[str]) -> np.ndarray:
    """
    Compute RMS over selected channels and time.

    Input tensor shape:
        (n_windows, n_channels, n_timepoints)

    Output shape:
        (n_windows,)
    """
    indices = channel_indices(channels)
    values = X[:, indices, :]

    return np.sqrt(np.mean(np.square(values), axis=(1, 2)))


def compute_subject_features(subject_id: str) -> pd.DataFrame:
    """Compute movement-intensity features for one PAMAP2 subject."""
    base_dir = PROCESSED_DATA_DIR / "pamap2" / "by_subject"

    X = np.load(base_dir / f"X_subject{subject_id}.npy")
    metadata = pd.read_csv(base_dir / f"metadata_subject{subject_id}.csv")

    features = metadata.copy()

    for position, channels in ACC_CHANNELS.items():
        features[f"{position}_acc_rms"] = rms_over_channels_and_time(X, channels)

    for position, channels in GYRO_CHANNELS.items():
        features[f"{position}_gyro_rms"] = rms_over_channels_and_time(X, channels)

    features["mean_extremity_acc_rms"] = (
        features["hand_acc_rms"] + features["ankle_acc_rms"]
    ) / 2.0

    features["mean_extremity_gyro_rms"] = (
        features["hand_gyro_rms"] + features["ankle_gyro_rms"]
    ) / 2.0

    features["total_acc_rms"] = (
        features["hand_acc_rms"]
        + features["chest_acc_rms"]
        + features["ankle_acc_rms"]
    ) / 3.0

    features["total_gyro_rms"] = (
        features["hand_gyro_rms"]
        + features["chest_gyro_rms"]
        + features["ankle_gyro_rms"]
    ) / 3.0

    features["log_extremity_chest_acc_ratio"] = safe_log_ratio(
        features["mean_extremity_acc_rms"].to_numpy(),
        features["chest_acc_rms"].to_numpy(),
    )

    features["log_hand_ankle_acc_ratio"] = safe_log_ratio(
        features["hand_acc_rms"].to_numpy(),
        features["ankle_acc_rms"].to_numpy(),
    )

    features["log_hand_ankle_gyro_ratio"] = safe_log_ratio(
        features["hand_gyro_rms"].to_numpy(),
        features["ankle_gyro_rms"].to_numpy(),
    )

    return features


def build_all_movement_features() -> pd.DataFrame:
    """Compute PAMAP2 movement features for all valid subjects."""
    parts = []

    for subject_id in VALID_SUBJECT_IDS:
        print(f"Computing movement features for subject {subject_id} ...")
        parts.append(compute_subject_features(subject_id))

    return pd.concat(parts, ignore_index=True)


def summarize_features(features: pd.DataFrame) -> pd.DataFrame:
    """Create a compact subject-level feature summary."""
    rows = []

    for subject_id, group in features.groupby("subject_id"):
        rows.append(
            {
                "subject_id": subject_id,
                "n_windows": len(group),
                "n_activities": group["activity_id"].nunique(),
                "mean_total_acc_rms": group["total_acc_rms"].mean(),
                "std_total_acc_rms": group["total_acc_rms"].std(),
                "mean_total_gyro_rms": group["total_gyro_rms"].mean(),
                "std_total_gyro_rms": group["total_gyro_rms"].std(),
                "mean_log_extremity_chest_acc_ratio": group[
                    "log_extremity_chest_acc_ratio"
                ].mean(),
                "std_log_extremity_chest_acc_ratio": group[
                    "log_extremity_chest_acc_ratio"
                ].std(),
                "mean_log_hand_ankle_acc_ratio": group[
                    "log_hand_ankle_acc_ratio"
                ].mean(),
                "std_log_hand_ankle_acc_ratio": group[
                    "log_hand_ankle_acc_ratio"
                ].std(),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    out_dir = PROCESSED_DATA_DIR / "pamap2" / "features"
    out_dir.mkdir(parents=True, exist_ok=True)

    report_dir = REPORTS_DIR / "dysbalance"
    report_dir.mkdir(parents=True, exist_ok=True)

    features = build_all_movement_features()
    summary = summarize_features(features)

    features_path = out_dir / "pamap2_movement_features.csv"
    summary_path = report_dir / "pamap2_movement_feature_summary.csv"

    features.to_csv(features_path, index=False)
    summary.to_csv(summary_path, index=False)

    print()
    print("Feature table shape:", features.shape)
    print("Summary:")
    print(summary.to_string(index=False))
    print()
    print(f"Saved features to: {features_path}")
    print(f"Saved summary to: {summary_path}")


if __name__ == "__main__":
    main()
