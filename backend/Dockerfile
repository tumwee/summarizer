FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y ffmpeg

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONDONTWRITEBYTECODE True

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 "app.main:create_app(testing=False)"
