from celery import Celery  # type: ignore
from celery.schedules import crontab  # type: ignore

from src.api.deps import get_redis_url

redis_url = get_redis_url()
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)

# WORKER
# add more tasks roots here
celery_app.autodiscover_tasks(["src.core.tasks"], related_name="tasks", force=True)

# BEAT
celery_app.conf.beat_schedule = {
    # Executes every 3rd minute
    "hello-every-third-minute": {
        "task": "src.core.tasks.hello_world_task",
        "schedule": crontab(minute="*/3"),
    },
}
