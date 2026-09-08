from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_DIR = Path("reports/models/cross_dataset/multirocket_error_memory_link")
FIGURE_DIR = Path("reports/figures/multirocket_error_memory_link")
DOC_PATH = Path("docs/results/multirocket_error_memory_link_summary.md")

FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def save_memory_event_rate_plot(summary: pd.DataFrame) -> None:
    x = range(len(summary))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width / 2 for i in x], summary["memory_event_rate_correct_pct"], width, label="Correct")
    ax.bar([i + width / 2 for i in x], summary["memory_event_rate_incorrect_pct"], width, label="Incorrect")

    ax.set_title("MultiRocket Error-Memory Link: Event Rate")
    ax.set_ylabel("Memory event rate (%)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary["dataset"])
    ax.legend()

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "memory_event_rate_correct_vs_incorrect.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_memory_hypothesis_rate_plot(summary: pd.DataFrame) -> None:
    x = range(len(summary))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width / 2 for i in x], summary["memory_hypothesis_rate_correct_pct"], width, label="Correct")
    ax.bar([i + width / 2 for i in x], summary["memory_hypothesis_rate_incorrect_pct"], width, label="Incorrect")

    ax.set_title("MultiRocket Error-Memory Link: Hypothesis Rate")
    ax.set_ylabel("Memory hypothesis rate (%)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary["dataset"])
    ax.legend()

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "memory_hypothesis_rate_correct_vs_incorrect.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_event_odds_ratio_plot(summary: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(summary["dataset"], summary["memory_event_odds_ratio_incorrect_vs_correct"])
    ax.axhline(1, linewidth=1)

    ax.set_title("MultiRocket Error-Memory Link: Event Odds Ratio")
    ax.set_ylabel("Odds ratio, incorrect vs. correct")

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "memory_event_odds_ratio_incorrect_vs_correct.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_combined_event_rate_plot(summary: pd.DataFrame) -> None:
    x = range(len(summary))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width / 2 for i in x], summary["combined_score_model_event_rate_correct_pct"], width, label="Correct")
    ax.bar([i + width / 2 for i in x], summary["combined_score_model_event_rate_incorrect_pct"], width, label="Incorrect")

    ax.set_title("Combined Score-Model Events")
    ax.set_ylabel("Combined event rate (%)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary["dataset"])
    ax.legend()

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "combined_score_model_event_rate_correct_vs_incorrect.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def update_doc() -> None:
    text = DOC_PATH.read_text()

    section = """
## Abbildungen

Die folgenden Abbildungen wurden für den späteren Ergebnisteil erzeugt:

| Abbildung | Datei |
|---|---|
| Memory Event Rate korrekt vs. falsch | `reports/figures/multirocket_error_memory_link/memory_event_rate_correct_vs_incorrect.png` |
| Memory Hypothesis Rate korrekt vs. falsch | `reports/figures/multirocket_error_memory_link/memory_hypothesis_rate_correct_vs_incorrect.png` |
| Memory Event Odds Ratio | `reports/figures/multirocket_error_memory_link/memory_event_odds_ratio_incorrect_vs_correct.png` |
| Combined Score-Model Event Rate | `reports/figures/multirocket_error_memory_link/combined_score_model_event_rate_correct_vs_incorrect.png` |
""".strip()

    heading = "## Abbildungen"
    if heading in text:
        text = text.split(heading)[0].rstrip() + "\n\n" + section + "\n"
    else:
        text = text.rstrip() + "\n\n" + section + "\n"

    DOC_PATH.write_text(text)


def main() -> None:
    summary = pd.read_csv(INPUT_DIR / "cross_dataset_error_memory_summary.csv")

    save_memory_event_rate_plot(summary)
    save_memory_hypothesis_rate_plot(summary)
    save_event_odds_ratio_plot(summary)
    save_combined_event_rate_plot(summary)
    update_doc()

    print("Saved figures:")
    for path in sorted(FIGURE_DIR.glob("*.png")):
        print(path)

    print()
    print("Updated doc:", DOC_PATH)


if __name__ == "__main__":
    main()
