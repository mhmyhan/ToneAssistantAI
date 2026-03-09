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

# list of potential effects pedals to be drawn upon for each chain
# (maybe expand later to include more effects)
PEDALS = [
    "compressor",
    "overdrive",
    "distortion",
    "chorus",
    "delay",
    "reverb"
    ]



## FUNCTIONS ##

# Maps pedal names to their respective effects pedals+params
def create_pedal_effect(pedal, params):

    if pedal == "compressor":
        return Compressor(
            threshold_db=params["threshold_db"],
            ratio=params["ratio"]
        )

    if pedal == "overdrive":
        return Distortion(
            drive_db=params["drive"] * 30
        )

    if pedal == "distortion":
        return Distortion(
            drive_db=35
        )

    if pedal == "chorus":
        return Chorus(
            rate_hz=params["rate_hz"],
            depth=params["depth"]
        )

    if pedal == "delay":
        return Delay(
            delay_seconds=params["delay_seconds"],
            feedback=params["feedback"],
            mix=params["mix"]
        )

    if pedal == "reverb":
        return Reverb(
            room_size=params["room_size"]
        )

    return None

# randomly selects pedals in a defined order, returns list[] of strings
# generates randomly ristricted to most likely pedal chains, but with some variability to avoid overfitting
def generate_chain():

    chain = []

    # compressor (optional)
    if rand.random() < 0.4:
        chain.append("compressor")

    # drive stage (very common)
    if rand.random() < 0.8:
        chain.append(rand.choice(["overdrive", "distortion"]))

    # modulation
    if rand.random() < 0.35:
        chain.append("chorus")

    # delay
    if rand.random() < 0.45:
        chain.append("delay")

    # reverb
    if rand.random() < 0.35:
        chain.append("reverb")

    # ensure at least ONE pedal
    if len(chain) == 0:
        chain.append(rand.choice(["compressor", "overdrive", "distortion"]))

    return chain



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