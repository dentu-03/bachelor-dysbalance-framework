import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.project_paths import REPORTS_DIR


CONTAMINATION = 0.05
FEATURE_SET = "component_level"


def load_dataset_scores(dataset: str) -> pd.DataFrame:
    path = REPORTS_DIR / "anomaly" / f"{dataset}_isolation_forest_anomaly_scores.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"Missing anomaly score file: {path}. "
            "Run src.anomaly.score_level_isolation_forest first."
        )

    scores = pd.read_csv(path)

    scores = scores[
        (scores["feature_set"] == FEATURE_SET)
        & (scores["contamination"] == CONTAMINATION)
    ].copy()

    return scores


def save_boxplot(
    values_by_group: list[pd.Series],
    labels: list[str],
    title: str,
    xlabel: str,
    ylabel: str,
    out_path,
    rotate_labels: bool = False,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.boxplot(values_by_group, tick_labels=labels, showfliers=False)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if rotate_labels:
        ax.tick_params(axis="x", labelrotation=45)

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    xlabel: str,
    ylabel: str,
    out_path,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.scatter(df[x_col], df[y_col], alpha=0.35, s=12)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_pamap2(fig_dir) -> None:
    scores = load_dataset_scores("pamap2")

    activity_summary = (
        scores.groupby(["activity_id", "activity_name"])["anomaly_score"]
        .median()
        .reset_index()
        .sort_values("activity_id")
    )

    labels = []
    values = []

    for _, row in activity_summary.iterrows():
        activity_id = row["activity_id"]
        activity_name = row["activity_name"]

        subset = scores[
            (scores["activity_id"] == activity_id)
            & (scores["activity_name"] == activity_name)
        ]

        labels.append(f"{int(activity_id)}\n{activity_name}")
        values.append(subset["anomaly_score"].dropna())

    save_boxplot(
        values_by_group=values,
        labels=labels,
        title="PAMAP2 Isolation Forest Anomaly Score by Activity",
        xlabel="Activity",
        ylabel="Isolation Forest anomaly score",
        out_path=fig_dir / "pamap2_isolation_forest_anomaly_score_by_activity.png",
        rotate_labels=True,
    )

    save_scatter(
        df=scores,
        x_col="functional_deviation_strength",
        y_col="anomaly_score",
        title="PAMAP2 Anomaly Score vs Functional Deviation Strength",
        xlabel="Functional deviation strength",
        ylabel="Isolation Forest anomaly score",
        out_path=fig_dir / "pamap2_isolation_forest_vs_functional_deviation_strength.png",
    )


def plot_wesad(fig_dir) -> None:
    scores = load_dataset_scores("wesad")

    label_order = [1, 2, 3, 4]
    label_names = {
        1: "baseline",
        2: "stress",
        3: "amusement",
        4: "meditation",
    }

    labels = []
    values = []

    for label in label_order:
        subset = scores[scores["label"] == label]
        labels.append(f"{label}\n{label_names[label]}")
        values.append(subset["anomaly_score"].dropna())

    save_boxplot(
        values_by_group=values,
        labels=labels,
        title="WESAD Isolation Forest Anomaly Score by Condition",
        xlabel="Condition",
        ylabel="Isolation Forest anomaly score",
        out_path=fig_dir / "wesad_isolation_forest_anomaly_score_by_condition.png",
        rotate_labels=False,
    )

    save_scatter(
        df=scores,
        x_col="autonomic_deviation_strength",
        y_col="anomaly_score",
        title="WESAD Anomaly Score vs Autonomic Deviation Strength",
        xlabel="Autonomic deviation strength",
        ylabel="Isolation Forest anomaly score",
        out_path=fig_dir / "wesad_isolation_forest_vs_autonomic_deviation_strength.png",
    )

    save_scatter(
        df=scores,
        x_col="z_autonomic_activation",
        y_col="anomaly_score",
        title="WESAD Anomaly Score vs Autonomic Activation",
        xlabel="z autonomic activation",
        ylabel="Isolation Forest anomaly score",
        out_path=fig_dir / "wesad_isolation_forest_vs_autonomic_activation.png",
    )


def main() -> None:
    fig_dir = REPORTS_DIR / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    plot_pamap2(fig_dir)
    plot_wesad(fig_dir)

    print("Saved anomaly figures:")
    for path in sorted(fig_dir.glob("*isolation_forest*.png")):
        print(path)


if __name__ == "__main__":
    main()
