from dataclasses import dataclass
import numpy as np

from .find_r_peaks import find_r_peaks
from .find_t_peak_ends import find_t_peak_ends
from .find_agreeing_points import Agree_reduce_method
from .constants import mean_s1_duration


@dataclass
class ECG_peaks:
    r_peaks: np.ndarray
    rpeaks_where_next_is_also_agreed: np.ndarray
    rpeaks_by_detector: dict
    downsampled_signal: np.ndarray
    downsampled_sample_rate: float

    t_peak_ends: np.ndarray
    t_peak_ends_by_detector: dict


def find_ecg_peaks(
    ecg,
    ecg_sample_rate,
    r_peak_agreement_time_threshold=0.1,
    r_peak_max_disagreers=2,
    r_peak_root_detector="xqrs",
    r_peak_agree_reduce_method=Agree_reduce_method.MAX,
    r_peak_max_num_detectors_with_between_point=2,
    t_peak_agreement_time_threshold=mean_s1_duration,
    t_peak_max_disagreers=1,
    t_peak_root_detector="cwt",
    t_peak_agree_reduce_method=Agree_reduce_method.MEDIAN,
):
    ecg_r_peaks = find_r_peaks(
        ecg,
        ecg_sample_rate,
        agreement_time_threshold=r_peak_agreement_time_threshold,
        max_disagreers=r_peak_max_disagreers,
        root_detector=r_peak_root_detector,
        agree_reduce_method=r_peak_agree_reduce_method,
        max_num_detectors_with_between_point=r_peak_max_num_detectors_with_between_point,
    )

    ecg_t_peak_ends = find_t_peak_ends(
        ecg,
        ecg_sample_rate,
        ecg_r_peaks.r_peaks,
        ecg_r_peaks.rpeaks_where_next_is_also_agreed,
        agreement_time_threshold=t_peak_agreement_time_threshold,
        max_disagreers=t_peak_max_disagreers,
        root_detector=t_peak_root_detector,
        agree_reduce_method=t_peak_agree_reduce_method,
    )

    return ECG_peaks(
        ecg_r_peaks.r_peaks,
        ecg_r_peaks.rpeaks_where_next_is_also_agreed,
        ecg_r_peaks.rpeaks_by_detector,
        ecg_r_peaks.downsampled_signal,
        ecg_r_peaks.downsampled_sample_rate,
        ecg_t_peak_ends.t_peak_ends,
        ecg_t_peak_ends.t_peak_ends_by_detector,
    )
