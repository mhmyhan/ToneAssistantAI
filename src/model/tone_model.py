import torch
import torch.nn as nn

class ToneCNN(nn.Module):

    def __init__(self, num_pedals):

        super().__init__()

        self.conv = nn.Sequential(

            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

        )

        self.fc = nn.Sequential(

            nn.Linear(32 * 32 * 32, 128),
            nn.ReLU(),
            nn.Linear(128, num_pedals),
            nn.Sigmoid()

        )

    def forward(self, x):

        x = self.conv(x)

        x = x.view(x.size(0), -1)

        return self.fc(x)
