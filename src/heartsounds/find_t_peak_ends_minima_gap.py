import math
import numpy as np
import scipy.signal


def find_t_peak_ends_minima_gap(
    sig: np.ndarray,
    r_peaks_where_next_is_also_agreed_indices: np.ndarray,
    agreed_r_peaks_indices: np.ndarray,
) -> np.ndarray:
    # find local minima, then first minima with greatest gap from prior minima, then find first >0 point after that minima

    derivative = np.gradient(sig)
    smoothed_derivative = scipy.signal.savgol_filter(derivative, 51, 3)

    minima = scipy.signal.argrelextrema(smoothed_derivative, np.less)[0]
    t_peak_ends = []

    for i in range(len(agreed_r_peaks_indices) - 1):
        peak_pre = agreed_r_peaks_indices[i]

        if peak_pre not in r_peaks_where_next_is_also_agreed_indices:
            continue

        peak_post = agreed_r_peaks_indices[i + 1]

        post_threshold = peak_pre + 0.7 * (
            peak_post - peak_pre
        )  # assume t peak end is in first 70% of r-r interval
        minima_between = minima[(minima > peak_pre) & (minima < post_threshold)]

        max_gap = -math.inf

        for i in range(1, len(minima_between)):
            gap = minima_between[i] - minima_between[i - 1]
            if gap > max_gap:
                max_gap = gap
                max_gap_ind = minima_between[i]

        # find first 0 point after minima
        for i in range(max_gap_ind, len(smoothed_derivative)):
            if smoothed_derivative[i] > 0:
                t_peak_end = i
                break

        t_peak_ends.append(t_peak_end)

    return np.array(t_peak_ends)
