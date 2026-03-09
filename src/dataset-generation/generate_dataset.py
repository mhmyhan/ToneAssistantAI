import os
import json
import pandas as pd
from tqdm import tqdm

from pedal_generator import generate_chain, generate_parameters, create_pedal_effect
from pedalboard.io import AudioFile
from pedalboard import Pedalboard

DI_FOLDER = "data/audio-raw"
OUTPUT_FOLDER = "data/audio-generated"
LABEL_FILE = "data/labels/dataset_labels.csv"

SAMPLES_PER_RIFF = 100



def main():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    labels = []

    di_files = os.listdir(DI_FOLDER)

    sample_id = 0

    for di_file in di_files:

        input_path = os.path.join(DI_FOLDER, di_file)

        for i in tqdm(range(SAMPLES_PER_RIFF)):

            chain = generate_chain()

            effects = []

            pedal_names = []

            for pedal in chain:

                params = generate_parameters(pedal)

                effect = create_pedal_effect(pedal, params)

                if effect:
                    effects.append(effect)
                    pedal_names.append(pedal)

            output_name = f"sample_{sample_id}.wav"

            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            process_audio(input_path, output_path, effects)

            labels.append({
                "file": output_name,
                "pedals": ",".join(pedal_names)
            })

            sample_id += 1

    df = pd.DataFrame(labels)

    df.to_csv(LABEL_FILE, index=False)


if __name__ == "__main__":
    main()

def process_audio(input_file, output_file, effects):

    board = Pedalboard(effects)

    with AudioFile(input_file) as f:

        audio = f.read(f.frames)
        effected = board(audio, f.samplerate)

        with AudioFile(output_file, 'w', f.samplerate, effected.shape[0]) as o:
            o.write(effected)
