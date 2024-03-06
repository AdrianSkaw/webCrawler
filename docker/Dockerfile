# syntax=docker/dockerfile:1.4

FROM python:3.10
RUN apt-get update && apt-get install -y redis-server
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
COPY run.sh /run.sh
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["redis-server"]
CMD ["/bin/bash", "/run.sh"]