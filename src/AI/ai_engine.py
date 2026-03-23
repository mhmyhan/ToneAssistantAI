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
        while self.running:

            # run if AI is enabled
            if not self.state.get_ai_on():
                time.sleep(0.1)
                continue

            # Get latest features from shared state
            features = self.state.get_features()

            if features is None:
                time.sleep(0.1)
                continue

            rms, centroid, zcr = features

            # generate predictions from features
            pred = predict_params(rms, centroid, zcr)
            print(f"RAW PRED: {pred}")

            # clamp values 
            target_drive = np.interp(pred[0], [0, 1], [5, 30])
            target_delay_mix = np.interp(pred[1], [0, 1], [0.1, 0.6])

            target_drive += random.uniform(-0.5, 0.5)
            target_delay_mix += random.uniform(-0.02, 0.02)

            # apply to pedals if AI mode is active
            if self.state.get_ai_on():
                if "distortion" in self.pedals:
                    self.pedals["distortion"].drive_db = target_drive

                if "delay" in self.pedals:
                    self.pedals["delay"].mix = target_delay_mix
                    self.pedals["delay"].feedback = 0.5

                # Update UI display with the actual values being used
                self.state.set_ai_params(target_drive, target_delay_mix)

            time.sleep(0.1)  # 10Hz update rate
