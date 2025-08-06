FROM python:3.13-slim AS base

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