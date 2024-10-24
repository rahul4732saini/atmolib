FROM python:3.13-slim AS base

RUN apt-get update && apt-get install -y build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /home/atmolib

RUN python -m pip install --no-cache-dir --upgrade pip

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./atmolib .

CMD ["/bin/bash"]