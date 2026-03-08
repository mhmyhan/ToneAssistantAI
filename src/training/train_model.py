import torch
from torch.utils.data import DataLoader

from dataset.audio_loader import GuitarToneDataset
from model.tone_model import ToneCNN

dataset = GuitarToneDataset(
    feature_dir="data/features",
    label_file="data/labels/pedal_labels.csv"
)

loader = DataLoader(dataset, batch_size=16, shuffle=True)

model = ToneCNN(num_pedals=6)

criterion = torch.nn.BCELoss()

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(20):

    for features, labels in loader:

        outputs = model(features)

        loss = criterion(outputs, labels)

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

    print(f"Epoch: {epoch}\n Loss {loss.item()}")

torch.save(model.state_dict(), "models/trained/tone_model.pt")
