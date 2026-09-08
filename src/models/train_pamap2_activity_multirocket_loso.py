from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from aeon.classification.convolution_based import MultiRocketClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from src.project_paths import PROCESSED_DATA_DIR, REPORTS_DIR


INPUT_DIR = PROCESSED_DATA_DIR / "pamap2" / "by_subject"
OUTPUT_DIR = REPORTS_DIR / "models" / "pamap2" / "multirocket_loso_5000"

SUBJECTS = ["101", "102", "103", "104", "105", "106", "107", "108"]

N_JOBS = 4
RANDOM_STATE = 42
N_KERNELS = 5000

ACTIVITY_LABELS = {
    1: "lying",
    2: "sitting",
    3: "standing",
    4: "walking",
    5: "running",
    6: "cycling",
    7: "Nordic walking",
    12: "ascending stairs",
    13: "descending stairs",
    16: "vacuum cleaning",
    17: "ironing",
    24: "rope jumping",
}


def load_subject(subject_id: str) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    x_path = INPUT_DIR / f"X_subject{subject_id}.npy"
    y_path = INPUT_DIR / f"y_subject{subject_id}.npy"
    metadata_path = INPUT_DIR / f"metadata_subject{subject_id}.csv"

    if not x_path.exists():
        raise FileNotFoundError(f"Missing X file: {x_path}")
    if not y_path.exists():
        raise FileNotFoundError(f"Missing y file: {y_path}")
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing metadata file: {metadata_path}")

    X = np.load(x_path).astype(np.float32)
    y = np.load(y_path).astype(int)
    metadata = pd.read_csv(metadata_path)

    metadata = metadata.copy()
    metadata["subject_id"] = str(subject_id)
    metadata["source_file"] = x_path.name

    if len(X) != len(y) or len(X) != len(metadata):
        raise ValueError(f"Mismatched X, y and metadata lengths for subject {subject_id}")

    return X, y, metadata


def load_dataset() -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    X_parts = []
    y_parts = []
    metadata_parts = []

    for subject_id in SUBJECTS:
        X, y, metadata = load_subject(subject_id)
        X_parts.append(X)
        y_parts.append(y)
        metadata_parts.append(metadata)

    X_all = np.concatenate(X_parts, axis=0)
    y_all = np.concatenate(y_parts, axis=0)
    metadata_all = pd.concat(metadata_parts, ignore_index=True)

    if len(X_all) != len(y_all) or len(X_all) != len(metadata_all):
        raise ValueError("Mismatched X, y and metadata lengths.")

    return X_all, y_all, metadata_all


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    X, y, metadata = load_dataset()

    labels = sorted(np.unique(y).astype(int).tolist())
    target_names = [ACTIVITY_LABELS.get(label, str(label)) for label in labels]

    print("Loaded PAMAP2 tensors")
    print("X:", X.shape)
    print("y:", y.shape)
    print("metadata:", metadata.shape)
    print("subjects:", SUBJECTS)
    print("labels:", labels)
    print("NaNs:", int(np.isnan(X).sum()))

    prediction_rows = []
    fold_rows = []
    confusion_matrices = {}

    for subject in SUBJECTS:
        test_mask = metadata["subject_id"].astype(str) == subject
        train_mask = ~test_mask

        X_train = X[train_mask]
        y_train = y[train_mask]
        X_test = X[test_mask]
        y_test = y[test_mask]
        test_metadata = metadata.loc[test_mask].reset_index(drop=True)

        print()
        print(f"=== LOSO subject {subject} ===")
        print("train:", X_train.shape, "test:", X_test.shape)
        print("train labels:", sorted(np.unique(y_train).astype(int).tolist()))
        print("test labels:", sorted(np.unique(y_test).astype(int).tolist()))

        clf = MultiRocketClassifier(
            n_kernels=N_KERNELS,
            n_jobs=N_JOBS,
            random_state=RANDOM_STATE,
        )

        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        macro_f1 = f1_score(y_test, y_pred, labels=labels, average="macro", zero_division=0)
        weighted_f1 = f1_score(y_test, y_pred, labels=labels, average="weighted", zero_division=0)

        report = classification_report(
            y_test,
            y_pred,
            labels=labels,
            target_names=target_names,
            output_dict=True,
            zero_division=0,
        )

        fold_rows.append(
            {
                "dataset": "pamap2",
                "model": "MultiRocketClassifier",
                "validation": "leave_one_subject_out",
                "test_subject": subject,
                "n_train": int(len(y_train)),
                "n_test": int(len(y_test)),
                "n_channels": int(X.shape[1]),
                "n_timepoints": int(X.shape[2]),
                "n_kernels": N_KERNELS,
                "accuracy": float(accuracy),
                "macro_f1": float(macro_f1),
                "weighted_f1": float(weighted_f1),
            }
        )

        fold_predictions = test_metadata.copy()
        fold_predictions["y_true"] = y_test
        fold_predictions["y_pred"] = y_pred
        fold_predictions["true_activity_name"] = [
            ACTIVITY_LABELS.get(int(label), str(label)) for label in y_test
        ]
        fold_predictions["pred_activity_name"] = [
            ACTIVITY_LABELS.get(int(label), str(label)) for label in y_pred
        ]
        fold_predictions["is_correct"] = y_test == y_pred
        fold_predictions["test_subject"] = subject
        prediction_rows.append(fold_predictions)

        confusion_matrices[subject] = confusion_matrix(
            y_test,
            y_pred,
            labels=labels,
        ).tolist()

        with open(OUTPUT_DIR / f"classification_report_subject_{subject}.json", "w") as f:
            json.dump(report, f, indent=2)

        print(
            f"accuracy={accuracy:.6f}, "
            f"macro_f1={macro_f1:.6f}, "
            f"weighted_f1={weighted_f1:.6f}"
        )

    folds = pd.DataFrame(fold_rows)
    predictions = pd.concat(prediction_rows, ignore_index=True)

    summary = {
        "dataset": "pamap2",
        "model": "MultiRocketClassifier",
        "validation": "leave_one_subject_out",
        "n_subjects": int(len(SUBJECTS)),
        "n_windows": int(len(y)),
        "x_shape": list(X.shape),
        "labels": labels,
        "label_names": target_names,
        "n_kernels": N_KERNELS,
        "random_state": RANDOM_STATE,
        "accuracy_mean": float(folds["accuracy"].mean()),
        "accuracy_std": float(folds["accuracy"].std(ddof=1)),
        "accuracy_min": float(folds["accuracy"].min()),
        "accuracy_max": float(folds["accuracy"].max()),
        "macro_f1_mean": float(folds["macro_f1"].mean()),
        "macro_f1_std": float(folds["macro_f1"].std(ddof=1)),
        "macro_f1_min": float(folds["macro_f1"].min()),
        "macro_f1_max": float(folds["macro_f1"].max()),
        "weighted_f1_mean": float(folds["weighted_f1"].mean()),
        "weighted_f1_std": float(folds["weighted_f1"].std(ddof=1)),
        "weighted_f1_min": float(folds["weighted_f1"].min()),
        "weighted_f1_max": float(folds["weighted_f1"].max()),
        "confusion_matrices_by_subject": confusion_matrices,
    }

    folds.to_csv(OUTPUT_DIR / "pamap2_multirocket_loso_folds.csv", index=False)
    predictions.to_csv(OUTPUT_DIR / "pamap2_multirocket_loso_predictions.csv", index=False)

    with open(OUTPUT_DIR / "pamap2_multirocket_loso_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print()
    print("=== PAMAP2 MultiRocket LOSO summary ===")
    print(json.dumps(summary, indent=2))

    print()
    print("Saved outputs to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
