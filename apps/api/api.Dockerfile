FROM python:3.11
WORKDIR /app
COPY ./req.txt /app/req.txt
RUN pip install --no-cache-dir --upgrade -r /app/req.txt
RUN apt-get update && apt-get install -y ffmpeg 
COPY ./ /app
EXPOSE 9000 
CMD ["python", "/app/main.py"]