# audio system configuration

# these largely determine latency and quality of audio (adjust to system requirements)
SAMPLE_RATE = 44100 # in Hz      (lower = more latency but less CPU usage)
BLOCK_SIZE = 512    # in samples (lower = less latency but more CPU usage)


# change to your audio input and output device (see testing.ipynb)
INPUT_DEVICE_ID = 1     # UA-25EX input
OUTPUT_DEVICE_ID = 11   # UA-25EX output

INPUT_CHANNEL = 1 # input 2 (right)