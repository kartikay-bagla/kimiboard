# Base python package
FROM python:3.8-slim-buster

# Working directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy the files
COPY . .