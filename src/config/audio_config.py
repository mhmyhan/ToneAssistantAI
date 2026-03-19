# audio system configuration

import sounddevice as sd
sd.default.hostapi = 3 # WDM-KS (check this is correct on different systems using sd.query_hostapis())
# check notebooks for quick run

# these largely determine latency and quality of audio (adjust to system requirements)
SAMPLE_RATE = 44100 # in Hz      (lower = more latency but less CPU usage)
BLOCK_SIZE = 512    # in samples (lower = less latency but more CPU usage)

# dynamically find device id based on name
# set to your audio interface name (in my case "UA-25EX" in and out)
def find_input_device(device_name):
    import sounddevice as sd
    for i, device in enumerate(sd.query_devices()):
        if device_name in device['name'] and device['max_input_channels'] > 0:
            return i
    raise ValueError("Input device not found")


def find_output_device(device_name):
    import sounddevice as sd
    for i, device in enumerate(sd.query_devices()):
        if device_name in device['name'] and device['max_output_channels'] > 0:
            return i
    raise ValueError("Output device not found")



# change to your audio input and output device (see testing.ipynb)
INPUT_DEVICE_ID = find_input_device("UA-25EX")     # UA-25EX input
OUTPUT_DEVICE_ID = find_output_device("UA-25EX")   # UA-25EX output

INPUT_CHANNEL = 1 # input 2 (right)


