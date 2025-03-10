FROM nvidia/cuda:12.4.0-base-ubuntu22.04

RUN apt update && apt upgrade -y && apt install -y git vim wget && apt clean && rm -rf /var/lib/apt/lists/*
RUN apt update && apt upgrade -y && apt install -y nodejs npm && apt clean && rm -rf /var/lib/apt/lists/*
RUN apt update && apt upgrade -y && apt install -y python3.10 python3-pip && apt clean && rm -rf /var/lib/apt/lists/*
RUN apt update && apt upgrade -y && apt install -y curl git-lfs ffmpeg && apt clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

COPY ./requirements.txt /opt
RUN pip install --no-cache-dir -r /opt/requirements.txt

RUN apt update && apt upgrade -y && apt install -y unzip sudo && apt clean && rm -rf /var/lib/apt/lists/*

RUN cd /opt && git clone https://github.com/kc3hack/2025_25.git && cd ./2025_25/frontend && npm install
ENTRYPOINT cd /opt/2025_25 && ls && exec /bin/bash