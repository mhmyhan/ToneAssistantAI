
# audio system configuration

#sd.default.hostapi = () # set to ASIO for best performance on Windows
# check notebooks for quick run

# dynamically find device id based on name
# set to your audio interface name (in my case "UA-25EX" in and out)
def find_input_device(device_name):
    import sounddevice as sd
    devices = sd.query_devices()
    
    for i, device in enumerate(devices):
        hostapi_name = sd.query_hostapis(device['hostapi'])['name']
        if device_name in device['name'] and "ASIO" in hostapi_name and device['max_input_channels'] > 0:
            return i

    # in case of failure, print available devices to terminal for debugging
    print("\n--- Available Devices ---")
    print(sd.query_devices())
    raise ValueError(f"Device '{device_name}' not found. See list above.")


def find_output_device(device_name):
    import sounddevice as sd

    for i, device in enumerate(sd.query_devices()):
        hostapi_name = sd.query_hostapis(device['hostapi'])['name']
        if device_name in device['name'] and "ASIO" in hostapi_name and device['max_output_channels'] > 0:
            return i

    raise ValueError("Output device not found")


def find_best_device(device_name, is_input=True):
    import sounddevice as sd
    devices = sd.query_devices()
    api_preference = ["ASIO", "Windows WASAPI", "Windows WDM-KS", "MME"]
    
    found_devices = []
    for i, dev in enumerate(devices):
        if device_name.upper() in dev['name'].upper():
            channels = dev['max_input_channels'] if is_input else dev['max_output_channels']
            if channels > 0:
                host_api = sd.query_hostapis(dev['hostapi'])['name']
                found_devices.append({"id": i, "api": host_api})

    if not found_devices:
        raise ValueError(f"Device '{device_name}' not found.")

    found_devices.sort(key=lambda x: api_preference.index(x['api']) if x['api'] in api_preference else 99)
    
    # Return BOTH the ID and the API Name
    return found_devices[0]['id'], found_devices[0]['api']

# Update these lines at the bottom of audio_config.py:
input_id, input_api = find_best_device("UA-25EX", is_input=True)
output_id, _ = find_best_device("UA-25EX", is_input=False)

INPUT_DEVICE_ID = input_id
OUTPUT_DEVICE_ID = output_id
HOST_API_NAME = input_api

## VARIABLES ##

# these largely determine latency and quality of audio (adjust to system requirements)

# sample-rate in Hz    (lower = more latency but less CPU usage)
# blocksize in samples (lower = less latency but more CPU usage)

# prefab configs for easier switching 
AUDIO_CONFIGS = {
    # higher latency more stable
    "safe_mode": {
        "samplerate": 44100,
        "blocksize": 124,
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

input_id, input_api = find_best_device("UA-25EX", is_input=True)    # UA-25EX input
output_id, output_api = find_best_device("UA-25EX", is_input=False) # UA-25EX output

# change to your audio input and output device (see testing.ipynb)
INPUT_DEVICE_ID = input_id  # UA-25EX input
OUTPUT_DEVICE_ID = output_id  
HOST_API_NAME = input_api

INPUT_CHANNEL = 1 # input 2 (right HighZ channel)


