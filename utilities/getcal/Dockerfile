FROM python:3

WORKDIR /usr/src/app
COPY getcal.py ./
COPY ../library/local_redis.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "getcal.py", "-c ${CONFIG_FILE}" ]
