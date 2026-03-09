import torch
import json
from model.tone_model import ToneCNN
from dataset.feature_extractor import extract_mel_spectrogram

# list with pedal names in same order as model output for mapping predictions to pedal names
pedal_names = [
    "compressor",
    "overdrive",
    "distortion",
    "chorus",
    "delay",
    "reverb"
]

model = ToneCNN(num_pedals=6)

model.load_state_dict(torch.load("models/trained/tone_model.pt"))

model.eval()

features = extract_mel_spectrogram("input.wav")

features = torch.tensor(features).unsqueeze(0).unsqueeze(0).float()

with torch.no_grad():

    predictions = model(features)[0]

results = []

for i, p in enumerate(predictions):

    if p > 0.5:

        results.append({
            "pedal": pedal_names[i],
            "confidence": float(p)
        })

print(json.dumps(results, indent=2))
