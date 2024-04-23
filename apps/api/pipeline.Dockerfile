FROM python:3.11
WORKDIR /app
COPY ./req.txt /app/req.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir --upgrade -r /app/req.txt
COPY ./ /app
CMD ["celery", "-A", "pipeline", "worker", "--loglevel=info", "-Q", "pipeline"]