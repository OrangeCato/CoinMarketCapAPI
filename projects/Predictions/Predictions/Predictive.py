import pandas as pd
import numpy as np
import sqlite3
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split

print("Loading and Preprocessing Data...")

# Connect to the SQLite database
conn = sqlite3.connect('/Users/alessandrazamora/Desktop/MLrsc/CoinMarketCap/projects/HistoricalData/Data_updated_24h.db')
cursor = conn.cursor()
query = "SELECT market_cap, price, volume_24h, hour_change, day_change, week_change, pull_date FROM daily_crypto_data"
crypto_data = pd.read_sql_query(query, conn)
cursor.close()
conn.close()

# Data preprocessing
crypto_data.drop_duplicates(inplace=True)
crypto_data.dropna(inplace=True)
crypto_data['pull_date'] = pd.to_datetime(crypto_data['pull_date'])
crypto_data.sort_values(by='pull_date', inplace=True)

X = crypto_data[['market_cap', 'volume_24h', 'hour_change', 'day_change', 'week_change']]
y = crypto_data['price']  # Use the current day's price as the target

# split dataset
print("Splitting the Dataset...")
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# convert processed data to PyTorch tensors
print("Converting data to PyTorch tensors...")
X_train = torch.tensor(X_train.values, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32)
X_val = torch.tensor(X_val.values, dtype=torch.float32)
y_val = torch.tensor(y_val.values, dtype=torch.float32)

# create data loader instances
print("Creating data loaders...")
batch_size = 64
train_data = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

# Define LSTM model
print("Defining LSTM model...")
class CryptoPricePredictionLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(CryptoPricePredictionLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x.unsqueeze(2))  # Add this line to adjust the input shape
        out = self.fc(out[:, -1, :])
        return out

# Instantiate the model
input_size = X_train.shape[1]
hidden_size = 64
num_layers = 2
model = CryptoPricePredictionLSTM(input_size, hidden_size, num_layers)

# Choose loss function and optimizer
print("Choosing Loss Function and Optimizer...")
criterion = nn.MSELoss()
learning_rate = 0.001
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train model
print("Training the model...")
epochs = 100
train_losses, val_losses = [], []
for epoch in range(epochs):
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()

        # Initialize hidden and cell states with zeros
        h0 = torch.zeros(num_layers, inputs.size(0), hidden_size).to(inputs.device)
        c0 = torch.zeros(num_layers, inputs.size(0), hidden_size).to(inputs.device)
        hc = (h0, c0)

        outputs = model(inputs, hc)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    train_losses.append(loss.item())

    model.eval()
    with torch.no_grad():
        val_outputs = model(X_val.unsqueeze(2))  # Adjust input shape for validation
        val_loss = criterion(val_outputs, y_val)
        val_losses.append(val_loss.item())

    print(f"Epoch [{epoch + 1}/{epochs}] - Training loss: {loss.item():.4f}, Validation Loss: {val_loss.item():.4f}")

# Evaluate
print("Evaluating model...")
model.eval()
with torch.no_grad():
    test_outputs = model(X_val)
    test_loss = criterion(test_outputs, y_val)

print(f"Test Loss: {test_loss.item():.4f}")

# Visualize training and validation loss
print("Visualizing training and validation loss...")
plt.figure(figsize=(10, 6))
plt.plot(train_losses, label="Training Loss", color='blue')
plt.plot(val_losses, label='Validation Loss', color='red')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title ('Training and Validation Loss')
plt.legend()
plt.show()

print("Prepare for future predictions...")

# Now, if you have future data, you can use the trained model to make predictions
