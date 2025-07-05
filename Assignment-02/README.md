# Computer Security Assignment-02: Website Fingerprinting

This README provides step-by-step instructions for setting up and running the website fingerprinting project.

## Prerequisites

- Python 3.12
- Google Chrome (for Selenium)

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Navigate to the assignment directory
cd /home/afzal/Academic/Computer-Security/Assignment-02/

# Create virtual environment
python -m venv Assignment-02_venv

# Activate virtual environment
source Assignment-02_venv/bin/activate
```

### 2. Install Required Packages

Since Python 3.12 removed `distutils` from the standard library, we need to ensure proper package installation:

```bash
# First, upgrade pip to the latest version
pip install --upgrade pip

# Install the following packages in this specific order
pip install setuptools wheel
pip install flask matplotlib numpy
pip install selenium webdriver-manager
pip install torch scikit-learn sqlalchemy
```

If you encounter any issues with `distutils` during installation, you can try one of these solutions:

```bash
# Option 1: Install the standalone distutils package
pip install setuptools-distutils-version

# Option 2: Use an older version of setuptools that works better with Python 3.12
pip install setuptools==65.5.0
```

### 3. Running the Web Fingerprinting Application

```bash
# Navigate to the template directory
cd /home/afzal/Academic/Computer-Security/Assignment-02/template

# Start the Flask server
python app.py
```

This will start the Flask application on `http://127.0.0.1:5000`.

### 4. Data Collection Process

The project includes a data collection script to gather website fingerprints:

```bash
# Make sure the Flask app is running in a separate terminal
python collect.py
```

The collection script:
- Opens each website in the predefined WEBSITES list
- Collects browser timing data
- Stores the data in a SQLite database
- Saves the dataset to a JSON file

### 5. Training the Model

After data collection, you can train the fingerprinting model:

```bash
# Make sure you have collected data first
python train.py
```

This will:
- Load the dataset
- Train a neural network model to identify websites based on timing data
- Save the trained model to the "saved_models" directory

## Project Structure

- `app.py`: Flask server that serves the web interface
- `collect.py`: Script for collecting website fingerprinting data
- `database.py`: Database utility for storing collected traces
- `train.py`: Model training script for website fingerprinting
- `static/`: Directory containing web interface files
  - `index.html`: Main web interface
  - `index.js`: JavaScript for the web interface
  - `worker.js`: Web worker for collecting timing data
  - `warmup.js`: Script for warming up browser cache

## Troubleshooting

### Package Installation Issues

If you encounter errors during package installation:

1. Make sure you're using the latest pip:
   ```bash
   pip install --upgrade pip
   ```

2. If you get specific errors about `distutils`, try installing it separately:
   ```bash
   pip install setuptools-distutils-version
   ```

3. If you get errors with specific packages, try installing them one by one with verbose output:
   ```bash
   pip install -v package_name
   ```

### Browser Driver Issues

If Selenium can't find the Chrome driver:

1. Make sure Chrome is installed
2. Try manually downloading and specifying the chromedriver path:
   ```python
   # In collect.py, modify the webdriver initialization:
   driver = webdriver.Chrome(service=Service('/path/to/chromedriver'))
   ```

### Database Access Issues

If you encounter database access errors:

1. Make sure the database file (`webfingerprint.db`) has the correct permissions
2. Try deleting the existing database and let the application create a new one:
   ```bash
   rm webfingerprint.db
   ```

## Additional Notes

- Make sure to run the Flask app first before running collection or training scripts
- The model training can take a significant amount of time depending on your hardware
- Adjust the number of traces collected per website in `collect.py` if needed
