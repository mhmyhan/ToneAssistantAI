# audio system configuration

# these largely determine latency and quality of audio (adjust to system requirements)
SAMPLE_RATE = 44100 # in Hz      (lower = more latency but less CPU usage)
BLOCK_SIZE = 512    # in samples (lower = less latency but more CPU usage)

def find_device_id(device_name):
    import sounddevice as sd
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device_name in device['name']:
            return i
    raise ValueError(f"Device '{device_name}' not found")


# change to your audio input and output device (see testing.ipynb)
INPUT_DEVICE_ID = find_device_id("UA-25EX")     # UA-25EX input
OUTPUT_DEVICE_ID = find_device_id("UA-25EX")   # UA-25EX output

INPUT_CHANNEL = 1 # input 2 (right)

