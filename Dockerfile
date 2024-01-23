# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.11-slim

RUN echo 'deb http://deb.debian.org/debian stable main contrib' > /etc/apt/sources.list
RUN apt-get update && apt-get install -y curl bzip2 ffmpeg festival flite festvox-us-slt-hts

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install all required festival voices
RUN chmod +x ./install-voices.sh
RUN ./install-voices.sh

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 2024 available to the world outside this container
EXPOSE 2024

# Run app.py when the container launches
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2024"]