import os
import json # for sending to cubase midi API later.
import numpy as np
import pandas as pd
from tqdm import tqdm
import librosa

from pedal_generator import generate_chain, generate_parameters, create_pedal_effect
from pedalboard.io import AudioFile
from pedalboard import Pedalboard

DI_FOLDER = "data/di"
OUTPUT_FOLDER = "data/generated/audio"
LABEL_FILE = "data/labels/dataset_labels.csv"

#less samples for testing(5), change to ~100-400 for model training
SAMPLES_PER_RIFF = 500

## FUNC ##
def process_audio(input_file, output_file, effects):

    board = Pedalboard(effects)

    with AudioFile(input_file) as f:
        audio = f.read(f.frames)
        effected = board(audio, f.samplerate)
        sr = f.samplerate

    with AudioFile(output_file, 'w', sr, effected.shape[0]) as o:
        o.write(effected)

    return effected, sr


def extract_features(audio, sr):
    mono = audio[0] if audio.ndim > 1 else audio

    # Core features
    rms = np.sqrt(np.mean(mono**2))
    zcr = np.mean(np.abs(np.diff(np.sign(mono)))) / 2

    # mel-frequency Cepstrum coefficients - only 8 (not used in live model too slow)
    mfccs = librosa.feature.mfcc(y=mono, sr=sr, n_mfcc=8)
    mfccs_mean = np.mean(mfccs, axis=1)

    # Spectral contrast (band-wise)
    contrast = librosa.feature.spectral_contrast(y=mono, sr=sr)
    contrast_mean = np.mean(contrast, axis=1)

    # Centroid calculation
    spectrum = np.abs(np.fft.rfft(mono))
    freqs = np.fft.rfftfreq(len(mono), d=1/sr)
    centroid = np.sum(freqs * spectrum) / (np.sum(spectrum) + 1e-6)

    feature_dict = {
        "rms": rms,
        "zcr": zcr,
        "centroid": centroid
    }

    # Add MFCCs
    for i, m in enumerate(mfccs_mean):
        feature_dict[f"mfcc_{i}"] = m

    # Add contrast bands
    for i, c in enumerate(contrast_mean):
        feature_dict[f"contrast_{i}"] = c

    return feature_dict


## MAIN ##
def main():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    labels = []

    di_files = os.listdir(DI_FOLDER)

    sample_id = 0

    # Iterate through di files in DI_FOLDER, genereate chains*SAMPLES_PER_RIFF
    for di_file in di_files:

        input_path = os.path.join(DI_FOLDER, di_file)

        for i in tqdm(range(SAMPLES_PER_RIFF), desc=di_file):

            chain = generate_chain()

            effects = []

            pedal_names = []

            param_record = {}

            for pedal in chain:
                params = generate_parameters(pedal)
                effect = create_pedal_effect(pedal, params)

                if effect:
                    effects.append(effect)
                    pedal_names.append(pedal)

                    # store parameters
                    for k, v in params.items():
                        param_record[f"{pedal}_{k}"] = v
                        param_record[f"{pedal}_active"] = 1


            # naming logic for generated files based on di file name and pedals used
            di_name = os.path.splitext(di_file)[0]

            pedal_tag = "_".join(pedal_names) if pedal_names else "clean"

            output_name = f"{di_name}_{pedal_tag}_{sample_id}.wav"


            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            effected, sr = process_audio(input_path, output_path, effects)

            features = extract_features(effected, sr)

            labels.append({
                "file": output_name,
                "source_di": di_file,
                **features,
                **param_record
            })


            print(f"Generated {output_name} with pedals: {', '.join(pedal_names)}")
            sample_id += 1

    df = pd.DataFrame(labels)

    df = pd.DataFrame(labels)
    df = df.fillna(0)  # or -1 for "not present" signal

    df.to_csv(LABEL_FILE, index=False)


if __name__ == "__main__":
    main()
