from celery import shared_task
from main import celery_app
from utils import load_audio, segments_to_sentences
from celery.result import allow_join_result

import pickle as pk 

@shared_task(name="process_file_stereo")
def process_file_stereo(
    id: str,
    file: str,
    language: str,
):
    try:
        employee_serialized_audio, client_serialized_audio = load_audio(file, sr=16000)
        task_empl = celery_app.send_task(
            "transcriber",
            kwargs={
                'serialized_audio':employee_serialized_audio,
                'language':language,
            },
            queue="transcriber"
            )
        task_client = celery_app.send_task(
            "transcriber",
            kwargs={
                'serialized_audio':client_serialized_audio,
                'language':language,
            },
            queue="transcriber"
            )
        with allow_join_result():
            employee_result = task_empl.get()
            client_result = task_client.get()
            
        employee_sentences = list(segments_to_sentences(employee_result, mark="Employee"))
        client_sentences = list(segments_to_sentences(client_result, mark="Client"))
        
        combined_sentences = sorted(employee_sentences + client_sentences, key=lambda sentence:sentence.start)
        
        for sentence in combined_sentences:
            print(sentence.speaker+":"+sentence.text)
    except Exception as E:
        print(f"There was an exception processing file with id:{id}, file:{file}.\nException: {E}")
        raise E