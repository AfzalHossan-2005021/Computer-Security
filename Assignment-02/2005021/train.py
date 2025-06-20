import os
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, Subset
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedShuffleSplit

# Configuration
DATASET_PATH = "dataset.json"
MODELS_DIR = "saved_models"
BATCH_SIZE = 64
EPOCHS = 50  
LEARNING_RATE = 1e-4
TRAIN_SPLIT = 0.8 
INPUT_SIZE = 1000  
HIDDEN_SIZE = 128

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)


class FingerprintClassifier(nn.Module):
    """Basic neural network model for website fingerprinting classification."""
    
    def __init__(self, input_size, hidden_size, num_classes):
        super(FingerprintClassifier, self).__init__()
        
        # 1D Convolutional layers
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=32, kernel_size=5, stride=2, padding=2)
        self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=5, stride=1, padding=2)
        self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)
        
        # Calculate the size after convolutions and pooling
        conv_output_size = input_size // 8  # After two 2x pooling operations
        self.fc_input_size = conv_output_size * 64
        
        # Fully connected layers
        self.fc1 = nn.Linear(self.fc_input_size, hidden_size)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_size, num_classes)
        
        # Activation functions
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # Reshape for 1D convolution: (batch_size, 1, input_size)
        x = x.unsqueeze(1)
        
        # Convolutional layers
        x = self.relu(self.conv1(x))
        x = self.pool1(x)
        x = self.relu(self.conv2(x))
        x = self.pool2(x)
        
        # Flatten for fully connected layers
        x = x.view(-1, self.fc_input_size)
        
        # Fully connected layers
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x
        
class ComplexFingerprintClassifier(nn.Module):
    """A more complex neural network model for website fingerprinting classification."""
    
    def __init__(self, input_size, hidden_size, num_classes):
        super(ComplexFingerprintClassifier, self).__init__()
        
        # 1D Convolutional layers with batch normalization
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=32, kernel_size=5, stride=1, padding=2)
        self.bn1 = nn.BatchNorm1d(32)
        self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm1d(64)
        self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)
        
        self.conv3 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm1d(128)
        self.pool3 = nn.MaxPool1d(kernel_size=2, stride=2)
        
        # Calculate the size after convolutions and pooling
        conv_output_size = input_size // 8  # After three 2x pooling operations
        self.fc_input_size = conv_output_size * 128
        
        # Fully connected layers
        self.fc1 = nn.Linear(self.fc_input_size, hidden_size*2)
        self.bn4 = nn.BatchNorm1d(hidden_size*2)
        self.dropout1 = nn.Dropout(0.5)
        
        self.fc2 = nn.Linear(hidden_size*2, hidden_size)
        self.bn5 = nn.BatchNorm1d(hidden_size)
        self.dropout2 = nn.Dropout(0.3)
        
        self.fc3 = nn.Linear(hidden_size, num_classes)
        
        # Activation functions
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # Reshape for 1D convolution: (batch_size, 1, input_size)
        x = x.unsqueeze(1)
        
        # Convolutional layers
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.pool1(x)
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.pool2(x)
        x = self.relu(self.bn3(self.conv3(x)))
        x = self.pool3(x)
        
        # Flatten for fully connected layers
        x = x.view(-1, self.fc_input_size)
        
        # Fully connected layers
        x = self.relu(self.bn4(self.fc1(x)))
        x = self.dropout1(x)
        x = self.relu(self.bn5(self.fc2(x)))
        x = self.dropout2(x)
        x = self.fc3(x)
        
        return x


class TransformerFingerprintClassifier(nn.Module):
    """1D Transformer Encoder for website fingerprinting."""
    def __init__(self, input_size, hidden_size, num_classes, nhead=4, num_layers=2):
        super(TransformerFingerprintClassifier, self).__init__()
        self.input_proj = nn.Linear(input_size, hidden_size)
        encoder_layer = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=nhead, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(hidden_size, num_classes)
    def forward(self, x):
        # x: (batch, input_size)
        x = self.input_proj(x)  # (batch, hidden_size)
        x = x.unsqueeze(1)      # (batch, seq_len=1, hidden_size)
        x = self.transformer(x) # (batch, seq_len=1, hidden_size)
        x = x.squeeze(1)        # (batch, hidden_size)
        x = self.dropout(x)
        x = self.fc(x)
        return x


class CNNLSTMClassifier(nn.Module):
    """Hybrid 1D CNN + LSTM classifier for sequence data."""
    def __init__(self, input_size, hidden_size, num_classes, lstm_hidden=128, lstm_layers=1):
        super(CNNLSTMClassifier, self).__init__()
        self.conv1 = nn.Conv1d(1, 32, kernel_size=5, stride=1, padding=2)
        self.bn1 = nn.BatchNorm1d(32)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm1d(64)
        self.pool2 = nn.MaxPool1d(2)
        # After two 2x pooling: seq_len = input_size // 4, channels = 64
        self.lstm_seq_len = input_size // 4
        self.lstm_input_size = 64
        self.lstm = nn.LSTM(input_size=self.lstm_input_size, hidden_size=lstm_hidden, num_layers=lstm_layers, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(lstm_hidden * 2, num_classes)
        self.relu = nn.ReLU()
    def forward(self, x):
        x = x.unsqueeze(1)  # (batch, 1, input_size)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.pool1(x)
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.pool2(x)
        # x: (batch, channels=64, seq_len=input_size//4)
        x = x.permute(0, 2, 1)  # (batch, seq_len, channels)
        lstm_out, _ = self.lstm(x)
        out = lstm_out[:, -1, :]  # Take last output
        out = self.dropout(out)
        out = self.fc(out)
        return out


class CNNBiLSTMAttentionClassifier(nn.Module):
    """Deeper CNN + Bidirectional LSTM with Attention for sequence classification."""
    def __init__(self, input_size, hidden_size, num_classes, lstm_hidden=128, lstm_layers=2):
        super(CNNBiLSTMAttentionClassifier, self).__init__()
        self.conv1 = nn.Conv1d(1, 64, kernel_size=5, stride=1, padding=2)
        self.bn1 = nn.BatchNorm1d(64)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(64, 128, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm1d(128)
        self.pool2 = nn.MaxPool1d(2)
        self.conv3 = nn.Conv1d(128, 256, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm1d(256)
        self.pool3 = nn.MaxPool1d(2)
        # After three 2x pooling: seq_len = input_size // 8, channels = 256
        self.lstm_seq_len = input_size // 8
        self.lstm_input_size = 256
        self.bilstm = nn.LSTM(input_size=self.lstm_input_size, hidden_size=lstm_hidden, num_layers=lstm_layers, batch_first=True, bidirectional=True)
        self.attention = nn.Linear(lstm_hidden * 2, 1)
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(lstm_hidden * 2, num_classes)
        self.relu = nn.ReLU()
    def forward(self, x):
        x = x.unsqueeze(1)  # (batch, 1, input_size)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.pool1(x)
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.pool2(x)
        x = self.relu(self.bn3(self.conv3(x)))
        x = self.pool3(x)
        # x: (batch, channels=256, seq_len=input_size//8)
        x = x.permute(0, 2, 1)  # (batch, seq_len, channels)
        lstm_out, _ = self.bilstm(x)  # (batch, seq_len, hidden*2)
        # Attention mechanism
        attn_weights = torch.softmax(self.attention(lstm_out), dim=1)  # (batch, seq_len, 1)
        context = torch.sum(attn_weights * lstm_out, dim=1)  # (batch, hidden*2)
        out = self.dropout(context)
        out = self.fc(out)
        return out


def train(model, train_loader, test_loader, criterion, optimizer, epochs, model_save_path):
    """Train a PyTorch model and evaluate on the test set.
    Args:
        model: PyTorch model to train
        train_loader: DataLoader for training data
        test_loader: DataLoader for testing data
        criterion: Loss function
        optimizer: Optimizer
        epochs: Number of epochs to train
        model_save_path: Path to save the best model
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    train_losses = []
    test_losses = []
    train_accuracies = []
    test_accuracies = []
    
    best_accuracy = 0.0
    
    for epoch in range(epochs):
        # Training
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for traces, labels in train_loader:
            traces, labels = traces.to(device), labels.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(traces)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            # Statistics
            running_loss += loss.item() * traces.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_accuracy = correct / total
        train_losses.append(epoch_loss)
        train_accuracies.append(epoch_accuracy)
        
        # Evaluation
        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for traces, labels in test_loader:
                traces, labels = traces.to(device), labels.to(device)
                outputs = model(traces)
                loss = criterion(outputs, labels)
                
                running_loss += loss.item() * traces.size(0)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        epoch_loss = running_loss / len(test_loader.dataset)
        epoch_accuracy = correct / total
        test_losses.append(epoch_loss)
        test_accuracies.append(epoch_accuracy)
        
        # Print status
        print(f'Epoch {epoch+1}/{epochs}, '
              f'Train Loss: {train_losses[-1]:.4f}, Train Acc: {train_accuracies[-1]:.4f}, '
              f'Test Loss: {test_losses[-1]:.4f}, Test Acc: {test_accuracies[-1]:.4f}')
        
        # Save the best model
        if epoch_accuracy > best_accuracy:
            best_accuracy = epoch_accuracy
            torch.save(model.state_dict(), model_save_path)
            print(f'Model saved with accuracy: {best_accuracy:.4f}')
    
    return best_accuracy



def evaluate(model, test_loader, website_names):
    """Evaluate a PyTorch model on the test set and show classification report with website names.
    Args:
        model: PyTorch model to evaluate
        test_loader: DataLoader for testing data
        website_names: List of website names for classification report
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for traces, labels in test_loader:
            traces, labels = traces.to(device), labels.to(device)
            outputs = model(traces)
            _, predicted = torch.max(outputs.data, 1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Print classification report with website names instead of indices
    print("\nClassification Report:")
    print(classification_report(
        all_labels, 
        all_preds, 
        target_names=website_names,
        zero_division=1
    ))
    
    return all_preds, all_labels


class TraceDataset(Dataset):
    """Custom Dataset for loading website fingerprinting traces from JSON."""
    def __init__(self, json_path, input_size, normalize=True):
        with open(json_path, 'r') as f:
            self.data = json.load(f)
        self.input_size = input_size
        self.normalize = normalize
        self.traces = []
        self.labels = []
        self.websites = []
        for entry in self.data:
            trace = entry['trace_data'][:input_size]
            if len(trace) < input_size:
                trace = trace + [0] * (input_size - len(trace))
            self.traces.append(trace)
            self.labels.append(entry['website_index'])
            self.websites.append(entry['website'])
        self.traces = np.array(self.traces, dtype=np.float32)
        self.labels = np.array(self.labels, dtype=np.int64)
        self.website_names = [w for i, w in sorted(set(zip(self.labels, self.websites)))]
        # Normalize if needed
        if self.normalize:
            self.mean = self.traces.mean()
            self.std = self.traces.std()
            self.traces = (self.traces - self.mean) / (self.std + 1e-8)
    def __len__(self):
        return len(self.traces)
    def __getitem__(self, idx):
        return torch.tensor(self.traces[idx]), torch.tensor(self.labels[idx])


def main():
    """ Implement the main function to train and evaluate the models.
    1. Load the dataset from the JSON file, probably using a custom Dataset class
    2. Split the dataset into training and testing sets
    3. Create data loader for training and testing
    4. Define the models to train
    5. Train and evaluate each model
    6. Print comparison of results
    """
    # 1. Load dataset using a custom Dataset class
    dataset = TraceDataset(DATASET_PATH, INPUT_SIZE, normalize=True)

    # 2. Stratified split
    sss = StratifiedShuffleSplit(n_splits=1, test_size=1-TRAIN_SPLIT, random_state=42)
    train_idx, test_idx = next(sss.split(np.zeros(len(dataset)), dataset.labels))   # Use dummy X (np.zeros) since only y is used for stratification
    train_set = Subset(dataset, train_idx)
    test_set = Subset(dataset, test_idx)

    # 3. DataLoaders
    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=False)

    # 4. Define models
    num_classes = len(dataset.website_names)
    models = {
        'basic_cnn': FingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, num_classes),
        'complex_cnn': ComplexFingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, num_classes),
        'transformer': TransformerFingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, num_classes),
        'cnn_lstm': CNNLSTMClassifier(INPUT_SIZE, HIDDEN_SIZE, num_classes),
        'cnn_bilstm_attention': CNNBiLSTMAttentionClassifier(INPUT_SIZE, HIDDEN_SIZE, num_classes)
    }

    # 5. Train and evaluate each model
    results = {}
    best_model = None
    best_acc = 0.0
    best_model_name = None
    for name, model in models.items():
        print(f"\nTraining {name}...")
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
        model_save_path = os.path.join(MODELS_DIR, f"{name}.pth")
        acc = train(model, train_loader, test_loader, criterion, optimizer, EPOCHS, model_save_path)
        results[name] = acc
        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_model_name = name
    # Save the best model as model.pth (in addition to individual model files)
    if best_model is not None:
        torch.save(best_model.state_dict(), "model.pth")
        print(f"\nBest model '{best_model_name}' also saved as 'model.pth' with accuracy: {best_acc*100:.2f}%")
    # 6. Print comparison of results
    print("\nModel comparison:")
    for name, acc in results.items():
        print(f"{name}: {acc*100:.2f}% accuracy")

if __name__ == "__main__":
    main()
