import numpy as np
import pandas as pd


def z_normalize_by_group(
    values: np.ndarray,
    groups: np.ndarray,
    ddof: int = 1,
    eps: float = 1e-8,
) -> np.ndarray:
    """
    Compute group-wise z-normalized values.

    Each value is normalized relative to the mean and standard deviation
    of its own group, for example one subject or one subject-condition group.
    """
    values = np.asarray(values, dtype=float)
    groups = np.asarray(groups)

    if values.ndim != 1:
        raise ValueError("values must be one-dimensional")

    if groups.ndim != 1:
        raise ValueError("groups must be one-dimensional")

    if len(values) != len(groups):
        raise ValueError("values and groups must have the same length")

    z = np.zeros_like(values, dtype=float)

    for group in pd.unique(groups):
        mask = groups == group
        group_values = values[mask]

        valid = ~np.isnan(group_values)

        if valid.sum() <= ddof:
            z[mask] = 0.0
            continue

        mu = np.nanmean(group_values)
        sd = np.nanstd(group_values, ddof=ddof)

        if sd <= eps or np.isnan(sd):
            z[mask] = 0.0
        else:
            z[mask] = (group_values - mu) / sd

    return z


def z_normalize_by_subject(
    values: np.ndarray,
    subject_ids: np.ndarray,
    ddof: int = 1,
) -> np.ndarray:
    """
    Convenience wrapper for subject-wise z-normalization.
    """
    return z_normalize_by_group(values=values, groups=subject_ids, ddof=ddof)


def z_normalize_by_subject_and_context(
    values: np.ndarray,
    subject_ids: np.ndarray,
    context_labels: np.ndarray,
    ddof: int = 1,
) -> np.ndarray:
    """
    Z-normalize values by subject and context.

    Useful when a metric should be normalized separately for each
    subject and condition, e.g. subject + activity.
    """
    subject_ids = np.asarray(subject_ids)
    context_labels = np.asarray(context_labels)

    if len(subject_ids) != len(context_labels):
        raise ValueError("subject_ids and context_labels must have the same length")

    groups = np.array(
        [f"{sid}__{ctx}" for sid, ctx in zip(subject_ids, context_labels)],
        dtype=object,
    )

    return z_normalize_by_group(values=values, groups=groups, ddof=ddof)
