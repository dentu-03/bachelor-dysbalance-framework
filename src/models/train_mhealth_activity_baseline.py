from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from aeon.classification.convolution_based import MiniRocketClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from src.project_paths import INTERIM_DATA_DIR, MODELS_DIR, REPORTS_DIR


INPUT_DIR = INTERIM_DATA_DIR / "mhealth" / "by_subject"
MODEL_DIR = MODELS_DIR / "mhealth"
REPORT_DIR = REPORTS_DIR / "models"

TRAIN_SUBJECTS = [1, 2, 3, 4, 5, 6, 7, 8]
TEST_SUBJECTS = [9, 10]

ACTIVITY_LABELS = {
    1: "standing_still",
    2: "sitting_relaxing",
    3: "lying_down",
    4: "walking",
    5: "climbing_stairs",
    6: "waist_bends_forward",
    7: "frontal_elevation_arms",
    8: "knees_bending",
    9: "cycling",
    10: "jogging",
    11: "running",
    12: "jump_front_back",
}


def load_subject(subject_id: int) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    x_path = INPUT_DIR / f"subject_{subject_id:02d}_X.npy"
    y_path = INPUT_DIR / f"subject_{subject_id:02d}_y.npy"
    metadata_path = INPUT_DIR / f"subject_{subject_id:02d}_metadata.csv"

    if not x_path.exists():
        raise FileNotFoundError(f"Missing tensor file: {x_path}")

    X = np.load(x_path)
    y = np.load(y_path)
    metadata = pd.read_csv(metadata_path)

    return X, y, metadata


def load_split(subject_ids: list[int]) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    xs = []
    ys = []
    metas = []

    for subject_id in subject_ids:
        X, y, metadata = load_subject(subject_id)
        xs.append(X)
        ys.append(y)
        metas.append(metadata)

    X_all = np.concatenate(xs, axis=0)
    y_all = np.concatenate(ys, axis=0)
    metadata_all = pd.concat(metas, ignore_index=True)

    return X_all, y_all, metadata_all


def label_distribution(y: np.ndarray) -> dict[int, int]:
    labels, counts = np.unique(y, return_counts=True)
    return {int(label): int(count) for label, count in zip(labels, counts)}


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    X_train, y_train, meta_train = load_split(TRAIN_SUBJECTS)
    X_test, y_test, meta_test = load_split(TEST_SUBJECTS)

    print("Train subjects:", TRAIN_SUBJECTS)
    print("Test subjects:", TEST_SUBJECTS)
    print("X_train:", X_train.shape)
    print("X_test:", X_test.shape)
    print("Train label distribution:", label_distribution(y_train))
    print("Test label distribution:", label_distribution(y_test))
    print("Train contains NaN:", bool(np.isnan(X_train).any()))
    print("Test contains NaN:", bool(np.isnan(X_test).any()))

    classifier = MiniRocketClassifier(random_state=42, n_jobs=-1)

    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    labels = sorted(ACTIVITY_LABELS)
    target_names = [ACTIVITY_LABELS[label] for label in labels]

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

    run_summary = {
        "dataset": "mhealth",
        "model": "MiniRocketClassifier",
        "train_subjects": ",".join(str(s) for s in TRAIN_SUBJECTS),
        "test_subjects": ",".join(str(s) for s in TEST_SUBJECTS),
        "n_train_windows": int(len(y_train)),
        "n_test_windows": int(len(y_test)),
        "n_channels": int(X_train.shape[1]),
        "window_size": int(X_train.shape[2]),
        "accuracy": float(accuracy),
        "train_contains_nan": bool(np.isnan(X_train).any()),
        "test_contains_nan": bool(np.isnan(X_test).any()),
    }

    prediction_df = meta_test.copy()
    prediction_df["true_label"] = y_test
    prediction_df["predicted_label"] = y_pred
    prediction_df["true_activity"] = prediction_df["true_label"].map(ACTIVITY_LABELS)
    prediction_df["predicted_activity"] = prediction_df["predicted_label"].map(ACTIVITY_LABELS)
    prediction_df["is_correct"] = prediction_df["true_label"] == prediction_df["predicted_label"]

    summary_path = REPORT_DIR / "mhealth_minirocket_subject_split_summary.csv"
    report_path = REPORT_DIR / "mhealth_minirocket_classification_report.csv"
    report_text_path = REPORT_DIR / "mhealth_minirocket_classification_report.txt"
    confusion_path = REPORT_DIR / "mhealth_minirocket_confusion_matrix.csv"
    prediction_path = REPORT_DIR / "mhealth_minirocket_predictions.csv"
    model_path = MODEL_DIR / "mhealth_minirocket_classifier.joblib"

    pd.DataFrame([run_summary]).to_csv(summary_path, index=False)
    pd.DataFrame(report_dict).T.to_csv(report_path)
    pd.DataFrame(
        cm,
        index=[ACTIVITY_LABELS[label] for label in labels],
        columns=[ACTIVITY_LABELS[label] for label in labels],
    ).to_csv(confusion_path)
    prediction_df.to_csv(prediction_path, index=False)

    with open(report_text_path, "w") as f:
        f.write(report_text)

    joblib.dump(classifier, model_path)

    print()
    print("Accuracy:", accuracy)
    print()
    print(report_text)
    print("Saved summary to:", summary_path)
    print("Saved classification report to:", report_path)
    print("Saved confusion matrix to:", confusion_path)
    print("Saved predictions to:", prediction_path)
    print("Saved model to:", model_path)


if __name__ == "__main__":
    main()
