import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from src.project_paths import INTERIM_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR
from src.parsers.parse_wesad_chest import CHEST_CHANNELS, VALID_LABELS


SUBJECT_IDS = [
    "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9",
    "S10", "S11", "S13", "S14", "S15", "S16", "S17",
]

FS = 700.0


def channel_index(name: str) -> int:
    """Return channel index in WESAD chest tensor."""
    return CHEST_CHANNELS.index(name)


def rms(values: np.ndarray) -> float:
    """Compute root mean square."""
    return float(np.sqrt(np.mean(np.square(values))))


def estimate_ecg_features(ecg: np.ndarray, fs: float = FS) -> tuple[float, float, int]:
    """
    Estimate HR and RMSSD from one ECG window.

    This is a lightweight, reproducible approximation for window-level
    autonomic feature extraction. It is not intended as clinical ECG analysis.
    """
    ecg = np.asarray(ecg, dtype=float)

    if np.std(ecg) == 0:
        return np.nan, np.nan, 0

    ecg_z = (ecg - np.mean(ecg)) / np.std(ecg)

    peaks, _ = find_peaks(
        ecg_z,
        distance=int(0.3 * fs),
        prominence=0.5,
    )

    n_peaks = len(peaks)

    if n_peaks < 2:
        return np.nan, np.nan, n_peaks

    rr_seconds = np.diff(peaks) / fs
    rr_ms = rr_seconds * 1000.0

    mean_rr = np.mean(rr_seconds)

    if mean_rr <= 0:
        hr_bpm = np.nan
    else:
        hr_bpm = 60.0 / mean_rr

    if len(rr_ms) < 2:
        rmssd_ms = np.nan
    else:
        rmssd_ms = np.sqrt(np.mean(np.square(np.diff(rr_ms))))

    return float(hr_bpm), float(rmssd_ms), int(n_peaks)


def compute_subject_features(subject_id: str) -> pd.DataFrame:
    """Compute autonomic features for one WESAD subject."""
    base_dir = INTERIM_DATA_DIR / "wesad" / "chest_by_subject"

    x_path = base_dir / f"X_{subject_id}.npy"
    meta_path = base_dir / f"metadata_{subject_id}.csv"

    if not x_path.exists():
        raise FileNotFoundError(f"Missing X file: {x_path}")
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing metadata file: {meta_path}")

    X = np.load(x_path, mmap_mode="r")
    metadata = pd.read_csv(meta_path)

    idx_acc = [channel_index("acc_x"), channel_index("acc_y"), channel_index("acc_z")]
    idx_ecg = channel_index("ecg")
    idx_emg = channel_index("emg")
    idx_eda = channel_index("eda")
    idx_temp = channel_index("temp")
    idx_resp = channel_index("resp")

    rows = []

    for window_idx in range(X.shape[0]):
        window = X[window_idx]

        acc_values = window[idx_acc, :]
        ecg = window[idx_ecg, :]
        emg = window[idx_emg, :]
        eda = window[idx_eda, :]
        temp = window[idx_temp, :]
        resp = window[idx_resp, :]

        hr_bpm, rmssd_ms, ecg_peak_count = estimate_ecg_features(ecg)

        rows.append(
            {
                "subject_id": subject_id,
                "window_index": int(metadata.loc[window_idx, "window_index"]),
                "label": int(metadata.loc[window_idx, "label"]),
                "label_name": metadata.loc[window_idx, "label_name"],
                "start_sample": int(metadata.loc[window_idx, "start_sample"]),
                "end_sample": int(metadata.loc[window_idx, "end_sample"]),
                "duration_seconds": float(metadata.loc[window_idx, "duration_seconds"]),
                "hr_bpm": hr_bpm,
                "rmssd_ms": rmssd_ms,
                "ecg_peak_count": ecg_peak_count,
                "eda_mean": float(np.mean(eda)),
                "eda_std": float(np.std(eda)),
                "eda_range": float(np.max(eda) - np.min(eda)),
                "resp_mean": float(np.mean(resp)),
                "resp_std": float(np.std(resp)),
                "resp_range": float(np.max(resp) - np.min(resp)),
                "temp_mean": float(np.mean(temp)),
                "temp_std": float(np.std(temp)),
                "emg_rms": rms(emg),
                "acc_rms": rms(acc_values),
            }
        )

    return pd.DataFrame(rows)


def build_all_autonomic_features() -> pd.DataFrame:
    """Compute WESAD autonomic features for all subjects."""
    parts = []

    for subject_id in SUBJECT_IDS:
        print(f"Computing WESAD autonomic features for {subject_id} ...")
        parts.append(compute_subject_features(subject_id))

    return pd.concat(parts, ignore_index=True)


def summarize_features(features: pd.DataFrame) -> pd.DataFrame:
    """Create compact subject and label summary."""
    rows = []

    for (subject_id, label), group in features.groupby(["subject_id", "label"]):
        rows.append(
            {
                "subject_id": subject_id,
                "label": int(label),
                "label_name": VALID_LABELS[int(label)],
                "n_windows": len(group),
                "hr_bpm_mean": group["hr_bpm"].mean(),
                "hr_bpm_std": group["hr_bpm"].std(),
                "rmssd_ms_mean": group["rmssd_ms"].mean(),
                "rmssd_ms_std": group["rmssd_ms"].std(),
                "eda_mean_mean": group["eda_mean"].mean(),
                "eda_std_mean": group["eda_std"].mean(),
                "resp_std_mean": group["resp_std"].mean(),
                "temp_mean_mean": group["temp_mean"].mean(),
                "emg_rms_mean": group["emg_rms"].mean(),
                "acc_rms_mean": group["acc_rms"].mean(),
                "hr_missing_pct": group["hr_bpm"].isna().mean() * 100,
                "rmssd_missing_pct": group["rmssd_ms"].isna().mean() * 100,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    out_dir = PROCESSED_DATA_DIR / "wesad" / "features"
    out_dir.mkdir(parents=True, exist_ok=True)

    report_dir = REPORTS_DIR / "dysbalance"
    report_dir.mkdir(parents=True, exist_ok=True)

    features = build_all_autonomic_features()
    summary = summarize_features(features)

    features_path = out_dir / "wesad_autonomic_features.csv"
    summary_path = report_dir / "wesad_autonomic_feature_summary.csv"

    features.to_csv(features_path, index=False)
    summary.to_csv(summary_path, index=False)

    print()
    print("Feature table shape:", features.shape)
    print("Summary shape:", summary.shape)
    print()
    print("Missing values:")
    print(features.isna().sum())
    print()
    print("Summary head:")
    print(summary.head(20).to_string(index=False))
    print()
    print(f"Saved features to: {features_path}")
    print(f"Saved summary to: {summary_path}")


if __name__ == "__main__":
    main()
