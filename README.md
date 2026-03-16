
# Tone Assistant 
Live IN-OUT ML Powered Tone generation system
(maybe neural powered soon?)


## Model Training
Run dataset generation in terminal with: 

python src/dataset_generation/generate_dataset.py


## Live System use
Run live Pedalboard feed using:

python src/live/live_pedalboard.py

### Latency
Ideally runs with a latency < 10ms

Latency is dependent on 3 features of the processing cycle:

Audio Interface Input -> Pedalboard Processing -> Audio Interface Output

- block_size
  - 256  -> ~6ms
  - 512  -> ~11ms
  - 1024 -> ~23ms
- Processing
- sample_rate

Check {src\live\live_pedalboard.py}








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