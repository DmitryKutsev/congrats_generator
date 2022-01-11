FROM python:3.8
MAINTAINER Dmitry Kutsev <dakutsev@gmail.com>

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD gunicorn -b 0.0.0.0:8000 --timeout 1000 --reload --workers=1 "start_app:start()"
