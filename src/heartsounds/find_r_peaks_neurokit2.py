import numpy as np
import neurokit2 as nk


def find_r_peaks_neurokit2(downsampled_signal: np.ndarray, fs: int) -> np.ndarray:
    _, results = nk.ecg_peaks(downsampled_signal, sampling_rate=fs)
    rpeaks = results["ECG_R_Peaks"]
    return rpeaks
