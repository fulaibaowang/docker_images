# syntax=docker/dockerfile:1

FROM python:3.11-slim

# -----
# System packages
# -----
# Included:
# - build-essential, python-dev headers: compiling wheels if needed
# - libxml2/libxslt: helps lxml build/use system libs
# - zlib: gzip related
# - git, curl, wget: fetching repos / debugging
# - ca-certificates: HTTPS
# - tini: clean signal handling
# - openjdk: needed for PyTerrier / Terrier later
# - procps, htop, less, vim-tiny: basic debugging tools
#
# Note: openjdk makes image larger, but it's extremely convenient if you plan PyTerrier.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    make \
    git \
    curl \
    wget \
    ca-certificates \
    tini \
    procps \
    htop \
    less \
    vim-tiny \
    unzip \
    libxml2 \
    libxslt1.1 \
    zlib1g \
    openjdk-21-jre-headless \
 && rm -rf /var/lib/apt/lists/*

# Make Java available for PyTerrier
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# -----
# Python environment
# -----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install core + "likely useful later" libs:
# Core parsing:
# - lxml, pubmed-parser
# IR:
# - python-terrier (PyTerrier), ir_datasets (optional), ranx (eval)
# Data:
# - numpy, pandas, pyarrow, polars
# NLP / embeddings:
# - sentence-transformers, transformers, torch (CPU), accelerate
# Utilities:
# - tqdm, orjson, ujson, requests, beautifulsoup4
#
# Notes:
# - torch CPU wheels are big but convenient. If you want a smaller image, remove torch/sentence-transformers/transformers.
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir \
      lxml \
      pubmed-parser \
      tqdm \
      requests \
      orjson \
      ujson \
      numpy \
      pandas \
      pyarrow \
      polars \
      python-terrier \
      ranx \
      beautifulsoup4 \
      accelerate \
      jupyterlab \
      matplotlib \
      scikit-learn

# Copy your script into the image
RUN git clone https://github.com/fulaibaowang/BioASQ.git /app/bioasq
WORKDIR /app/bioasq