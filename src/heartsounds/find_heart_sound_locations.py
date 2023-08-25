import numpy as np

from .constants import mean_s1_duration, mean_s2_duration


def find_s1s(rpeaks_where_next_is_also_agreed):
    return np.array(
        [(peak, peak + mean_s1_duration) for peak in rpeaks_where_next_is_also_agreed]
    )


def find_s2s(agreed_t_peak_ends):
    return np.array(
        [
            (peak - mean_s2_duration / 2, peak + mean_s2_duration / 2)
            for peak in agreed_t_peak_ends
        ]
    )
