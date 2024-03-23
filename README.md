# Video-Histogram-Demo

This project aims to match RGB distributions of a video to a reference image with temporal constraints. It includes a Docker container setup for easy deployment and isolation of dependencies.

## Contents

- `Dockerfile`: Docker configuration file.
- `main.py`: Main script for processing.
- `requirements.txt`: Python dependencies.
- `testfootage.mp4`: Sample video footage.
- `testreference.png`: Sample reference image.

## Getting Started

To use this project, you need Docker installed on your machine. If you do not have Docker, follow the installation instructions on the [official Docker website](https://docs.docker.com/get-docker/).

### Building the Docker Image

First, clone this repository and navigate to the cloned directory. Then, build the Docker image using the following command:

```bash
docker build -t video-histogram-demo .
