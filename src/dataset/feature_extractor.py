## Librosa version for future deeplearning algorithm

import librosa
import numpy as np

def extract_mel_spectrogram(file_path):

    y, sr = librosa.load(file_path, sr=44100)

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=128,
        hop_length=512
    )

    mel_db = librosa.power_to_db(mel)

    return mel_db
