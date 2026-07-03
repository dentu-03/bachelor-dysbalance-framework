import numpy as np


def validate_3d_tensor(X: np.ndarray) -> np.ndarray:
    """Validate and convert input to a floating-point 3D tensor."""
    X = np.asarray(X, dtype=float)

    if X.ndim != 3:
        raise ValueError("X must have shape (n_instances, n_channels, n_timepoints)")

    return X


def channel_nan_percentages(X: np.ndarray) -> np.ndarray:
    """
    Compute NaN percentage per channel for a 3D time-series tensor.

    Expected shape:
        (n_instances, n_channels, n_timepoints)
    """
    X = validate_3d_tensor(X)

    return np.isnan(X).mean(axis=(0, 2)) * 100


def compute_channel_medians(
    X: np.ndarray,
    fallback_value: float = 0.0,
) -> np.ndarray:
    """
    Compute one median value per channel.

    If a channel contains only NaNs, fallback_value is used.
    """
    X = validate_3d_tensor(X)

    medians = []

    for channel_idx in range(X.shape[1]):
        values = X[:, channel_idx, :]
        valid_values = values[~np.isnan(values)]

        if len(valid_values) == 0:
            medians.append(float(fallback_value))
        else:
            medians.append(float(np.median(valid_values)))

    return np.asarray(medians, dtype=float)


def impute_tensor_with_channel_values(
    X: np.ndarray,
    channel_values: np.ndarray,
) -> np.ndarray:
    """
    Replace NaNs in each channel with a predefined channel value.

    This function is useful when medians are computed on a training set and
    then applied to validation/test data.
    """
    X = validate_3d_tensor(X).copy()
    channel_values = np.asarray(channel_values, dtype=float)

    if channel_values.ndim != 1:
        raise ValueError("channel_values must be one-dimensional")

    if len(channel_values) != X.shape[1]:
        raise ValueError("channel_values length must match number of channels")

    for channel_idx, value in enumerate(channel_values):
        mask = np.isnan(X[:, channel_idx, :])
        X[:, channel_idx, :][mask] = value

    return X


def impute_tensor_channel_median(
    X: np.ndarray,
    fallback_value: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Impute NaNs in a 3D tensor using one median per channel.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Imputed tensor and channel medians.
    """
    medians = compute_channel_medians(X, fallback_value=fallback_value)
    X_imputed = impute_tensor_with_channel_values(X, medians)

    return X_imputed, medians
