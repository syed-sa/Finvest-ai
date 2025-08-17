from src.worker import celery_app


# tasks.py - Celery task definitions for the core application.
# This module contains background task implementations used by the application.


@celery_app.task  # type: ignore
def hello_world_task() -> None:
    print("Hello World")
