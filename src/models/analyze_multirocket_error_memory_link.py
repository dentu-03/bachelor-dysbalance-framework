from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

from src.project_paths import REPORTS_DIR


ERROR_LINK_DIR = REPORTS_DIR / "models" / "cross_dataset" / "multirocket_error_dysbalance_link"
OUTPUT_DIR = REPORTS_DIR / "models" / "cross_dataset" / "multirocket_error_memory_link"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EVENTS_PATH = REPORTS_DIR / "longitudinal" / "dysbalance_events.csv"
EPISODES_PATH = REPORTS_DIR / "longitudinal" / "dysbalance_episodes.csv"
HYPOTHESES_PATH = REPORTS_DIR / "longitudinal" / "dysbalance_hypotheses.csv"

DOC_PATH = Path("docs/results/multirocket_error_memory_link_summary.md")
FRAMEWORK_PATH = Path("docs/results/framework_cross_dataset_summary.md")


DATASETS = [
    {
        "dataset": "MHEALTH",
        "joined_path": ERROR_LINK_DIR / "mhealth_joined_predictions_scores_anomalies.csv",
        "score_column": "functional_deviation_strength",
        "true_col": "activity_name",
        "pred_col": "y_pred",
        "join_mode": "position",
    },
    {
        "dataset": "PAMAP2",
        "joined_path": ERROR_LINK_DIR / "pamap2_joined_predictions_scores_anomalies.csv",
        "score_column": "functional_deviation_strength",
        "true_col": "true_activity_name",
        "pred_col": "pred_activity_name",
        "join_mode": "window",
    },
    {
        "dataset": "WESAD",
        "joined_path": ERROR_LINK_DIR / "wesad_joined_predictions_scores_anomalies.csv",
        "score_column": "autonomic_deviation_strength",
        "true_col": "true_label_name",
        "pred_col": "pred_label_name",
        "join_mode": "window",
    },
]


def as_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def normalize_subject(series: pd.Series) -> pd.Series:
    return series.astype(str).str.replace(r"\.0$", "", regex=True)


def unique_join(values: pd.Series) -> str:
    cleaned = set()

    for value in values.dropna().tolist():
        for part in str(value).split(";"):
            part = part.strip()
            if part and part.lower() != "nan":
                cleaned.add(part)

    return ";".join(sorted(cleaned))


def odds_ratio_and_p(df: pd.DataFrame, flag_col: str) -> tuple[float, float]:
    correct = df[df["is_correct_bool"]]
    incorrect = df[~df["is_correct_bool"]]

    a = int(incorrect[flag_col].sum())
    b = int(len(incorrect) - a)
    c = int(correct[flag_col].sum())
    d = int(len(correct) - c)

    odds_ratio, p_value = fisher_exact([[a, b], [c, d]], alternative="two-sided")
    return float(odds_ratio), float(p_value)


def prepare_memory_events() -> pd.DataFrame:
    events = pd.read_csv(EVENTS_PATH)
    hypotheses = pd.read_csv(HYPOTHESES_PATH)

    events = events.copy()
    hypotheses = hypotheses.copy()

    events["dataset_key"] = events["dataset"].astype(str).str.lower()
    hypotheses["dataset_key"] = hypotheses["dataset"].astype(str).str.lower()

    events["subject_key"] = normalize_subject(events["subject_id"])
    hypotheses["subject_key"] = normalize_subject(hypotheses["subject_id"])

    events["window_key"] = pd.to_numeric(events["window_index"], errors="coerce").astype("Int64")
    events["start_key"] = pd.to_numeric(events["start_position"], errors="coerce").round().astype("Int64")
    events["end_key"] = pd.to_numeric(events["end_position"], errors="coerce").round().astype("Int64")

    hypothesis_lookup = (
        hypotheses.groupby(["dataset_key", "subject_key", "event_type", "context_name"])
        .agg(
            n_hypotheses=("hypothesis_id", "nunique"),
            hypothesis_ids=("hypothesis_id", unique_join),
            hypothesis_statuses=("current_status", unique_join),
            evidence_scopes=("evidence_scope", unique_join),
        )
        .reset_index()
    )

    events = events.merge(
        hypothesis_lookup,
        on=["dataset_key", "subject_key", "event_type", "context_name"],
        how="left",
    )

    events["n_hypotheses"] = events["n_hypotheses"].fillna(0).astype(int)
    events["has_memory_hypothesis"] = events["n_hypotheses"] > 0
    events["is_model_anomaly_bool"] = as_bool(events["is_model_anomaly"])
    events["is_threshold_event_bool"] = as_bool(events["is_threshold_event"])
    events["is_high_rank_event_bool"] = as_bool(events["is_high_rank_event"])
    events["is_combined_score_model_event"] = events["event_type"].astype(str).eq("combined_score_model_event")
    events["is_model_anomaly_event"] = events["event_type"].astype(str).eq("model_anomaly")

    return events


def aggregate_events(events: pd.DataFrame, dataset: str, join_mode: str) -> pd.DataFrame:
    dataset_key = dataset.lower()
    ev = events[events["dataset_key"] == dataset_key].copy()

    if join_mode == "position":
        keys = ["dataset_key", "subject_key", "start_key", "end_key"]
    elif join_mode == "window":
        keys = ["dataset_key", "subject_key", "window_key"]
    else:
        raise ValueError(f"Unknown join mode: {join_mode}")

    agg = (
        ev.groupby(keys)
        .agg(
            n_memory_events=("event_id", "nunique"),
            n_memory_episodes=("episode_id", "nunique"),
            n_memory_hypotheses=("n_hypotheses", "max"),
            max_memory_event_strength=("event_strength", "max"),
            mean_memory_event_strength=("event_strength", "mean"),
            memory_event_types=("event_type", unique_join),
            memory_episode_ids=("episode_id", unique_join),
            memory_hypothesis_ids=("hypothesis_ids", unique_join),
            memory_hypothesis_statuses=("hypothesis_statuses", unique_join),
            has_model_anomaly_memory=("is_model_anomaly_bool", "max"),
            has_threshold_memory=("is_threshold_event_bool", "max"),
            has_high_rank_memory=("is_high_rank_event_bool", "max"),
            has_combined_score_model_event=("is_combined_score_model_event", "max"),
            has_model_anomaly_event=("is_model_anomaly_event", "max"),
            has_memory_hypothesis=("has_memory_hypothesis", "max"),
        )
        .reset_index()
    )

    agg["has_memory_event"] = agg["n_memory_events"] > 0
    agg["has_memory_episode"] = agg["n_memory_episodes"] > 0
    agg["has_memory_hypothesis"] = agg["has_memory_hypothesis"].astype(bool)

    return agg


def load_and_join_dataset(config: dict, memory_events: pd.DataFrame) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    dataset = config["dataset"]
    dataset_key = dataset.lower()
    join_mode = config["join_mode"]

    df = pd.read_csv(config["joined_path"]).copy()

    df["dataset_key"] = dataset_key
    df["subject_key"] = normalize_subject(df["subject_id"])
    df["is_correct_bool"] = as_bool(df["is_correct"])

    if "is_model_anomaly" in df.columns:
        df["is_model_anomaly_bool"] = as_bool(df["is_model_anomaly"])
    else:
        df["is_model_anomaly_bool"] = False

    if join_mode == "position":
        df["start_key"] = pd.to_numeric(df["start_sample"], errors="coerce").round().astype("Int64")
        df["end_key"] = pd.to_numeric(df["end_sample"], errors="coerce").round().astype("Int64")
        keys = ["dataset_key", "subject_key", "start_key", "end_key"]
    else:
        df["window_key"] = pd.to_numeric(df["window_index"], errors="coerce").astype("Int64")
        keys = ["dataset_key", "subject_key", "window_key"]

    event_agg = aggregate_events(memory_events, dataset, join_mode)

    joined = df.merge(event_agg, on=keys, how="left", validate="many_to_one")

    fill_false_cols = [
        "has_model_anomaly_memory",
        "has_threshold_memory",
        "has_high_rank_memory",
        "has_combined_score_model_event",
        "has_model_anomaly_event",
        "has_memory_event",
        "has_memory_episode",
        "has_memory_hypothesis",
    ]

    for col in fill_false_cols:
        joined[col] = joined[col].map(lambda value: bool(value) if pd.notna(value) else False)

    fill_zero_cols = [
        "n_memory_events",
        "n_memory_episodes",
        "n_memory_hypotheses",
        "max_memory_event_strength",
        "mean_memory_event_strength",
    ]

    for col in fill_zero_cols:
        joined[col] = joined[col].fillna(0)

    for col in [
        "memory_event_types",
        "memory_episode_ids",
        "memory_hypothesis_ids",
        "memory_hypothesis_statuses",
    ]:
        joined[col] = joined[col].fillna("")

    joined.to_csv(OUTPUT_DIR / f"{dataset_key}_joined_predictions_scores_anomalies_memory.csv", index=False)

    summary = summarize_dataset(joined, dataset, config["score_column"])

    top_errors = summarize_top_errors(
        joined,
        dataset=dataset,
        true_col=config["true_col"],
        pred_col=config["pred_col"],
        score_col=config["score_column"],
    )

    return joined, summary, top_errors


def summarize_dataset(df: pd.DataFrame, dataset: str, score_col: str) -> dict:
    correct = df[df["is_correct_bool"]]
    incorrect = df[~df["is_correct_bool"]]

    def rate(frame: pd.DataFrame, col: str) -> float:
        if len(frame) == 0:
            return float("nan")
        return float(frame[col].mean() * 100)

    event_or, event_p = odds_ratio_and_p(df, "has_memory_event")
    episode_or, episode_p = odds_ratio_and_p(df, "has_memory_episode")
    hypothesis_or, hypothesis_p = odds_ratio_and_p(df, "has_memory_hypothesis")

    return {
        "dataset": dataset,
        "n_total": int(len(df)),
        "n_correct": int(len(correct)),
        "n_incorrect": int(len(incorrect)),
        "error_rate_pct": float(len(incorrect) / len(df) * 100),
        "score_column": score_col,
        "mean_score_correct": float(correct[score_col].mean()),
        "mean_score_incorrect": float(incorrect[score_col].mean()),
        "memory_event_rate_correct_pct": rate(correct, "has_memory_event"),
        "memory_event_rate_incorrect_pct": rate(incorrect, "has_memory_event"),
        "memory_event_rate_difference_pct": rate(incorrect, "has_memory_event") - rate(correct, "has_memory_event"),
        "memory_event_odds_ratio_incorrect_vs_correct": event_or,
        "memory_event_fisher_p": event_p,
        "memory_episode_rate_correct_pct": rate(correct, "has_memory_episode"),
        "memory_episode_rate_incorrect_pct": rate(incorrect, "has_memory_episode"),
        "memory_episode_odds_ratio_incorrect_vs_correct": episode_or,
        "memory_episode_fisher_p": episode_p,
        "memory_hypothesis_rate_correct_pct": rate(correct, "has_memory_hypothesis"),
        "memory_hypothesis_rate_incorrect_pct": rate(incorrect, "has_memory_hypothesis"),
        "memory_hypothesis_odds_ratio_incorrect_vs_correct": hypothesis_or,
        "memory_hypothesis_fisher_p": hypothesis_p,
        "combined_score_model_event_rate_correct_pct": rate(correct, "has_combined_score_model_event"),
        "combined_score_model_event_rate_incorrect_pct": rate(incorrect, "has_combined_score_model_event"),
        "model_anomaly_event_rate_correct_pct": rate(correct, "has_model_anomaly_event"),
        "model_anomaly_event_rate_incorrect_pct": rate(incorrect, "has_model_anomaly_event"),
    }


def summarize_top_errors(
    df: pd.DataFrame,
    dataset: str,
    true_col: str,
    pred_col: str,
    score_col: str,
) -> pd.DataFrame:
    errors = df[~df["is_correct_bool"]].copy()

    if errors.empty:
        out = pd.DataFrame()
    else:
        out = (
            errors.groupby([true_col, pred_col])
            .agg(
                n_errors=(score_col, "size"),
                mean_score=(score_col, "mean"),
                memory_event_rate_pct=("has_memory_event", lambda s: float(s.mean() * 100)),
                memory_episode_rate_pct=("has_memory_episode", lambda s: float(s.mean() * 100)),
                memory_hypothesis_rate_pct=("has_memory_hypothesis", lambda s: float(s.mean() * 100)),
                combined_score_model_event_rate_pct=("has_combined_score_model_event", lambda s: float(s.mean() * 100)),
                model_anomaly_event_rate_pct=("has_model_anomaly_event", lambda s: float(s.mean() * 100)),
                top_memory_event_types=("memory_event_types", unique_join),
            )
            .reset_index()
            .sort_values(["n_errors", "memory_event_rate_pct", "mean_score"], ascending=[False, False, False])
        )

    out.to_csv(OUTPUT_DIR / f"{dataset.lower()}_top_error_groups_with_memory.csv", index=False)
    return out


def format_p(value: float) -> str:
    if value < 1e-99:
        return "<1e-99"
    return f"{value:.3e}"


def write_docs(summary_df: pd.DataFrame, top_errors: dict[str, pd.DataFrame]) -> None:
    summary_df.to_csv(OUTPUT_DIR / "cross_dataset_error_memory_summary.csv", index=False)
    (OUTPUT_DIR / "cross_dataset_error_memory_summary.json").write_text(
        json.dumps(summary_df.to_dict(orient="records"), indent=2)
    )

    lines = []
    lines.append("# MultiRocket Error-Memory Link Summary")
    lines.append("")
    lines.append("Dieses Dokument untersucht, ob falsch klassifizierte MultiRocket-Fenster häufiger in der Longitudinal Dysbalance Memory-Schicht erscheinen.")
    lines.append("")
    lines.append("## Leitfrage")
    lines.append("")
    lines.append("Die Auswertung erweitert die Error-Dysbalance-Frage um die temporale Memory-Ebene:")
    lines.append("")
    lines.append("> Tauchen falsch klassifizierte Fenster häufiger als Events, Episoden oder Hypothesen im Dysbalance Memory auf?")
    lines.append("")
    lines.append("## Cross-Dataset Ergebnisübersicht")
    lines.append("")
    lines.append("| Dataset | Fehlerquote % | Memory Events korrekt % | Memory Events falsch % | Differenz | Event OR | Fisher p | Hypothesen korrekt % | Hypothesen falsch % |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in summary_df.iterrows():
        lines.append(
            f"| {r['dataset']} | {r['error_rate_pct']:.2f} | "
            f"{r['memory_event_rate_correct_pct']:.2f} | {r['memory_event_rate_incorrect_pct']:.2f} | "
            f"{r['memory_event_rate_difference_pct']:.2f} | "
            f"{r['memory_event_odds_ratio_incorrect_vs_correct']:.4f} | "
            f"{format_p(r['memory_event_fisher_p'])} | "
            f"{r['memory_hypothesis_rate_correct_pct']:.2f} | {r['memory_hypothesis_rate_incorrect_pct']:.2f} |"
        )
    lines.append("")
    lines.append("## Dataset-spezifische Error-Memory-Struktur")
    lines.append("")
    for _, item in summary_df.iterrows():
        dataset = item["dataset"]
        lines.append(f"### {dataset}")
        lines.append("")
        lines.append(
            f"Bei {dataset} liegt die Memory-Event-Rate für korrekt klassifizierte Fenster bei "
            f"{item['memory_event_rate_correct_pct']:.2f} % und für falsch klassifizierte Fenster bei "
            f"{item['memory_event_rate_incorrect_pct']:.2f} %."
        )
        lines.append("")
        lines.append(
            f"Die Event-Odds-Ratio falsch gegenüber korrekt beträgt {item['memory_event_odds_ratio_incorrect_vs_correct']:.4f}. "
            f"Die Hypothesenrate verändert sich von {item['memory_hypothesis_rate_correct_pct']:.2f} % auf "
            f"{item['memory_hypothesis_rate_incorrect_pct']:.2f} %."
        )
        lines.append("")
        top = top_errors[dataset].head(8)
        lines.append("| True | Predicted | Errors | Score | Memory Event % | Memory Hypothesis % | Event Types |")
        lines.append("|---|---|---:|---:|---:|---:|---|")
        if top.empty:
            lines.append("| | | 0 | | | | |")
        else:
            true_col = top.columns[0]
            pred_col = top.columns[1]
            for _, r in top.iterrows():
                lines.append(
                    f"| {r[true_col]} | {r[pred_col]} | {int(r['n_errors'])} | "
                    f"{r['mean_score']:.4f} | {r['memory_event_rate_pct']:.2f} | "
                    f"{r['memory_hypothesis_rate_pct']:.2f} | {r['top_memory_event_types']} |"
                )
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("Die Memory-Verknüpfung prüft, ob Modellfehler nur punktuelle Klassifikationsprobleme sind oder ob sie auch in der temporalen Hypothesenbildung des Frameworks sichtbar werden.")
    lines.append("")
    lines.append("Ein hoher Error-Memory-Zusammenhang bedeutet nicht automatisch klinische Relevanz. Er zeigt aber, dass ein Fehlerfenster nicht isoliert steht, sondern mit Score-, Anomaly- oder Episodenstruktur verbunden ist.")
    lines.append("")
    lines.append("Besonders wichtig ist die Trennung der Ebenen: Klassifikationsfehler, Dysbalance Score, Anomaly Detection und Memory markieren verwandte, aber nicht identische Phänomene.")
    lines.append("")
    lines.append("## Methodische Vorsicht")
    lines.append("")
    lines.append("- Das aktuelle Memory basiert auf kontrollierten Window-Sequenzen, nicht auf echter Langzeitbeobachtung.")
    lines.append("- Memory-Hypothesen sind keine Diagnosen.")
    lines.append("- Events entstehen aus Scores und Anomaly Detection; sie sind keine unabhängige Ground Truth.")
    lines.append("- Ein fehlender Memory-Treffer bedeutet nicht, dass ein Fehler irrelevant ist.")
    lines.append("")
    lines.append("## Zwischenfazit")
    lines.append("")
    lines.append("Die Error-Memory-Verknüpfung erweitert die Arbeit um eine wichtige Frage: Werden Modellfehler auch temporal und hypothesenbezogen sichtbar? Diese Ebene verbindet starke Zeitreihenklassifikation mit erklärbarer, vorsichtig interpretierter Dysbalance-Hypothesenbildung.")

    DOC_PATH.write_text("\n".join(lines) + "\n")

    framework_section = []
    framework_section.append("## MultiRocket Error-Memory Linking")
    framework_section.append("")
    framework_section.append("Zusätzlich zur Error-Dysbalance-Auswertung wurde geprüft, ob falsch klassifizierte MultiRocket-Fenster häufiger in der Longitudinal Dysbalance Memory-Schicht erscheinen.")
    framework_section.append("")
    framework_section.append("| Dataset | Memory Events korrekt | Memory Events falsch | Event-Odds-Ratio | Hypothesen korrekt | Hypothesen falsch |")
    framework_section.append("|---|---:|---:|---:|---:|---:|")
    for _, r in summary_df.iterrows():
        framework_section.append(
            f"| {r['dataset']} | {r['memory_event_rate_correct_pct']:.2f} % | "
            f"{r['memory_event_rate_incorrect_pct']:.2f} % | "
            f"{r['memory_event_odds_ratio_incorrect_vs_correct']:.4f} | "
            f"{r['memory_hypothesis_rate_correct_pct']:.2f} % | "
            f"{r['memory_hypothesis_rate_incorrect_pct']:.2f} % |"
        )
    framework_section.append("")
    framework_section.append("Diese Auswertung verbindet Modellunsicherheit mit temporaler Event-, Episoden- und Hypothesenbildung. Sie bleibt vorsichtig zu interpretieren, weil das aktuelle Memory kontrollierte Window-Sequenzen und noch keine echte Langzeitvalidierung abbildet.")

    text = FRAMEWORK_PATH.read_text()
    heading = "## MultiRocket Error-Memory Linking"
    section = "\n".join(framework_section)
    if heading in text:
        text = text.split(heading)[0].rstrip() + "\n\n" + section + "\n"
    else:
        text = text.rstrip() + "\n\n" + section + "\n"
    FRAMEWORK_PATH.write_text(text)


def main() -> None:
    memory_events = prepare_memory_events()

    summaries = []
    top_errors = {}

    for config in DATASETS:
        _, summary, top = load_and_join_dataset(config, memory_events)
        summaries.append(summary)
        top_errors[config["dataset"]] = top

    summary_df = pd.DataFrame(summaries)
    write_docs(summary_df, top_errors)

    print("=== Cross-dataset Error-Memory Summary ===")
    print(summary_df.to_string(index=False))

    for dataset, top in top_errors.items():
        print()
        print(f"=== Top error groups with memory: {dataset} ===")
        print(top.head(10).to_string(index=False))

    print()
    print("Saved outputs to:", OUTPUT_DIR)
    print("Saved doc to:", DOC_PATH)
    print("Updated framework:", FRAMEWORK_PATH)


if __name__ == "__main__":
    main()
