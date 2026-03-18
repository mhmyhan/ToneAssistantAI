import sounddevice as sd
import numpy as np

from src.audio.audio_engine import create_callback
from src.audio.pedalboard_builder import build_demo_board
from src.config.audio_config import SAMPLE_RATE, BLOCK_SIZE, INPUT_DEVICE_ID, OUTPUT_DEVICE_ID, INPUT_CHANNEL


print("Initialising live...")

# create callback function for processing audio from template in audio_engine.py
audio_callback = create_callback(build_demo_board())

with sd.Stream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    channels=(2, 2), # 2 input & 2 output channels
    callback=audio_callback,
    device=(INPUT_DEVICE_ID, OUTPUT_DEVICE_ID)):

    print("Live pedalboard is running. Ctrl+C to exit.")

    while True:
        pass
