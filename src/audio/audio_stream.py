import sounddevice as sd

# This class centralises audio stream management, allowing for easy start/stop UI integration
class AudioStream:
    def __init__(self, callback, config):
        self.callback = callback
        self.config = config
        self.stream = None

    def start(self):
        if self.stream is not None:
            return

        self.stream = sd.Stream(
            samplerate=self.config["samplerate"],
            blocksize=self.config["blocksize"],
            device=self.config["device"],
            channels=self.config["channels"],
            dtype=self.config["dtype"],
            callback=self.callback
        )

        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
