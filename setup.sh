#!/bin/bash

# Update package list and install system dependencies
apt-get update
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Download the FER model
python -c "from fer import FER; detector = FER()" || echo "Warning: Could not download FER model"

echo "Setup complete. Run 'source venv/bin/activate' to activate the virtual environment."
