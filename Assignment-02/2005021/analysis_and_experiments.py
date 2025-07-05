import os
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, Subset
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.metrics import f1_score, precision_recall_fscore_support
from sklearn.model_selection import StratifiedShuffleSplit
import warnings
warnings.filterwarnings('ignore')

# Import models from train.py
from train import TraceDataset, ComplexFingerprintClassifier, INPUT_SIZE, HIDDEN_SIZE

# Configuration
DATASET_PATH = "dataset.json"
MODELS_DIR = "saved_models"
INPUT_SIZE = 1000
HIDDEN_SIZE = 128

# Create results directories
os.makedirs('experiments_and_analysis', exist_ok=True)

# --- Dataset Classes ---
class ExperimentalTraceDataset(Dataset):
    """Enhanced Dataset with different preprocessing options."""
    def __init__(self, json_path, input_size, preprocessing='zscore', augment=False):
        with open(json_path, 'r') as f:
            self.data = json.load(f)
        self.input_size = input_size
        self.preprocessing = preprocessing
        self.augment = augment
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
        self._apply_preprocessing()
        if self.augment:
            self._apply_augmentation()
    def _apply_preprocessing(self):
        # Ensure self.traces is a numpy array
        self.traces = np.array(self.traces, dtype=np.float32)
        if self.preprocessing == 'zscore':
            self.mean = self.traces.mean()
            self.std = self.traces.std()
            self.traces = (self.traces - self.mean) / (self.std + 1e-8)
        elif self.preprocessing == 'minmax':
            scaler = MinMaxScaler()
            self.traces = scaler.fit_transform(self.traces)
        elif self.preprocessing == 'robust':
            scaler = RobustScaler()
            self.traces = scaler.fit_transform(self.traces)
        elif self.preprocessing == 'log':
            self.traces = np.log(self.traces + 1)
            self.mean = self.traces.mean()
            self.std = self.traces.std()
            self.traces = (self.traces - self.mean) / (self.std + 1e-8)
        elif self.preprocessing == 'none':
            pass
        elif self.preprocessing == 'clipped':
            q1, q99 = np.percentile(self.traces, [1, 99])
            self.traces = np.clip(self.traces, q1, q99)
            self.mean = self.traces.mean()
            self.std = self.traces.std()
            self.traces = (self.traces - self.mean) / (self.std + 1e-8)
    def _apply_augmentation(self):
        original_traces = self.traces.copy()
        original_labels = self.labels.copy()
        augmented_traces = []
        augmented_labels = []
        for trace, label in zip(original_traces, original_labels):
            augmented_traces.append(trace)
            augmented_labels.append(label)
            noise_trace = trace + np.random.normal(0, 0.01, trace.shape)
            augmented_traces.append(noise_trace)
            augmented_labels.append(label)
            shift_amount = np.random.randint(-50, 51)
            shifted_trace = np.roll(trace, shift_amount)
            augmented_traces.append(shifted_trace)
            augmented_labels.append(label)
        self.traces = np.array(augmented_traces, dtype=np.float32)
        self.labels = np.array(augmented_labels, dtype=np.int64)
    def __len__(self):
        return len(self.traces)
    def __getitem__(self, idx):
        return torch.tensor(self.traces[idx], dtype=torch.float32), torch.tensor(self.labels[idx])

# --- Shared Model Training Logic ---
def train_model_experiment(model, train_loader, test_loader, lr, epochs=20, device=torch.device('cpu')):
    """Train a model with specific configuration and return metrics."""
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    best_accuracy = 0.0
    train_accuracies = []
    test_accuracies = []
    train_losses = []
    test_losses = []
    all_preds = []
    all_labels = []
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        correct = 0
        total = 0
        for traces, labels in train_loader:
            traces, labels = traces.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(traces)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        train_acc = correct / total
        train_loss = total_loss / len(train_loader)
        train_accuracies.append(train_acc)
        train_losses.append(train_loss)
        model.eval()
        total_loss = 0
        correct = 0
        total = 0
        all_preds = []
        all_labels = []
        with torch.no_grad():
            for traces, labels in test_loader:
                traces, labels = traces.to(device), labels.to(device)
                outputs = model(traces)
                loss = criterion(outputs, labels)
                total_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                all_preds.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        test_acc = correct / total
        test_loss = total_loss / len(test_loader)
        test_accuracies.append(test_acc)
        test_losses.append(test_loss)
        if test_acc > best_accuracy:
            best_accuracy = test_acc
    f1 = f1_score(all_labels, all_preds, average='weighted')
    return {
        'best_accuracy': best_accuracy,
        'final_accuracy': test_accuracies[-1],
        'f1_score': f1,
        'train_accuracies': train_accuracies,
        'test_accuracies': test_accuracies,
        'train_losses': train_losses,
        'test_losses': test_losses
    }

def experiment_learning_rates():
    print("\n" + "="*60)
    print("LEARNING RATE EXPERIMENTS")
    print("="*60)
    dataset = ExperimentalTraceDataset(DATASET_PATH, INPUT_SIZE, preprocessing='zscore')
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(sss.split(np.zeros(len(dataset)), dataset.labels))
    train_set = Subset(dataset, train_idx)
    test_set = Subset(dataset, test_idx)
    learning_rates = [1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2]
    results = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for lr in learning_rates:
        print(f"\nTesting Learning Rate: {lr}")
        model = ComplexFingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, len(dataset.website_names))
        train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
        test_loader = DataLoader(test_set, batch_size=64, shuffle=False)
        metrics = train_model_experiment(model, train_loader, test_loader, lr, epochs=25, device=device)
        result = {
            'learning_rate': lr,
            'best_accuracy': metrics['best_accuracy'],
            'final_accuracy': metrics['final_accuracy'],
            'f1_score': metrics['f1_score']
        }
        results.append(result)
        print(f"  Best Accuracy: {metrics['best_accuracy']:.4f}")
        print(f"  Final Accuracy: {metrics['final_accuracy']:.4f}")
        print(f"  F1-Score: {metrics['f1_score']:.4f}")
    results_df = pd.DataFrame(results)
    results_df.to_csv('experiments_and_analysis/learning_rate_experiments.csv', index=False)
    best_lr_idx = results_df['best_accuracy'].idxmax()
    optimal_lr = results_df.loc[best_lr_idx, 'learning_rate']
    optimal_acc = results_df.loc[best_lr_idx, 'best_accuracy']
    print(f"\n🏆 OPTIMAL LEARNING RATE: {optimal_lr}")
    print(f"   Best Accuracy: {optimal_acc:.4f}")
    return results_df, optimal_lr

def experiment_batch_sizes():
    print("\n" + "="*60)
    print("BATCH SIZE EXPERIMENTS")
    print("="*60)
    dataset = ExperimentalTraceDataset(DATASET_PATH, INPUT_SIZE, preprocessing='zscore')
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(sss.split(np.zeros(len(dataset)), dataset.labels))
    train_set = Subset(dataset, train_idx)
    test_set = Subset(dataset, test_idx)
    batch_sizes = [16, 32, 64, 128]
    results = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for batch_size in batch_sizes:
        print(f"\nTesting Batch Size: {batch_size}")
        model = ComplexFingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, len(dataset.website_names))
        train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)
        metrics = train_model_experiment(model, train_loader, test_loader, lr=1e-4, epochs=25, device=device)
        result = {
            'batch_size': batch_size,
            'best_accuracy': metrics['best_accuracy'],
            'final_accuracy': metrics['final_accuracy'],
            'f1_score': metrics['f1_score']
        }
        results.append(result)
        print(f"  Best Accuracy: {metrics['best_accuracy']:.4f}")
        print(f"  Final Accuracy: {metrics['final_accuracy']:.4f}")
        print(f"  F1-Score: {metrics['f1_score']:.4f}")
    results_df = pd.DataFrame(results)
    results_df.to_csv('experiments_and_analysis/batch_size_experiments.csv', index=False)
    best_batch_idx = results_df['best_accuracy'].idxmax()
    optimal_batch = results_df.loc[best_batch_idx, 'batch_size']
    optimal_acc = results_df.loc[best_batch_idx, 'best_accuracy']
    print(f"\n🏆 OPTIMAL BATCH SIZE: {optimal_batch}")
    print(f"   Best Accuracy: {optimal_acc:.4f}")
    return results_df, optimal_batch

def experiment_preprocessing():
    print("\n" + "="*60)
    print("PREPROCESSING EXPERIMENTS")
    print("="*60)
    preprocessing_methods = ['zscore', 'minmax', 'robust', 'log', 'none', 'clipped']
    results = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for method in preprocessing_methods:
        print(f"\nTesting Preprocessing: {method}")
        dataset = ExperimentalTraceDataset(DATASET_PATH, INPUT_SIZE, preprocessing=method)
        sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        train_idx, test_idx = next(sss.split(np.zeros(len(dataset)), dataset.labels))
        train_set = Subset(dataset, train_idx)
        test_set = Subset(dataset, test_idx)
        model = ComplexFingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, len(dataset.website_names))
        train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
        test_loader = DataLoader(test_set, batch_size=64, shuffle=False)
        metrics = train_model_experiment(model, train_loader, test_loader, lr=1e-4, epochs=25, device=device)
        result = {
            'preprocessing': method,
            'best_accuracy': metrics['best_accuracy'],
            'final_accuracy': metrics['final_accuracy'],
            'f1_score': metrics['f1_score']
        }
        results.append(result)
        print(f"  Best Accuracy: {metrics['best_accuracy']:.4f}")
        print(f"  Final Accuracy: {metrics['final_accuracy']:.4f}")
        print(f"  F1-Score: {metrics['f1_score']:.4f}")
    results_df = pd.DataFrame(results)
    results_df.to_csv('experiments_and_analysis/preprocessing_experiments.csv', index=False)
    best_prep_idx = results_df['best_accuracy'].idxmax()
    optimal_prep = results_df.loc[best_prep_idx, 'preprocessing']
    optimal_acc = results_df.loc[best_prep_idx, 'best_accuracy']
    print(f"\n🏆 OPTIMAL PREPROCESSING: {optimal_prep}")
    print(f"   Best Accuracy: {optimal_acc:.4f}")
    return results_df, optimal_prep

def experiment_data_augmentation():
    print("\n" + "="*60)
    print("DATA AUGMENTATION EXPERIMENTS")
    print("="*60)
    results = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for augment in [False, True]:
        print(f"\nTesting Data Augmentation: {augment}")
        dataset = ExperimentalTraceDataset(DATASET_PATH, INPUT_SIZE, preprocessing='zscore', augment=augment)
        sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        train_idx, test_idx = next(sss.split(np.zeros(len(dataset)), dataset.labels))
        train_set = Subset(dataset, train_idx)
        test_set = Subset(dataset, test_idx)
        model = ComplexFingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, len(dataset.website_names))
        train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
        test_loader = DataLoader(test_set, batch_size=64, shuffle=False)
        metrics = train_model_experiment(model, train_loader, test_loader, lr=1e-4, epochs=25, device=device)
        result = {
            'augmentation': augment,
            'best_accuracy': metrics['best_accuracy'],
            'final_accuracy': metrics['final_accuracy'],
            'f1_score': metrics['f1_score']
        }
        results.append(result)
        print(f"  Best Accuracy: {metrics['best_accuracy']:.4f}")
        print(f"  Final Accuracy: {metrics['final_accuracy']:.4f}")
        print(f"  F1-Score: {metrics['f1_score']:.4f}")
    results_df = pd.DataFrame(results)
    results_df.to_csv('experiments_and_analysis/data_augmentation_experiments.csv', index=False)
    return results_df

def analyze_website_difficulty(dataset):
    print("="*60)
    print("WEBSITE CLASSIFICATION DIFFICULTY ANALYSIS")
    print("="*60)
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(sss.split(np.zeros(len(dataset)), dataset.labels))
    train_set = Subset(dataset, train_idx)
    test_set = Subset(dataset, test_idx)
    train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=64, shuffle=False)
    model = ComplexFingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, len(dataset.website_names))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    metrics = train_model_experiment(model, train_loader, test_loader, lr=1e-4, epochs=30, device=device)
    preds = []
    labels = []
    model.eval()
    with torch.no_grad():
        for traces, lbls in test_loader:
            traces, lbls = traces.to(device), lbls.to(device)
            outputs = model(traces)
            _, predicted = torch.max(outputs.data, 1)
            preds.extend(predicted.cpu().numpy())
            labels.extend(lbls.cpu().numpy())
    precision, recall, f1, support = precision_recall_fscore_support(labels, preds, average=None)
    analysis_data = []
    for i, website in enumerate(dataset.website_names):
        website_short = website.split('/')[-1] if '/' in website else website
        analysis_data.append({
            'Website': website_short,
            'Precision': precision[i] if isinstance(precision, (np.ndarray, list)) else float('nan'),
            'Recall': recall[i] if isinstance(recall, (np.ndarray, list)) else float('nan'),
            'F1-Score': f1[i] if isinstance(f1, (np.ndarray, list)) else float('nan'),
            'Support': support[i] if isinstance(support, (np.ndarray, list)) else float('nan'),
            'Difficulty': 'Easy' if (f1[i] if isinstance(f1, (np.ndarray, list)) else 0) > 0.95 else 'Medium' if (f1[i] if isinstance(f1, (np.ndarray, list)) else 0) > 0.90 else 'Hard'
        })
    df = pd.DataFrame(analysis_data)
    df = df.sort_values('F1-Score', ascending=True)
    print("\nWebsite Classification Difficulty (sorted by F1-Score):")
    print(df.to_string(index=False, float_format='%.4f'))
    df.to_csv('experiments_and_analysis/website_difficulty.csv', index=False)
    return df

def analyze_training_data_effect(dataset):
    print("\n" + "="*60)
    print("TRAINING DATA SIZE ANALYSIS")
    print("="*60)
    data_fractions = [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 1.0]
    results = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for fraction in data_fractions:
        print(f"\nTesting with {fraction*100}% of training data...")
        sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        train_idx, test_idx = next(sss.split(np.zeros(len(dataset)), dataset.labels))
        if fraction < 1.0:
            sss_reduced = StratifiedShuffleSplit(n_splits=1, test_size=1-fraction, random_state=42)
            train_idx_reduced, _ = next(sss_reduced.split(np.zeros(len(train_idx)), dataset.labels[train_idx]))
            train_idx = train_idx[train_idx_reduced]
        train_set = Subset(dataset, train_idx)
        test_set = Subset(dataset, test_idx)
        train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
        test_loader = DataLoader(test_set, batch_size=64, shuffle=False)
        metrics = train_model_experiment(
            ComplexFingerprintClassifier(INPUT_SIZE, HIDDEN_SIZE, len(dataset.website_names)),
            train_loader, test_loader, 1e-4, epochs=25, device=device
        )
        precision, recall, f1, _ = precision_recall_fscore_support(metrics['test_accuracies'], metrics['test_accuracies'], average='weighted')
        results.append({
            'Data_Fraction': fraction,
            'Training_Samples': len(train_set),
            'Test_Accuracy': metrics['best_accuracy'],
            'Precision': precision,
            'Recall': recall,
            'F1_Score': f1
        })
        print(f"   Test Accuracy: {metrics['best_accuracy']:.4f}")
        print(f"   F1-Score: {f1:.4f}")
    results_df = pd.DataFrame(results)
    results_df.to_csv('experiments_and_analysis/training_data_size_analysis.csv', index=False)
    return results_df

def main():
    print("Starting Combined Website Fingerprinting Analysis and Experiments...")
    dataset = TraceDataset(DATASET_PATH, INPUT_SIZE, normalize=True)
    # Run all experiments ONCE (no duplicate tasks)
    print("\n🔬 Phase 1: Learning Rate Optimization")
    lr_results, optimal_lr = experiment_learning_rates()
    print("\n🔬 Phase 2: Batch Size Optimization")
    batch_results, optimal_batch = experiment_batch_sizes()
    print("\n🔬 Phase 3: Preprocessing Method Comparison")
    prep_results, optimal_prep = experiment_preprocessing()
    print("\n🔬 Phase 4: Data Augmentation Analysis")
    aug_results = experiment_data_augmentation()
    print("\n📋 Phase 5: Hyperparameter Report Generation")
    # Run all analyses ONCE (no duplicate tasks)
    print("\n🔬 Phase 6: Website Difficulty Analysis")
    website_difficulty = analyze_website_difficulty(dataset)
    print("\n🔬 Phase 7: Training Data Size Effect Analysis")
    training_data_results = analyze_training_data_effect(dataset)
    print("\n📋 Phase 8: Comprehensive Analysis Report Generation")

if __name__ == "__main__":
    main()
