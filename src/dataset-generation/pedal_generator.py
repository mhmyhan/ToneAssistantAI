import random as rand

from pedalboard import (
    Pedalboard,
    Compressor,
    Distortion,
    Chorus,
    Delay,
    Reverb
)
from pedalboard.io import AudioFile

# list of potential effects pedals to be drawn upon for dataset generation
PEDALS = [
    "Compression",
    "Overdrive",
    "Distortion",
    "Chorus",
    "Delay",
    "Reverb"
    ]



## FUNCTIONS ##


def process_audio(input_file, output_file, chain):

    effects = [e for e in chain if e is not None]

    board = Pedalboard(effects)


    with AudioFile(input_file) as f:

        audio = f.read(f.frames)
        effected = board(audio, f.samplerate)
        
        with AudioFile(output_file, 'w', f.samplerate, effected.shape[0]) as o:
            o.write(effected)

# Maps pedal names to their respective effects pedals+params
def create_pedal_effect(pedal, params):

    if pedal == "compressor":
        return Compressor(**params)

    # overdrive is just distortion with a lower drive setting
    if pedal == "overdrive": 
        return Distortion(**params)

    # we'll define distiortion as drive above a minimum threshold
    if pedal == "distortion":
        return Distortion(drive=0.9)

    if pedal == "chorus":
        return Chorus(**params)

    if pedal == "delay":
        return Delay(**params)

    if pedal == "reverb":
        return Reverb(**params)

    return None

# randomly selects a maximum of 3 pedals in any order, returns list[] of strings
def generate_chain(max_length=3):

    length = rand.randint(0, max_length)
    return rand.sample(PEDALS, length)


# generates random parameters relative to each pedal type, returns dict{} of parameter names and values
def generate_parameters(pedal):

    if pedal == "compressor":

        return {
            "threshold_db": rand.uniform(-30, -10),
            "ratio": rand.uniform(2, 6)
        }

    if pedal == "overdrive":

        return {
            "drive": rand.uniform(0.2, 0.8),
            "tone": rand.uniform(0.3, 0.7)
        }

    if pedal == "chorus":

        return {
            "rate_hz": rand.uniform(0.5, 3),
            "depth": rand.uniform(0.2, 0.8)
        }

    if pedal == "delay":

        return {
            "delay_seconds": rand.uniform(0.2, 0.6),
            "feedback": rand.uniform(0.2, 0.6),
            "mix": rand.uniform(0.2, 0.5)
        }

    if pedal == "reverb":

        return {
            "room_size": rand.uniform(0.2, 0.8)
        }

    return {}