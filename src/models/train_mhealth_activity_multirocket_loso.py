from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from aeon.classification.convolution_based import MultiRocketClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from src.project_paths import DATA_DIR, REPORTS_DIR


INPUT_DIR = DATA_DIR / "interim" / "mhealth" / "by_subject"
OUTPUT_DIR = REPORTS_DIR / "models" / "mhealth" / "multirocket_loso"

N_JOBS = -1
RANDOM_STATE = 42
N_KERNELS = 10000


def load_subject_npy_triplet(x_path: Path) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    prefix = x_path.name.replace("_X.npy", "")
    y_path = x_path.with_name(f"{prefix}_y.npy")
    metadata_path = x_path.with_name(f"{prefix}_metadata.csv")

    if not y_path.exists():
        raise FileNotFoundError(f"Missing y file for {x_path}: {y_path}")

    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing metadata file for {x_path}: {metadata_path}")

    X = np.load(x_path).astype(np.float32)
    y = np.load(y_path).astype(int)
    metadata = pd.read_csv(metadata_path)

    if "subject_id" not in metadata.columns:
        subject_id = int(prefix.split("_")[-1])
        metadata["subject_id"] = subject_id

    return X, y, metadata


def load_subject_npz(path: Path) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    data = np.load(path, allow_pickle=True)

    X = data["X"].astype(np.float32)
    y = data["y"].astype(int)

    if "metadata" in data.files:
        metadata = pd.DataFrame(data["metadata"].tolist())
    elif "window_metadata" in data.files:
        metadata = pd.DataFrame(data["window_metadata"].tolist())
    else:
        metadata = pd.DataFrame({"window_index": np.arange(len(y))})

    if "subject_id" not in metadata.columns:
        subject_id = int(path.stem.split("subject")[-1].replace("_", ""))
        metadata["subject_id"] = subject_id

    return X, y, metadata


def load_dataset() -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    npy_subject_files = sorted(INPUT_DIR.glob("subject_*_X.npy"))
    npz_subject_files = sorted(INPUT_DIR.glob("*.npz"))

    X_parts = []
    y_parts = []
    metadata_parts = []

    if npy_subject_files:
        subject_files = npy_subject_files
        loader = load_subject_npy_triplet
    elif npz_subject_files:
        subject_files = npz_subject_files
        loader = load_subject_npz
    else:
        raise FileNotFoundError(f"No MHEALTH subject tensors found in {INPUT_DIR}")

    for path in subject_files:
        X, y, metadata = loader(path)
        metadata = metadata.copy()
        metadata["source_file"] = path.name

        if len(X) != len(y) or len(X) != len(metadata):
            raise ValueError(f"Mismatched X, y and metadata lengths for {path}")

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

    subjects = sorted(metadata["subject_id"].astype(str).unique())

    print("Loaded MHEALTH tensors")
    print("X:", X.shape)
    print("y:", y.shape)
    print("metadata:", metadata.shape)
    print("subjects:", subjects)

    prediction_rows = []
    fold_rows = []
    confusion_matrices = {}

    for subject in subjects:
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

        clf = MultiRocketClassifier(
            n_kernels=N_KERNELS,
            n_jobs=N_JOBS,
            random_state=RANDOM_STATE,
        )
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        macro_f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
        weighted_f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        report = classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0,
        )

        fold_rows.append(
            {
                "dataset": "mhealth",
                "model": "MultiRocketClassifier",
                "validation": "leave_one_subject_out",
                "test_subject": subject,
                "n_train": int(len(y_train)),
                "n_test": int(len(y_test)),
                "n_kernels": N_KERNELS,
                "accuracy": float(accuracy),
                "macro_f1": float(macro_f1),
                "weighted_f1": float(weighted_f1),
            }
        )

        fold_predictions = test_metadata.copy()
        fold_predictions["y_true"] = y_test
        fold_predictions["y_pred"] = y_pred
        fold_predictions["is_correct"] = y_test == y_pred
        fold_predictions["test_subject"] = subject
        prediction_rows.append(fold_predictions)

        labels = sorted(np.unique(y))
        confusion_matrices[subject] = confusion_matrix(
            y_test,
            y_pred,
            labels=labels,
        ).tolist()

        print(
            f"accuracy={accuracy:.6f}, "
            f"macro_f1={macro_f1:.6f}, "
            f"weighted_f1={weighted_f1:.6f}"
        )

        report_path = OUTPUT_DIR / f"classification_report_subject_{subject}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

    folds = pd.DataFrame(fold_rows)
    predictions = pd.concat(prediction_rows, ignore_index=True)

    summary = {
        "dataset": "mhealth",
        "model": "MultiRocketClassifier",
        "validation": "leave_one_subject_out",
        "n_subjects": int(len(subjects)),
        "n_windows": int(len(y)),
        "x_shape": list(X.shape),
        "n_kernels": N_KERNELS,
        "random_state": RANDOM_STATE,
        "accuracy_mean": float(folds["accuracy"].mean()),
        "accuracy_std": float(folds["accuracy"].std(ddof=1)),
        "accuracy_min": float(folds["accuracy"].min()),
        "accuracy_max": float(folds["accuracy"].max()),
        "macro_f1_mean": float(folds["macro_f1"].mean()),
        "macro_f1_std": float(folds["macro_f1"].std(ddof=1)),
        "weighted_f1_mean": float(folds["weighted_f1"].mean()),
        "weighted_f1_std": float(folds["weighted_f1"].std(ddof=1)),
        "confusion_matrices_by_subject": confusion_matrices,
    }

    folds.to_csv(OUTPUT_DIR / "mhealth_multirocket_loso_folds.csv", index=False)
    predictions.to_csv(OUTPUT_DIR / "mhealth_multirocket_loso_predictions.csv", index=False)

    with open(OUTPUT_DIR / "mhealth_multirocket_loso_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print()
    print("=== MultiRocket LOSO summary ===")
    print(json.dumps(summary, indent=2))

    print()
    print("Saved outputs to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
