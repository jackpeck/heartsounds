def find_good_intervals(ecg_peaks):
    peak_in_interval = []
    peak_in_intervals = []

    for i in range(len(ecg_peaks.r_peaks)):
        peak = ecg_peaks.r_peaks[i]
        prevPeak = None if i == 0 else ecg_peaks.r_peaks[i - 1]

        good = peak in ecg_peaks.rpeaks_where_next_is_also_agreed

        if good and prevPeak is not None:
            # check there exists a t peak end between prevPeak and peak
            mask = (ecg_peaks.t_peak_ends > prevPeak) & (ecg_peaks.t_peak_ends < peak)
            n = mask.sum()
            good = n == 1

        if good:
            peak_in_interval.append(peak)
        else:
            peak_in_interval.append(peak)
            if len(peak_in_interval) > 1:
                peak_in_intervals.append(peak_in_interval)
            peak_in_interval = []

    # don't need to push last interval, as last peak in r_peaks
    # is always not in rpeaks_where_next_is_also_agreed, so good is
    # always False, so interval is always empty as this point

    return [
        {
            "intervalStart": peak_in_interval[0],
            "intervalEnd": peak_in_interval[-1],
        }
        for peak_in_interval in peak_in_intervals
    ]


def align_intervals(unaligned_intervals, timing_offset):
    return [
        {
            "intervalStart": interval["intervalStart"] + timing_offset,
            "intervalEnd": interval["intervalEnd"] + timing_offset,
        }
        for interval in unaligned_intervals
    ]
