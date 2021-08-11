FROM ubuntu:latest

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -y python3.8 && apt-get install -y python3-pip
RUN apt install -y redis-server
RUN pip install fastapi uvicorn[standard] rq
WORKDIR /app


