# Users python 3.13-slim for the build
FROM python@sha256:4c2cf9917bd1cbacc5e9b07320025bdb7cdf2df7b0ceaccb55e9dd7e30987419 \
 AS base

RUN apt-get update && apt-get install -y build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /home/atmolib
COPY . .

# Upgrades pip, and installs the base requirements for the
# running the package and pytest for testing purposes.
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt pytest

CMD ["/bin/bash"]
