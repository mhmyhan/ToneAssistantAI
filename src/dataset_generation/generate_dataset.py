import os
import json # for sending to cubase midi API later.
import pandas as pd
from tqdm import tqdm

from pedal_generator import generate_chain, generate_parameters, create_pedal_effect
from pedalboard.io import AudioFile
from pedalboard import Pedalboard

DI_FOLDER = "data/di"
OUTPUT_FOLDER = "data/generated/audio"
LABEL_FILE = "data/labels/dataset_labels.csv"

#less samples for testing(5), change to ~100-400 for model training
SAMPLES_PER_RIFF = 5

## FUNC ##
def process_audio(input_file, output_file, effects):

    board = Pedalboard(effects)

    with AudioFile(input_file) as f:

        audio = f.read(f.frames)

        effected = board(audio, f.samplerate)

    with AudioFile(output_file, 'w', f.samplerate, effected.shape[0]) as o:
        o.write(effected)

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

            for pedal in chain:

                params = generate_parameters(pedal)

                effect = create_pedal_effect(pedal, params)

                if effect:
                    effects.append(effect)
                    pedal_names.append(pedal)

            # naming logic for generated files based on di file name and pedals used
            di_name = os.path.splitext(di_file)[0]

            pedal_tag = "_".join(pedal_names) if pedal_names else "clean"

            output_name = f"{di_name}_{pedal_tag}_{sample_id}.wav"


            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            process_audio(input_path, output_path, effects)

            labels.append({
                "file": output_name,
                "source_di": di_file,
                "pedals": ",".join(pedal_names)
            })

            print(f"Generated {output_name} with pedals: {', '.join(pedal_names)}")
            sample_id += 1

    df = pd.DataFrame(labels)

    df.to_csv(LABEL_FILE, index=False)


if __name__ == "__main__":
    main()
