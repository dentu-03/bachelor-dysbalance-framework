import numpy as np


def safe_log_ratio(
    numerator: np.ndarray,
    denominator: np.ndarray,
    eps: float = 1e-8,
) -> np.ndarray:
    """
    Compute a numerically stable log-ratio.

    The log-ratio is useful for dysbalance metrics because it treats
    doubling and halving symmetrically:

    log(2 / 1)  > 0
    log(1 / 2)  < 0

    Parameters
    ----------
    numerator:
        Numerator values.
    denominator:
        Denominator values.
    eps:
        Small value to avoid division by zero.

    Returns
    -------
    np.ndarray
        log((numerator + eps) / (denominator + eps))
    """
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)

    if numerator.shape != denominator.shape:
        raise ValueError("numerator and denominator must have the same shape")

    return np.log((numerator + eps) / (denominator + eps))


def absolute_log_ratio(
    numerator: np.ndarray,
    denominator: np.ndarray,
    eps: float = 1e-8,
) -> np.ndarray:
    """
    Compute the absolute log-ratio.

    This removes direction and keeps only deviation strength.
    """
    return np.abs(safe_log_ratio(numerator, denominator, eps=eps))
