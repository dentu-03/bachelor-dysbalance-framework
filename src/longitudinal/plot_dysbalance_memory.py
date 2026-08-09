from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.project_paths import REPORTS_DIR


def plot_hypothesis_status(hypotheses: pd.DataFrame, output_path: Path) -> None:
    status_order = ["new", "observed", "confirmed", "stable", "weakened", "discarded"]

    counts = pd.crosstab(
        hypotheses["dataset"],
        hypotheses["current_status"],
    )

    counts = counts.reindex(columns=[c for c in status_order if c in counts.columns], fill_value=0)

    ax = counts.plot(kind="bar", figsize=(9, 5))

    ax.set_title("Longitudinal Dysbalance Memory: Hypothesis Status by Dataset")
    ax.set_xlabel("Dataset")
    ax.set_ylabel("Number of hypotheses")
    ax.legend(title="Hypothesis status")
    ax.grid(axis="y", alpha=0.3)

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_hypothesis_types(hypotheses: pd.DataFrame, output_path: Path) -> None:
    counts = pd.crosstab(
        hypotheses["dataset"],
        hypotheses["event_type"],
    )

    ax = counts.plot(kind="bar", figsize=(11, 5))

    ax.set_title("Longitudinal Dysbalance Memory: Hypothesis Types by Dataset")
    ax.set_xlabel("Dataset")
    ax.set_ylabel("Number of hypotheses")
    ax.legend(title="Event type", fontsize=8)
    ax.grid(axis="y", alpha=0.3)

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def main() -> None:
    input_path = REPORTS_DIR / "longitudinal" / "dysbalance_hypotheses.csv"
    output_dir = REPORTS_DIR / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Missing memory hypotheses file: {input_path}")

    hypotheses = pd.read_csv(input_path)

    status_path = output_dir / "longitudinal_memory_hypothesis_status_by_dataset.png"
    type_path = output_dir / "longitudinal_memory_hypothesis_types_by_dataset.png"

    plot_hypothesis_status(hypotheses, status_path)
    plot_hypothesis_types(hypotheses, type_path)

    print(f"Saved: {status_path}")
    print(f"Saved: {type_path}")


if __name__ == "__main__":
    main()
