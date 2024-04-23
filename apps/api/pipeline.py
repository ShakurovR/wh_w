from celery import shared_task
from main import celery_app
from utils import load_audio_stereo, segments_to_sent
from celery.result import allow_join_result

@shared_task(name="process_file")
def process_file(
    id: str,
    file: str,
    language: str,
):
    try:
        employee_raw_ffmpeg_out = load_audio_stereo(file, 0) # left
        client_raw_ffmpeg_out = load_audio_stereo(file, 1)  # right
        task_empl = celery_app.send_task(
            "transcriber",
            kwargs={
                'raw_ffmpeg_out':employee_raw_ffmpeg_out,
                'language':language,
            },
            queue="transcriber"
            )
        task_client = celery_app.send_task(
            "transcriber",
            kwargs={
                'raw_ffmpeg_out':client_raw_ffmpeg_out,
                'language':language,
            },
            queue="transcriber"
            )
        with allow_join_result():
            employee_result = task_empl.get()
            client_result = task_client.get()

        task_empl = celery_app.send_task(
            "aligner",
            kwargs={
                'transcription_result':employee_result,
                'raw_ffmpeg_out':client_raw_ffmpeg_out,
                'language':language,
            },
            queue="aligner"
            )
        task_client = celery_app.send_task(
            "aligner",
            kwargs={
                'transcription_result':client_result,
                'raw_ffmpeg_out':client_raw_ffmpeg_out,
                'language':language,
            },
            queue="aligner"
            )
        with allow_join_result():
            employee_result = task_empl.get()
            client_result = task_client.get()
            
        employee_sent = list(segments_to_sent(employee_result, mark="Employee"))
        client_sent = list(segments_to_sent(client_result, mark="Client"))
        
        res = sorted(employee_sent + client_sent, key=lambda x:x[1])#(x[1]+x[2])/2)
        
        for t,_,_,sp in res:
            print(sp+":"+t)
    except Exception as E:
        print("There was an exception processing file with id:{id}, file:{file}.\nException: {E}")
        raise E