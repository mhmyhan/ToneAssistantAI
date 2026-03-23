## Librosa version

import librosa
import numpy as np

# DONT RUN LIBROSA FUNCTIONS IN AUDIO CALLBACK 
# it's slow and will cause skipping on the online feed
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


def extract_features(audio, sr):
    mono = audio[0] if audio.ndim > 1 else audio

    # Core features
    rms = np.sqrt(np.mean(mono**2))
    zcr = np.mean(np.abs(np.diff(np.sign(mono)))) / 2

    # MFCCs
    mfccs = librosa.feature.mfcc(y=mono, sr=sr, n_mfcc=8)
    mfccs_mean = np.mean(mfccs, axis=1)

    # Spectral contrast
    contrast = librosa.feature.spectral_contrast(y=mono, sr=sr)
    contrast_mean = np.mean(contrast, axis=1)

    feature_dict = {
        "rms": rms,
        "zcr": zcr,
    }

    for i, m in enumerate(mfccs_mean):
        feature_dict[f"mfcc_{i}"] = m

    for i, c in enumerate(contrast_mean):
        feature_dict[f"contrast_{i}"] = c

    return feature_dict
