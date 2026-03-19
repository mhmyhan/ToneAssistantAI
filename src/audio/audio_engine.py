import numpy as np
from src.config.audio_config import SAMPLE_RATE, INPUT_CHANNEL


# Callback function that processes audio through pedalboard in realtime

monitoring_enabled = True # global flag to enable/disable audio monitoring

def create_callback(board, level_callback=None):

    def audio_callback(indata, outdata, frames, time, status):

        if status:
            print(status)

        channel = indata[:, 1]

        level = float((channel**2).mean() ** 0.5)

        if level_callback:
            level_callback(level)

        audio = channel.reshape(1, -1)

        processed = board(audio, SAMPLE_RATE)

        out = np.repeat(processed.T, 2, axis=1)

        # Monitoring control
        from src.live.live_ui import monitoring_enabled
        if not monitoring_enabled:
            out *= 0

        outdata[:] = out

    return audio_callback
