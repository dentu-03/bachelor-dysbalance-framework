import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from aeon.classification.convolution_based import MiniRocketClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from src.project_paths import INTERIM_DATA_DIR, REPORTS_DIR, MODELS_DIR


TRAIN_SUBJECTS = ["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11"]
TEST_SUBJECTS = ["S13", "S14", "S15", "S16", "S17"]


LABEL_NAMES = {
    1: "baseline",
    2: "stress",
    3: "amusement",
    4: "meditation",
}


def load_subject_tensors(subject_ids: list[str]) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """Load and concatenate WESAD chest tensors for selected subjects."""
    base_dir = INTERIM_DATA_DIR / "wesad" / "chest_by_subject"

    X_parts = []
    y_parts = []
    metadata_parts = []

    for subject_id in subject_ids:
        x_path = base_dir / f"X_{subject_id}.npy"
        y_path = base_dir / f"y_{subject_id}.npy"
        meta_path = base_dir / f"metadata_{subject_id}.csv"

        if not x_path.exists():
            raise FileNotFoundError(f"Missing X file: {x_path}")
        if not y_path.exists():
            raise FileNotFoundError(f"Missing y file: {y_path}")
        if not meta_path.exists():
            raise FileNotFoundError(f"Missing metadata file: {meta_path}")

        X = np.load(x_path, mmap_mode="r").astype(np.float32)
        y = np.load(y_path)
        metadata = pd.read_csv(meta_path)

        X_parts.append(X)
        y_parts.append(y)
        metadata_parts.append(metadata)

    X_all = np.concatenate(X_parts, axis=0)
    y_all = np.concatenate(y_parts, axis=0)
    metadata_all = pd.concat(metadata_parts, ignore_index=True)

    return X_all, y_all, metadata_all


def make_label_names(labels: list[int]) -> list[str]:
    """Create readable class labels for plots."""
    return [f"{label}\n{LABEL_NAMES.get(int(label), 'unknown')}" for label in labels]


def compute_channel_standardization(X_train: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute train-set channel-wise mean and standard deviation.

    Statistics are computed across windows and timepoints for each channel.
    """
    means = X_train.mean(axis=(0, 2), keepdims=True)
    stds = X_train.std(axis=(0, 2), keepdims=True)

    stds = np.where(stds == 0, 1.0, stds)

    return means.astype(np.float32), stds.astype(np.float32)


def apply_channel_standardization(
    X: np.ndarray,
    means: np.ndarray,
    stds: np.ndarray,
) -> np.ndarray:
    """Apply channel-wise standardization to a 3D tensor."""
    return ((X - means) / stds).astype(np.float32)


def save_confusion_matrix_plot(
    cm: np.ndarray,
    labels: list[int],
    out_path,
    title: str,
    normalize: bool = False,
) -> None:
    """Save confusion matrix heatmap as PNG."""
    plot_values = cm.astype(float)

    if normalize:
        row_sums = plot_values.sum(axis=1, keepdims=True)
        plot_values = np.divide(
            plot_values,
            row_sums,
            out=np.zeros_like(plot_values),
            where=row_sums != 0,
        )

    fig, ax = plt.subplots(figsize=(7, 6))

    image = ax.imshow(plot_values, interpolation="nearest")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    label_names = make_label_names(labels)

    ax.set_title(title)
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(label_names, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(label_names, fontsize=9)

    threshold = plot_values.max() / 2 if plot_values.size > 0 else 0

    for i in range(plot_values.shape[0]):
        for j in range(plot_values.shape[1]):
            if normalize:
                text = f"{plot_values[i, j]:.2f}"
            else:
                text = str(int(cm[i, j]))

            ax.text(
                j,
                i,
                text,
                ha="center",
                va="center",
                fontsize=9,
                color="white" if plot_values[i, j] > threshold else "black",
            )

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    report_dir = REPORTS_DIR / "models"
    report_dir.mkdir(parents=True, exist_ok=True)

    model_dir = MODELS_DIR / "wesad"
    model_dir.mkdir(parents=True, exist_ok=True)

    print("Loading train tensors...")
    X_train, y_train, train_metadata = load_subject_tensors(TRAIN_SUBJECTS)

    print("Loading test tensors...")
    X_test, y_test, test_metadata = load_subject_tensors(TEST_SUBJECTS)

    print()
    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)
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

    clf = MiniRocketClassifier(random_state=42)

    print()
    print("Training standardized WESAD MiniRocket baseline...")
    clf.fit(X_train, y_train)

    print("Predicting...")
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    labels = sorted(np.unique(np.concatenate([y_test, y_pred])).astype(int).tolist())
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    report_dict = classification_report(
        y_test,
        y_pred,
        labels=labels,
        target_names=[LABEL_NAMES.get(label, str(label)) for label in labels],
        output_dict=True,
        zero_division=0,
    )

    report_text = classification_report(
        y_test,
        y_pred,
        labels=labels,
        target_names=[LABEL_NAMES.get(label, str(label)) for label in labels],
        zero_division=0,
    )

    print()
    print(f"Accuracy: {accuracy:.4f}")
    print()
    print("Classification report:")
    print(report_text)

    result_summary = {
        "model": "MiniRocketClassifier",
        "preprocessing": "train-set channel-wise standardization",
        "task": "WESAD chest condition classification",
        "split": "subject-wise",
        "train_subjects": TRAIN_SUBJECTS,
        "test_subjects": TEST_SUBJECTS,
        "train_shape": list(X_train.shape),
        "test_shape": list(X_test.shape),
        "accuracy": float(accuracy),
        "train_labels": sorted(np.unique(y_train).astype(int).tolist()),
        "test_labels": sorted(np.unique(y_test).astype(int).tolist()),
        "label_names": LABEL_NAMES,
        "n_train_windows": int(X_train.shape[0]),
        "n_test_windows": int(X_test.shape[0]),
        "n_channels": int(X_train.shape[1]),
        "n_timepoints": int(X_train.shape[2]),
        "nan_train": int(np.isnan(X_train).sum()),
        "nan_test": int(np.isnan(X_test).sum()),
        "channel_means_shape": list(channel_means.shape),
        "channel_stds_shape": list(channel_stds.shape),
    }

    with open(report_dir / "wesad_minirocket_standardized_baseline_summary.json", "w") as f:
        json.dump(result_summary, f, indent=2)

    with open(report_dir / "wesad_minirocket_standardized_classification_report.json", "w") as f:
        json.dump(report_dict, f, indent=2)

    with open(report_dir / "wesad_minirocket_standardized_classification_report.txt", "w") as f:
        f.write(report_text)

    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    cm_df.to_csv(report_dir / "wesad_minirocket_standardized_confusion_matrix.csv")

    save_confusion_matrix_plot(
        cm=cm,
        labels=labels,
        out_path=report_dir / "wesad_minirocket_standardized_confusion_matrix_raw.png",
        title=f"WESAD MiniRocket Standardized Confusion Matrix\nAccuracy: {accuracy:.4f}",
        normalize=False,
    )

    save_confusion_matrix_plot(
        cm=cm,
        labels=labels,
        out_path=report_dir / "wesad_minirocket_standardized_confusion_matrix_normalized.png",
        title=f"WESAD MiniRocket Standardized Normalized Confusion Matrix\nAccuracy: {accuracy:.4f}",
        normalize=True,
    )

    joblib.dump(clf, model_dir / "wesad_minirocket_standardized_subject_split.joblib")

    print()
    print(f"Saved reports to: {report_dir}")
    print(f"Saved raw confusion matrix PNG to: {report_dir / 'wesad_minirocket_standardized_confusion_matrix_raw.png'}")
    print(f"Saved normalized confusion matrix PNG to: {report_dir / 'wesad_minirocket_standardized_confusion_matrix_normalized.png'}")
    print(f"Saved model to: {model_dir / 'wesad_minirocket_standardized_subject_split.joblib'}")


if __name__ == "__main__":
    main()
