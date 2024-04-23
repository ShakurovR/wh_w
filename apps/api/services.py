from fastapi import HTTPException, UploadFile, status
from utils import load_audio_stereo
import os

def check_file(id: str, file: str, language: str) -> tuple:
    if(not os.path.isfile(file) ):
        raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File does not exist"
        )
    elif(os.path.getsize(file) == 0):
        raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File is empty"
        )
    try:
        load_audio_stereo(file, 0) # left
        load_audio_stereo(file, 1) # right
    except Exception as E:
        raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Exception while trying to load file, exception:{E}"
        )
    return True
