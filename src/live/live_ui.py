import sounddevice as sd
import numpy as np
import tkinter as tk

from src.audio.pedalboard_builder import build_demo_board
from src.audio.audio_engine import create_callback
from src.config.audio_config import (
    SAMPLE_RATE,
    BLOCK_SIZE,
    INPUT_DEVICE_ID,
    OUTPUT_DEVICE_ID
)


# Build board + pedal references
board, pedals = build_demo_board()

stream = None

# Shared state
audio_level = 0
monitoring_enabled = True


# Audio Level Callback
def update_level(level):
    global audio_level
    audio_level = level


# Create audio callback with level tracking
audio_callback = create_callback(board, update_level)


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
        stream = None


# Pedal controls
def set_drive(value):
    pedals["distortion"].drive_db = float(value)


def set_delay_mix(value):
    pedals["delay"].mix = float(value)


# Monitoring toggle
def toggle_monitoring():
    global monitoring_enabled
    monitoring_enabled = not monitoring_enabled


## UI ##
def main():
    root = tk.Tk()
    root.title("Tone Assistant LIVE")

    tk.Label(root, text="Tone Assistant", font=("Arial", 16)).pack()

    tk.Button(root, text="Start", command=start_audio).pack()
    tk.Button(root, text="Stop", command=stop_audio).pack()

    tk.Button(root, text="Toggle Monitoring", command=toggle_monitoring).pack()

    # Distortion
    drive_slider = tk.Scale(
        root,
        from_=0,
        to=40,
        label="Distortion Drive (dB)",
        orient=tk.HORIZONTAL,
        command=set_drive
    )
    drive_slider.set(25)
    drive_slider.pack()

    # Delay
    delay_slider = tk.Scale(
        root,
        from_=0,
        to=1,
        resolution=0.01,
        label="Delay Mix",
        orient=tk.HORIZONTAL,
        command=set_delay_mix
    )
    delay_slider.set(0.3)
    delay_slider.pack()

    # VU Meter
    tk.Label(root, text="Input Level").pack()

    vu = tk.Canvas(root, width=200, height=20, bg="black")
    vu.pack()

    def update_vu():
        vu.delete("all")

        level_scaled = min(audio_level * 50, 1.0)
        width = int(level_scaled * 200)

        color = "green" if audio_level < 0.9 else "red"

        vu.create_rectangle(0, 0, width, 20, fill=color)

        root.after(50, update_vu)

    update_vu()

    root.mainloop()


if __name__ == "__main__":
    main()
