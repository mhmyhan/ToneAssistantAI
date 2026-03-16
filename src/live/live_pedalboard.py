import sounddevice as sd
from pedalboard import Pedalboard, Compressor, Distortion, Chorus, Delay, Reverb
import numpy as np

print("Initialising live...")

print(sd.query_devices())

# both majoritively determine latency and quality of audio (adjust to system requirements)
sample_rate = 44100 # in Hz     (lower = more latency but less CPU usage)
block_size = 256 # in samples   (lower = less latency but more CPU usage)

# example pedalboard setup that can be controlled using ToneAsst Later
demoboard = Pedalboard([
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

    processed = demoboard(audio, sample_rate)

    outdata[:] = processed.T

with sd.Stream(
    samplerate=sample_rate,
    blocksize=block_size,
    channels=1,
    callback=audio_callback):

    print("Live pedalboard is running. Ctrl+C to exit.")

    while True:
        pass
