import sounddevice as sd
import numpy as np
import tkinter as tk
from pedalboard import Pedalboard, Compressor, Distortion, Chorus, Delay, Reverb

from src.audio.pedalboard_builder import build_demo_board
from src.audio.audio_engine import create_callback
from src.config.audio_config import SAMPLE_RATE, BLOCK_SIZE, INPUT_DEVICE_ID, OUTPUT_DEVICE_ID, INPUT_CHANNEL


board, pedals = build_demo_board()

stream = None

audio_callback = create_callback(board)


def start_audio():

    global stream

    stream = sd.Stream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        device=(INPUT_DEVICE_ID, OUTPUT_DEVICE_ID),
        channels=(2, 2),
        callback=audio_callback
    )

    stream.start()

def stop_audio():

    global stream

    if stream is not None:
        stream.stop()
        stream.close()

## list structure:
# board[0] = compressor
# board[1] = distortion
# board[2] = chorus
# board[3] = delay
# board[4] = reverb

def set_drive(value):
    pedals["distortion"].drive_db = float(value)

def set_delay(value):
    pedals["delay"].mix = float(value)

def toggle_monitoring():
    global monitoring_enabled
    monitoring_enabled = not monitoring_enabled

def main():
    root = tk.Tk()
    root.title("Tone Assistant LIVE")
    start_button = tk.Button(root, text="Start", command=start_audio)
    start_button.pack()
    stop_button = tk.Button(root, text="Stop", command=stop_audio)
    stop_button.pack()

    drive_slider = tk.Scale(root, from_=0, to=40,
                            label="Distortion Drive (dB)",
                            orient=tk.HORIZONTAL,
                            command=set_drive)

    drive_slider.set(0.3) # default value
    drive_slider.pack()

    delay_slider = tk.Scale(root, from_=0, to=1,
                            resolution=0.01,
                            label="Delay Mix",
                            orient=tk.HORIZONTAL,
                            command=set_delay)

    delay_slider.set(25)
    delay_slider.pack()

    root.mainloop()

if __name__ == "__main__":
    main()