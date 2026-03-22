import threading

class SharedState:
    def __init__(self):
        self.lock = threading.Lock()

        # audio features:
        self.level = 0.0 # for vu meter

        # control flags
        self.monitoring_enabled = True

        # AI outputs
        self.suggested_drive = 25.0
        self.suggested_delay = 0.3

    def set_level(self, value):
        with self.lock:
            self.level = value

    def get_level(self):
        with self.lock:
            return self.level
        
    def set_ai_params(self, drive, delay):
        with self.lock:
            self.suggested_drive = drive
            self.suggested_delay = delay

    def get_ai_params(self):
        with self.lock:
            return self.suggested_drive, self.suggested_delay
        
    def get_monitoring(self):
        with self.lock:
            return self.monitoring_enabled