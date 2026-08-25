from __future__ import annotations

import numpy as np
import pandas as pd

from src.dysbalance.ratios import safe_log_ratio
from src.project_paths import INTERIM_DATA_DIR, PROCESSED_DATA_DIR


INPUT_DIR = INTERIM_DATA_DIR / "mhealth" / "by_subject"
OUTPUT_DIR = PROCESSED_DATA_DIR / "mhealth" / "features"

CHANNELS = {
    "chest_acc": [0, 1, 2],
    "ecg_lead_1": [3],
    "ecg_lead_2": [4],
    "ankle_acc": [5, 6, 7],
    "ankle_gyro": [8, 9, 10],
    "ankle_mag": [11, 12, 13],
    "arm_acc": [14, 15, 16],
    "arm_gyro": [17, 18, 19],
    "arm_mag": [20, 21, 22],
}


def grouped_rms(X: np.ndarray, channel_indices: list[int]) -> np.ndarray:
    values = X[:, channel_indices, :]
    return np.sqrt(np.mean(values**2, axis=(1, 2)))


def single_channel_rms(X: np.ndarray, channel_index: int) -> np.ndarray:
    values = X[:, channel_index, :]
    return np.sqrt(np.mean(values**2, axis=1))


def single_channel_abs_mean(X: np.ndarray, channel_index: int) -> np.ndarray:
    values = X[:, channel_index, :]
    return np.mean(np.abs(values), axis=1)


def load_subject(subject_id: int) -> tuple[np.ndarray, pd.DataFrame]:
    x_path = INPUT_DIR / f"subject_{subject_id:02d}_X.npy"
    metadata_path = INPUT_DIR / f"subject_{subject_id:02d}_metadata.csv"

    if not x_path.exists():
        raise FileNotFoundError(f"Missing tensor file: {x_path}")

    X = np.load(x_path)
    metadata = pd.read_csv(metadata_path)

    if len(X) != len(metadata):
        raise ValueError(
            f"Window count mismatch for subject {subject_id}: "
            f"X={len(X)}, metadata={len(metadata)}"
        )

    return X, metadata


def compute_subject_features(subject_id: int, global_offset: int) -> pd.DataFrame:
    X, metadata = load_subject(subject_id)

    chest_acc_rms = grouped_rms(X, CHANNELS["chest_acc"])
    ankle_acc_rms = grouped_rms(X, CHANNELS["ankle_acc"])
    arm_acc_rms = grouped_rms(X, CHANNELS["arm_acc"])

    ankle_gyro_rms = grouped_rms(X, CHANNELS["ankle_gyro"])
    arm_gyro_rms = grouped_rms(X, CHANNELS["arm_gyro"])

    ankle_mag_rms = grouped_rms(X, CHANNELS["ankle_mag"])
    arm_mag_rms = grouped_rms(X, CHANNELS["arm_mag"])

    ecg_lead_1_rms = single_channel_rms(X, CHANNELS["ecg_lead_1"][0])
    ecg_lead_2_rms = single_channel_rms(X, CHANNELS["ecg_lead_2"][0])
    ecg_lead_1_abs_mean = single_channel_abs_mean(X, CHANNELS["ecg_lead_1"][0])
    ecg_lead_2_abs_mean = single_channel_abs_mean(X, CHANNELS["ecg_lead_2"][0])

    ecg_diff = X[:, CHANNELS["ecg_lead_1"][0], :] - X[:, CHANNELS["ecg_lead_2"][0], :]
    ecg_diff_rms = np.sqrt(np.mean(ecg_diff**2, axis=1))

    extremity_acc_rms = (ankle_acc_rms + arm_acc_rms) / 2.0
    extremity_gyro_rms = (ankle_gyro_rms + arm_gyro_rms) / 2.0
    total_acc_rms = (chest_acc_rms + ankle_acc_rms + arm_acc_rms) / 3.0

    feature_df = metadata[
        [
            "subject_id",
            "label",
            "activity_name",
            "start_sample",
            "end_sample",
            "window_size",
            "step_size",
            "sampling_rate_hz",
            "duration_seconds",
        ]
    ].copy()

    feature_df.insert(0, "window_index", np.arange(global_offset, global_offset + len(feature_df)))
    feature_df.insert(2, "subject_window_index", np.arange(len(feature_df)))

    feature_df["chest_acc_rms"] = chest_acc_rms
    feature_df["ankle_acc_rms"] = ankle_acc_rms
    feature_df["arm_acc_rms"] = arm_acc_rms
    feature_df["extremity_acc_rms"] = extremity_acc_rms
    feature_df["total_acc_rms"] = total_acc_rms

    feature_df["ankle_gyro_rms"] = ankle_gyro_rms
    feature_df["arm_gyro_rms"] = arm_gyro_rms
    feature_df["extremity_gyro_rms"] = extremity_gyro_rms

    feature_df["ankle_mag_rms"] = ankle_mag_rms
    feature_df["arm_mag_rms"] = arm_mag_rms

    feature_df["ecg_lead_1_rms"] = ecg_lead_1_rms
    feature_df["ecg_lead_2_rms"] = ecg_lead_2_rms
    feature_df["ecg_lead_1_abs_mean"] = ecg_lead_1_abs_mean
    feature_df["ecg_lead_2_abs_mean"] = ecg_lead_2_abs_mean
    feature_df["ecg_diff_rms"] = ecg_diff_rms

    feature_df["log_extremity_chest_acc_ratio"] = safe_log_ratio(
        extremity_acc_rms,
        chest_acc_rms,
    )
    feature_df["log_arm_ankle_acc_ratio"] = safe_log_ratio(
        arm_acc_rms,
        ankle_acc_rms,
    )
    feature_df["log_arm_ankle_gyro_ratio"] = safe_log_ratio(
        arm_gyro_rms,
        ankle_gyro_rms,
    )
    feature_df["log_arm_ankle_mag_ratio"] = safe_log_ratio(
        arm_mag_rms,
        ankle_mag_rms,
    )

    return feature_df


def build_summary_by_activity(features: pd.DataFrame) -> pd.DataFrame:
    summary_columns = [
        "total_acc_rms",
        "log_extremity_chest_acc_ratio",
        "log_arm_ankle_acc_ratio",
        "log_arm_ankle_gyro_ratio",
        "ecg_diff_rms",
    ]

    summary = (
        features.groupby(["label", "activity_name"])[summary_columns]
        .agg(["count", "mean", "std", "min", "max"])
        .reset_index()
    )

    summary.columns = [
        "_".join(str(part) for part in col if part != "")
        for col in summary.columns.to_flat_index()
    ]

    return summary


def build_summary_by_subject(features: pd.DataFrame) -> pd.DataFrame:
    summary_columns = [
        "total_acc_rms",
        "log_extremity_chest_acc_ratio",
        "log_arm_ankle_acc_ratio",
        "log_arm_ankle_gyro_ratio",
        "ecg_diff_rms",
    ]

    summary = (
        features.groupby("subject_id")[summary_columns]
        .agg(["count", "mean", "std", "min", "max"])
        .reset_index()
    )

    summary.columns = [
        "_".join(str(part) for part in col if part != "")
        for col in summary.columns.to_flat_index()
    ]

    return summary


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_features = []
    global_offset = 0

    for subject_id in range(1, 11):
        features = compute_subject_features(subject_id, global_offset=global_offset)
        global_offset += len(features)
        all_features.append(features)

        print(
            f"subject_{subject_id:02d}: features={features.shape}, "
            f"labels={sorted(features['label'].unique().tolist())}, "
            f"nan={int(features.isna().sum().sum())}"
        )

    feature_df = pd.concat(all_features, ignore_index=True)

    feature_path = OUTPUT_DIR / "mhealth_movement_features.csv"
    activity_summary_path = OUTPUT_DIR / "mhealth_movement_feature_summary_by_activity.csv"
    subject_summary_path = OUTPUT_DIR / "mhealth_movement_feature_summary_by_subject.csv"

    activity_summary = build_summary_by_activity(feature_df)
    subject_summary = build_summary_by_subject(feature_df)

    feature_df.to_csv(feature_path, index=False)
    activity_summary.to_csv(activity_summary_path, index=False)
    subject_summary.to_csv(subject_summary_path, index=False)

    print()
    print("Feature table shape:", feature_df.shape)
    print("Total missing values:", int(feature_df.isna().sum().sum()))
    print("Label counts:")
    print(feature_df["label"].value_counts().sort_index().to_string())

    print()
    print("Feature preview:")
    preview_columns = [
        "window_index",
        "subject_id",
        "label",
        "activity_name",
        "total_acc_rms",
        "log_extremity_chest_acc_ratio",
        "log_arm_ankle_acc_ratio",
        "log_arm_ankle_gyro_ratio",
        "ecg_diff_rms",
    ]
    print(feature_df[preview_columns].head(20).to_string(index=False))

    print()
    print(f"Saved features to: {feature_path}")
    print(f"Saved activity summary to: {activity_summary_path}")
    print(f"Saved subject summary to: {subject_summary_path}")


if __name__ == "__main__":
    main()
