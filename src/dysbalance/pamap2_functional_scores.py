import pandas as pd

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR
from src.dysbalance.normalization import z_normalize_by_subject_and_context
from src.dysbalance.thresholds import threshold_sweep


SCORE_FEATURES = [
    "total_acc_rms",
    "log_extremity_chest_acc_ratio",
    "log_hand_ankle_acc_ratio",
]


def load_movement_features() -> pd.DataFrame:
    """Load PAMAP2 movement feature table."""
    path = PROCESSED_DATA_DIR / "pamap2" / "features" / "pamap2_movement_features.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"Missing movement feature file: {path}. "
            "Run src.dysbalance.pamap2_movement_features first."
        )

    return pd.read_csv(path)


def add_functional_z_scores(features: pd.DataFrame) -> pd.DataFrame:
    """
    Add subject- and activity-normalized z-scores for functional features.

    This models deviations relative to the same subject performing the same
    activity.
    """
    scored = features.copy()

    subject_ids = scored["subject_id"].to_numpy()
    activity_ids = scored["activity_id"].to_numpy()

    for feature in SCORE_FEATURES:
        scored[f"z_{feature}"] = z_normalize_by_subject_and_context(
            values=scored[feature].to_numpy(),
            subject_ids=subject_ids,
            context_labels=activity_ids,
        )

    scored["functional_deviation_strength"] = scored[
        [f"z_{feature}" for feature in SCORE_FEATURES]
    ].abs().mean(axis=1)

    return scored


def build_threshold_report(scored: pd.DataFrame) -> pd.DataFrame:
    """Build threshold sweep report for all functional z-scores."""
    rows = []

    for feature in SCORE_FEATURES:
        z_col = f"z_{feature}"

        by_subject = threshold_sweep(
            z_values=scored[z_col].to_numpy(),
            groups=scored["subject_id"].to_numpy(),
            value_name=z_col,
        )
        by_subject["aggregation"] = "subject"

        by_activity = threshold_sweep(
            z_values=scored[z_col].to_numpy(),
            groups=scored["activity_id"].to_numpy(),
            value_name=z_col,
        )
        by_activity["aggregation"] = "activity"

        rows.append(by_subject)
        rows.append(by_activity)

    deviation_strength_report = threshold_sweep(
        z_values=scored["functional_deviation_strength"].to_numpy(),
        groups=scored["subject_id"].to_numpy(),
        value_name="functional_deviation_strength",
        thresholds=(1.0, 1.5, 2.0, 2.5),
    )
    deviation_strength_report["aggregation"] = "subject"

    rows.append(deviation_strength_report)

    return pd.concat(rows, ignore_index=True)


def summarize_subject_scores(scored: pd.DataFrame) -> pd.DataFrame:
    """Create subject-level summary of functional deviation scores."""
    rows = []

    for subject_id, group in scored.groupby("subject_id"):
        row = {
            "subject_id": subject_id,
            "n_windows": len(group),
            "mean_functional_deviation_strength": group[
                "functional_deviation_strength"
            ].mean(),
            "std_functional_deviation_strength": group[
                "functional_deviation_strength"
            ].std(),
        }

        for feature in SCORE_FEATURES:
            z_col = f"z_{feature}"
            row[f"mean_abs_{z_col}"] = group[z_col].abs().mean()
            row[f"pct_abs_{z_col}_gt_2"] = (group[z_col].abs() > 2.0).mean() * 100

        row["pct_functional_deviation_strength_gt_1_5"] = (
            group["functional_deviation_strength"] > 1.5
        ).mean() * 100

        row["pct_functional_deviation_strength_gt_2_0"] = (
            group["functional_deviation_strength"] > 2.0
        ).mean() * 100

        rows.append(row)

    return pd.DataFrame(rows)


def main() -> None:
    out_dir = PROCESSED_DATA_DIR / "pamap2" / "dysbalance"
    out_dir.mkdir(parents=True, exist_ok=True)

    report_dir = REPORTS_DIR / "dysbalance"
    report_dir.mkdir(parents=True, exist_ok=True)

    features = load_movement_features()
    scored = add_functional_z_scores(features)

    threshold_report = build_threshold_report(scored)
    subject_summary = summarize_subject_scores(scored)

    scored_path = out_dir / "pamap2_functional_scores.csv"
    threshold_path = report_dir / "pamap2_functional_threshold_sweep.csv"
    subject_summary_path = report_dir / "pamap2_functional_subject_summary.csv"

    scored.to_csv(scored_path, index=False)
    threshold_report.to_csv(threshold_path, index=False)
    subject_summary.to_csv(subject_summary_path, index=False)

    print("Scored table shape:", scored.shape)
    print()
    print("Subject summary:")
    print(subject_summary.to_string(index=False))
    print()
    print("Selected threshold report rows:")
    print(threshold_report.head(20).to_string(index=False))
    print()
    print(f"Saved scored table to: {scored_path}")
    print(f"Saved threshold report to: {threshold_path}")
    print(f"Saved subject summary to: {subject_summary_path}")


if __name__ == "__main__":
    main()
