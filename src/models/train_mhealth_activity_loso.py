from __future__ import annotations

import numpy as np
import pandas as pd
from aeon.classification.convolution_based import MiniRocketClassifier
from sklearn.metrics import accuracy_score, classification_report

from src.project_paths import INTERIM_DATA_DIR, REPORTS_DIR


INPUT_DIR = INTERIM_DATA_DIR / "mhealth" / "by_subject"
REPORT_DIR = REPORTS_DIR / "models"

SUBJECTS = list(range(1, 11))

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
    X = np.load(INPUT_DIR / f"subject_{subject_id:02d}_X.npy")
    y = np.load(INPUT_DIR / f"subject_{subject_id:02d}_y.npy")
    metadata = pd.read_csv(INPUT_DIR / f"subject_{subject_id:02d}_metadata.csv")
    return X, y, metadata


def load_subjects(subject_ids: list[int]) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    xs = []
    ys = []
    metas = []

    for subject_id in subject_ids:
        X, y, metadata = load_subject(subject_id)
        xs.append(X)
        ys.append(y)
        metas.append(metadata)

    return (
        np.concatenate(xs, axis=0),
        np.concatenate(ys, axis=0),
        pd.concat(metas, ignore_index=True),
    )


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    labels = sorted(ACTIVITY_LABELS)
    target_names = [ACTIVITY_LABELS[label] for label in labels]

    fold_rows = []
    class_rows = []
    prediction_parts = []

    for test_subject in SUBJECTS:
        train_subjects = [s for s in SUBJECTS if s != test_subject]

        X_train, y_train, _ = load_subjects(train_subjects)
        X_test, y_test, meta_test = load_subjects([test_subject])

        print()
        print(f"LOSO fold: test_subject={test_subject}")
        print("Train subjects:", train_subjects)
        print("X_train:", X_train.shape)
        print("X_test:", X_test.shape)
        print("Train contains NaN:", bool(np.isnan(X_train).any()))
        print("Test contains NaN:", bool(np.isnan(X_test).any()))

        classifier = MiniRocketClassifier(random_state=42, n_jobs=-1)
        classifier.fit(X_train, y_train)

        y_pred = classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

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
                "dataset": "mhealth",
                "model": "MiniRocketClassifier",
                "split": "leave_one_subject_out",
                "test_subject": test_subject,
                "train_subjects": ",".join(str(s) for s in train_subjects),
                "n_train_windows": int(len(y_train)),
                "n_test_windows": int(len(y_test)),
                "n_channels": int(X_train.shape[1]),
                "window_size": int(X_train.shape[2]),
                "accuracy": float(accuracy),
                "macro_f1": float(report["macro avg"]["f1-score"]),
                "weighted_f1": float(report["weighted avg"]["f1-score"]),
                "train_contains_nan": bool(np.isnan(X_train).any()),
                "test_contains_nan": bool(np.isnan(X_test).any()),
            }
        )

        for activity_name, metrics in report.items():
            if activity_name in {"accuracy", "macro avg", "weighted avg"}:
                continue

            class_rows.append(
                {
                    "test_subject": test_subject,
                    "activity_name": activity_name,
                    "precision": float(metrics["precision"]),
                    "recall": float(metrics["recall"]),
                    "f1_score": float(metrics["f1-score"]),
                    "support": int(metrics["support"]),
                }
            )

        predictions = meta_test.copy()
        predictions["test_subject"] = test_subject
        predictions["true_label"] = y_test
        predictions["predicted_label"] = y_pred
        predictions["true_activity"] = predictions["true_label"].map(ACTIVITY_LABELS)
        predictions["predicted_activity"] = predictions["predicted_label"].map(ACTIVITY_LABELS)
        predictions["is_correct"] = predictions["true_label"] == predictions["predicted_label"]
        prediction_parts.append(predictions)

        print(f"Accuracy: {accuracy:.4f}")
        print(f"Macro F1: {report['macro avg']['f1-score']:.4f}")
        print(f"Weighted F1: {report['weighted avg']['f1-score']:.4f}")

    fold_df = pd.DataFrame(fold_rows)
    class_df = pd.DataFrame(class_rows)
    prediction_df = pd.concat(prediction_parts, ignore_index=True)

    fold_path = REPORT_DIR / "mhealth_minirocket_loso_summary.csv"
    class_path = REPORT_DIR / "mhealth_minirocket_loso_class_report.csv"
    prediction_path = REPORT_DIR / "mhealth_minirocket_loso_predictions.csv"

    fold_df.to_csv(fold_path, index=False)
    class_df.to_csv(class_path, index=False)
    prediction_df.to_csv(prediction_path, index=False)

    print()
    print("LOSO summary:")
    print(fold_df.to_string(index=False))

    print()
    print("Aggregate LOSO metrics:")
    print(fold_df[["accuracy", "macro_f1", "weighted_f1"]].describe().to_string())

    print()
    print(f"Saved LOSO summary to: {fold_path}")
    print(f"Saved LOSO class report to: {class_path}")
    print(f"Saved LOSO predictions to: {prediction_path}")


if __name__ == "__main__":
    main()
