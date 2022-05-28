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
    make \
    libxml2-dev \
    libxslt-dev

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "process_temperatures.py", "-c ${CONFIG_FILE}" ]
