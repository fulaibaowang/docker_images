FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1

# ffmpeg is required for merging/remux/convert
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Pin yt-dlp for reproducibility; adjust as needed
RUN python -m pip install --upgrade pip \
 && pip install "yt-dlp==2025.01.26"

WORKDIR /app
COPY youtube_download_merge.py /app/youtube_download_merge.py

# Where downloads & outputs go (bind-mount your host dir here)
WORKDIR /work

ENTRYPOINT ["python", "/app/youtube_download_merge.py"]
