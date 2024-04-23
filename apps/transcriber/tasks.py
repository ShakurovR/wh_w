from app import celery_app
from celery.signals import worker_process_init
from celery import shared_task
import whisperx
import torch
import os
import numpy as np

model = None
compute_type = 'int8'
batch_size=32

@worker_process_init.connect()
def init_worker_process(**kwargs):
    print("Initializing the model...")
    global model
    model = whisperx.load_model("large-v3", 'cuda', language="es", compute_type=compute_type)
    model.transcribe(np.zeros(1).astype("float32"))
    print("Initialization complete")

@shared_task(name='transcriber', bind=True)
def transcribe(self, raw_ffmpeg_out, language=None):
    audio = np.frombuffer(raw_ffmpeg_out, np.int16).flatten().astype(np.float32) / 32768.0
    if(language is None): 
        language=detect_lang(audio, model)
    print("Starting transcribing...")
    tr_result = model.transcribe(
        audio, 
        batch_size=batch_size, 
        language=language, 
        task="transcribe"
        )
    return tr_result
