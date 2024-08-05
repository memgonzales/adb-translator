FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY . /app
WORKDIR /app

RUN set -ex 

RUN apt-get update \
    && apt-get install -y \
    bedtools \
    cron \
    git \
    python3-dev \
    python3-pip \
    && apt-get clean

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt