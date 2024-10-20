# Use an official ARM base image
FROM arm32v7/python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 1883 available to the world outside this container
EXPOSE 1883

# Define environment variable
ENV NAME World

# Run the application
CMD ["python", "your_script.py"]
