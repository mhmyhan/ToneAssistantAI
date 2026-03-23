import threading
import time
import numpy as np
import random
from src.AI.predict_params import predict_params


class AIEngine:
    def __init__(self, state, pedals):
        self.state = state
        self.pedals = pedals
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def loop(self):
        from src.config.presets import PRESETS

        while self.running:

            if not self.state.get_ai_on():
                time.sleep(0.1)
                continue

            features = self.state.get_features()

            if features is None:
                time.sleep(0.1)
                continue

            rms, centroid, zcr = features

            # Get current mode + preset
            mode = self.state.get_ai_mode()
            preset = PRESETS.get(mode, PRESETS["clean"])

            base_drive = preset["drive"]
            base_delay = preset["delay_mix"]

            # AI prediction
            pred = predict_params(rms, centroid, zcr)
            # pred = [0.5 + random.uniform(-0.1, 0.1), 0.5 + random.uniform(-0.1, 0.1)] ##DEBUG

            # Convert prediction into deviation from center
            ai_drive_offset = np.tanh(pred[0]) * 6
            ai_delay_offset = np.tanh(pred[1]) * 0.1



            # minimise influence of nosy predictions
            if abs(pred[0] - 0.5) < 0.05:
                ai_drive_offset = 0

            if abs(pred[1] - 0.5) < 0.05:
                ai_delay_offset = 0


            # Combine preset + AI
            target_drive = base_drive + ai_drive_offset
            target_delay_mix = base_delay + ai_delay_offset

            # Clamp safely
            target_drive = max(0, min(target_drive, 40))
            target_delay_mix = max(0.05, min(target_delay_mix, 0.8))

            # React to playing dynamics
            target_drive *= (1 + rms * 2.5)
            target_delay_mix *= (1 - rms * 0.7)
            target_drive += random.uniform(-0.3, 0.3)
            target_delay_mix += random.uniform(-0.01, 0.01)

            # smoothing
            prev_drive, prev_delay = self.state.get_ai_params()

            alpha = 0.1 + (rms * 0.2)  # smoothing factor (0 = frozen, 1 = instant)

            # final Clamp
            target_drive = max(3, min(target_drive, 40))
            target_delay_mix = max(0.05, min(target_delay_mix, 0.8))


            print(f"PRED: {pred} | DRIVE: {target_drive:.2f} | DELAY: {target_delay_mix:.2f}")

            target_drive = prev_drive + alpha * (target_drive - prev_drive)
            target_delay_mix = prev_delay + alpha * (target_delay_mix - prev_delay)

            # Apply to pedals
            if "distortion" in self.pedals:
                self.pedals["distortion"].drive_db = target_drive

            if "delay" in self.pedals:
                self.pedals["delay"].mix = target_delay_mix
                self.pedals["delay"].feedback = preset["delay_feedback"]

            # Store for UI
            self.state.set_ai_params(target_drive, target_delay_mix)

            time.sleep(0.1)
