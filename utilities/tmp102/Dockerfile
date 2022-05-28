FROM python:3.10.0-alpine

WORKDIR /usr/src/app
COPY *.py ./
COPY requirements.txt ./

RUN apk add --no-cache \
    gcc \
    libc-dev \
    libffi-dev \
    py3-pip \
    zlib-dev \
    make
#apk add --no-cache \
#    gcc \
#    git \
#    openssl-dev \
#    py3-pip \

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "redis_sensor.py" ]
