import numpy as np
from src.config.audio_config import SAMPLE_RATE, INPUT_CHANNEL


# Callback function that processes audio through pedalboard in realtime

monitoring_enabled = True # global flag to enable/disable audio monitoring

def create_callback(board):

    def audio_callback(indata, outdata, frames, time, status):
        if status:
            print(status)

        right_channel = indata[:, INPUT_CHANNEL] #input 2 (right) us used for processing

        # Process the audio through the pedalboard
        audio = right_channel.reshape(1, -1) # adjust shape to right channel exclusive

        processed = board(audio, SAMPLE_RATE)

        out = np.repeat(processed.T, 2, axis=1) # duplicate processed signal into stereo

        if not monitoring_enabled:
            out *= 0 # mute output if monitoring is disabled

        outdata[:] = out

    return audio_callback