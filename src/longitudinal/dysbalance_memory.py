from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.project_paths import REPORTS_DIR


FEATURE_SET = "component_level"
CONTAMINATION = 0.05
MAX_GAP_WINDOWS = 2


@dataclass(frozen=True)
class MemoryConfig:
    dataset: str
    domain: str
    anomaly_path: Path
    subject_column: str
    session_column: str
    window_column: str
    start_column: str
    end_column: str
    context_column: str
    context_name_column: str


def load_configs() -> tuple[MemoryConfig, MemoryConfig]:
    anomaly_dir = REPORTS_DIR / "anomaly"

    pamap2 = MemoryConfig(
        dataset="pamap2",
        domain="functional_motor",
        anomaly_path=anomaly_dir / "pamap2_isolation_forest_anomaly_scores.csv",
        subject_column="subject_id",
        session_column="session_id",
        window_column="window_index",
        start_column="timestamp_start",
        end_column="timestamp_end",
        context_column="activity_id",
        context_name_column="activity_name",
    )

    wesad = MemoryConfig(
        dataset="wesad",
        domain="autonomic",
        anomaly_path=anomaly_dir / "wesad_isolation_forest_anomaly_scores.csv",
        subject_column="subject_id",
        session_column="session_id",
        window_column="window_index",
        start_column="start_sample",
        end_column="end_sample",
        context_column="label",
        context_name_column="label_name",
    )

    return pamap2, wesad


def load_anomaly_scores(config: MemoryConfig) -> pd.DataFrame:
    if not config.anomaly_path.exists():
        raise FileNotFoundError(
            f"Missing anomaly score file for {config.dataset}: {config.anomaly_path}"
        )

    df = pd.read_csv(config.anomaly_path)

    df = df[
        (df["feature_set"] == FEATURE_SET)
        & (df["contamination"] == CONTAMINATION)
    ].copy()

    df["dataset"] = config.dataset
    df["domain"] = config.domain

    return df


def safe_float(value) -> float | None:
    if pd.isna(value):
        return None

    return float(value)


def create_pamap2_events(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for _, row in df.iterrows():
        strength = float(row["functional_deviation_strength"])
        is_threshold_event = strength >= 2.0
        is_rank_event = float(row["anomaly_rank_percent"]) >= 95.0
        is_model_anomaly = bool(row["is_model_anomaly"])

        if not (is_threshold_event or is_rank_event or is_model_anomaly):
            continue

        if is_threshold_event and is_model_anomaly:
            event_type = "combined_score_model_event"
        elif is_threshold_event:
            event_type = "functional_motor_deviation"
        elif is_model_anomaly:
            event_type = "model_anomaly"
        else:
            event_type = "high_rank_anomaly"

        rows.append(
            {
                "dataset": "pamap2",
                "domain": "functional_motor",
                "subject_id": str(row["subject_id"]),
                "session_id": str(row["session_id"]),
                "source_level": "window",
                "window_index": int(row["window_index"]),
                "start_position": safe_float(row["timestamp_start"]),
                "end_position": safe_float(row["timestamp_end"]),
                "context_label": row["activity_id"],
                "context_name": row["activity_name"],
                "primary_score_name": "functional_deviation_strength",
                "primary_score_value": strength,
                "secondary_score_name": None,
                "secondary_score_value": None,
                "anomaly_score": safe_float(row["anomaly_score"]),
                "anomaly_score_z": safe_float(row["anomaly_score_z"]),
                "anomaly_rank_percent": safe_float(row["anomaly_rank_percent"]),
                "is_threshold_event": bool(is_threshold_event),
                "is_model_anomaly": bool(is_model_anomaly),
                "is_high_rank_event": bool(is_rank_event),
                "event_strength": max(
                    strength,
                    float(row["anomaly_score_z"]) if not pd.isna(row["anomaly_score_z"]) else 0.0,
                ),
                "event_type": event_type,
                "component_summary": (
                    f"z_total_acc_rms={row.get('z_total_acc_rms', np.nan):.3f}; "
                    f"z_ext_chest={row.get('z_log_extremity_chest_acc_ratio', np.nan):.3f}; "
                    f"z_hand_ankle={row.get('z_log_hand_ankle_acc_ratio', np.nan):.3f}"
                ),
                "created_from": "pamap2_component_level_isolation_forest",
            }
        )

    events = pd.DataFrame(rows)

    if events.empty:
        return events

    events.insert(0, "event_id", [f"EVT_PAMAP2_{i:06d}" for i in range(1, len(events) + 1)])

    return events


def create_wesad_events(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for _, row in df.iterrows():
        activation = float(row["z_autonomic_activation"])
        deviation = float(row["autonomic_deviation_strength"])

        activation_threshold = activation >= 2.0
        deviation_threshold = deviation >= 1.5
        is_rank_event = float(row["anomaly_rank_percent"]) >= 95.0
        is_model_anomaly = bool(row["is_model_anomaly"])

        if not (activation_threshold or deviation_threshold or is_rank_event or is_model_anomaly):
            continue

        if activation_threshold:
            rows.append(
                {
                    "dataset": "wesad",
                    "domain": "autonomic",
                    "subject_id": str(row["subject_id"]),
                    "session_id": str(row["session_id"]),
                    "source_level": "window",
                    "window_index": int(row["window_index"]),
                    "start_position": safe_float(row["start_sample"]),
                    "end_position": safe_float(row["end_sample"]),
                    "context_label": row["label"],
                    "context_name": row["label_name"],
                    "primary_score_name": "z_autonomic_activation",
                    "primary_score_value": activation,
                    "secondary_score_name": "autonomic_deviation_strength",
                    "secondary_score_value": deviation,
                    "anomaly_score": safe_float(row["anomaly_score"]),
                    "anomaly_score_z": safe_float(row["anomaly_score_z"]),
                    "anomaly_rank_percent": safe_float(row["anomaly_rank_percent"]),
                    "is_threshold_event": True,
                    "is_model_anomaly": bool(is_model_anomaly),
                    "is_high_rank_event": bool(is_rank_event),
                    "event_strength": max(
                        activation,
                        float(row["anomaly_score_z"]) if not pd.isna(row["anomaly_score_z"]) else 0.0,
                    ),
                    "event_type": "autonomic_activation",
                    "component_summary": (
                        f"z_hr={row.get('z_hr_bpm', np.nan):.3f}; "
                        f"z_eda={row.get('z_eda_mean', np.nan):.3f}; "
                        f"z_resp={row.get('z_resp_std', np.nan):.3f}; "
                        f"z_inv_rmssd={row.get('z_inverse_rmssd', np.nan):.3f}"
                    ),
                    "created_from": "wesad_component_level_isolation_forest",
                }
            )

        if deviation_threshold or is_model_anomaly or is_rank_event:
            if deviation_threshold and is_model_anomaly:
                event_type = "combined_score_model_event"
            elif deviation_threshold:
                event_type = "autonomic_deviation"
            elif is_model_anomaly:
                event_type = "model_anomaly"
            else:
                event_type = "high_rank_anomaly"

            rows.append(
                {
                    "dataset": "wesad",
                    "domain": "autonomic",
                    "subject_id": str(row["subject_id"]),
                    "session_id": str(row["session_id"]),
                    "source_level": "window",
                    "window_index": int(row["window_index"]),
                    "start_position": safe_float(row["start_sample"]),
                    "end_position": safe_float(row["end_sample"]),
                    "context_label": row["label"],
                    "context_name": row["label_name"],
                    "primary_score_name": "autonomic_deviation_strength",
                    "primary_score_value": deviation,
                    "secondary_score_name": "z_autonomic_activation",
                    "secondary_score_value": activation,
                    "anomaly_score": safe_float(row["anomaly_score"]),
                    "anomaly_score_z": safe_float(row["anomaly_score_z"]),
                    "anomaly_rank_percent": safe_float(row["anomaly_rank_percent"]),
                    "is_threshold_event": bool(deviation_threshold),
                    "is_model_anomaly": bool(is_model_anomaly),
                    "is_high_rank_event": bool(is_rank_event),
                    "event_strength": max(
                        deviation,
                        float(row["anomaly_score_z"]) if not pd.isna(row["anomaly_score_z"]) else 0.0,
                    ),
                    "event_type": event_type,
                    "component_summary": (
                        f"z_hr={row.get('z_hr_bpm', np.nan):.3f}; "
                        f"z_eda={row.get('z_eda_mean', np.nan):.3f}; "
                        f"z_resp={row.get('z_resp_std', np.nan):.3f}; "
                        f"z_inv_rmssd={row.get('z_inverse_rmssd', np.nan):.3f}"
                    ),
                    "created_from": "wesad_component_level_isolation_forest",
                }
            )

    events = pd.DataFrame(rows)

    if events.empty:
        return events

    events.insert(0, "event_id", [f"EVT_WESAD_{i:06d}" for i in range(1, len(events) + 1)])

    return events


def assign_episode_ids(events: pd.DataFrame) -> pd.DataFrame:
    if events.empty:
        return events

    events = events.copy()
    events["episode_id"] = None

    group_columns = [
        "dataset",
        "domain",
        "subject_id",
        "session_id",
        "event_type",
        "context_name",
    ]

    episode_counter = 1

    for _, group in events.groupby(group_columns, dropna=False):
        group = group.sort_values("window_index")

        current_episode_rows = []
        previous_window = None

        for index, row in group.iterrows():
            current_window = int(row["window_index"])

            if previous_window is None:
                current_episode_rows = [index]
            elif current_window - previous_window <= MAX_GAP_WINDOWS:
                current_episode_rows.append(index)
            else:
                episode_id = f"EP_{episode_counter:06d}"
                events.loc[current_episode_rows, "episode_id"] = episode_id
                episode_counter += 1
                current_episode_rows = [index]

            previous_window = current_window

        if current_episode_rows:
            episode_id = f"EP_{episode_counter:06d}"
            events.loc[current_episode_rows, "episode_id"] = episode_id
            episode_counter += 1

    return events


def build_episodes(events: pd.DataFrame) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()

    rows = []

    for episode_id, group in events.groupby("episode_id", dropna=False):
        group = group.sort_values("window_index")

        rows.append(
            {
                "episode_id": episode_id,
                "dataset": group["dataset"].iloc[0],
                "domain": group["domain"].iloc[0],
                "subject_id": group["subject_id"].iloc[0],
                "session_id": group["session_id"].iloc[0],
                "event_type": group["event_type"].iloc[0],
                "context_name": group["context_name"].iloc[0],
                "n_events": len(group),
                "start_position": group["start_position"].min(),
                "end_position": group["end_position"].max(),
                "first_window_index": int(group["window_index"].min()),
                "last_window_index": int(group["window_index"].max()),
                "mean_event_strength": group["event_strength"].mean(),
                "max_event_strength": group["event_strength"].max(),
                "mean_primary_score": group["primary_score_value"].mean(),
                "max_primary_score": group["primary_score_value"].max(),
                "mean_anomaly_score": group["anomaly_score"].mean(),
                "n_threshold_events": int(group["is_threshold_event"].sum()),
                "n_model_anomalies": int(group["is_model_anomaly"].sum()),
                "n_high_rank_events": int(group["is_high_rank_event"].sum()),
                "dominant_primary_score": group["primary_score_name"].mode().iloc[0],
                "dominant_context": group["context_name"].mode().iloc[0],
                "episode_strength": max(
                    group["event_strength"].mean(),
                    group["event_strength"].max() * 0.75,
                ),
            }
        )

    episodes = pd.DataFrame(rows)

    return episodes.sort_values(
        ["dataset", "domain", "subject_id", "event_type", "first_window_index"]
    ).reset_index(drop=True)


def initial_status(n_episodes: int, max_strength: float, mean_strength: float) -> str:
    if n_episodes >= 3:
        return "confirmed"

    if n_episodes == 2:
        return "observed"

    if max_strength >= 3.0 or mean_strength >= 2.0:
        return "observed"

    return "new"


def build_hypotheses(episodes: pd.DataFrame) -> pd.DataFrame:
    if episodes.empty:
        return pd.DataFrame()

    rows = []
    hypothesis_counter = 1

    group_columns = [
        "dataset",
        "domain",
        "subject_id",
        "event_type",
        "context_name",
    ]

    for group_values, group in episodes.groupby(group_columns, dropna=False):
        dataset, domain, subject_id, event_type, context_name = group_values

        n_episodes = len(group)
        max_strength = float(group["episode_strength"].max())
        mean_strength = float(group["episode_strength"].mean())

        status = initial_status(
            n_episodes=n_episodes,
            max_strength=max_strength,
            mean_strength=mean_strength,
        )

        if dataset in {"pamap2", "wesad", "mhealth"}:
            evidence_scope = "controlled_window_sequence"
            is_true_longitudinal_evidence = False
        elif dataset in {"tiles2018", "tiles"}:
            evidence_scope = "longitudinal_real_world_sequence"
            is_true_longitudinal_evidence = True
        else:
            evidence_scope = "session_or_pilot_sequence"
            is_true_longitudinal_evidence = False

        rows.append(
            {
                "hypothesis_id": f"HYP_{hypothesis_counter:06d}",
                "dataset": dataset,
                "evidence_scope": evidence_scope,
                "is_true_longitudinal_evidence": is_true_longitudinal_evidence,
                "subject_id": subject_id,
                "domain": domain,
                "event_type": event_type,
                "context_name": context_name,
                "n_episodes": n_episodes,
                "first_seen": group["start_position"].min(),
                "last_seen": group["end_position"].max(),
                "mean_episode_strength": mean_strength,
                "max_episode_strength": max_strength,
                "recurrence_count": max(0, n_episodes - 1),
                "current_status": status,
                "status_interpretation": (
                    f"{status} within {evidence_scope}; "
                    "not a clinical confirmation."
                ),
                "evidence_summary": (
                    f"{n_episodes} episode(s), "
                    f"mean_strength={mean_strength:.3f}, "
                    f"max_strength={max_strength:.3f}"
                ),
                "interpretation_note": (
                    "Framework-level dysbalance hypothesis; not a diagnosis."
                ),
                "limitations_note": (
                    "Generated from window-level scores and model anomalies. "
                    "Requires contextual interpretation and later longitudinal validation."
                ),
            }
        )

        hypothesis_counter += 1

    hypotheses = pd.DataFrame(rows)

    return hypotheses.sort_values(
        ["dataset", "domain", "subject_id", "event_type", "context_name"]
    ).reset_index(drop=True)


def summarize_memory(events: pd.DataFrame, episodes: pd.DataFrame, hypotheses: pd.DataFrame) -> dict:
    summary = {
        "feature_set": FEATURE_SET,
        "contamination": CONTAMINATION,
        "max_gap_windows": MAX_GAP_WINDOWS,
        "n_events": int(len(events)),
        "n_episodes": int(len(episodes)),
        "n_hypotheses": int(len(hypotheses)),
        "events_by_dataset": {},
        "episodes_by_dataset": {},
        "hypotheses_by_dataset": {},
        "hypothesis_status_counts": {},
    }

    if not events.empty:
        summary["events_by_dataset"] = events["dataset"].value_counts().to_dict()
        summary["events_by_type"] = events["event_type"].value_counts().to_dict()

    if not episodes.empty:
        summary["episodes_by_dataset"] = episodes["dataset"].value_counts().to_dict()
        summary["episodes_by_type"] = episodes["event_type"].value_counts().to_dict()

    if not hypotheses.empty:
        summary["hypotheses_by_dataset"] = hypotheses["dataset"].value_counts().to_dict()
        summary["hypotheses_by_type"] = hypotheses["event_type"].value_counts().to_dict()
        summary["hypothesis_status_counts"] = hypotheses["current_status"].value_counts().to_dict()

        if "evidence_scope" in hypotheses.columns:
            summary["hypothesis_evidence_scope_counts"] = (
                hypotheses["evidence_scope"].value_counts().to_dict()
            )

        if "is_true_longitudinal_evidence" in hypotheses.columns:
            summary["true_longitudinal_hypotheses"] = int(
                hypotheses["is_true_longitudinal_evidence"].sum()
            )

    return summary


def main() -> None:
    output_dir = REPORTS_DIR / "longitudinal"
    output_dir.mkdir(parents=True, exist_ok=True)

    pamap2_config, wesad_config = load_configs()

    pamap2_scores = load_anomaly_scores(pamap2_config)
    wesad_scores = load_anomaly_scores(wesad_config)

    print("Loaded PAMAP2 anomaly scores:", pamap2_scores.shape)
    print("Loaded WESAD anomaly scores:", wesad_scores.shape)

    pamap2_events = create_pamap2_events(pamap2_scores)
    wesad_events = create_wesad_events(wesad_scores)

    event_parts = [
        part for part in [pamap2_events, wesad_events]
        if part is not None and not part.empty
    ]

    if event_parts:
        event_parts = [
            part.dropna(axis=1, how="all")
            for part in event_parts
        ]
        events = pd.concat(event_parts, ignore_index=True)
    else:
        events = pd.DataFrame()

    events = assign_episode_ids(events)

    episodes = build_episodes(events)
    hypotheses = build_hypotheses(episodes)

    summary = summarize_memory(events, episodes, hypotheses)

    events_path = output_dir / "dysbalance_events.csv"
    episodes_path = output_dir / "dysbalance_episodes.csv"
    hypotheses_path = output_dir / "dysbalance_hypotheses.csv"
    summary_path = output_dir / "dysbalance_memory_summary.json"

    events.to_csv(events_path, index=False)
    episodes.to_csv(episodes_path, index=False)
    hypotheses.to_csv(hypotheses_path, index=False)

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print()
    print("Memory summary:")
    print(json.dumps(summary, indent=2))

    print()
    print("Top hypotheses by max strength:")
    if not hypotheses.empty:
        print(
            hypotheses.sort_values("max_episode_strength", ascending=False)
            .head(20)
            .to_string(index=False)
        )

    print()
    print(f"Saved events to: {events_path}")
    print(f"Saved episodes to: {episodes_path}")
    print(f"Saved hypotheses to: {hypotheses_path}")
    print(f"Saved summary to: {summary_path}")


if __name__ == "__main__":
    main()
