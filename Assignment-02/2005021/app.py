import io
import uuid
import base64
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)

stored_traces = []
stored_heatmaps = []

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)