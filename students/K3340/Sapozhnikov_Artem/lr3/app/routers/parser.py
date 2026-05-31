import os
import requests

from fastapi import APIRouter
from celery.result import AsyncResult

from app.parser.tasks import parse_books_task
from app.celery_app import celery_app

router = APIRouter(prefix="/parser", tags=["Parser"])

PARSER_API_URL = os.getenv("PARSER_API_URL", "http://parser_api:8001")


@router.post("/sync")
def run_parser_sync(urls: list[str] | None = None):
    response = requests.post(
        f"{PARSER_API_URL}/parse",
        json={"urls": urls},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


@router.post("/async")
def run_parser_async(urls: list[str] | None = None):
    task = parse_books_task.delay(urls)
    return {
        "status": "started",
        "task_id": task.id,
    }


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None,
    }