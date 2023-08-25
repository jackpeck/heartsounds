import json
import datetime

from .find_heart_sound_locations import find_s1s, find_s2s
from .intervals import find_good_intervals, align_intervals


def save_annotations_to_file(
    annotations_folder_path,
    base_filename,
    timings_for_intervals,
    include_timestamp=False,
):
    data = json.dumps(timings_for_intervals, indent=4)

    extension = ".json"
    annotations_file_path = f"{annotations_folder_path}/{base_filename}"

    if include_timestamp:
        time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        annotations_file_path += f"_annotation_produced_{time_str}"

    annotations_file_path += extension

    with open(annotations_file_path, "w") as f:
        f.write(data)


def soundIsInPeriod(sound_times, period):
    return period[0] <= sound_times[0] and sound_times[1] <= period[1]


def get_heart_sound_timings_by_intervals(ecg_peaks, audio_timing_offset=0):
    s1s = find_s1s(ecg_peaks.rpeaks_where_next_is_also_agreed) + audio_timing_offset
    s2s = find_s2s(ecg_peaks.t_peak_ends) + audio_timing_offset

    intervals_unaligned = find_good_intervals(ecg_peaks)

    intervals = align_intervals(intervals_unaligned, audio_timing_offset)

    timings_for_intervals = []

    for interval in intervals:
        start_time = interval["intervalStart"]
        end_time = interval["intervalEnd"]

        period = [start_time, end_time]
        s1s_for_interval = [s1.tolist() for s1 in s1s if soundIsInPeriod(s1, period)]
        s2s_for_interval = [s2.tolist() for s2 in s2s if soundIsInPeriod(s2, period)]

        timings_for_interval = {
            "intervalStart": start_time,
            "intervalEnd": end_time,
            "s1Timings": s1s_for_interval,
            "s2Timings": s2s_for_interval,
        }

        timings_for_intervals.append(timings_for_interval)

    return timings_for_intervals
