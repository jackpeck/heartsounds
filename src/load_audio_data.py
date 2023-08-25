import librosa


def load_audio_data(audio_filepath):
    audio, audio_sample_rate = librosa.load(audio_filepath, sr=None)
    return audio, audio_sample_rate
