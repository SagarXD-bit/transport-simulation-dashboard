# ------------------------------------------------------------
#   GENERIC SNN TRAINING SCRIPT (SIMULATED AMS HARDWARE DATA)
# ------------------------------------------------------------

import torch
import torch.nn as nn
import snntorch as snn
from snntorch import surrogate
import torch.optim as optim
import numpy as np
import random, os

# ------------------------------------------------------------
# 1. SEED, DEVICE, RANDOM FOLDER NAME
# ------------------------------------------------------------

SEED = 7
np.random.seed(SEED)
random.seed(SEED)
torch.manual_seed(SEED)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

OUTPUT_DIR = f"snn_logs_{random.randint(1000,9999)}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Saving all results to:", OUTPUT_DIR)

# ------------------------------------------------------------
# 2. SIMULATED AMS SENSOR DATA
# ------------------------------------------------------------
# Replace this with real AMS hardware samples when available.

NUM_SAMPLES = 4000
NUM_FEATURES = 32          # e.g., 32-dimensional sensor vector
NUM_CLASSES = 5            # random classification task

X = torch.rand(NUM_SAMPLES, NUM_FEATURES)        # fake AMS data
Y = torch.randint(0, NUM_CLASSES, (NUM_SAMPLES,))

train_size = int(0.8 * NUM_SAMPLES)
test_size = NUM_SAMPLES - train_size

X_train, X_test = X[:train_size], X[train_size:]
Y_train, Y_test = Y[:train_size], Y[train_size:]

# ------------------------------------------------------------
# 3. SIMPLE FEED-FORWARD SNN MODEL
# ------------------------------------------------------------

beta = 0.85                              # leak
spike_grad = surrogate.fast_sigmoid()    # surrogate gradient

class TinySNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(NUM_FEATURES, 64)
        self.lif1 = snn.Leaky(beta=beta, spike_grad=spike_grad, init_hidden=True)

        self.fc2 = nn.Linear(64, NUM_CLASSES)
        self.lif2 = snn.Leaky(beta=beta, spike_grad=spike_grad, init_hidden=True)

    def forward(self, x):
        mem1 = spike1 = mem2 = spike2 = None
        
        # One timestep (you can increase for multi-step)
        x = self.fc1(x)
        spike1, mem1 = self.lif1(x, mem1)

        x = self.fc2(spike1)
        spike2, mem2 = self.lif2(x, mem2)

        return mem2   # returning membrane potential for loss

model = TinySNN().to(DEVICE)

# ------------------------------------------------------------
# 4. LOSS AND OPTIMIZER
# ------------------------------------------------------------

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

EPOCHS = 10
BATCH = 64

# ------------------------------------------------------------
# 5. TRAINING LOOP
# ------------------------------------------------------------

print("\nTraining SNN...\n")

for epoch in range(EPOCHS):
    model.train()
    total_loss, correct = 0, 0

    for i in range(0, train_size, BATCH):
        xb = X_train[i:i+BATCH].to(DEVICE)
        yb = Y_train[i:i+BATCH].to(DEVICE)

        optimizer.zero_grad()
        out = model(xb)
        loss = criterion(out, yb)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * xb.size(0)
        _, pred = out.max(1)
        correct += pred.eq(yb).sum().item()

    avg_loss = total_loss / train_size
    acc = 100 * correct / train_size

    print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {avg_loss:.4f} | Accuracy: {acc:.2f}%")

# ------------------------------------------------------------
# 6. TESTING
# ------------------------------------------------------------

model.eval()
correct = 0

with torch.no_grad():
    out = model(X_test.to(DEVICE))
    _, pred = out.max(1)
    correct = pred.eq(Y_test.to(DEVICE)).sum().item()

test_acc = 100 * correct / test_size
print(f"\nTest Accuracy: {test_acc:.2f}%")

# ------------------------------------------------------------
# 7. SAVE MODEL (RANDOM NAME)
# ------------------------------------------------------------

model_file = os.path.join(OUTPUT_DIR, f"snn_model_{random.randint(100,999)}.pth")
torch.save(model.state_dict(), model_file)

print("\nModel saved to:", model_file)
print("Training completed.\n")
