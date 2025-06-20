import io
import uuid
import base64
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify
import torch
import json
from train import CNNBiLSTMAttentionClassifier , INPUT_SIZE, HIDDEN_SIZE

app = Flask(__name__)

stored_traces = []
stored_heatmaps = []


# You may need to adjust this import if your normalization params are saved elsewhere
def load_model(model_path, num_classes):
    model = CNNBiLSTMAttentionClassifier(INPUT_SIZE, HIDDEN_SIZE, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def preprocess_trace(trace, input_size, min, max, mean, std):
    # Pad or truncate
    trace = trace[:input_size]
    if len(trace) < input_size:
        trace = trace + [0] * (input_size - len(trace))
    arr = np.array(trace, dtype=np.float32)

    # min-max normalization
    arr = (arr - min) / (max - min + 1e-8)  # Avoid division by zero

    # Standardize the array 
    arr = (arr - mean) / (std + 1e-8)
    return torch.tensor(arr).unsqueeze(0)  # shape: (1, input_size)


# Load website names and normalization params from dataset.json
with open('dataset.json', 'r') as f:
    data = json.load(f)
website_map = sorted(set((entry['website_index'], entry['website']) for entry in data))
website_names = [w for i, w in website_map]

# Load normalization params from files
with open('trace_minmax.json', 'r') as f:
    minmax = json.load(f)
    min_val = minmax['min']
    max_val = minmax['max']

npz = np.load('normalization_params.npz')
mean = float(npz['mean'])
std = float(npz['std'])

# Load model (choose your best model)
MODEL_PATH = 'model.pth'
model = load_model(MODEL_PATH, len(website_names))

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/collect_trace', methods=['POST'])
def collect_trace():
    try:
        data = request.get_json()
        
        id = str(uuid.uuid4())
        trace_data = data['trace_data']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Calculate stats
        min_val = int(np.min(trace_data))
        max_val = int(np.max(trace_data))
        range_val = int(np.ptp(trace_data))
        samples = len(trace_data)
        
        # Create stats dictionary with both individual values and formatted string
        stats = f"Min: {min_val}, Max: {max_val}, Range: {range_val}, Samples: {samples}"

        stored_traces.append(trace_data)

        trace_array = np.array(trace_data, dtype=float).reshape(1, -1)

        plt.figure(figsize=(20, 2))
        plt.imshow(trace_array, aspect='auto', cmap='plasma', vmin=min(trace_data), vmax=max(trace_data))
        plt.axis('off')

        buffer = io.BytesIO()
        # Increase bbox with padding
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.25, facecolor="#ffffff")
        plt.close()
        buffer.seek(0)

        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        heatmap = {
            'id': id,
            'timestamp': timestamp,
            'image': img_str,
            'stats': stats
        }
        stored_heatmaps.append(heatmap)

        return jsonify({'heatmap': heatmap}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_results', methods=['GET'])
def get_results():
    try:
        return jsonify({'traces': stored_traces}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear_results', methods=['POST'])
def clear_results():
    try:
        global stored_traces, stored_heatmaps
        stored_traces = []
        stored_heatmaps = []
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict_website():
    try:
        data = request.get_json()
        trace = data['trace_data']
        x = preprocess_trace(trace, 1000, min_val, max_val, mean, std)
        with torch.no_grad():
            logits = model(x)
            pred = int(torch.argmax(logits, dim=1).item())
            website = website_names[pred]
        return jsonify({'predicted_index': pred, 'predicted_website': website}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)