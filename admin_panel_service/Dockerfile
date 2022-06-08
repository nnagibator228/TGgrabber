FROM python:3.8-slim

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    manpages-dev \
    procps \
    python3-dev \
    python3-pip \
    && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY secret_utils.py ./
COPY bot_restart.py ./
COPY socksend.py ./
COPY sql.py ./


RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

RUN rm -frv ./requirements.txt
ENV script bot_restart.py
CMD python ${script}
