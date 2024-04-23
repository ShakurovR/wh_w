FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ENV PIP_ROOT_USER_ACTION=ignore
ENV DEBIAN_FRONTEND=noninteractive
ENV APP_NAME=aligner

WORKDIR /app
COPY ./req.txt /app/req.txt

RUN apt-get update && apt-get install -y python3-pip git ffmpeg
RUN pip install --no-cache-dir --upgrade -r /app/req.txt
RUN pip install git+https://github.com/m-bain/whisperx.git@f2da2f858e99e4211fe4f64b5f2938b007827e17#egg=whisperx

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info", "-Q", "aligner", "-c", "2"]
