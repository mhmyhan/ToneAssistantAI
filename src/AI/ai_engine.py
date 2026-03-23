import time

class AIEngine:
    def __init__(self, state, pedals):
        self.state = state
        self.pedals = pedals
        self.running = False
        
        # --- Smoothing State ---
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
            level = self.state.get_level()

            # Calculate the target pedalstate
            if level > 0.05:
                target_drive = min(40, 20 + level * 50)
                target_delay = min(1.0, 0.2 + level * 0.5)
            else:
                target_drive = 10
                target_delay = 0.1

            # Apply Smoothing
            # New Value = Current + (Target - Current) * Alpha
            self.current_drive += (target_drive - self.current_drive) * self.smoothing
            self.current_delay += (target_delay - self.current_delay) * self.smoothing

            # Update Shared State (for UI)
            self.state.set_ai_params(self.current_drive, self.current_delay)

            # Apply to Pedals if AI mode is enabled
            if self.state.get_ai_mode():
                self.pedals["distortion"].drive_db = self.current_drive
                self.pedals["delay"].mix = self.current_delay

            # Run at 20Hz (0.05s) for smooth transitions
            time.sleep(0.05)