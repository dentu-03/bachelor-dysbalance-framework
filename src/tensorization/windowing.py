import numpy as np


def sliding_window_starts(
    n_samples: int,
    window_size: int,
    step_size: int,
) -> np.ndarray:
    """
    Compute valid start indices for sliding windows.

    Parameters
    ----------
    n_samples:
        Number of samples in the sequence.
    window_size:
        Number of time points per window.
    step_size:
        Step size between consecutive windows.

    Returns
    -------
    np.ndarray
        One-dimensional array of window start indices.
    """
    if n_samples < 0:
        raise ValueError("n_samples must be non-negative")

    if window_size <= 0:
        raise ValueError("window_size must be positive")

    if step_size <= 0:
        raise ValueError("step_size must be positive")

    if n_samples < window_size:
        return np.array([], dtype=int)

    return np.arange(0, n_samples - window_size + 1, step_size, dtype=int)


def window_array(
    values: np.ndarray,
    window_size: int,
    step_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Convert a 2D time series array into aeon-compatible sliding windows.

    Input shape:
        (n_samples, n_channels)

    Output shape:
        (n_windows, n_channels, window_size)
    """
    values = np.asarray(values, dtype=float)

    if values.ndim != 2:
        raise ValueError("values must have shape (n_samples, n_channels)")

    starts = sliding_window_starts(
        n_samples=values.shape[0],
        window_size=window_size,
        step_size=step_size,
    )

    windows = np.empty(
        (len(starts), values.shape[1], window_size),
        dtype=float,
    )

    for i, start in enumerate(starts):
        stop = start + window_size
        windows[i] = values[start:stop].T

    return windows, starts


def majority_labels(
    labels: np.ndarray,
    starts: np.ndarray,
    window_size: int,
) -> np.ndarray:
    """
    Assign one label per window using majority voting.
    """
    labels = np.asarray(labels)
    starts = np.asarray(starts, dtype=int)

    if labels.ndim != 1:
        raise ValueError("labels must be one-dimensional")

    y = []

    for start in starts:
        stop = start + window_size
        window_labels = labels[start:stop]

        unique, counts = np.unique(window_labels, return_counts=True)
        majority = unique[np.argmax(counts)]
        y.append(majority)

    return np.asarray(y)


def window_timestamps(
    timestamps: np.ndarray,
    starts: np.ndarray,
    window_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return start and end timestamps for each window.
    """
    timestamps = np.asarray(timestamps)
    starts = np.asarray(starts, dtype=int)

    if timestamps.ndim != 1:
        raise ValueError("timestamps must be one-dimensional")

    start_times = timestamps[starts]
    end_times = timestamps[starts + window_size - 1]

    return start_times, end_times
