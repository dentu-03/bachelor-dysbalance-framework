from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_DIR = Path("reports/models/cross_dataset/multirocket_error_dysbalance_link")
FIGURE_DIR = Path("reports/figures/multirocket_error_dysbalance_link")
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def save_score_group_plot(summary: pd.DataFrame) -> None:
    plot_df = summary[[
        "dataset",
        "mean_score_correct",
        "mean_score_incorrect",
    ]].copy()

    x = range(len(plot_df))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width / 2 for i in x], plot_df["mean_score_correct"], width, label="Correct")
    ax.bar([i + width / 2 for i in x], plot_df["mean_score_incorrect"], width, label="Incorrect")

    ax.set_title("MultiRocket Error-Dysbalance Link: Mean Score")
    ax.set_ylabel("Mean dysbalance score")
    ax.set_xticks(list(x))
    ax.set_xticklabels(plot_df["dataset"])
    ax.legend()

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "mean_score_correct_vs_incorrect.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_anomaly_rate_plot(summary: pd.DataFrame) -> None:
    plot_df = summary[[
        "dataset",
        "anomaly_rate_correct_pct",
        "anomaly_rate_incorrect_pct",
    ]].copy()

    x = range(len(plot_df))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width / 2 for i in x], plot_df["anomaly_rate_correct_pct"], width, label="Correct")
    ax.bar([i + width / 2 for i in x], plot_df["anomaly_rate_incorrect_pct"], width, label="Incorrect")

    ax.set_title("MultiRocket Error-Dysbalance Link: Anomaly Rate")
    ax.set_ylabel("Anomaly rate (%)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(plot_df["dataset"])
    ax.legend()

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "anomaly_rate_correct_vs_incorrect.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_score_diff_ci_plot(stats: pd.DataFrame) -> None:
    plot_df = stats.copy()
    x = range(len(plot_df))
    y = plot_df["mean_score_diff_incorrect_minus_correct"]
    low = plot_df["score_diff_ci95_low"]
    high = plot_df["score_diff_ci95_high"]

    yerr_low = y - low
    yerr_high = high - y

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(
        list(x),
        y,
        yerr=[yerr_low, yerr_high],
        fmt="o",
        capsize=5,
    )
    ax.axhline(0, linewidth=1)

    ax.set_title("Score Difference: Incorrect Minus Correct")
    ax.set_ylabel("Mean score difference with 95% CI")
    ax.set_xticks(list(x))
    ax.set_xticklabels(plot_df["dataset"])

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "score_difference_incorrect_minus_correct_ci.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_cliffs_delta_plot(stats: pd.DataFrame) -> None:
    plot_df = stats.copy()
    x = range(len(plot_df))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(list(x), plot_df["score_cliffs_delta_incorrect_vs_correct"])
    ax.axhline(0, linewidth=1)

    ax.set_title("Effect Size: Cliff's Delta")
    ax.set_ylabel("Cliff's delta, incorrect vs. correct")
    ax.set_xticks(list(x))
    ax.set_xticklabels(plot_df["dataset"])

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "cliffs_delta_incorrect_vs_correct.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    summary = pd.read_csv(INPUT_DIR / "cross_dataset_error_dysbalance_summary.csv")
    stats = pd.read_csv(INPUT_DIR / "cross_dataset_error_dysbalance_statistics.csv")

    save_score_group_plot(summary)
    save_anomaly_rate_plot(summary)
    save_score_diff_ci_plot(stats)
    save_cliffs_delta_plot(stats)

    print("Saved figures:")
    for path in sorted(FIGURE_DIR.glob("*.png")):
        print(path)


if __name__ == "__main__":
    main()
