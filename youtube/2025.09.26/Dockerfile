FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1

# ffmpeg is required for merging/remux/convert
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Pin yt-dlp for update
ARG YTDLP_VERSION=2025.09.26
RUN python -m pip install --upgrade pip \
 && pip install "yt-dlp==${YTDLP_VERSION}"

WORKDIR /app
COPY youtube_download_merge.py /app/youtube_download_merge.py

# Where downloads & outputs go (bind-mount your host dir here)
WORKDIR /work

ENTRYPOINT ["python", "/app/youtube_download_merge.py"]
