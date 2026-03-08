## reference file grabbed from online, not used in project, just for reference on how to do inference with the trained model

import torch
import json

model = ToneNet(num_pedals=6)
model.load_state_dict(torch.load("tone_model.pt"))
model.eval()

features = extract_features("input.wav")
features = torch.tensor(features).unsqueeze(0).unsqueeze(0)

with torch.no_grad():
    output = model(features)

recommendations = recommend_pedals(output[0])

print(json.dumps(recommendations, indent=2))
