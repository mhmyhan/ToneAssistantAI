import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import os

class GuitarToneDataset(Dataset):

    def __init__(self, feature_dir, label_file):

        self.labels = pd.read_csv(label_file)
        self.feature_dir = feature_dir

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):

        row = self.labels.iloc[idx]

        file_name = row['filename'].replace('.wav', '.npy')

        feature_path = os.path.join(self.feature_dir, file_name)

        features = np.load(feature_path)

        features = torch.tensor(features).unsqueeze(0).float()

        labels = torch.tensor(row[1:].values).float()

        return features, labels
