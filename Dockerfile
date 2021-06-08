FROM python:3.8-slim

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV IST_SERVICE_PORT=9999
ENV IST_SERVICE_HOST="0.0.0.0"
# Should be removed from file. Only for local testing now
ENV IST_DB_USER="postgres"
ENV IST_DB_PASSWORD="123456789test_user"
ENV IST_DB_HOST="db"
ENV IST_DB_PORT=5432


COPY ./server /server