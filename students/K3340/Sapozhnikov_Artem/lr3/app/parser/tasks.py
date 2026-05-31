from app.celery_app import celery_app
from app.parser.parser_service import parse_urls


@celery_app.task(name="parse_books_task")
def parse_books_task(urls: list[str] | None = None):
    return parse_urls(urls)