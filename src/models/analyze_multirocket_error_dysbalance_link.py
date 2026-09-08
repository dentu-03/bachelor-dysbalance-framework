from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR


OUTPUT_DIR = REPORTS_DIR / "models" / "cross_dataset" / "multirocket_error_dysbalance_link"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DOC_PATH = Path("docs/results/multirocket_error_dysbalance_link_summary.md")


def bool_series(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def safe_ratio(a: float, b: float) -> float:
    if pd.isna(a) or pd.isna(b) or abs(b) < 1e-12:
        return float("nan")
    return float(a / b)


def summarize_correctness(
    df: pd.DataFrame,
    dataset: str,
    score_column: str,
    anomaly_score_column: str = "anomaly_score",
    anomaly_flag_column: str = "is_model_anomaly",
) -> dict:
    rows = []

    for value, group in df.groupby("is_correct"):
        label = "correct" if bool(value) else "incorrect"
        row = {
            "dataset": dataset,
            "prediction_group": label,
            "n_windows": int(len(group)),
            "score_column": score_column,
            "mean_score": float(group[score_column].mean()),
            "median_score": float(group[score_column].median()),
            "std_score": float(group[score_column].std(ddof=1)),
            "mean_anomaly_score": float(group[anomaly_score_column].mean()),
            "median_anomaly_score": float(group[anomaly_score_column].median()),
            "anomaly_rate_pct": float(bool_series(group[anomaly_flag_column]).mean() * 100),
        }
        rows.append(row)

    out = pd.DataFrame(rows)
    out.to_csv(OUTPUT_DIR / f"{dataset.lower()}_correct_vs_incorrect.csv", index=False)

    correct = out[out["prediction_group"] == "correct"].iloc[0]
    incorrect = out[out["prediction_group"] == "incorrect"].iloc[0]

    return {
        "dataset": dataset,
        "n_total": int(len(df)),
        "n_correct": int(correct["n_windows"]),
        "n_incorrect": int(incorrect["n_windows"]),
        "error_rate_pct": float(incorrect["n_windows"] / len(df) * 100),
        "score_column": score_column,
        "mean_score_correct": float(correct["mean_score"]),
        "mean_score_incorrect": float(incorrect["mean_score"]),
        "mean_score_difference_incorrect_minus_correct": float(
            incorrect["mean_score"] - correct["mean_score"]
        ),
        "mean_score_ratio_incorrect_over_correct": safe_ratio(
            incorrect["mean_score"], correct["mean_score"]
        ),
        "median_score_correct": float(correct["median_score"]),
        "median_score_incorrect": float(incorrect["median_score"]),
        "mean_anomaly_score_correct": float(correct["mean_anomaly_score"]),
        "mean_anomaly_score_incorrect": float(incorrect["mean_anomaly_score"]),
        "mean_anomaly_score_difference_incorrect_minus_correct": float(
            incorrect["mean_anomaly_score"] - correct["mean_anomaly_score"]
        ),
        "anomaly_rate_correct_pct": float(correct["anomaly_rate_pct"]),
        "anomaly_rate_incorrect_pct": float(incorrect["anomaly_rate_pct"]),
        "anomaly_rate_difference_pct": float(
            incorrect["anomaly_rate_pct"] - correct["anomaly_rate_pct"]
        ),
    }


def top_error_groups(
    df: pd.DataFrame,
    dataset: str,
    true_col: str,
    pred_col: str,
    score_col: str,
    anomaly_flag_col: str,
) -> pd.DataFrame:
    errors = df[~bool_series(df["is_correct"])].copy()

    if errors.empty:
        out = pd.DataFrame()
    else:
        out = (
            errors.groupby([true_col, pred_col])
            .agg(
                n_errors=(score_col, "size"),
                mean_score=(score_col, "mean"),
                median_score=(score_col, "median"),
                mean_anomaly_score=("anomaly_score", "mean"),
                anomaly_rate_pct=(anomaly_flag_col, lambda s: bool_series(s).mean() * 100),
            )
            .reset_index()
            .sort_values(["n_errors", "mean_score"], ascending=[False, False])
        )

    out.to_csv(OUTPUT_DIR / f"{dataset.lower()}_top_error_groups_with_scores.csv", index=False)
    return out


def load_mhealth() -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    pred = pd.read_csv(REPORTS_DIR / "models" / "mhealth" / "multirocket_loso" / "mhealth_multirocket_loso_predictions.csv")
    scores = pd.read_csv(PROCESSED_DATA_DIR / "mhealth" / "dysbalance" / "mhealth_functional_scores.csv")
    anomaly = pd.read_csv(REPORTS_DIR / "anomaly" / "mhealth" / "mhealth_isolation_forest_predictions.csv")

    anomaly = anomaly[
        (anomaly["feature_set"] == "movement_component_level")
        & (np.isclose(anomaly["contamination"], 0.05))
    ].copy()

    keys = ["subject_id", "label", "start_sample", "end_sample"]
    pred["subject_id"] = pred["subject_id"].astype(int)
    scores["subject_id"] = scores["subject_id"].astype(int)
    anomaly["subject_id"] = anomaly["subject_id"].astype(int)

    merged = pred.merge(
        scores[
            keys
            + [
                "functional_deviation_strength",
                "ecg_signal_deviation_strength",
                "combined_movement_ecg_deviation_strength",
                "dominant_functional_component",
            ]
        ],
        on=keys,
        how="left",
        validate="one_to_one",
    )

    merged = merged.merge(
        anomaly[
            keys
            + [
                "is_anomaly",
                "anomaly_score",
            ]
        ],
        on=keys,
        how="left",
        validate="one_to_one",
    )

    merged = merged.rename(columns={"is_anomaly": "is_model_anomaly"})
    merged["dataset"] = "MHEALTH"
    merged.to_csv(OUTPUT_DIR / "mhealth_joined_predictions_scores_anomalies.csv", index=False)

    summary = summarize_correctness(
        merged,
        dataset="MHEALTH",
        score_column="functional_deviation_strength",
        anomaly_flag_column="is_model_anomaly",
    )

    top = top_error_groups(
        merged,
        dataset="MHEALTH",
        true_col="activity_name",
        pred_col="y_pred",
        score_col="functional_deviation_strength",
        anomaly_flag_col="is_model_anomaly",
    )

    return merged, summary, top


def load_pamap2() -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    pred = pd.read_csv(REPORTS_DIR / "models" / "pamap2" / "multirocket_loso_5000" / "pamap2_multirocket_loso_predictions.csv")
    scores = pd.read_csv(PROCESSED_DATA_DIR / "pamap2" / "dysbalance" / "pamap2_functional_scores.csv")
    anomaly = pd.read_csv(REPORTS_DIR / "anomaly" / "pamap2_isolation_forest_anomaly_scores.csv")

    anomaly = anomaly[
        (anomaly["feature_set"] == "component_level")
        & (np.isclose(anomaly["contamination"], 0.05))
    ].copy()

    score_keys = ["subject_id", "window_index", "activity_id", "start_row", "end_row"]
    anomaly_keys = ["subject_id", "window_index", "activity_id"]

    pred["subject_id"] = pred["subject_id"].astype(int)
    scores["subject_id"] = scores["subject_id"].astype(int)
    anomaly["subject_id"] = anomaly["subject_id"].astype(int)
    anomaly["activity_id"] = anomaly["activity_id"].astype(int)

    merged = pred.merge(
        scores[
            score_keys
            + [
                "functional_deviation_strength",
                "z_total_acc_rms",
                "z_log_extremity_chest_acc_ratio",
                "z_log_hand_ankle_acc_ratio",
            ]
        ],
        on=score_keys,
        how="left",
        validate="one_to_one",
    )

    merged = merged.merge(
        anomaly[
            anomaly_keys
            + [
                "is_model_anomaly",
                "anomaly_score",
                "anomaly_score_z",
                "anomaly_rank_percent",
            ]
        ],
        on=anomaly_keys,
        how="left",
        validate="one_to_one",
    )

    merged["dataset"] = "PAMAP2"
    merged.to_csv(OUTPUT_DIR / "pamap2_joined_predictions_scores_anomalies.csv", index=False)

    summary = summarize_correctness(
        merged,
        dataset="PAMAP2",
        score_column="functional_deviation_strength",
        anomaly_flag_column="is_model_anomaly",
    )

    top = top_error_groups(
        merged,
        dataset="PAMAP2",
        true_col="true_activity_name",
        pred_col="pred_activity_name",
        score_col="functional_deviation_strength",
        anomaly_flag_col="is_model_anomaly",
    )

    return merged, summary, top


def load_wesad() -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    pred = pd.read_csv(REPORTS_DIR / "models" / "wesad" / "multirocket_standardized_split_stride10" / "wesad_multirocket_standardized_split_predictions.csv")
    scores = pd.read_csv(PROCESSED_DATA_DIR / "wesad" / "dysbalance" / "wesad_autonomic_scores.csv")
    anomaly = pd.read_csv(REPORTS_DIR / "anomaly" / "wesad_isolation_forest_anomaly_scores.csv")

    anomaly = anomaly[
        (anomaly["feature_set"] == "component_level")
        & (np.isclose(anomaly["contamination"], 0.05))
    ].copy()

    keys = ["subject_id", "window_index", "label", "start_sample", "end_sample"]

    for frame in [pred, scores, anomaly]:
        frame["subject_id"] = frame["subject_id"].astype(str)
        frame["window_index"] = frame["window_index"].astype(int)
        frame["label"] = frame["label"].astype(int)
        frame["start_sample"] = frame["start_sample"].astype(int)
        frame["end_sample"] = frame["end_sample"].astype(int)

    merged = pred.merge(
        scores[
            keys
            + [
                "z_autonomic_activation",
                "autonomic_deviation_strength",
                "z_hr_bpm",
                "z_eda_mean",
                "z_resp_std",
                "z_inverse_rmssd",
            ]
        ],
        on=keys,
        how="left",
        validate="one_to_one",
    )

    merged = merged.merge(
        anomaly[
            keys
            + [
                "is_model_anomaly",
                "anomaly_score",
                "anomaly_score_z",
                "anomaly_rank_percent",
            ]
        ],
        on=keys,
        how="left",
        validate="one_to_one",
    )

    merged["dataset"] = "WESAD"
    merged.to_csv(OUTPUT_DIR / "wesad_joined_predictions_scores_anomalies.csv", index=False)

    summary = summarize_correctness(
        merged,
        dataset="WESAD",
        score_column="autonomic_deviation_strength",
        anomaly_flag_column="is_model_anomaly",
    )

    top = top_error_groups(
        merged,
        dataset="WESAD",
        true_col="true_label_name",
        pred_col="pred_label_name",
        score_col="autonomic_deviation_strength",
        anomaly_flag_col="is_model_anomaly",
    )

    return merged, summary, top


def write_doc(summaries: list[dict], tops: dict[str, pd.DataFrame]) -> None:
    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(OUTPUT_DIR / "cross_dataset_error_dysbalance_summary.csv", index=False)
    (OUTPUT_DIR / "cross_dataset_error_dysbalance_summary.json").write_text(
        json.dumps(summaries, indent=2)
    )

    lines = []
    lines.append("# MultiRocket Error-Dysbalance Link Summary")
    lines.append("")
    lines.append("Dieses Dokument hält eine zentrale Anschlussfrage für die Thesis fest: Sind falsch klassifizierte MultiRocket-Fenster zugleich physiologisch oder funktional auffälliger?")
    lines.append("")
    lines.append("## Forschungsfrage der Auswertung")
    lines.append("")
    lines.append("Die Auswertung verbindet drei Ebenen meines Frameworks:")
    lines.append("")
    lines.append("| Ebene | Rolle |")
    lines.append("|---|---|")
    lines.append("| MultiRocket | diskriminative Zeitreihenklassifikation |")
    lines.append("| Dysbalance Scores | erklärbare funktionale oder autonom-physiologische Abweichung |")
    lines.append("| Isolation Forest | modellbasierte Anomaly-Schicht auf Score-/Komponentenebene |")
    lines.append("")
    lines.append("Die Leitfrage lautet: Treten Klassifikationsfehler bevorzugt dort auf, wo die erklärbaren Dysbalance- oder Anomaly-Schichten bereits erhöhte Abweichungen anzeigen?")
    lines.append("")
    lines.append("## Cross-Dataset Ergebnisübersicht")
    lines.append("")
    lines.append("| Dataset | Fehlerquote % | Score correct | Score incorrect | Differenz | Ratio | Anomaly % correct | Anomaly % incorrect | Anomaly-Differenz |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in summary_df.iterrows():
        lines.append(
            f"| {r['dataset']} | {r['error_rate_pct']:.2f} | "
            f"{r['mean_score_correct']:.4f} | {r['mean_score_incorrect']:.4f} | "
            f"{r['mean_score_difference_incorrect_minus_correct']:.4f} | "
            f"{r['mean_score_ratio_incorrect_over_correct']:.4f} | "
            f"{r['anomaly_rate_correct_pct']:.2f} | {r['anomaly_rate_incorrect_pct']:.2f} | "
            f"{r['anomaly_rate_difference_pct']:.2f} |"
        )
    lines.append("")
    lines.append("## Dataset-spezifische Lesart")
    lines.append("")
    for item in summaries:
        dataset = item["dataset"]
        lines.append(f"### {dataset}")
        lines.append("")
        lines.append(
            f"Bei {dataset} liegt die Fehlerquote bei {item['error_rate_pct']:.2f} %. "
            f"Der mittlere erklärbare Score beträgt {item['mean_score_correct']:.4f} für korrekt klassifizierte Fenster "
            f"und {item['mean_score_incorrect']:.4f} für falsch klassifizierte Fenster."
        )
        lines.append("")
        lines.append(
            f"Die mittlere Score-Differenz falsch minus korrekt beträgt {item['mean_score_difference_incorrect_minus_correct']:.4f}. "
            f"Die Anomaly-Rate steigt von {item['anomaly_rate_correct_pct']:.2f} % auf {item['anomaly_rate_incorrect_pct']:.2f} %."
        )
        lines.append("")
        top = tops[dataset].head(8)
        lines.append("| True | Predicted | Errors | Mean score | Anomaly % |")
        lines.append("|---|---|---:|---:|---:|")
        if top.empty:
            lines.append("| | | 0 | | |")
        else:
            true_col = top.columns[0]
            pred_col = top.columns[1]
            for _, r in top.iterrows():
                lines.append(
                    f"| {r[true_col]} | {r[pred_col]} | {int(r['n_errors'])} | "
                    f"{r['mean_score']:.4f} | {r['anomaly_rate_pct']:.2f} |"
                )
        lines.append("")

    lines.append("## Bedeutung für die Thesis")
    lines.append("")
    lines.append("Diese Auswertung ist besonders wichtig, weil sie Modellfehler nicht nur als technische Fehlklassifikationen behandelt. Stattdessen werden Fehler mit erklärbaren Score- und Anomaly-Strukturen verbunden.")
    lines.append("")
    lines.append("Ein positiver Zusammenhang würde bedeuten: MultiRocket scheitert nicht zufällig, sondern häufiger an Fenstern, die im Framework ohnehin als funktional oder physiologisch auffällig erscheinen.")
    lines.append("")
    lines.append("Ein schwacher Zusammenhang wäre ebenfalls relevant: Dann würden Klassifikationsfehler eher aus Klassenähnlichkeit, Sensorrauschen oder subject-spezifischer Variation entstehen und müssten getrennt von Dysbalance interpretiert werden.")
    lines.append("")
    lines.append("## Aktuelle methodische Vorsicht")
    lines.append("")
    lines.append("- Die Analyse zeigt Zusammenhänge, aber keine Kausalität.")
    lines.append("- Die Anomaly-Schicht nutzt eigene Modelle und darf nicht als Ground Truth gelesen werden.")
    lines.append("- Bei WESAD sind affektive Zustände physiologisch überlappend, besonders amusement, stress und meditation.")
    lines.append("- Bei PAMAP2 und MHEALTH können Fehler aus ähnlichen Bewegungsabläufen entstehen, auch wenn keine physiologische Auffälligkeit vorliegt.")
    lines.append("")
    lines.append("## Zwischenfazit")
    lines.append("")
    lines.append("Die Error-Dysbalance-Verknüpfung ist eine zentrale Brücke zwischen starker Zeitreihenklassifikation und erklärbarer Dysbalance-Modellierung. Sie macht sichtbar, ob Modellunsicherheit, funktionale Abweichung und modellbasierte Anomalie dieselben Fensterbereiche markieren oder unterschiedliche Aspekte der Daten beschreiben.")

    DOC_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    mhealth, mhealth_summary, mhealth_top = load_mhealth()
    pamap2, pamap2_summary, pamap2_top = load_pamap2()
    wesad, wesad_summary, wesad_top = load_wesad()

    summaries = [mhealth_summary, pamap2_summary, wesad_summary]
    tops = {
        "MHEALTH": mhealth_top,
        "PAMAP2": pamap2_top,
        "WESAD": wesad_top,
    }

    write_doc(summaries, tops)

    print("=== Cross-dataset Error-Dysbalance Summary ===")
    print(pd.DataFrame(summaries).to_string(index=False))

    print()
    print("=== Top error groups: MHEALTH ===")
    print(mhealth_top.head(10).to_string(index=False))

    print()
    print("=== Top error groups: PAMAP2 ===")
    print(pamap2_top.head(10).to_string(index=False))

    print()
    print("=== Top error groups: WESAD ===")
    print(wesad_top.head(10).to_string(index=False))

    print()
    print("Saved outputs to:", OUTPUT_DIR)
    print("Saved doc to:", DOC_PATH)


if __name__ == "__main__":
    main()
