import numpy as np


def find_agreed_points_runs(
    max_num_detectors_with_between_point,
    agreement_time_threshold,
    agreed_points,
    points_by_detector,
    sample_rate,
):
    """
    Find any points found by a detector that are greater than
    agreement_threshold from the current and next agreed point.
    If the number of detectors that have at least one point
    like this is greater than some threshold, then we are
    not confident that next point in the agreed points is
    correct. Otherwise, we are sufficiently confident that the
    next point in the agreed points is correct (ie we may have
    missed one), and add the current point to the list of points
    where next point is also agreed.
    """

    points_where_next_is_also_agreed = []

    for i in range(len(agreed_points) - 1):
        point = agreed_points[i]
        next_point = agreed_points[i + 1]

        num_detectors_with_non_agreeing_point = 0

        for detector in points_by_detector:
            points = points_by_detector[detector]
            # times_for_detector = signal_times[points]
            times_for_detector = points / sample_rate

            mask = (times_for_detector > point + agreement_time_threshold) & (
                times_for_detector < next_point - agreement_time_threshold
            )

            if np.any(mask):
                num_detectors_with_non_agreeing_point += 1

        if (
            num_detectors_with_non_agreeing_point
            <= max_num_detectors_with_between_point
        ):
            points_where_next_is_also_agreed.append(point)

    points_where_next_is_also_agreed = np.array(points_where_next_is_also_agreed)

    return points_where_next_is_also_agreed
