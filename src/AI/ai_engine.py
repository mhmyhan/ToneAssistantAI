import time

class AIEngine:
    def __init__(self, state, pedals):
        self.state = state
        self.pedals = pedals
        self.running = False

    def start(self):
        import threading
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            level = self.state.get_level()

            # rule based ai logic for now, implement model later
            if level > 0.05:
                drive = min(40, 20 + level * 50)
                delay = min(1.0, 0.2 + level * 0.5)
            else:
                drive = 10
                delay = 0.1

            # update shared state
            self.state.set_ai_params(drive, delay)

            # directly control pedals fr debugging
            if self.state.get_ai_mode():
                self.pedals["distortion"].drive_db = drive
                self.pedals["delay"].mix = delay

            time.sleep(0.1)  # 10Hz update rate provide room for 