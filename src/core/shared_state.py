import threading

class SharedState:
    def __init__(self):
        self.lock = threading.Lock()

        self.level = 0.0 # for vu meter
        self.monitoring_enabled = True # toggle monitoring
        self.ai_mode = False # toggle ai takeover
        self.suggested_drive = 25.0
        self.suggested_delay = 0.3

    def set_level(self, value):
        with self.lock:
            self.level = value

    def get_level(self):
        with self.lock:
            return self.level
        
    def set_ai_mode(self, value):
        with self.lock:
            self.ai_mode = value

    def get_ai_mode(self):
        with self.lock:
            return self.ai_mode
        
    def set_ai_params(self, drive, delay):
        with self.lock:
            self.suggested_drive = drive
            self.suggested_delay = delay

    def get_ai_params(self):
        with self.lock:
            return self.suggested_drive, self.suggested_delay
        
    def set_monitoring(self, status):
        with self.lock:
            self.monitoring_enabled = status

    def get_monitoring(self):
        with self.lock:
            return self.monitoring_enabled