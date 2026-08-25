from __future__ import annotations

import numpy as np
import pandas as pd

from src.dysbalance.normalization import z_normalize_by_subject_and_context
from src.dysbalance.thresholds import threshold_sweep
from src.project_paths import PROCESSED_DATA_DIR


INPUT_PATH = (
    PROCESSED_DATA_DIR
    / "mhealth"
    / "features"
    / "mhealth_movement_features.csv"
)

OUTPUT_DIR = PROCESSED_DATA_DIR / "mhealth" / "dysbalance"

MOVEMENT_SCORE_FEATURES = [
    "total_acc_rms",
    "log_extremity_chest_acc_ratio",
    "log_arm_ankle_acc_ratio",
    "log_arm_ankle_gyro_ratio",
]

ECG_AUXILIARY_FEATURES = [
    "ecg_diff_rms",
]

THRESHOLDS = (1.5, 2.0, 2.5, 3.0)


def add_z_scores(features: pd.DataFrame) -> pd.DataFrame:
    scored = features.copy()

    for feature in MOVEMENT_SCORE_FEATURES + ECG_AUXILIARY_FEATURES:
        scored[f"z_{feature}"] = z_normalize_by_subject_and_context(
            scored[feature].to_numpy(),
            scored["subject_id"].to_numpy(),
            scored["label"].to_numpy(),
        )

    return scored


def compute_scores(scored: pd.DataFrame) -> pd.DataFrame:
    movement_z_columns = [f"z_{feature}" for feature in MOVEMENT_SCORE_FEATURES]
    ecg_z_columns = [f"z_{feature}" for feature in ECG_AUXILIARY_FEATURES]

    scored = scored.copy()

    scored["functional_deviation_strength"] = (
        scored[movement_z_columns].abs().mean(axis=1)
    )

    scored["max_functional_component_abs_z"] = (
        scored[movement_z_columns].abs().max(axis=1)
    )

    scored["dominant_functional_component"] = (
        scored[movement_z_columns]
        .abs()
        .idxmax(axis=1)
        .str.replace("z_", "", regex=False)
    )

    scored["ecg_signal_deviation_strength"] = (
        scored[ecg_z_columns].abs().mean(axis=1)
    )

    scored["combined_movement_ecg_deviation_strength"] = (
        0.85 * scored["functional_deviation_strength"]
        + 0.15 * scored["ecg_signal_deviation_strength"]
    )

    return scored


def build_subject_summary(scored: pd.DataFrame) -> pd.DataFrame:
    summary = (
        scored.groupby("subject_id")
        .agg(
            n_windows=("window_index", "count"),
            mean_functional_deviation_strength=(
                "functional_deviation_strength",
                "mean",
            ),
            std_functional_deviation_strength=(
                "functional_deviation_strength",
                "std",
            ),
            max_functional_deviation_strength=(
                "functional_deviation_strength",
                "max",
            ),
            pct_functional_strength_gt_1_5=(
                "functional_deviation_strength",
                lambda s: float((s > 1.5).mean() * 100.0),
            ),
            pct_functional_strength_gt_2_0=(
                "functional_deviation_strength",
                lambda s: float((s > 2.0).mean() * 100.0),
            ),
            mean_ecg_signal_deviation_strength=(
                "ecg_signal_deviation_strength",
                "mean",
            ),
            max_ecg_signal_deviation_strength=(
                "ecg_signal_deviation_strength",
                "max",
            ),
            mean_combined_movement_ecg_deviation_strength=(
                "combined_movement_ecg_deviation_strength",
                "mean",
            ),
            max_combined_movement_ecg_deviation_strength=(
                "combined_movement_ecg_deviation_strength",
                "max",
            ),
        )
        .reset_index()
    )

    return summary


def build_activity_summary(scored: pd.DataFrame) -> pd.DataFrame:
    summary = (
        scored.groupby(["label", "activity_name"])
        .agg(
            n_windows=("window_index", "count"),
            mean_functional_deviation_strength=(
                "functional_deviation_strength",
                "mean",
            ),
            std_functional_deviation_strength=(
                "functional_deviation_strength",
                "std",
            ),
            max_functional_deviation_strength=(
                "functional_deviation_strength",
                "max",
            ),
            pct_functional_strength_gt_1_5=(
                "functional_deviation_strength",
                lambda s: float((s > 1.5).mean() * 100.0),
            ),
            pct_functional_strength_gt_2_0=(
                "functional_deviation_strength",
                lambda s: float((s > 2.0).mean() * 100.0),
            ),
            mean_ecg_signal_deviation_strength=(
                "ecg_signal_deviation_strength",
                "mean",
            ),
            max_ecg_signal_deviation_strength=(
                "ecg_signal_deviation_strength",
                "max",
            ),
        )
        .reset_index()
    )

    return summary


def build_threshold_tables(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    functional_by_subject = threshold_sweep(
        scored["functional_deviation_strength"].to_numpy(),
        groups=scored["subject_id"].to_numpy(),
        thresholds=THRESHOLDS,
        value_name="functional_deviation_strength",
    )

    functional_by_activity = threshold_sweep(
        scored["functional_deviation_strength"].to_numpy(),
        groups=scored["activity_name"].to_numpy(),
        thresholds=THRESHOLDS,
        value_name="functional_deviation_strength",
    )

    ecg_by_subject = threshold_sweep(
        scored["ecg_signal_deviation_strength"].to_numpy(),
        groups=scored["subject_id"].to_numpy(),
        thresholds=THRESHOLDS,
        value_name="ecg_signal_deviation_strength",
    )

    return functional_by_subject, functional_by_activity, ecg_by_subject


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing MHEALTH feature file: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    features = pd.read_csv(INPUT_PATH)

    scored = add_z_scores(features)
    scored = compute_scores(scored)

    subject_summary = build_subject_summary(scored)
    activity_summary = build_activity_summary(scored)
    functional_threshold_subject, functional_threshold_activity, ecg_threshold_subject = (
        build_threshold_tables(scored)
    )

    score_path = OUTPUT_DIR / "mhealth_functional_scores.csv"
    subject_summary_path = OUTPUT_DIR / "mhealth_functional_score_summary_by_subject.csv"
    activity_summary_path = OUTPUT_DIR / "mhealth_functional_score_summary_by_activity.csv"
    threshold_subject_path = OUTPUT_DIR / "mhealth_functional_threshold_sweep_by_subject.csv"
    threshold_activity_path = OUTPUT_DIR / "mhealth_functional_threshold_sweep_by_activity.csv"
    ecg_threshold_subject_path = OUTPUT_DIR / "mhealth_ecg_signal_threshold_sweep_by_subject.csv"

    scored.to_csv(score_path, index=False)
    subject_summary.to_csv(subject_summary_path, index=False)
    activity_summary.to_csv(activity_summary_path, index=False)
    functional_threshold_subject.to_csv(threshold_subject_path, index=False)
    functional_threshold_activity.to_csv(threshold_activity_path, index=False)
    ecg_threshold_subject.to_csv(ecg_threshold_subject_path, index=False)

    print("Input features:", features.shape)
    print("Scored features:", scored.shape)
    print("Total missing values:", int(scored.isna().sum().sum()))

    print()
    print("Subject summary:")
    print(subject_summary.to_string(index=False))

    print()
    print("Activity summary:")
    print(activity_summary.to_string(index=False))

    print()
    print("Top 20 functional deviations:")
    top_columns = [
        "window_index",
        "subject_id",
        "label",
        "activity_name",
        "start_sample",
        "end_sample",
        "functional_deviation_strength",
        "max_functional_component_abs_z",
        "dominant_functional_component",
        "ecg_signal_deviation_strength",
        "combined_movement_ecg_deviation_strength",
    ]
    print(
        scored.sort_values(
            "functional_deviation_strength",
            ascending=False,
        )[top_columns]
        .head(20)
        .to_string(index=False)
    )

    print()
    print("Saved scores to:", score_path)
    print("Saved subject summary to:", subject_summary_path)
    print("Saved activity summary to:", activity_summary_path)
    print("Saved threshold sweep by subject to:", threshold_subject_path)
    print("Saved threshold sweep by activity to:", threshold_activity_path)
    print("Saved ECG threshold sweep by subject to:", ecg_threshold_subject_path)


if __name__ == "__main__":
    main()
