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
pip install selenium==4.15.0 webdriver-manager==4.0.1
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

