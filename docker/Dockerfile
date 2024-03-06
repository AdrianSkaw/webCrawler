# syntax=docker/dockerfile:1.4

FROM python:3.10
RUN apt-get update && apt-get install -y redis-server
EXPOSE 7900
WORKDIR /app
COPY requirements.txt /app
COPY run.sh /run.sh
RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["sh", "-c", "redis-server & /bin/bash /run.sh"]