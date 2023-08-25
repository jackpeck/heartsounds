import numpy as np
from wfdb import processing


def find_r_peaks_gqrs(original_signal: np.ndarray, fs: int) -> np.ndarray:
    qrs_inds = processing.qrs.gqrs_detect(sig=original_signal, fs=fs)

    # Correct the peaks shifting them to local maxima
    max_bpm = 230
    # Use the maximum possible bpm as the search radius
    search_radius = int(fs * 60 / max_bpm)
    corrected_peak_inds = processing.peaks.correct_peaks(
        original_signal,
        peak_inds=qrs_inds,
        search_radius=search_radius,
        smooth_window_size=150,
        peak_dir="up",
    )

    return corrected_peak_inds
