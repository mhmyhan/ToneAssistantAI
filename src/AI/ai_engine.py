import threading
import time
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

            # clamp values 
            drive = max(0, min(pred[23], 1)) # 23rd column is overdrive_drive
            delay_mix = max(0, min(pred[31], 1)) # 31st column in csv is delay_mix

            # apply to pedals
            if "distortion" in self.pedals:
                self.pedals["distortion"].drive_db = drive * 30

            if "delay" in self.pedals:
                self.pedals["delay"].mix = delay_mix

            # Update UI display
            self.state.set_ai_params(drive * 30, delay_mix)

            time.sleep(0.1)  # 10Hz update rate
