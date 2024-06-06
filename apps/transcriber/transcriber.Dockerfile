FROM nvidia/cuda:12.0.0-cudnn8-devel-ubuntu20.04

ENV PIP_ROOT_USER_ACTION=ignore
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY ./req.txt /app/req.txt

RUN apt-get update && apt-get install -y python3-pip git ffmpeg 
RUN pip install -r /app/req.txt
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info", "-Q", "transcriber", "-c", "2"]
