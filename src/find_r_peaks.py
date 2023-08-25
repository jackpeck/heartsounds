from scipy import signal
import numpy as np
from ecgdetectors import Detectors
from dataclasses import dataclass

from .find_r_peaks_neurokit2 import find_r_peaks_neurokit2
from .find_r_peaks_xqrs import find_r_peaks_xqrs
from .find_agreed_points_runs import find_agreed_points_runs
from .find_agreeing_points import find_agreeing_points, Agree_reduce_method


@dataclass
class ECG_r_peaks:
    r_peaks: np.ndarray
    rpeaks_where_next_is_also_agreed: np.ndarray
    rpeaks_by_detector: dict
    downsampled_signal: np.ndarray
    downsampled_sample_rate: float


def find_r_peaks(
    ecg,
    ecg_sample_rate,
    agreement_time_threshold=0.1,
    max_disagreers=2,
    root_detector="xqrs",
    agree_reduce_method=Agree_reduce_method.MAX,
    max_num_detectors_with_between_point=2,
):
    (
        rpeaks_by_detector,
        downsampled_signal,
        downsampled_sample_rate,
    ) = find_r_peaks_by_detector(ecg, ecg_sample_rate)

    agreed_r_peaks = find_agreeing_points(
        agreement_time_threshold=agreement_time_threshold,
        max_disagreers=max_disagreers,
        indices_by_detector=rpeaks_by_detector,
        signal=downsampled_signal,
        sample_rate=downsampled_sample_rate,
        root_detector=root_detector,
        agree_reduce_method=agree_reduce_method,
    )

    rpeaks_where_next_is_also_agreed = find_agreed_points_runs(
        max_num_detectors_with_between_point=max_num_detectors_with_between_point,
        agreement_time_threshold=agreement_time_threshold,
        agreed_points=agreed_r_peaks,
        points_by_detector=rpeaks_by_detector,
        sample_rate=downsampled_sample_rate,
    )

    return ECG_r_peaks(
        agreed_r_peaks,
        rpeaks_where_next_is_also_agreed,
        rpeaks_by_detector,
        downsampled_signal,
        downsampled_sample_rate,
    )


def find_r_peaks_by_detector(ecg, ecg_sample_rate):
    downsampled_signal, target_fs = preprocess_ecg(ecg, ecg_sample_rate)

    py_ecg_detectors = Detectors(target_fs)

    rpeaks_by_detector = {}
    rpeaks_by_detector["neurokit2"] = find_r_peaks_neurokit2(
        downsampled_signal, target_fs
    )
    rpeaks_by_detector["xqrs"] = find_r_peaks_xqrs(downsampled_signal, target_fs)
    rpeaks_by_detector["hamilton"] = np.array(
        py_ecg_detectors.hamilton_detector(downsampled_signal)
    )
    rpeaks_by_detector["engzee"] = np.array(
        py_ecg_detectors.engzee_detector(downsampled_signal)
    )
    rpeaks_by_detector["pan_tompkins"] = np.array(
        py_ecg_detectors.pan_tompkins_detector(downsampled_signal)
    )
    rpeaks_by_detector["swt"] = np.array(
        py_ecg_detectors.swt_detector(downsampled_signal)
    )
    rpeaks_by_detector["two_average"] = np.array(
        py_ecg_detectors.two_average_detector(downsampled_signal)
    )

    return rpeaks_by_detector, downsampled_signal, target_fs


def downsample_ecg(ecg, ecg_sample_rate):
    # downsample to 360Hz if original sample rate is higher
    original_signal = ecg.copy()
    original_fs = ecg_sample_rate
    target_fs = 360

    if ecg_sample_rate <= target_fs:
        target_fs = ecg_sample_rate
        downsampled_signal = original_signal
    else:
        downsampled_signal = signal.resample(
            original_signal, int(len(original_signal) * target_fs / original_fs)
        )

    return downsampled_signal, target_fs


def preprocess_ecg(ecg, ecg_sample_rate):
    downsampled_signal, target_fs = downsample_ecg(ecg, ecg_sample_rate)

    return downsampled_signal, target_fs
