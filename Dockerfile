FROM python:3.13-slim AS base

RUN apt-get update && apt-get install -y build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /home/atmolib
COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash"]