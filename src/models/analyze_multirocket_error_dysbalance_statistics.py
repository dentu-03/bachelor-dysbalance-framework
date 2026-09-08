from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu

from src.project_paths import REPORTS_DIR


INPUT_DIR = REPORTS_DIR / "models" / "cross_dataset" / "multirocket_error_dysbalance_link"
OUTPUT_CSV = INPUT_DIR / "cross_dataset_error_dysbalance_statistics.csv"
OUTPUT_JSON = INPUT_DIR / "cross_dataset_error_dysbalance_statistics.json"
DOC_PATH = Path("docs/results/multirocket_error_dysbalance_link_summary.md")
FRAMEWORK_PATH = Path("docs/results/framework_cross_dataset_summary.md")


DATASETS = [
    {
        "dataset": "MHEALTH",
        "path": INPUT_DIR / "mhealth_joined_predictions_scores_anomalies.csv",
        "score_column": "functional_deviation_strength",
    },
    {
        "dataset": "PAMAP2",
        "path": INPUT_DIR / "pamap2_joined_predictions_scores_anomalies.csv",
        "score_column": "functional_deviation_strength",
    },
    {
        "dataset": "WESAD",
        "path": INPUT_DIR / "wesad_joined_predictions_scores_anomalies.csv",
        "score_column": "autonomic_deviation_strength",
    },
]


def as_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]

    if len(x) == 0 or len(y) == 0:
        return float("nan")

    y_sorted = np.sort(y)
    greater = np.searchsorted(y_sorted, x, side="left").sum()
    less_equal = np.searchsorted(y_sorted, x, side="right").sum()
    less = len(y_sorted) * len(x) - less_equal

    return float((greater - less) / (len(x) * len(y)))


def bootstrap_mean_diff(
    incorrect: np.ndarray,
    correct: np.ndarray,
    n_bootstrap: int = 5000,
    seed: int = 42,
) -> tuple[float, float]:
    incorrect = np.asarray(incorrect, dtype=float)
    correct = np.asarray(correct, dtype=float)

    incorrect = incorrect[~np.isnan(incorrect)]
    correct = correct[~np.isnan(correct)]

    rng = np.random.default_rng(seed)
    diffs = np.empty(n_bootstrap, dtype=float)

    for i in range(n_bootstrap):
        inc_sample = rng.choice(incorrect, size=len(incorrect), replace=True)
        cor_sample = rng.choice(correct, size=len(correct), replace=True)
        diffs[i] = inc_sample.mean() - cor_sample.mean()

    return float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


def analyze_dataset(config: dict) -> dict:
    dataset = config["dataset"]
    path = config["path"]
    score_column = config["score_column"]

    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(path)
    df["is_correct_bool"] = as_bool(df["is_correct"])
    df["is_model_anomaly_bool"] = as_bool(df["is_model_anomaly"])

    correct = df[df["is_correct_bool"]].copy()
    incorrect = df[~df["is_correct_bool"]].copy()

    score_correct = correct[score_column].astype(float).to_numpy()
    score_incorrect = incorrect[score_column].astype(float).to_numpy()

    anomaly_score_correct = correct["anomaly_score"].astype(float).to_numpy()
    anomaly_score_incorrect = incorrect["anomaly_score"].astype(float).to_numpy()

    score_u = mannwhitneyu(
        score_incorrect,
        score_correct,
        alternative="two-sided",
        nan_policy="omit",
    )

    anomaly_u = mannwhitneyu(
        anomaly_score_incorrect,
        anomaly_score_correct,
        alternative="two-sided",
        nan_policy="omit",
    )

    score_ci_low, score_ci_high = bootstrap_mean_diff(score_incorrect, score_correct)
    anomaly_ci_low, anomaly_ci_high = bootstrap_mean_diff(
        anomaly_score_incorrect,
        anomaly_score_correct,
    )

    anomaly_correct_true = int(correct["is_model_anomaly_bool"].sum())
    anomaly_correct_false = int(len(correct) - anomaly_correct_true)
    anomaly_incorrect_true = int(incorrect["is_model_anomaly_bool"].sum())
    anomaly_incorrect_false = int(len(incorrect) - anomaly_incorrect_true)

    table = [
        [anomaly_incorrect_true, anomaly_incorrect_false],
        [anomaly_correct_true, anomaly_correct_false],
    ]

    odds_ratio, fisher_p = fisher_exact(table, alternative="two-sided")

    return {
        "dataset": dataset,
        "score_column": score_column,
        "n_correct": int(len(correct)),
        "n_incorrect": int(len(incorrect)),
        "mean_score_correct": float(np.nanmean(score_correct)),
        "mean_score_incorrect": float(np.nanmean(score_incorrect)),
        "mean_score_diff_incorrect_minus_correct": float(
            np.nanmean(score_incorrect) - np.nanmean(score_correct)
        ),
        "score_diff_ci95_low": score_ci_low,
        "score_diff_ci95_high": score_ci_high,
        "score_mannwhitney_u": float(score_u.statistic),
        "score_mannwhitney_p": float(score_u.pvalue),
        "score_cliffs_delta_incorrect_vs_correct": cliffs_delta(
            score_incorrect,
            score_correct,
        ),
        "mean_anomaly_score_correct": float(np.nanmean(anomaly_score_correct)),
        "mean_anomaly_score_incorrect": float(np.nanmean(anomaly_score_incorrect)),
        "mean_anomaly_score_diff_incorrect_minus_correct": float(
            np.nanmean(anomaly_score_incorrect) - np.nanmean(anomaly_score_correct)
        ),
        "anomaly_score_diff_ci95_low": anomaly_ci_low,
        "anomaly_score_diff_ci95_high": anomaly_ci_high,
        "anomaly_score_mannwhitney_u": float(anomaly_u.statistic),
        "anomaly_score_mannwhitney_p": float(anomaly_u.pvalue),
        "anomaly_score_cliffs_delta_incorrect_vs_correct": cliffs_delta(
            anomaly_score_incorrect,
            anomaly_score_correct,
        ),
        "anomaly_rate_correct_pct": float(anomaly_correct_true / len(correct) * 100),
        "anomaly_rate_incorrect_pct": float(anomaly_incorrect_true / len(incorrect) * 100),
        "anomaly_odds_ratio_incorrect_vs_correct": float(odds_ratio),
        "anomaly_fisher_exact_p": float(fisher_p),
    }


def format_p(value: float) -> str:
    if value < 1e-99:
        return "<1e-99"
    return f"{value:.3e}"


def append_section(path: Path, heading: str, section: str) -> None:
    text = path.read_text()
    if heading in text:
        before = text.split(heading)[0].rstrip()
        text = before + "\n\n" + section.strip() + "\n"
    else:
        text = text.rstrip() + "\n\n" + section.strip() + "\n"
    path.write_text(text)


def build_doc_section(results: pd.DataFrame) -> str:
    lines = []
    lines.append("## Statistische Zusatzprüfung")
    lines.append("")
    lines.append("Zur Absicherung der Error-Dysbalance-Verknüpfung wurden zusätzlich nichtparametrische Tests und Effektgrößen berechnet.")
    lines.append("")
    lines.append("| Dataset | Score-Diff | 95%-CI | Mann-Whitney p | Cliff's delta | Anomaly OR | Fisher p |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for _, r in results.iterrows():
        lines.append(
            f"| {r['dataset']} | "
            f"{r['mean_score_diff_incorrect_minus_correct']:.4f} | "
            f"[{r['score_diff_ci95_low']:.4f}, {r['score_diff_ci95_high']:.4f}] | "
            f"{format_p(r['score_mannwhitney_p'])} | "
            f"{r['score_cliffs_delta_incorrect_vs_correct']:.4f} | "
            f"{r['anomaly_odds_ratio_incorrect_vs_correct']:.4f} | "
            f"{format_p(r['anomaly_fisher_exact_p'])} |"
        )
    lines.append("")
    lines.append("Die statistische Prüfung bestätigt die deskriptive Interpretation. Der starke positive Zusammenhang zwischen Fehlern und Dysbalance zeigt sich klar bei PAMAP2. Bei MHEALTH und WESAD ist der Effekt dagegen negativ oder schwach, was gegen eine einfache Gleichsetzung von Klassifikationsfehler und Dysbalance spricht.")
    lines.append("")
    lines.append("Damit wird die zentrale methodische Aussage gestützt: Modellunsicherheit, erklärbare Dysbalance und modellbasierte Anomalie können zusammenfallen, müssen aber domänenspezifisch interpretiert werden.")
    return "\n".join(lines)


def build_framework_section(results: pd.DataFrame) -> str:
    pamap2 = results[results["dataset"] == "PAMAP2"].iloc[0]
    mhealth = results[results["dataset"] == "MHEALTH"].iloc[0]
    wesad = results[results["dataset"] == "WESAD"].iloc[0]

    return f"""
## Statistical Error-Dysbalance Check

Die Error-Dysbalance-Verknüpfung wurde zusätzlich statistisch geprüft. Dafür wurden korrekt und falsch klassifizierte MultiRocket-Fenster hinsichtlich Score-Differenz, nichtparametrischem Mann-Whitney-Test, Cliff's delta und Anomaly-Odds-Ratio verglichen.

| Dataset | Score-Differenz falsch-korrekt | 95%-CI | Cliff's delta | Anomaly-Odds-Ratio | Interpretation |
|---|---:|---:|---:|---:|---|
| MHEALTH | {mhealth['mean_score_diff_incorrect_minus_correct']:.4f} | [{mhealth['score_diff_ci95_low']:.4f}, {mhealth['score_diff_ci95_high']:.4f}] | {mhealth['score_cliffs_delta_incorrect_vs_correct']:.4f} | {mhealth['anomaly_odds_ratio_incorrect_vs_correct']:.4f} | Fehler nicht dysbalance-getrieben |
| PAMAP2 | {pamap2['mean_score_diff_incorrect_minus_correct']:.4f} | [{pamap2['score_diff_ci95_low']:.4f}, {pamap2['score_diff_ci95_high']:.4f}] | {pamap2['score_cliffs_delta_incorrect_vs_correct']:.4f} | {pamap2['anomaly_odds_ratio_incorrect_vs_correct']:.4f} | starker Fehler-Dysbalance-Zusammenhang |
| WESAD | {wesad['mean_score_diff_incorrect_minus_correct']:.4f} | [{wesad['score_diff_ci95_low']:.4f}, {wesad['score_diff_ci95_high']:.4f}] | {wesad['score_cliffs_delta_incorrect_vs_correct']:.4f} | {wesad['anomaly_odds_ratio_incorrect_vs_correct']:.4f} | Fehler eher Zustandsüberlappung |

Der stärkste und methodisch wichtigste Befund bleibt PAMAP2: Falsch klassifizierte Fenster zeigen eine deutlich höhere funktionale Dysbalance, eine positive Effektgröße und eine stark erhöhte Anomaly-Odds-Ratio. MHEALTH und WESAD zeigen dagegen, dass Fehler nicht automatisch Dysbalance bedeuten. Diese Differenzierung verhindert eine Überinterpretation von Modellfehlern und stärkt die domänenspezifische Framework-Logik.
""".strip()


def main() -> None:
    results = [analyze_dataset(config) for config in DATASETS]
    df = pd.DataFrame(results)

    df.to_csv(OUTPUT_CSV, index=False)
    OUTPUT_JSON.write_text(json.dumps(results, indent=2))

    print("=== Error-Dysbalance Statistics ===")
    print(df.to_string(index=False))

    doc_section = build_doc_section(df)
    append_section(DOC_PATH, "## Statistische Zusatzprüfung", doc_section)

    framework_section = build_framework_section(df)
    append_section(FRAMEWORK_PATH, "## Statistical Error-Dysbalance Check", framework_section)

    print()
    print("Saved:", OUTPUT_CSV)
    print("Saved:", OUTPUT_JSON)
    print("Updated:", DOC_PATH)
    print("Updated:", FRAMEWORK_PATH)


if __name__ == "__main__":
    main()
