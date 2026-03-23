import sounddevice as sd


class BaseAudioBackend:
    def start(self): pass
    def stop(self): pass

# This class centralises audio stream management, allowing for easy start/stop UI integration
class AudioStream:
    def __init__(self, callback, config, monitor_callback=None, host_api="Windows WASAPI"):
        self.callback = callback
        self.config = config
        self.monitor_callback = monitor_callback
        self.stream = None
        self.host_api = host_api

    def start(self):
        if self.stream is not None:
            return
        
        extra_settings = None
        if "WASAPI" in self.host_api:
            print("Enabling WASAPI Exclusive Mode...")
            extra_settings = sd.WasapiSettings(exclusive=True)

        self.stream = sd.Stream(
            samplerate=self.config["samplerate"],
            blocksize=self.config["blocksize"],
            device=self.config["device"],
            channels=self.config["channels"],
            dtype=self.config["dtype"],
            callback=self.callback,
            extra_settings=extra_settings
        )

        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
