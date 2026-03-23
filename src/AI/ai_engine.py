import time

class AIEngine:
    def __init__(self, state, pedals):
        self.state = state
        self.pedals = pedals
        self.running = False
        
        # Smoothing State
        self.current_drive = 25.0
        self.current_delay = 0.3
        self.smoothing = 0.15  # alpha for smoothness (0.0 - 1.0) lower is slower

    def start(self):
        import threading
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.running = False


    ## Currently working with algorithmic ai, Model implementation to come
    def run(self):
        while self.running:
            rms, centroid, zcr = self.state.get_features()
            mode = self.state.get_ai_mode()

            # BASE MODEL (replace with ml)
            drive = min(40, 10 + rms * 60)
            delay = min(1.0, 0.1 + rms * 0.6)

            # AI Modes
            if mode == "clean":
                drive *= 0.5
                delay *= 0.3

            elif mode == "rock":
                drive *= 1.2
                delay *= 0.5

            elif mode == "lead":
                drive *= 1.5
                delay *= 1.2

            elif mode == "auto":
                # use spectral info
                if centroid > 2000:  # bright signal
                    drive *= 1.3
                if zcr > 0.1:
                    delay *= 0.7

            # clamp values
            drive = max(0, min(40, drive))
            delay = max(0, min(1.0, delay))

            # smoothing
            self.current_drive += (drive - self.current_drive) * self.smoothing
            self.current_delay += (delay - self.current_delay) * self.smoothing

            # update state
            self.state.set_ai_params(self.current_drive, self.current_delay)

            # apply if enabled
            if self.state.get_ai_on() and self.state.get_ai_mode() != "manual":
                self.pedals["distortion"].drive_db = self.current_drive
                self.pedals["delay"].mix = self.current_delay

            time.sleep(0.05)