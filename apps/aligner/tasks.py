from app import celery_app
from celery.signals import worker_process_init
from celery import shared_task
import whisperx
import torch
import os 
import numpy as np

models_dict = {}
allowed_lngs = ('en', 'es')

@worker_process_init.connect()
def init_worker_process(**kwargs):
    print("Initializing models...")
    global models_dict
    for lng in allowed_lngs:
        models_dict[lng] = whisperx.load_align_model(language_code=lng,device="cuda")
    print("Initialization complete")

@shared_task(name='aligner', bind=True)
def align(self, transcription_result, raw_ffmpeg_out, language):
    if(language not in allowed_lngs):
        raise Exception(f"Wrong language code: {language}")
    audio = np.frombuffer(raw_ffmpeg_out, np.int16).flatten().astype(np.float32) / 32768.0
    print("Starting aligning...")
    aligned_result = whisperx.align(
        transcription_result["segments"],
        models_dict[language][0], 
        models_dict[language][1],
        audio,
        "cuda",
        return_char_alignments=False
        )
    return aligned_result