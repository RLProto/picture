# Use an official Python runtime as a parent image
FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    gcc \
    libopencv-dev \
    python3-opencv \
    curl \
    # Add dependencies for OPC UA
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code from your host to your image filesystem.
COPY . .

# Run app.py when the container launches
CMD ["python", "app.py"]

