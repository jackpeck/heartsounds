import librosa
import numpy as np

def load_audio_data (audio_filepath):
    audio, audio_sample_rate = librosa.load(audio_filepath, sr=None)
    audio_timestamps = np.array([i / audio_sample_rate for i in range(len(audio))])
    return audio, audio_timestamps, audio_sample_rate