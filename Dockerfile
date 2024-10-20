# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary dependencies for building Python 3.11
RUN apt-get update && apt-get install -y \
    build-essential \
    tk-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline6-dev \
    libdb5.3-dev \
    libgdbm-dev \
    libsqlite3-dev \
    libssl-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    zlib1g-dev \
    libffi-dev

# Install Python 3.11
RUN wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tar.xz && \
    tar -xf Python-3.11.0.tar.xz && \
    cd Python-3.11.0 && \
    ./configure --enable-optimizations && \
    make -j4 && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.11.0 Python-3.11.0.tar.xz

# Install Python packages specified in requirements.txt
RUN pip3.11 install --no-cache-dir -r requirements.txt

# Make port 1883 available to the world outside this container
EXPOSE 1883

# Run the application
CMD ["python3.11", "app.py"]
