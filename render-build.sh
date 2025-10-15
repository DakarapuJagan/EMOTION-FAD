#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Download the FER model
python -c "from fer import FER; detector = FER()" || echo "Warning: Could not download FER model"

echo "Build completed successfully"
