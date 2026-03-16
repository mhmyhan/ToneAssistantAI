import sounddevice as sd
from pedalboard import Pedalboard, Compressor, Distortion, Chorus, Delay, Reverb
import numpy as np

sample_rate = 44100
block_size = 512

# example pedalboard setup that can be controlled using ToneAsst Later
board = Pedalboard([
    Compressor(threshold_db=-20, ratio=3),
    Distortion(drive_db=25),
    Chorus(rate_hz=1.5, depth=0.4),
    Delay(delay_seconds=0.35, feedback=0.4, mix=0.3),
    Reverb(room_size=0.5)
])


def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    # Process the audio through the pedalboard
    audio = indata.T

    processed = board(audio, sample_rate)

    outdata[:] = processed.T

with sd.Stream(
    samplerate=sample_rate,
    blocksize=block_size,
    channels=1,
    callback=audio_callback):

    print("Live pedalboard is running. Ctrl+C to exit.")

    while True:
        pass
