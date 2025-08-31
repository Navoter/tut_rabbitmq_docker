FROM alpine:latest
RUN apk add --no-cache python3 py3-pip python3-dev \
    && apk add --no-cache --virtual .build-deps gcc musl-dev
WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .build-deps
# COPY consumer.py .
CMD ["python", "producer.py"]
