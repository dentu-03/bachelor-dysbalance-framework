import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR


LABEL_ORDER = [1, 2, 3, 4]
LABEL_NAMES = {
    1: "baseline",
    2: "stress",
    3: "amusement",
    4: "meditation",
}

COMPONENT_COLUMNS = [
    "z_hr_bpm",
    "z_eda_mean",
    "z_resp_std",
    "z_inverse_rmssd",
]


def load_scores() -> pd.DataFrame:
    """Load WESAD autonomic score table."""
    path = PROCESSED_DATA_DIR / "wesad" / "dysbalance" / "wesad_autonomic_scores.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"Missing WESAD autonomic score file: {path}. "
            "Run src.dysbalance.wesad_autonomic_scores first."
        )

    return pd.read_csv(path)


def label_tick_names() -> list[str]:
    """Create readable label names for plots."""
    return [f"{label}\n{LABEL_NAMES[label]}" for label in LABEL_ORDER]


def save_activation_boxplot(scores: pd.DataFrame, out_path) -> None:
    """Plot subject-normalized autonomic activation by label."""
    data = [
        scores.loc[scores["label"] == label, "z_autonomic_activation"].dropna()
        for label in LABEL_ORDER
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.boxplot(data, tick_labels=label_tick_names(), showfliers=False)
    ax.axhline(0.0, linestyle="--", linewidth=1)
    ax.axhline(1.5, linestyle="--", linewidth=1)
    ax.axhline(2.0, linestyle="--", linewidth=1)

    ax.set_title("WESAD Autonomic Activation by Condition")
    ax.set_xlabel("Condition")
    ax.set_ylabel("Subject-normalized autonomic activation (z)")

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_deviation_strength_boxplot(scores: pd.DataFrame, out_path) -> None:
    """Plot autonomic deviation strength by label."""
    data = [
        scores.loc[scores["label"] == label, "autonomic_deviation_strength"].dropna()
        for label in LABEL_ORDER
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.boxplot(data, tick_labels=label_tick_names(), showfliers=False)
    ax.axhline(1.5, linestyle="--", linewidth=1)
    ax.axhline(2.0, linestyle="--", linewidth=1)

    ax.set_title("WESAD Autonomic Deviation Strength by Condition")
    ax.set_xlabel("Condition")
    ax.set_ylabel("Mean absolute component z-score")

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_component_mean_plot(scores: pd.DataFrame, out_path) -> None:
    """Plot mean autonomic score components by condition."""
    component_means = (
        scores.groupby("label")[COMPONENT_COLUMNS]
        .mean()
        .reindex(LABEL_ORDER)
    )

    component_means.index = [LABEL_NAMES[label] for label in LABEL_ORDER]

    fig, ax = plt.subplots(figsize=(9, 5))

    component_means.plot(kind="bar", ax=ax)

    ax.axhline(0.0, linestyle="--", linewidth=1)
    ax.set_title("WESAD Mean Autonomic Components by Condition")
    ax.set_xlabel("Condition")
    ax.set_ylabel("Mean subject-normalized component value")
    ax.legend(
        [
            "HR",
            "EDA",
            "Respiration variability",
            "Inverse RMSSD",
        ],
        title="Component",
        fontsize=8,
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    fig_dir = REPORTS_DIR / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    scores = load_scores()

    activation_path = fig_dir / "wesad_autonomic_activation_by_condition.png"
    strength_path = fig_dir / "wesad_autonomic_deviation_strength_by_condition.png"
    component_path = fig_dir / "wesad_autonomic_component_means_by_condition.png"

    save_activation_boxplot(scores, activation_path)
    save_deviation_strength_boxplot(scores, strength_path)
    save_component_mean_plot(scores, component_path)

    print("Saved WESAD autonomic plots:")
    print(activation_path)
    print(strength_path)
    print(component_path)


if __name__ == "__main__":
    main()
