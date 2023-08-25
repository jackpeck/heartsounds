import numpy as np
import pandas as pd


def load_ecg_data(ecg_csv_filepath):
    df = pd.read_csv(ecg_csv_filepath)
    ecg = df["data"].to_numpy()

    # need to convert to datetime, 18/05/2023 16:51:24.523
    ecg_timestamps_datetime = pd.to_datetime(df["time"], format="%d/%m/%Y %H:%M:%S.%f")

    ecg_timestamps_gradient = np.gradient(ecg_timestamps_datetime)

    # check if gradient is constant, and if so use that as the sampling rate to avoid having to deal with the timestamps
    ecg_timestamps_gradient = ecg_timestamps_gradient.astype("float64")
    first_interval = ecg_timestamps_gradient[0]

    if not np.allclose(ecg_timestamps_gradient, first_interval):
        print("warning: timestamps are not evenly spaced")
        raise Exception(
            "Error: detecting ecg sample rate failed, timestamps are not evenly spaced"
        )

    nanoseconds_per_second = 1e9
    ecg_sample_rate = 1 / first_interval * nanoseconds_per_second

    return ecg, ecg_sample_rate
