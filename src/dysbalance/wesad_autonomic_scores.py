import numpy as np
import pandas as pd

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR
from src.dysbalance.normalization import z_normalize_by_subject
from src.dysbalance.thresholds import threshold_sweep


ACTIVATION_COMPONENTS = [
    "z_hr_bpm",
    "z_eda_mean",
    "z_resp_std",
    "z_inverse_rmssd",
]


def load_autonomic_features() -> pd.DataFrame:
    """Load WESAD autonomic feature table."""
    path = PROCESSED_DATA_DIR / "wesad" / "features" / "wesad_autonomic_features.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"Missing WESAD autonomic feature file: {path}. "
            "Run src.dysbalance.wesad_autonomic_features first."
        )

    return pd.read_csv(path)


def add_autonomic_scores(features: pd.DataFrame) -> pd.DataFrame:
    """
    Add subject-normalized autonomic activation and dysbalance scores.

    Components:
    - high HR
    - high EDA
    - high respiratory variability
    - low RMSSD represented as inverse RMSSD z-score
    """
    scored = features.copy()
    subject_ids = scored["subject_id"].to_numpy()

    scored["z_hr_bpm"] = z_normalize_by_subject(
        values=scored["hr_bpm"].to_numpy(),
        subject_ids=subject_ids,
    )

    scored["z_eda_mean"] = z_normalize_by_subject(
        values=scored["eda_mean"].to_numpy(),
        subject_ids=subject_ids,
    )

    scored["z_resp_std"] = z_normalize_by_subject(
        values=scored["resp_std"].to_numpy(),
        subject_ids=subject_ids,
    )

    scored["z_rmssd_ms"] = z_normalize_by_subject(
        values=scored["rmssd_ms"].to_numpy(),
        subject_ids=subject_ids,
    )

    scored["z_inverse_rmssd"] = -scored["z_rmssd_ms"]

    scored["autonomic_activation_raw"] = scored[ACTIVATION_COMPONENTS].mean(axis=1)

    scored["z_autonomic_activation"] = z_normalize_by_subject(
        values=scored["autonomic_activation_raw"].to_numpy(),
        subject_ids=subject_ids,
    )

    scored["autonomic_deviation_strength"] = scored[
        [
            "z_hr_bpm",
            "z_eda_mean",
            "z_resp_std",
            "z_inverse_rmssd",
        ]
    ].abs().mean(axis=1)

    return scored


def summarize_by_label(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize autonomic scores by WESAD condition label."""
    rows = []

    for label, group in scored.groupby("label"):
        rows.append(
            {
                "label": int(label),
                "label_name": group["label_name"].iloc[0],
                "n_windows": len(group),
                "mean_z_autonomic_activation": group[
                    "z_autonomic_activation"
                ].mean(),
                "std_z_autonomic_activation": group[
                    "z_autonomic_activation"
                ].std(),
                "mean_autonomic_deviation_strength": group[
                    "autonomic_deviation_strength"
                ].mean(),
                "pct_z_autonomic_activation_gt_1_5": (
                    group["z_autonomic_activation"] > 1.5
                ).mean()
                * 100,
                "pct_z_autonomic_activation_gt_2_0": (
                    group["z_autonomic_activation"] > 2.0
                ).mean()
                * 100,
                "pct_autonomic_deviation_strength_gt_1_5": (
                    group["autonomic_deviation_strength"] > 1.5
                ).mean()
                * 100,
                "pct_autonomic_deviation_strength_gt_2_0": (
                    group["autonomic_deviation_strength"] > 2.0
                ).mean()
                * 100,
            }
        )

    return pd.DataFrame(rows)


def summarize_by_subject_and_label(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize autonomic scores by subject and label."""
    rows = []

    for (subject_id, label), group in scored.groupby(["subject_id", "label"]):
        rows.append(
            {
                "subject_id": subject_id,
                "label": int(label),
                "label_name": group["label_name"].iloc[0],
                "n_windows": len(group),
                "mean_z_autonomic_activation": group[
                    "z_autonomic_activation"
                ].mean(),
                "mean_autonomic_deviation_strength": group[
                    "autonomic_deviation_strength"
                ].mean(),
                "pct_z_autonomic_activation_gt_1_5": (
                    group["z_autonomic_activation"] > 1.5
                ).mean()
                * 100,
                "pct_z_autonomic_activation_gt_2_0": (
                    group["z_autonomic_activation"] > 2.0
                ).mean()
                * 100,
            }
        )

    return pd.DataFrame(rows)


def build_threshold_report(scored: pd.DataFrame) -> pd.DataFrame:
    """Build absolute threshold sweep reports for autonomic scores."""
    rows = []

    for value_name in [
        "z_autonomic_activation",
        "autonomic_deviation_strength",
        "z_hr_bpm",
        "z_eda_mean",
        "z_resp_std",
        "z_inverse_rmssd",
    ]:
        report = threshold_sweep(
            z_values=scored[value_name].to_numpy(),
            groups=scored["label_name"].to_numpy(),
            value_name=value_name,
            thresholds=(1.0, 1.5, 2.0, 2.5, 3.0),
        )
        report["aggregation"] = "label"
        rows.append(report)

    return pd.concat(rows, ignore_index=True)


def main() -> None:
    out_dir = PROCESSED_DATA_DIR / "wesad" / "dysbalance"
    out_dir.mkdir(parents=True, exist_ok=True)

    report_dir = REPORTS_DIR / "dysbalance"
    report_dir.mkdir(parents=True, exist_ok=True)

    features = load_autonomic_features()
    scored = add_autonomic_scores(features)

    label_summary = summarize_by_label(scored)
    subject_label_summary = summarize_by_subject_and_label(scored)
    threshold_report = build_threshold_report(scored)

    scored_path = out_dir / "wesad_autonomic_scores.csv"
    label_summary_path = report_dir / "wesad_autonomic_label_summary.csv"
    subject_label_summary_path = report_dir / "wesad_autonomic_subject_label_summary.csv"
    threshold_path = report_dir / "wesad_autonomic_threshold_sweep.csv"

    scored.to_csv(scored_path, index=False)
    label_summary.to_csv(label_summary_path, index=False)
    subject_label_summary.to_csv(subject_label_summary_path, index=False)
    threshold_report.to_csv(threshold_path, index=False)

    print("Scored table shape:", scored.shape)
    print()
    print("Label summary:")
    print(label_summary.to_string(index=False))
    print()
    print("Selected threshold rows:")
    print(threshold_report.head(20).to_string(index=False))
    print()
    print(f"Saved scored table to: {scored_path}")
    print(f"Saved label summary to: {label_summary_path}")
    print(f"Saved subject-label summary to: {subject_label_summary_path}")
    print(f"Saved threshold report to: {threshold_path}")


if __name__ == "__main__":
    main()
