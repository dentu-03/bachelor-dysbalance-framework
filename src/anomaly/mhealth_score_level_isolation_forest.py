from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR


INPUT_PATH = (
    PROCESSED_DATA_DIR
    / "mhealth"
    / "dysbalance"
    / "mhealth_functional_scores.csv"
)

OUTPUT_DIR = REPORTS_DIR / "anomaly" / "mhealth"

RANDOM_STATE = 42
CONTAMINATIONS = (0.02, 0.05, 0.10)
THRESHOLDS = (1.5, 2.0, 2.5, 3.0)


@dataclass(frozen=True)
class FeatureSet:
    name: str
    columns: tuple[str, ...]


FEATURE_SETS = (
    FeatureSet(
        name="score_level",
        columns=(
            "functional_deviation_strength",
            "ecg_signal_deviation_strength",
            "combined_movement_ecg_deviation_strength",
        ),
    ),
    FeatureSet(
        name="movement_component_level",
        columns=(
            "z_total_acc_rms",
            "z_log_extremity_chest_acc_ratio",
            "z_log_arm_ankle_acc_ratio",
            "z_log_arm_ankle_gyro_ratio",
        ),
    ),
    FeatureSet(
        name="movement_ecg_component_level",
        columns=(
            "z_total_acc_rms",
            "z_log_extremity_chest_acc_ratio",
            "z_log_arm_ankle_acc_ratio",
            "z_log_arm_ankle_gyro_ratio",
            "z_ecg_diff_rms",
        ),
    ),
)


def validate_columns(df: pd.DataFrame, columns: tuple[str, ...]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def fit_isolation_forest(
    df: pd.DataFrame,
    feature_set: FeatureSet,
    contamination: float,
) -> pd.DataFrame:
    validate_columns(df, feature_set.columns)

    X = df.loc[:, feature_set.columns].to_numpy(dtype=float)

    if np.isnan(X).any():
        raise ValueError(
            f"NaN values detected for feature set {feature_set.name}"
        )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=300,
        contamination=contamination,
        random_state=RANDOM_STATE,
    )

    predictions = model.fit_predict(X_scaled)
    decision_function = model.decision_function(X_scaled)

    result = df[
        [
            "window_index",
            "subject_id",
            "label",
            "activity_name",
            "start_sample",
            "end_sample",
            "functional_deviation_strength",
            "ecg_signal_deviation_strength",
            "combined_movement_ecg_deviation_strength",
            "dominant_functional_component",
        ]
    ].copy()

    result["feature_set"] = feature_set.name
    result["contamination"] = contamination
    result["is_anomaly"] = predictions == -1
    result["anomaly_score"] = -decision_function

    return result


def summarize_by_activity(results: pd.DataFrame) -> pd.DataFrame:
    return (
        results.groupby(["feature_set", "contamination", "label", "activity_name"])
        .agg(
            n_windows=("window_index", "count"),
            n_anomalies=("is_anomaly", "sum"),
            anomaly_rate_pct=("is_anomaly", lambda s: float(s.mean() * 100.0)),
            mean_anomaly_score=("anomaly_score", "mean"),
            max_anomaly_score=("anomaly_score", "max"),
            mean_functional_deviation_strength=(
                "functional_deviation_strength",
                "mean",
            ),
            max_functional_deviation_strength=(
                "functional_deviation_strength",
                "max",
            ),
        )
        .reset_index()
    )


def summarize_by_subject(results: pd.DataFrame) -> pd.DataFrame:
    return (
        results.groupby(["feature_set", "contamination", "subject_id"])
        .agg(
            n_windows=("window_index", "count"),
            n_anomalies=("is_anomaly", "sum"),
            anomaly_rate_pct=("is_anomaly", lambda s: float(s.mean() * 100.0)),
            mean_anomaly_score=("anomaly_score", "mean"),
            max_anomaly_score=("anomaly_score", "max"),
            mean_functional_deviation_strength=(
                "functional_deviation_strength",
                "mean",
            ),
            max_functional_deviation_strength=(
                "functional_deviation_strength",
                "max",
            ),
        )
        .reset_index()
    )


def compute_threshold_overlap(results: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for (feature_set, contamination), group in results.groupby(
        ["feature_set", "contamination"]
    ):
        model_mask = group["is_anomaly"].to_numpy(dtype=bool)
        n_model = int(model_mask.sum())

        for threshold in THRESHOLDS:
            threshold_mask = (
                group["functional_deviation_strength"].to_numpy(dtype=float)
                > threshold
            )

            n_threshold = int(threshold_mask.sum())
            n_overlap = int(np.logical_and(model_mask, threshold_mask).sum())
            n_union = int(np.logical_or(model_mask, threshold_mask).sum())

            rows.append(
                {
                    "feature_set": feature_set,
                    "contamination": contamination,
                    "threshold": threshold,
                    "n_model_anomalies": n_model,
                    "n_threshold_anomalies": n_threshold,
                    "n_overlap": n_overlap,
                    "model_overlap_pct": (
                        0.0 if n_model == 0 else n_overlap / n_model * 100.0
                    ),
                    "threshold_overlap_pct": (
                        0.0
                        if n_threshold == 0
                        else n_overlap / n_threshold * 100.0
                    ),
                    "jaccard": 0.0 if n_union == 0 else n_overlap / n_union,
                }
            )

    return pd.DataFrame(rows)


def compute_correlations(results: pd.DataFrame) -> pd.DataFrame:
    rows = []

    targets = [
        "functional_deviation_strength",
        "ecg_signal_deviation_strength",
        "combined_movement_ecg_deviation_strength",
    ]

    for (feature_set, contamination), group in results.groupby(
        ["feature_set", "contamination"]
    ):
        for target in targets:
            x = group["anomaly_score"].to_numpy(dtype=float)
            y = group[target].to_numpy(dtype=float)

            pearson_value = pearsonr(x, y).statistic
            spearman_value = spearmanr(x, y).statistic

            rows.append(
                {
                    "feature_set": feature_set,
                    "contamination": contamination,
                    "target": target,
                    "pearson": float(pearson_value),
                    "spearman": float(spearman_value),
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing MHEALTH score file: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(INPUT_PATH)

    all_results = []

    for feature_set in FEATURE_SETS:
        for contamination in CONTAMINATIONS:
            result = fit_isolation_forest(
                scores,
                feature_set=feature_set,
                contamination=contamination,
            )
            all_results.append(result)

            print(
                f"{feature_set.name} contamination={contamination:.2f}: "
                f"anomalies={int(result['is_anomaly'].sum())} / {len(result)} "
                f"({result['is_anomaly'].mean() * 100.0:.3f}%)"
            )

    results = pd.concat(all_results, ignore_index=True)

    activity_summary = summarize_by_activity(results)
    subject_summary = summarize_by_subject(results)
    overlap = compute_threshold_overlap(results)
    correlations = compute_correlations(results)

    results_path = OUTPUT_DIR / "mhealth_isolation_forest_predictions.csv"
    activity_summary_path = OUTPUT_DIR / "mhealth_isolation_forest_summary_by_activity.csv"
    subject_summary_path = OUTPUT_DIR / "mhealth_isolation_forest_summary_by_subject.csv"
    overlap_path = OUTPUT_DIR / "mhealth_isolation_forest_threshold_overlap.csv"
    correlations_path = OUTPUT_DIR / "mhealth_isolation_forest_correlations.csv"

    results.to_csv(results_path, index=False)
    activity_summary.to_csv(activity_summary_path, index=False)
    subject_summary.to_csv(subject_summary_path, index=False)
    overlap.to_csv(overlap_path, index=False)
    correlations.to_csv(correlations_path, index=False)

    print()
    print("Activity anomaly rates for movement_component_level, contamination=0.05:")
    selected_activity = activity_summary[
        (activity_summary["feature_set"] == "movement_component_level")
        & (activity_summary["contamination"] == 0.05)
    ].sort_values("anomaly_rate_pct", ascending=False)
    print(selected_activity.to_string(index=False))

    print()
    print("Subject anomaly rates for movement_component_level, contamination=0.05:")
    selected_subject = subject_summary[
        (subject_summary["feature_set"] == "movement_component_level")
        & (subject_summary["contamination"] == 0.05)
    ].sort_values("anomaly_rate_pct", ascending=False)
    print(selected_subject.to_string(index=False))

    print()
    print("Threshold overlap for movement_component_level, contamination=0.05:")
    selected_overlap = overlap[
        (overlap["feature_set"] == "movement_component_level")
        & (overlap["contamination"] == 0.05)
    ]
    print(selected_overlap.to_string(index=False))

    print()
    print("Correlations for movement_component_level, contamination=0.05:")
    selected_correlations = correlations[
        (correlations["feature_set"] == "movement_component_level")
        & (correlations["contamination"] == 0.05)
    ]
    print(selected_correlations.to_string(index=False))

    print()
    print(f"Saved predictions to: {results_path}")
    print(f"Saved activity summary to: {activity_summary_path}")
    print(f"Saved subject summary to: {subject_summary_path}")
    print(f"Saved threshold overlap to: {overlap_path}")
    print(f"Saved correlations to: {correlations_path}")


if __name__ == "__main__":
    main()
