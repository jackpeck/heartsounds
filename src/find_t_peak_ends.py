import neurokit2 as nk
import numpy as np
from dataclasses import dataclass

from .find_agreeing_points import find_agreeing_points, Agree_reduce_method
from .find_t_peak_ends_minima_gap import find_t_peak_ends_minima_gap


@dataclass
class ECG_t_end_peaks:
    t_peak_ends: np.ndarray
    t_peak_ends_by_detector: dict


def find_t_peak_ends(
    signal,
    sample_rate,
    agreed_r_peaks,
    rpeaks_where_next_is_also_agreed,
    agreement_time_threshold=0.1,
    max_disagreers=1,
    root_detector="cwt",
    agree_reduce_method=Agree_reduce_method.MEDIAN,
):
    t_peak_ends_by_detector = find_t_peak_ends_by_detector(
        signal, sample_rate, agreed_r_peaks, rpeaks_where_next_is_also_agreed
    )

    agreed_t_peak_ends = find_agreeing_points(
        agreement_time_threshold=agreement_time_threshold,
        max_disagreers=max_disagreers,
        indices_by_detector=t_peak_ends_by_detector,
        signal=signal,
        sample_rate=sample_rate,
        root_detector=root_detector,
        agree_reduce_method=agree_reduce_method,
    )

    return ECG_t_end_peaks(agreed_t_peak_ends, t_peak_ends_by_detector)


def find_t_peak_ends_by_detector(
    signal, sample_rate, agreed_r_peaks, rpeaks_where_next_is_also_agreed
):
    signal_times = np.arange(len(signal)) / sample_rate
    agreed_peaks_indices = [np.argmin(np.abs(signal_times - t)) for t in agreed_r_peaks]

    _, waves_peak = nk.ecg_delineate(
        signal, agreed_peaks_indices, sampling_rate=sample_rate, method="peak"
    )

    _, waves_cwt = nk.ecg_delineate(
        signal, agreed_peaks_indices, sampling_rate=sample_rate, method="cwt"
    )

    _, waves_dwt = nk.ecg_delineate(
        signal, agreed_peaks_indices, sampling_rate=sample_rate, method="dwt"
    )

    rpeaks_where_next_is_also_agreed_indices = [
        np.argmin(np.abs(signal_times - t)) for t in rpeaks_where_next_is_also_agreed
    ]

    minima_gap = find_t_peak_ends_minima_gap(
        signal, rpeaks_where_next_is_also_agreed_indices, agreed_peaks_indices
    )

    t_peak_ends_inc_nan_by_detector = {
        "peak": waves_peak["ECG_T_Offsets"],
        "cwt": waves_cwt["ECG_T_Offsets"],
        "dwt": waves_dwt["ECG_T_Offsets"],
        "minima_gap": minima_gap,
    }

    t_peak_ends_by_detector = {}

    for detector, indices in t_peak_ends_inc_nan_by_detector.items():
        # remove nans, and convert to int
        v = np.array(indices)
        v = v[~np.isnan(v)]
        v = v.astype(int)

        t_peak_ends_by_detector[detector] = v

    return t_peak_ends_by_detector
