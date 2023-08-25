import numpy as np
from enum import Enum

Agree_reduce_method = Enum("Agree_reduce_method", ("MEDIAN", "MAX"))


def find_agreeing_points(
    agreement_time_threshold: float,
    max_disagreers: int,
    indices_by_detector: dict,
    signal: np.ndarray,
    sample_rate: float,
    root_detector: str,
    agree_reduce_method: Agree_reduce_method,
) -> np.ndarray:
    signal_times = np.arange(len(signal)) / sample_rate

    times_by_detector = {}
    for detector in indices_by_detector:
        indices = indices_by_detector[detector]
        times_by_detector[detector] = signal_times[indices]

    agreed_points = []

    for peak_time in times_by_detector[root_detector]:
        closest_by_detector = {}

        for detector in times_by_detector:
            times = times_by_detector[detector]
            closest_by_detector[detector] = times[np.argmin(np.abs(times - peak_time))]

        sorted_times = np.sort(list(closest_by_detector.values()))
        mask = np.abs((sorted_times - peak_time)) < agreement_time_threshold
        num_disagreers = np.sum(~mask)
        if num_disagreers <= max_disagreers:
            agreeing_times = sorted_times[mask]

            if agree_reduce_method == Agree_reduce_method.MAX:
                min_time = np.min(agreeing_times)
                max_time = np.max(agreeing_times)

                # find time of max peak in range

                range_mask = (signal_times >= min_time) & (signal_times <= max_time)
                time_range = signal_times[range_mask]
                signal_range = signal[range_mask]

                max_peak_time = time_range[np.argmax(signal_range)]

                agreed_points.append(max_peak_time)
            elif agree_reduce_method == Agree_reduce_method.MEDIAN:
                agreeing_times = sorted_times[mask]
                median = np.median(agreeing_times)
                agreed_points.append(median)
            else:
                print(agree_reduce_method == Agree_reduce_method.MAX)
                raise NotImplementedError(
                    f"unknown agree_reduce_method {agree_reduce_method}"
                )
    agreed_points = np.array(agreed_points)

    return agreed_points
