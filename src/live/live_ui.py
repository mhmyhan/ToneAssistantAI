import sounddevice as sd
import numpy as np
import tkinter as tk

from src.audio.pedalboard_builder import build_demo_board
from src.audio.audio_engine import create_callback
from src.audio.audio_stream import AudioStream
from src.config.audio_config import (AUDIO_CONFIGS, INPUT_DEVICE_ID, OUTPUT_DEVICE_ID)
from src.core.shared_state import SharedState
from src.AI.ai_engine import AIEngine


# Audio Level Callback for live vu meter
def update_level(level):
    state.audio_level = level

def get_monitoring():
    return state.get_monitoring()


# start and stop button functions
def start_audio():
    audio_stream.start()
    ai_engine.start()

def stop_audio():
    audio_stream.stop()
    ai_engine.stop()



# Pedal controls
def set_drive(value):
    pedals["distortion"].drive_db = float(value)


def set_delay_mix(value):
    pedals["delay"].mix = float(value)


# Monitoring toggle
def toggle_monitoring():
    global monitoring_enabled
    monitoring_enabled = not monitoring_enabled



########
## UI ##
########
state = SharedState()

# Build board + pedal references + Callback algorithm
board, pedals = build_demo_board() # currently hardcoded demo board
ai_engine = AIEngine(state, pedals)

config = AUDIO_CONFIGS["safe_mode"] # low latency config for live performance
config["device"] = (INPUT_DEVICE_ID, OUTPUT_DEVICE_ID)


stream = None


engine_callback = create_callback(board, update_level, get_monitoring)

audio_stream = AudioStream(engine_callback, config)

def main():
    root = tk.Tk()
    root.title("Tone Assistant LIVE")

    tk.Label(root, text="Tone Assistant", font=("Arial", 16)).pack()

    tk.Button(root, text="Start", command=start_audio).pack()
    tk.Button(root, text="Stop", command=stop_audio).pack()

    # audio status label
    status_label = tk.Label(root, text="No Signal")
    status_label.pack()

    # AI modifier status label
    ai_label = tk.Label(root, text="AI: ---")
    ai_label.pack()

    def update_status():
        if state.get_level() > 0.01:
            status_label.config(text="Playing")
        else:
            status_label.config(text="Silence")

        root.after(100, update_status)

    update_status()

    def update_ai_display():
        drive, delay = state.get_ai_params()
        ai_label.config(text=f"AI Drive: {drive:.1f} | Delay: {delay:.2f}")
        root.after(100, update_ai_display)

    # monitoring toggle
    monitor_var = tk.BooleanVar(value=True)

    def update_monitoring():
        global monitoring_enabled
        monitoring_enabled = monitor_var.get()

    monitor_checkbox = tk.Checkbutton(
        root,
        text="Monitoring",
        variable=monitor_var,
        command=update_monitoring
    )

    monitor_checkbox.pack()


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

        level_scaled = min(state.get_level() * 5, 1.0)
        width = int(level_scaled * 200 * 2) # *2 to exagerrate so it moves more

        color = "green" if state.get_level() < 0.9 else "red"

        vu.create_rectangle(0, 0, width, 20, fill=color)

        root.after(50, update_vu)

    update_vu()
 
    root.mainloop()


if __name__ == "__main__":
    main()
