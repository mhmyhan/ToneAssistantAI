import threading

class SharedState:
    def __init__(self):
        self.lock = threading.Lock()

        self.level = 0.0 # for vu meter
        self.monitoring_enabled = True # toggle monitoring
        self.ai_on = False # toggle ai takeover
        self.ai_mode = "auto" # auto, clean, rock, lead
        self.suggested_drive = 25.0
        self.suggested_delay = 0.3
        self.features = (0, 0, 0)
        

    def set_level(self, value):
        with self.lock:
            self.level = value

    def get_level(self):
        with self.lock:
            return self.level
        

    def set_ai_on(self, value):
        with self.lock:
            self.ai_on = value

    def get_ai_on(self):
        with self.lock:
            return self.ai_on
        
    def set_ai_mode(self, mode):
        with self.lock:
            self.ai_mode = mode

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
        

    def set_features(self, rms, centroid, zcr):
        with self.lock:
            self.features = (rms, centroid, zcr)

    def get_features(self):
        with self.lock:
            return self.features