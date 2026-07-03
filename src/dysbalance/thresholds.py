import numpy as np
import pandas as pd


def threshold_sweep(
    z_values: np.ndarray,
    groups: np.ndarray | None = None,
    thresholds: list[float] | tuple[float, ...] = (1.5, 2.0, 2.5, 3.0),
    value_name: str = "z_value",
) -> pd.DataFrame:
    """
    Compute abnormality rates for multiple absolute z-score thresholds.

    A value is considered abnormal if:

        abs(z) > threshold

    Parameters
    ----------
    z_values:
        One-dimensional array of z-normalized values.
    groups:
        Optional one-dimensional group labels, e.g. subject IDs, activity labels
        or combined subject-condition labels. If None, all values are treated
        as one group.
    thresholds:
        Threshold values to evaluate.
    value_name:
        Name of the analyzed value, used in the result table.

    Returns
    -------
    pd.DataFrame
        Table with abnormality rates per group and threshold.
    """
    z_values = np.asarray(z_values, dtype=float)

    if z_values.ndim != 1:
        raise ValueError("z_values must be one-dimensional")

    if groups is None:
        groups = np.array(["all"] * len(z_values), dtype=object)
    else:
        groups = np.asarray(groups)

    if groups.ndim != 1:
        raise ValueError("groups must be one-dimensional")

    if len(z_values) != len(groups):
        raise ValueError("z_values and groups must have the same length")

    rows = []

    for group in pd.unique(groups):
        mask = groups == group
        group_values = z_values[mask]
        valid = ~np.isnan(group_values)

        n_total = int(len(group_values))
        n_valid = int(valid.sum())

        for threshold in thresholds:
            if n_valid == 0:
                abnormal_rate_pct = np.nan
                n_abnormal = 0
            else:
                abnormal = np.abs(group_values[valid]) > threshold
                n_abnormal = int(abnormal.sum())
                abnormal_rate_pct = float(abnormal.mean() * 100)

            rows.append(
                {
                    "group": group,
                    "value_name": value_name,
                    "threshold": float(threshold),
                    "n_total": n_total,
                    "n_valid": n_valid,
                    "n_abnormal": n_abnormal,
                    "abnormal_rate_pct": abnormal_rate_pct,
                }
            )

    return pd.DataFrame(rows)
