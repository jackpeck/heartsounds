import numpy as np
from wfdb import processing


def find_r_peaks_xqrs(downsampled_signal: np.ndarray, fs: int) -> np.ndarray:
    xqrs = processing.XQRS(sig=downsampled_signal, fs=fs)
    xqrs.detect(verbose=False)

    # Correct the peaks shifting them to local maxima
    max_bpm = 230
    # Use the maximum possible bpm as the search radius
    search_radius = int(fs * 60 / max_bpm * 0.3)
    corrected_peak_inds = processing.peaks.correct_peaks(
        downsampled_signal,
        peak_inds=xqrs.qrs_inds,
        search_radius=search_radius,
        smooth_window_size=150,
        peak_dir="up",
    )

    return corrected_peak_inds
