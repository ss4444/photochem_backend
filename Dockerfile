FROM python:3.10

WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt-get -y install netcat-traditional
COPY requirements.txt /usr/app/requirements.txt

RUN pip install -r /usr/app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY . .