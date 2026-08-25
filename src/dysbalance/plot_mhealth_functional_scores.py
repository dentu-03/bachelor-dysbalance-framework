from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR


INPUT_PATH = (
    PROCESSED_DATA_DIR
    / "mhealth"
    / "dysbalance"
    / "mhealth_functional_scores.csv"
)

OUTPUT_DIR = REPORTS_DIR / "figures"


def plot_functional_deviation_by_activity(scores: pd.DataFrame) -> None:
    output_path = OUTPUT_DIR / "mhealth_functional_deviation_by_activity.png"

    order = (
        scores[["label", "activity_name"]]
        .drop_duplicates()
        .sort_values("label")["activity_name"]
        .tolist()
    )

    data = [
        scores.loc[scores["activity_name"] == activity, "functional_deviation_strength"]
        for activity in order
    ]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.boxplot(data, tick_labels=order, showfliers=True)
    ax.axhline(1.5, linestyle="--", linewidth=1, label="threshold 1.5")
    ax.axhline(2.0, linestyle="--", linewidth=1, label="threshold 2.0")
    ax.set_title("MHEALTH Functional Deviation Strength by Activity")
    ax.set_xlabel("Activity")
    ax.set_ylabel("Functional deviation strength")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved: {output_path}")


def plot_functional_deviation_by_subject(scores: pd.DataFrame) -> None:
    output_path = OUTPUT_DIR / "mhealth_functional_deviation_by_subject.png"

    subjects = sorted(scores["subject_id"].unique())
    data = [
        scores.loc[scores["subject_id"] == subject, "functional_deviation_strength"]
        for subject in subjects
    ]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot(data, tick_labels=[str(subject) for subject in subjects], showfliers=True)
    ax.axhline(1.5, linestyle="--", linewidth=1, label="threshold 1.5")
    ax.axhline(2.0, linestyle="--", linewidth=1, label="threshold 2.0")
    ax.set_title("MHEALTH Functional Deviation Strength by Subject")
    ax.set_xlabel("Subject")
    ax.set_ylabel("Functional deviation strength")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved: {output_path}")


def plot_dominant_components(scores: pd.DataFrame) -> None:
    output_path = OUTPUT_DIR / "mhealth_top_deviation_components.png"

    top = scores.sort_values("functional_deviation_strength", ascending=False).head(100)
    counts = top["dominant_functional_component"].value_counts().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    counts.plot(kind="bar", ax=ax)
    ax.set_title("MHEALTH Dominant Components in Top 100 Functional Deviations")
    ax.set_xlabel("Dominant functional component")
    ax.set_ylabel("Number of top-deviation windows")
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved: {output_path}")


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing MHEALTH score file: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(INPUT_PATH)

    plot_functional_deviation_by_activity(scores)
    plot_functional_deviation_by_subject(scores)
    plot_dominant_components(scores)


if __name__ == "__main__":
    main()
