import numpy as np
from src.config.audio_config import SAMPLE_RATE, INPUT_CHANNEL


# Callback function that processes audio through pedalboard in realtime

monitoring_enabled = True # global flag to enable/disable audio monitoring

######
## DO NOT PUT AI PROCESSING INSIDE CALLBACK - It'll cause crashes and audio dropouts. 
## use shared state to communicate between callback and AI processing loop
######
def create_callback(board, level_callback=None, monitor_callback=None):

    def audio_callback(indata, outdata, frames, time, status):

        if status:
            print(status)

        # Use INPUT_CHANNEL from config (0 for Left/Input 1, 1 for Right/Input 2)
        # .copy() should eliminate any buffer issues
        channel = indata[:, INPUT_CHANNEL].copy() # high-z input on UA-25EX is input 2 (right) which is index 1, but this can be changed in config

        # Calculate RMS level for VU monitoring
        level = np.sqrt(np.mean(channel**2))

        if level_callback:
            level_callback(level)

        # pedalboard expects (num_channels, num_samples)
        audio = channel.reshape(1, -1)
        processed = board(audio, SAMPLE_RATE)

        # processed audio is float32 and reshaped for stereo output
        # outdata shape is (samples, 2)
        # mp .stack should be more efficient than np.repeat
        out = np.column_stack((processed[0], processed[0]))

        if monitor_callback and not monitor_callback():
            out *= 0

        outdata[:] = out

    return audio_callback
