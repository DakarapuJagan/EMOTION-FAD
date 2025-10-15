# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Download the FER model during build
RUN python -c "from fer import FER; detector = FER()" || echo "Warning: Could not download FER model"

# Expose the port the app runs on
EXPOSE $PORT

# Command to run the application
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--threads", "1", "--timeout", "300", "--bind", "0.0.0.0:$PORT", "wsgi:application"]
