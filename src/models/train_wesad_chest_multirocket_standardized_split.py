from __future__ import annotations

import json

import numpy as np
import pandas as pd
from aeon.classification.convolution_based import MultiRocketClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from src.project_paths import INTERIM_DATA_DIR, REPORTS_DIR


INPUT_DIR = INTERIM_DATA_DIR / "wesad" / "chest_by_subject"
OUTPUT_DIR = REPORTS_DIR / "models" / "wesad" / "multirocket_standardized_split_stride10"

TRAIN_SUBJECTS = ["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11"]
TEST_SUBJECTS = ["S13", "S14", "S15", "S16", "S17"]

LABEL_NAMES = {
    1: "baseline",
    2: "stress",
    3: "amusement",
    4: "meditation",
}

TEMPORAL_STRIDE = 10
N_KERNELS = 5000
N_JOBS = 4
RANDOM_STATE = 42


def load_subject_tensors(subject_ids: list[str]) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    X_parts = []
    y_parts = []
    metadata_parts = []

    for subject_id in subject_ids:
        x_path = INPUT_DIR / f"X_{subject_id}.npy"
        y_path = INPUT_DIR / f"y_{subject_id}.npy"
        metadata_path = INPUT_DIR / f"metadata_{subject_id}.csv"

        if not x_path.exists():
            raise FileNotFoundError(f"Missing X file: {x_path}")
        if not y_path.exists():
            raise FileNotFoundError(f"Missing y file: {y_path}")
        if not metadata_path.exists():
            raise FileNotFoundError(f"Missing metadata file: {metadata_path}")

        X = np.load(x_path, mmap_mode="r").astype(np.float32)
        y = np.load(y_path).astype(int)
        metadata = pd.read_csv(metadata_path)

        X = X[:, :, ::TEMPORAL_STRIDE].astype(np.float32)

        metadata = metadata.copy()
        metadata["subject_id"] = subject_id
        metadata["source_file"] = x_path.name

        if len(X) != len(y) or len(X) != len(metadata):
            raise ValueError(f"Mismatched X, y and metadata lengths for {subject_id}")

        X_parts.append(X)
        y_parts.append(y)
        metadata_parts.append(metadata)

    X_all = np.concatenate(X_parts, axis=0)
    y_all = np.concatenate(y_parts, axis=0)
    metadata_all = pd.concat(metadata_parts, ignore_index=True)

    return X_all, y_all, metadata_all


def compute_channel_standardization(X_train: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    means = X_train.mean(axis=(0, 2), keepdims=True)
    stds = X_train.std(axis=(0, 2), keepdims=True)
    stds = np.where(stds == 0, 1.0, stds)

    return means.astype(np.float32), stds.astype(np.float32)


def apply_channel_standardization(
    X: np.ndarray,
    means: np.ndarray,
    stds: np.ndarray,
) -> np.ndarray:
    return ((X - means) / stds).astype(np.float32)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading train tensors...")
    X_train, y_train, train_metadata = load_subject_tensors(TRAIN_SUBJECTS)

    print("Loading test tensors...")
    X_test, y_test, test_metadata = load_subject_tensors(TEST_SUBJECTS)

    print()
    print("Train shape before standardization:", X_train.shape)
    print("Test shape before standardization:", X_test.shape)
    print("Train subjects:", TRAIN_SUBJECTS)
    print("Test subjects:", TEST_SUBJECTS)
    print("Train labels:", sorted(np.unique(y_train).astype(int).tolist()))
    print("Test labels:", sorted(np.unique(y_test).astype(int).tolist()))
    print("NaNs train before standardization:", int(np.isnan(X_train).sum()))
    print("NaNs test before standardization:", int(np.isnan(X_test).sum()))

    print()
    print("Applying train-set channel-wise standardization...")
    channel_means, channel_stds = compute_channel_standardization(X_train)
    X_train = apply_channel_standardization(X_train, channel_means, channel_stds)
    X_test = apply_channel_standardization(X_test, channel_means, channel_stds)

    print("NaNs train after standardization:", int(np.isnan(X_train).sum()))
    print("NaNs test after standardization:", int(np.isnan(X_test).sum()))

    clf = MultiRocketClassifier(
        n_kernels=N_KERNELS,
        n_jobs=N_JOBS,
        random_state=RANDOM_STATE,
    )

    print()
    print("Training WESAD MultiRocket standardized split...")
    clf.fit(X_train, y_train)

    print("Predicting...")
    y_pred = clf.predict(X_test)

    labels = sorted(np.unique(np.concatenate([y_test, y_pred])).astype(int).tolist())
    target_names = [LABEL_NAMES.get(label, str(label)) for label in labels]

    accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, labels=labels, average="macro", zero_division=0)
    weighted_f1 = f1_score(y_test, y_pred, labels=labels, average="weighted", zero_division=0)

    report_dict = classification_report(
        y_test,
        y_pred,
        labels=labels,
        target_names=target_names,
        output_dict=True,
        zero_division=0,
    )

    report_text = classification_report(
        y_test,
        y_pred,
        labels=labels,
        target_names=target_names,
        zero_division=0,
    )

    cm = confusion_matrix(y_test, y_pred, labels=labels)

    predictions = test_metadata.copy()
    predictions["y_true"] = y_test
    predictions["y_pred"] = y_pred
    predictions["true_label_name"] = [LABEL_NAMES.get(int(label), str(label)) for label in y_test]
    predictions["pred_label_name"] = [LABEL_NAMES.get(int(label), str(label)) for label in y_pred]
    predictions["is_correct"] = y_test == y_pred

    summary = {
        "dataset": "wesad",
        "model": "MultiRocketClassifier",
        "task": "WESAD chest condition classification",
        "split": "subject-wise",
        "preprocessing": "train-set channel-wise standardization",
        "temporal_stride": TEMPORAL_STRIDE,
        "effective_timepoints": int(X_train.shape[2]),
        "train_subjects": TRAIN_SUBJECTS,
        "test_subjects": TEST_SUBJECTS,
        "train_shape": list(X_train.shape),
        "test_shape": list(X_test.shape),
        "n_kernels": N_KERNELS,
        "n_jobs": N_JOBS,
        "random_state": RANDOM_STATE,
        "accuracy": float(accuracy),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "labels": labels,
        "label_names": {str(k): v for k, v in LABEL_NAMES.items()},
        "nan_train": int(np.isnan(X_train).sum()),
        "nan_test": int(np.isnan(X_test).sum()),
    }

    predictions.to_csv(OUTPUT_DIR / "wesad_multirocket_standardized_split_predictions.csv", index=False)
    pd.DataFrame(cm, index=labels, columns=labels).to_csv(
        OUTPUT_DIR / "wesad_multirocket_standardized_split_confusion_matrix.csv"
    )

    with open(OUTPUT_DIR / "wesad_multirocket_standardized_split_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    with open(OUTPUT_DIR / "wesad_multirocket_standardized_split_classification_report.json", "w") as f:
        json.dump(report_dict, f, indent=2)

    with open(OUTPUT_DIR / "wesad_multirocket_standardized_split_classification_report.txt", "w") as f:
        f.write(report_text)

    print()
    print("=== WESAD MultiRocket standardized split summary ===")
    print(json.dumps(summary, indent=2))

    print()
    print("Classification report:")
    print(report_text)

    print()
    print("Saved outputs to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
