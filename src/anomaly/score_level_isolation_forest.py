from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR


RANDOM_STATE = 42
CONTAMINATION_VALUES = (0.02, 0.05, 0.10)
THRESHOLDS = (1.5, 2.0, 2.5)
N_ESTIMATORS = 300
TOP_N = 30


PAMAP2_ACTIVITY_LABELS = {
    1: "lying",
    2: "sitting",
    3: "standing",
    4: "walking",
    5: "running",
    6: "cycling",
    7: "Nordic walking",
    12: "ascending stairs",
    13: "descending stairs",
    16: "vacuum cleaning",
    17: "ironing",
    24: "rope jumping",
}


@dataclass(frozen=True)
class FeatureSet:
    name: str
    columns: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class ThresholdReference:
    name: str
    column: str
    direction: str


@dataclass(frozen=True)
class DatasetConfig:
    dataset: str
    domain: str
    input_path: Path
    session_id: str
    context_columns: tuple[str, ...]
    subject_column: str
    condition_column: str
    condition_name_column: str
    feature_sets: tuple[FeatureSet, ...]
    threshold_references: tuple[ThresholdReference, ...]
    primary_score_columns: tuple[str, ...]


def zscore(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    mean = np.nanmean(values)
    std = np.nanstd(values)

    if std == 0 or np.isnan(std):
        return np.zeros_like(values, dtype=float)

    return (values - mean) / std


def rank_percent(values: np.ndarray) -> np.ndarray:
    series = pd.Series(values)
    return series.rank(method="average", pct=True).to_numpy() * 100.0


def load_pamap2_scores() -> pd.DataFrame:
    path = PROCESSED_DATA_DIR / "pamap2" / "dysbalance" / "pamap2_functional_scores.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing PAMAP2 score file: {path}")

    df = pd.read_csv(path)

    df["dataset"] = "pamap2"
    df["domain"] = "functional_motor"
    df["session_id"] = "public_pamap2_protocol"
    df["activity_name"] = df["activity_id"].map(PAMAP2_ACTIVITY_LABELS).fillna("unknown")

    return df


def load_wesad_scores() -> pd.DataFrame:
    path = PROCESSED_DATA_DIR / "wesad" / "dysbalance" / "wesad_autonomic_scores.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing WESAD score file: {path}")

    df = pd.read_csv(path)

    df["dataset"] = "wesad"
    df["domain"] = "autonomic"
    df["session_id"] = "public_wesad_chest"

    return df


def build_dataset_configs() -> tuple[DatasetConfig, DatasetConfig]:
    pamap2_config = DatasetConfig(
        dataset="pamap2",
        domain="functional_motor",
        input_path=PROCESSED_DATA_DIR / "pamap2" / "dysbalance" / "pamap2_functional_scores.csv",
        session_id="public_pamap2_protocol",
        context_columns=(
            "dataset",
            "domain",
            "session_id",
            "subject_id",
            "window_index",
            "segment_id",
            "activity_id",
            "activity_name",
            "timestamp_start",
            "timestamp_end",
        ),
        subject_column="subject_id",
        condition_column="activity_id",
        condition_name_column="activity_name",
        feature_sets=(
            FeatureSet(
                name="score_level",
                columns=("functional_deviation_strength",),
                description="Final functional dysbalance score only.",
            ),
            FeatureSet(
                name="component_level",
                columns=(
                    "z_total_acc_rms",
                    "z_log_extremity_chest_acc_ratio",
                    "z_log_hand_ankle_acc_ratio",
                ),
                description="Interpretable normalized PAMAP2 dysbalance components.",
            ),
            FeatureSet(
                name="feature_level",
                columns=(
                    "total_acc_rms",
                    "log_extremity_chest_acc_ratio",
                    "log_hand_ankle_acc_ratio",
                ),
                description="Selected physiological movement features before final aggregation.",
            ),
        ),
        threshold_references=(
            ThresholdReference(
                name="functional_deviation_strength",
                column="functional_deviation_strength",
                direction="greater",
            ),
        ),
        primary_score_columns=("functional_deviation_strength",),
    )

    wesad_config = DatasetConfig(
        dataset="wesad",
        domain="autonomic",
        input_path=PROCESSED_DATA_DIR / "wesad" / "dysbalance" / "wesad_autonomic_scores.csv",
        session_id="public_wesad_chest",
        context_columns=(
            "dataset",
            "domain",
            "session_id",
            "subject_id",
            "window_index",
            "label",
            "label_name",
            "start_sample",
            "end_sample",
            "duration_seconds",
        ),
        subject_column="subject_id",
        condition_column="label",
        condition_name_column="label_name",
        feature_sets=(
            FeatureSet(
                name="score_level",
                columns=(
                    "z_autonomic_activation",
                    "autonomic_deviation_strength",
                ),
                description="Final WESAD autonomic activation and deviation scores.",
            ),
            FeatureSet(
                name="component_level",
                columns=(
                    "z_hr_bpm",
                    "z_eda_mean",
                    "z_resp_std",
                    "z_inverse_rmssd",
                ),
                description="Interpretable normalized autonomic dysbalance components.",
            ),
            FeatureSet(
                name="feature_level",
                columns=(
                    "hr_bpm",
                    "rmssd_ms",
                    "eda_mean",
                    "resp_std",
                ),
                description="Selected autonomic features before final score aggregation.",
            ),
        ),
        threshold_references=(
            ThresholdReference(
                name="z_autonomic_activation",
                column="z_autonomic_activation",
                direction="greater",
            ),
            ThresholdReference(
                name="autonomic_deviation_strength",
                column="autonomic_deviation_strength",
                direction="greater",
            ),
        ),
        primary_score_columns=(
            "z_autonomic_activation",
            "autonomic_deviation_strength",
        ),
    )

    return pamap2_config, wesad_config


def validate_columns(df: pd.DataFrame, config: DatasetConfig) -> None:
    required_columns = set(config.context_columns)

    for feature_set in config.feature_sets:
        required_columns.update(feature_set.columns)

    for threshold_ref in config.threshold_references:
        required_columns.add(threshold_ref.column)

    for score_column in config.primary_score_columns:
        required_columns.add(score_column)

    missing = sorted(required_columns.difference(df.columns))

    if missing:
        raise ValueError(
            f"Dataset {config.dataset} is missing required columns: {missing}"
        )


def fit_isolation_forest(
    df: pd.DataFrame,
    config: DatasetConfig,
    feature_set: FeatureSet,
    contamination: float,
) -> pd.DataFrame:
    feature_values = df.loc[:, feature_set.columns].replace([np.inf, -np.inf], np.nan)
    valid_mask = feature_values.notna().all(axis=1)

    if valid_mask.sum() < 10:
        raise ValueError(
            f"Not enough valid rows for {config.dataset}/{feature_set.name}: "
            f"{valid_mask.sum()}"
        )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feature_values.loc[valid_mask].to_numpy())

    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=contamination,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    predictions = model.fit_predict(X_scaled)
    raw_anomaly_scores = -model.score_samples(X_scaled)

    result_columns = []
    result_columns.extend(config.context_columns)

    for column in config.primary_score_columns:
        if column not in result_columns:
            result_columns.append(column)

    for column in feature_set.columns:
        if column not in result_columns:
            result_columns.append(column)

    result = df.loc[:, result_columns].copy()

    result["feature_set"] = feature_set.name
    result["feature_columns"] = ",".join(feature_set.columns)
    result["feature_set_description"] = feature_set.description
    result["model"] = "IsolationForest"
    result["contamination"] = contamination
    result["n_estimators"] = N_ESTIMATORS
    result["random_state"] = RANDOM_STATE
    result["is_valid_for_model"] = valid_mask.to_numpy()
    result["anomaly_score"] = np.nan
    result["anomaly_score_z"] = np.nan
    result["anomaly_rank_percent"] = np.nan
    result["is_model_anomaly"] = False

    result.loc[valid_mask, "anomaly_score"] = raw_anomaly_scores
    result.loc[valid_mask, "anomaly_score_z"] = zscore(raw_anomaly_scores)
    result.loc[valid_mask, "anomaly_rank_percent"] = rank_percent(raw_anomaly_scores)
    result.loc[valid_mask, "is_model_anomaly"] = predictions == -1

    return result


def run_dataset(df: pd.DataFrame, config: DatasetConfig) -> pd.DataFrame:
    validate_columns(df, config)

    parts = []

    for feature_set in config.feature_sets:
        for contamination in CONTAMINATION_VALUES:
            print(
                f"Running {config.dataset} | {feature_set.name} | "
                f"contamination={contamination}"
            )

            parts.append(
                fit_isolation_forest(
                    df=df,
                    config=config,
                    feature_set=feature_set,
                    contamination=contamination,
                )
            )

    return pd.concat(parts, ignore_index=True)


def summarize_by_group(
    scores: pd.DataFrame,
    group_columns: tuple[str, ...],
    score_columns: tuple[str, ...],
) -> pd.DataFrame:
    rows = []

    base_groups = ["dataset", "domain", "feature_set", "contamination"]
    all_group_columns = base_groups + list(group_columns)

    for group_values, group in scores.groupby(all_group_columns, dropna=False):
        if not isinstance(group_values, tuple):
            group_values = (group_values,)

        row = dict(zip(all_group_columns, group_values))

        row["n_windows"] = len(group)
        row["n_valid_for_model"] = int(group["is_valid_for_model"].sum())
        row["n_model_anomalies"] = int(group["is_model_anomaly"].sum())
        row["model_anomaly_rate_pct"] = (
            group["is_model_anomaly"].mean() * 100.0
        )
        row["mean_anomaly_score"] = group["anomaly_score"].mean()
        row["median_anomaly_score"] = group["anomaly_score"].median()
        row["mean_anomaly_score_z"] = group["anomaly_score_z"].mean()

        for score_column in score_columns:
            if score_column in group.columns:
                row[f"mean_{score_column}"] = group[score_column].mean()
                row[f"median_{score_column}"] = group[score_column].median()

        rows.append(row)

    return pd.DataFrame(rows)


def threshold_flag(values: pd.Series, reference: ThresholdReference, threshold: float) -> pd.Series:
    if reference.direction == "greater":
        return values > threshold

    if reference.direction == "absolute_greater":
        return values.abs() > threshold

    raise ValueError(f"Unsupported threshold direction: {reference.direction}")


def compute_overlap_report(
    scores: pd.DataFrame,
    config: DatasetConfig,
) -> pd.DataFrame:
    rows = []

    for (feature_set, contamination), group in scores.groupby(
        ["feature_set", "contamination"], dropna=False
    ):
        model_flag = group["is_model_anomaly"].astype(bool)

        for reference in config.threshold_references:
            for threshold in THRESHOLDS:
                ref_flag = threshold_flag(
                    group[reference.column],
                    reference=reference,
                    threshold=threshold,
                )

                n_total = len(group)
                n_model = int(model_flag.sum())
                n_threshold = int(ref_flag.sum())
                n_overlap = int((model_flag & ref_flag).sum())
                n_union = int((model_flag | ref_flag).sum())

                rows.append(
                    {
                        "dataset": config.dataset,
                        "domain": config.domain,
                        "feature_set": feature_set,
                        "contamination": contamination,
                        "threshold_reference": reference.name,
                        "threshold_column": reference.column,
                        "threshold": threshold,
                        "threshold_direction": reference.direction,
                        "n_total": n_total,
                        "n_model_anomalies": n_model,
                        "n_threshold_anomalies": n_threshold,
                        "n_overlap": n_overlap,
                        "model_anomaly_rate_pct": n_model / n_total * 100.0,
                        "threshold_anomaly_rate_pct": n_threshold / n_total * 100.0,
                        "overlap_rate_of_model_pct": (
                            n_overlap / n_model * 100.0 if n_model else 0.0
                        ),
                        "overlap_rate_of_threshold_pct": (
                            n_overlap / n_threshold * 100.0 if n_threshold else 0.0
                        ),
                        "jaccard_index": n_overlap / n_union if n_union else 0.0,
                    }
                )

    return pd.DataFrame(rows)


def build_top_windows(scores: pd.DataFrame) -> pd.DataFrame:
    parts = []

    filtered = scores[scores["contamination"] == 0.05].copy()

    for (dataset, feature_set), group in filtered.groupby(["dataset", "feature_set"]):
        top = group.sort_values("anomaly_score", ascending=False).head(TOP_N).copy()
        top["top_rank_within_dataset_feature_set"] = np.arange(1, len(top) + 1)
        parts.append(top)

    if not parts:
        return pd.DataFrame()

    return pd.concat(parts, ignore_index=True)


def save_dataset_outputs(
    scores: pd.DataFrame,
    config: DatasetConfig,
    output_dir: Path,
) -> dict[str, str]:
    dataset_scores = scores[scores["dataset"] == config.dataset].copy()

    scores_path = output_dir / f"{config.dataset}_isolation_forest_anomaly_scores.csv"
    subject_summary_path = (
        output_dir / f"{config.dataset}_isolation_forest_summary_by_subject.csv"
    )
    condition_summary_path = (
        output_dir / f"{config.dataset}_isolation_forest_summary_by_condition.csv"
    )
    overlap_path = (
        output_dir / f"{config.dataset}_isolation_forest_overlap_with_thresholds.csv"
    )
    top_path = output_dir / f"{config.dataset}_isolation_forest_top_windows.csv"

    dataset_scores.to_csv(scores_path, index=False)

    subject_summary = summarize_by_group(
        scores=dataset_scores,
        group_columns=(config.subject_column,),
        score_columns=config.primary_score_columns,
    )
    subject_summary.to_csv(subject_summary_path, index=False)

    condition_summary = summarize_by_group(
        scores=dataset_scores,
        group_columns=(config.condition_column, config.condition_name_column),
        score_columns=config.primary_score_columns,
    )
    condition_summary.to_csv(condition_summary_path, index=False)

    overlap_report = compute_overlap_report(
        scores=dataset_scores,
        config=config,
    )
    overlap_report.to_csv(overlap_path, index=False)

    top_windows = build_top_windows(dataset_scores)
    top_windows.to_csv(top_path, index=False)

    return {
        "scores": str(scores_path),
        "subject_summary": str(subject_summary_path),
        "condition_summary": str(condition_summary_path),
        "overlap": str(overlap_path),
        "top_windows": str(top_path),
    }


def main() -> None:
    output_dir = REPORTS_DIR / "anomaly"
    output_dir.mkdir(parents=True, exist_ok=True)

    pamap2_config, wesad_config = build_dataset_configs()

    pamap2_df = load_pamap2_scores()
    wesad_df = load_wesad_scores()

    print("Loaded PAMAP2:", pamap2_df.shape)
    print("Loaded WESAD:", wesad_df.shape)
    print()

    pamap2_scores = run_dataset(pamap2_df, pamap2_config)
    wesad_scores = run_dataset(wesad_df, wesad_config)

    all_scores = pd.concat([pamap2_scores, wesad_scores], ignore_index=True)

    combined_scores_path = output_dir / "isolation_forest_anomaly_scores_all.csv"
    combined_summary_path = output_dir / "isolation_forest_overall_summary.json"

    all_scores.to_csv(combined_scores_path, index=False)

    pamap2_paths = save_dataset_outputs(
        scores=all_scores,
        config=pamap2_config,
        output_dir=output_dir,
    )

    wesad_paths = save_dataset_outputs(
        scores=all_scores,
        config=wesad_config,
        output_dir=output_dir,
    )

    summary = {
        "model": "IsolationForest",
        "random_state": RANDOM_STATE,
        "n_estimators": N_ESTIMATORS,
        "contamination_values": list(CONTAMINATION_VALUES),
        "thresholds": list(THRESHOLDS),
        "top_n": TOP_N,
        "combined_scores": str(combined_scores_path),
        "pamap2_outputs": pamap2_paths,
        "wesad_outputs": wesad_paths,
        "schema_note": (
            "Outputs include dataset, domain, session_id, subject_id, context columns, "
            "feature_set, anomaly_score, anomaly_score_z, anomaly_rank_percent, and "
            "is_model_anomaly. This schema is intended to remain compatible with later "
            "pilot sensor sessions such as Polar chest strap experiments."
        ),
    }

    with open(combined_summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print()
    print("Saved combined scores:")
    print(combined_scores_path)
    print()
    print("Saved summary:")
    print(combined_summary_path)
    print()
    print("PAMAP2 outputs:")
    for key, value in pamap2_paths.items():
        print(f"- {key}: {value}")
    print()
    print("WESAD outputs:")
    for key, value in wesad_paths.items():
        print(f"- {key}: {value}")

    print()
    print("Quick WESAD condition summary, component_level, contamination=0.05:")
    wesad_condition_summary = pd.read_csv(
        wesad_paths["condition_summary"]
    )
    selected_wesad = wesad_condition_summary[
        (wesad_condition_summary["feature_set"] == "component_level")
        & (wesad_condition_summary["contamination"] == 0.05)
    ]
    print(selected_wesad.to_string(index=False))

    print()
    print("Quick PAMAP2 activity summary, component_level, contamination=0.05:")
    pamap2_condition_summary = pd.read_csv(
        pamap2_paths["condition_summary"]
    )
    selected_pamap2 = pamap2_condition_summary[
        (pamap2_condition_summary["feature_set"] == "component_level")
        & (pamap2_condition_summary["contamination"] == 0.05)
    ]
    print(selected_pamap2.to_string(index=False))


if __name__ == "__main__":
    main()
