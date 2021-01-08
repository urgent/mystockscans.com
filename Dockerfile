FROM python:3.7-slim
RUN apt update
RUN apt install -y git
ADD requirements.txt /
RUN pip install -r /requirements.txt
ADD . /app
VOLUME /voldata
WORKDIR /app
ENV PORT 8088
EXPOSE $PORT