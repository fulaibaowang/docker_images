FROM debian:bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends exiftool ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Copy in wrappers
COPY exif-gps.sh /usr/local/bin/exif-gps
COPY exif-gpano.sh /usr/local/bin/exif-gpano
RUN chmod +x /usr/local/bin/exif-gps /usr/local/bin/exif-gpano

ENTRYPOINT ["/bin/bash"]
