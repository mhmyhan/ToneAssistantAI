# audio system configuration

import sounddevice as sd
#sd.default.hostapi = 3 # WDM-KS (check this is correct on different systems using sd.query_hostapis())
# check notebooks for quick run

# dynamically find device id based on name
# set to your audio interface name (in my case "UA-25EX" in and out)
def find_input_device(device_name):
    import sounddevice as sd
    devices = sd.query_devices()
    
    for i, device in enumerate(devices):
        # We check if the name matches and it actually has inputs
        if device_name in device['name'] and device['max_input_channels'] > 0:
            return i

    # in case of failure, print available devices to terminal for debugging
    print("\n--- Available Devices ---")
    print(sd.query_devices())
    raise ValueError(f"Device '{device_name}' not found. See list above.")


def find_output_device(device_name):
    import sounddevice as sd

    for i, device in enumerate(sd.query_devices()):
        hostapi = sd.query_hostapis(device['hostapi'])['name']

        if (
            device_name in device['name'] and device['max_output_channels'] > 0
        ):
            return i

    raise ValueError("Output device not found")

## VARIABLES ##

# these largely determine latency and quality of audio (adjust to system requirements)

# sample-rate in Hz    (lower = more latency but less CPU usage)
# blocksize in samples (lower = less latency but more CPU usage)

# prefab configs for easier switching 
AUDIO_CONFIGS = {
    "safe_mode": {
        "samplerate": 44100,
        "blocksize": 512,
        "channels": (2, 2),
        "dtype": "float32"
    },
    "standard": {
        "samplerate": 44100,
        "blocksize": 512,
        "channels": (2, 2),
        "dtype": "float32"
    },
    "low_latency": {
        "samplerate": 48000,
        "blocksize": 128,
        "channels": (2, 2),
        "dtype": "float32"
    }
}


SAMPLE_RATE = AUDIO_CONFIGS["safe_mode"]["samplerate"]
BLOCK_SIZE = AUDIO_CONFIGS["safe_mode"]["blocksize"]

# change to your audio input and output device (see testing.ipynb)
INPUT_DEVICE_ID = find_input_device("UA-25EX")     # UA-25EX input
OUTPUT_DEVICE_ID = find_output_device("UA-25EX")   # UA-25EX output

INPUT_CHANNEL = 1 # input 2 (right HighZ channel)


