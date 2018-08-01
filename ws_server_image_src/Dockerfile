# Use an official Python runtime as a parent image
FROM python:3.6.6-slim-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Create data directory for redis persistent storage
RUN mkdir ./data

# Make port 5995 available to the world outside this container
EXPOSE 5995

# Run ws_server.py when the container launches
CMD ["python", "ws_server.py"]
