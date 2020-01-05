FROM python:3.8-alpine as base

FROM base as builder

RUN apk update && apk add gcc bcc
RUN mkdir /wheels
COPY requirements.txt /requirements.txt
RUN pip wheel -r /requirements.txt --wheel-dir=/wheels && \
    pip install -r /requirements.txt --find-links=/wheels

FROM base

ENV PYTHONUNBUFFERED 1
COPY --from=builder /wheels /wheels
RUN pip install /wheels/*.whl
WORKDIR /code
COPY . .

CMD ["python", "ipfs_monitor/app.py"]
