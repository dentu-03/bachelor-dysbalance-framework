from __future__ import annotations

from pathlib import Path

import pandas as pd


ERROR_DYSBALANCE_DIR = Path("reports/models/cross_dataset/multirocket_error_dysbalance_link")
ERROR_MEMORY_DIR = Path("reports/models/cross_dataset/multirocket_error_memory_link")
DOC_PATH = Path("docs/results/multirocket_error_case_studies.md")


DATASETS = {
    "MHEALTH": {
        "path": ERROR_MEMORY_DIR / "mhealth_joined_predictions_scores_anomalies_memory.csv",
        "score": "functional_deviation_strength",
        "true": "activity_name",
        "pred": "y_pred",
        "position": ["subject_id", "start_sample", "end_sample"],
        "components": [
            "ecg_signal_deviation_strength",
            "combined_movement_ecg_deviation_strength",
            "dominant_functional_component",
        ],
    },
    "PAMAP2": {
        "path": ERROR_MEMORY_DIR / "pamap2_joined_predictions_scores_anomalies_memory.csv",
        "score": "functional_deviation_strength",
        "true": "true_activity_name",
        "pred": "pred_activity_name",
        "position": ["subject_id", "window_index", "timestamp_start", "timestamp_end"],
        "components": [
            "z_total_acc_rms",
            "z_log_extremity_chest_acc_ratio",
            "z_log_hand_ankle_acc_ratio",
        ],
    },
    "WESAD": {
        "path": ERROR_MEMORY_DIR / "wesad_joined_predictions_scores_anomalies_memory.csv",
        "score": "autonomic_deviation_strength",
        "true": "true_label_name",
        "pred": "pred_label_name",
        "position": ["subject_id", "window_index", "start_sample", "end_sample"],
        "components": [
            "z_autonomic_activation",
            "z_hr_bpm",
            "z_eda_mean",
            "z_resp_std",
            "z_inverse_rmssd",
        ],
    },
}


def as_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def select_cases(df: pd.DataFrame, score_col: str) -> dict[str, pd.DataFrame]:
    errors = df[~as_bool(df["is_correct"])].copy()
    errors["has_memory_event_bool"] = as_bool(errors["has_memory_event"])
    errors["has_memory_hypothesis_bool"] = as_bool(errors["has_memory_hypothesis"])

    high_memory = (
        errors[errors["has_memory_event_bool"]]
        .sort_values([score_col, "max_memory_event_strength"], ascending=False)
        .head(8)
    )

    high_score_no_memory = (
        errors[~errors["has_memory_event_bool"]]
        .sort_values(score_col, ascending=False)
        .head(8)
    )

    frequent_low_memory = (
        errors.sort_values(score_col, ascending=True)
        .head(8)
    )

    return {
        "high_memory": high_memory,
        "high_score_no_memory": high_score_no_memory,
        "frequent_low_memory": frequent_low_memory,
    }


def row_to_markdown(row: pd.Series, config: dict) -> str:
    true_value = row[config["true"]]
    pred_value = row[config["pred"]]
    score = row[config["score"]]
    anomaly_score = row.get("anomaly_score", "")
    memory_types = row.get("memory_event_types", "")
    episode_ids = row.get("memory_episode_ids", "")
    hypothesis_ids = row.get("memory_hypothesis_ids", "")

    position_parts = []
    for col in config["position"]:
        if col in row.index:
            position_parts.append(f"{col}={row[col]}")

    component_parts = []
    for col in config["components"]:
        if col in row.index and pd.notna(row[col]):
            value = row[col]
            if isinstance(value, float):
                component_parts.append(f"{col}={value:.3f}")
            else:
                component_parts.append(f"{col}={value}")

    if isinstance(score, float):
        score_text = f"{score:.4f}"
    else:
        score_text = str(score)

    if isinstance(anomaly_score, float):
        anomaly_text = f"{anomaly_score:.4f}"
    else:
        anomaly_text = str(anomaly_score)

    return (
        f"| {true_value} | {pred_value} | {score_text} | {anomaly_text} | "
        f"{'; '.join(position_parts)} | {'; '.join(component_parts)} | "
        f"{memory_types} | {episode_ids} | {hypothesis_ids} |"
    )


def write_case_section(lines: list[str], title: str, df: pd.DataFrame, config: dict) -> None:
    lines.append(f"### {title}")
    lines.append("")
    lines.append("| True | Predicted | Score | Anomaly Score | Position | Components | Memory Types | Episodes | Hypotheses |")
    lines.append("|---|---|---:|---:|---|---|---|---|---|")

    if df.empty:
        lines.append("| | | | | | | | | |")
    else:
        for _, row in df.iterrows():
            lines.append(row_to_markdown(row, config))

    lines.append("")


def main() -> None:
    lines = []
    lines.append("# MultiRocket Error Case Studies")
    lines.append("")
    lines.append("Dieses Dokument sammelt qualitative Fallbeispiele aus der MultiRocket-Experimentphase.")
    lines.append("")
    lines.append("## Ziel")
    lines.append("")
    lines.append("Die Case Studies sollen später im Ergebnisteil helfen, abstrakte Tabellenbefunde an konkreten Fenstern zu erklären.")
    lines.append("")
    lines.append("Im Vordergrund steht die Frage, wann ein MultiRocket-Fehler nur eine plausible Klassenverwechslung ist und wann er zugleich mit Dysbalance Score, Anomaly Detection und Memory zusammenfällt.")
    lines.append("")
    lines.append("## Auswahlprinzip")
    lines.append("")
    lines.append("Für jeden Datensatz werden drei Typen von Fehlerfenstern gesammelt:")
    lines.append("")
    lines.append("| Typ | Bedeutung |")
    lines.append("|---|---|")
    lines.append("| High-memory errors | Fehler mit Memory-Event, häufig thesis-relevant |")
    lines.append("| High-score errors without memory | hohe Score-Auffälligkeit, aber nicht im Memory verdichtet |")
    lines.append("| Low-score errors | eher Klassenähnlichkeit oder Modellgrenze statt Dysbalance |")
    lines.append("")

    for dataset, config in DATASETS.items():
        path = config["path"]
        if not path.exists():
            raise FileNotFoundError(path)

        df = pd.read_csv(path)
        cases = select_cases(df, config["score"])

        lines.append(f"## {dataset}")
        lines.append("")
        lines.append(f"Score-Spalte: `{config['score']}`")
        lines.append("")

        write_case_section(lines, "High-memory errors", cases["high_memory"], config)
        write_case_section(lines, "High-score errors without memory", cases["high_score_no_memory"], config)
        write_case_section(lines, "Low-score errors", cases["frequent_low_memory"], config)

    lines.append("## Interpretation")
    lines.append("")
    lines.append("Die Case Studies unterstützen eine vorsichtige, domänenspezifische Lesart.")
    lines.append("")
    lines.append("Bei PAMAP2 sind Fehler mit hoher funktionaler Dysbalance und Memory-Treffern besonders wichtig, weil sie zeigen, dass Modellunsicherheit, Score-Auffälligkeit und temporale Hypothesenbildung zusammenfallen können.")
    lines.append("")
    lines.append("Bei MHEALTH und WESAD sind viele Fehler dagegen besser als Klassenähnlichkeit oder Zustandsüberlappung zu lesen. Das verhindert eine Überinterpretation von Modellfehlern.")
    lines.append("")
    lines.append("## Thesis-Nutzung")
    lines.append("")
    lines.append("Diese Fallbeispiele eignen sich später für:")
    lines.append("")
    lines.append("- Ergebnisteil: exemplarische Fehleranalyse.")
    lines.append("- Diskussion: Abgrenzung von Modellfehler, Dysbalance und physiologischer Interpretation.")
    lines.append("- Methodik: Begründung der mehrschichtigen Framework-Architektur.")
    lines.append("")
    lines.append("## Zwischenfazit")
    lines.append("")
    lines.append("Die qualitative Fehleranalyse ergänzt die quantitativen MultiRocket-Ergebnisse. Sie macht sichtbar, dass der wissenschaftliche Mehrwert nicht allein in hoher Klassifikationsleistung liegt, sondern in der erklärbaren Einordnung von Modellunsicherheit.")

    DOC_PATH.write_text("\n".join(lines) + "\n")

    print("Wrote:", DOC_PATH)
    print()
    print("Generated case-study sections:")
    for dataset in DATASETS:
        print("-", dataset)


if __name__ == "__main__":
    main()
