# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy Python dependencies file into the container at /app
COPY requirements.txt requirements.txt

# Install the required Python packages
RUN pip3 install -r requirements.txt

# Copy your application files into the container
COPY app1.py app1.py

# Specify the command to run the app1.py
CMD ["python3", "app1.py"]
 