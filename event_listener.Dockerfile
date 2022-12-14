# Pull base image
FROM python:3.10-slim-buster as builder
# Set environment variables
COPY requirements.txt requirements.txt

# Install pipenv
RUN set -ex && pip install --upgrade pip

# Install dependencies
RUN set -ex && pip install -r requirements.txt

FROM builder as final
WORKDIR /web-app
COPY ./app/ /web-app/app/
COPY event_listener.py /web-app/event_listener.py
COPY .env /web-app/
CMD ["python3", "event_listener.py"]