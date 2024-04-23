from celery import Celery
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os
from logging_conf import LOG_FORMAT
from services import check_file
app = FastAPI()


celery_app = Celery(
    "CELERY_APP",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

celery_app.conf.update(task_track_started=True, broker_connection_retry_on_startup=True)

@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    return JSONResponse(status_code=200, content={"healthchek": True})

@app.post("/api/process_audio")
def process_file(
    id: str,
    file: str, 
    language: str,
) -> str:
    check_file(id=id, file=file, language=language)
    celery_app.send_task(
        "process_file",
        kwargs={
            "id":id,
            "file":file, 
            "language":language,
        },
        queue="pipeline"
        )
    return JSONResponse(status_code=200, content={"ok": True})

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = LOG_FORMAT
    log_config["formatters"]["default"]["fmt"] = LOG_FORMAT
    uvicorn.run(
        "main:app", host="0.0.0.0", port=9000, reload=True, log_config=log_config
    )