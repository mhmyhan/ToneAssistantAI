import sounddevice as sd
from pedalboard import Pedalboard, Compressor, Distortion, Chorus, Delay, Reverb
import numpy as np

print("Initialising live...")

# use this command (use testing.ipynb) to find your input and output device IDs
# print(sd.query_devices())

input_id = 1 # change to your audio input device ID (see testing.ipynb)
output_id = 11 # change to your audio output device ID (see testing.ipynb)

# these majoritively determine latency and quality of audio (adjust to system requirements)
sample_rate = 44100 # in Hz     (lower = more latency but less CPU usage)
block_size = 512 # in samples   (lower = less latency but more CPU usage)

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

    right_channel = indata[:, 1] #input 2 (right) us used for processing

    # Process the audio through the pedalboard
    audio = right_channel.reshape(1, -1) # adjust shape to right channel exclusive

    processed = demoboard(audio, sample_rate)

    out = np.repeat(processed.T, 2, axis=1) # duplicate processed signal into stereo

    outdata[:] = out

with sd.Stream(
    samplerate=sample_rate,
    blocksize=block_size,
    channels=(2, 2), # 2 input & 2 output channels
    callback=audio_callback,
    device=(input_id, output_id)):

    print("Live pedalboard is running. Ctrl+C to exit.")

    while True:
        pass
