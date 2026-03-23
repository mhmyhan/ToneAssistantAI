
# Tone Assistant 
Live IN-OUT ML Powered Tone generation system
(maybe neural powered soon?)


## Model Training
Run dataset generation in terminal with: 

CAREFUL - make sure you check SAMPLES_PER_RIFF in src\dataset_generation\generate_dataset.py
python src/dataset_generation/generate_dataset.py


## Live System

### requirements:
- Audio Interface that allows for sample processing speed of 44.1kHz (you can change system sample rate on line:6 of live_pedalboard.py(Other sample rates will not be tested))
- Guitar or bass(not supported) Going into the interface
- check requirements.txt for python packages

### RUN
Run program UI using:

python run_app.py

---

Run live Pedalboard feed raw using:

python src/live/live_pedalboard.py
(For debugging audio array processing)

### Latency
Ideally runs with a latency < 10ms

Latency is dependent the response period of the processing cycle:

Audio Interface Input -> Pedalboard Processing -> Audio Interface Output

Depending on audio hostAPI used (ASIO for best results)
- block_size (sample size)
  - 256  -> ~6ms
  - 512  -> ~11ms
  - 1024 -> ~23ms
- Processing
- sample_rate
Check {src\live\live_pedalboard.py} to make changes

### notes on performance:
 Roland's UA-25ex drivers provided ([here](https://www.roland.com/global/support/by_product/ua-25ex/updates_drivers/)) are not visible to the sounddevice library, more modern devices may have drivers that make themselves visible, but new audio-interfaces can be very expensive. This puts a bit of a dampener on my ability in the short term to make a proper low latency interface for live audio processing. 

 #### Potential Solutions
 - Circumvent Sounddevice's reliance on ASIO Host device interfacing
 - WASAPI; Forces exclusivity but low latency
 - Get a new audio interface









Bibtex Reference

pedalboard:
@software{sobot_peter_2023_7817838,
  author       = {Sobot, Peter},
  title        = {Pedalboard},
  month        = jul,
  year         = 2021,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.7817838},
  url          = {https://doi.org/10.5281/zenodo.7817838}
}