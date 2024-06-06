from app import celery_app
from celery.signals import worker_process_init
from celery import shared_task
import faster_whisper as fw
import os
import numpy as np
import io

model = None
compute_type = 'float16'
batch_size=32
model_name = "large-v3"
device="cuda"

def init_model(**kwargs):
    print("Initializing the model...")
    global model
    model = fw.WhisperModel(model_name, device, compute_type=compute_type)
    print("Initialization complete")

@shared_task(name='transcriber', bind=True)
def transcribe(self, serialized_audio, language=None):
    if(model is None):
        init_model()
    # Deserialize to numpy array
    memfile = io.BytesIO()
    memfile.write(serialized_audio)
    memfile.seek(0)
    audio = np.load(memfile)
    print("Starting transcribing...")
    tr_result, info = model.transcribe(
        audio,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        word_timestamps=True,
        language=language,
    )
    return list(tr_result)

