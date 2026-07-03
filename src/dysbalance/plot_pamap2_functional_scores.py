import matplotlib.pyplot as plt
import pandas as pd

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR


def load_scores() -> pd.DataFrame:
    """Load PAMAP2 functional score table."""
    path = (
        PROCESSED_DATA_DIR
        / "pamap2"
        / "dysbalance"
        / "pamap2_functional_scores.csv"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Missing score file: {path}. "
            "Run src.dysbalance.pamap2_functional_scores first."
        )

    return pd.read_csv(path)


def plot_subject_boxplot(scores: pd.DataFrame, out_path) -> None:
    """Plot functional deviation strength distribution per subject."""
    subjects = sorted(scores["subject_id"].unique())
    data = [
        scores.loc[
            scores["subject_id"] == subject,
            "functional_deviation_strength",
        ].to_numpy()
        for subject in subjects
    ]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.boxplot(data, tick_labels=[str(subject) for subject in subjects], showfliers=False)
    ax.axhline(1.5, linestyle="--", linewidth=1)
    ax.axhline(2.0, linestyle="--", linewidth=1)

    ax.set_title("PAMAP2 Functional Deviation Strength by Subject")
    ax.set_xlabel("Subject")
    ax.set_ylabel("Functional Deviation Strength")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_activity_boxplot(scores: pd.DataFrame, out_path) -> None:
    """Plot functional deviation strength distribution per activity."""
    activities = sorted(scores["activity_id"].unique())
    data = [
        scores.loc[
            scores["activity_id"] == activity,
            "functional_deviation_strength",
        ].to_numpy()
        for activity in activities
    ]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.boxplot(data, tick_labels=[str(activity) for activity in activities], showfliers=False)
    ax.axhline(1.5, linestyle="--", linewidth=1)
    ax.axhline(2.0, linestyle="--", linewidth=1)

    ax.set_title("PAMAP2 Functional Deviation Strength by Activity")
    ax.set_xlabel("Activity ID")
    ax.set_ylabel("Functional Deviation Strength")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    scores = load_scores()

    out_dir = REPORTS_DIR / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    subject_plot = out_dir / "pamap2_functional_deviation_by_subject.png"
    activity_plot = out_dir / "pamap2_functional_deviation_by_activity.png"

    plot_subject_boxplot(scores, subject_plot)
    plot_activity_boxplot(scores, activity_plot)

    print(f"Saved subject plot to: {subject_plot}")
    print(f"Saved activity plot to: {activity_plot}")


if __name__ == "__main__":
    main()
