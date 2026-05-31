from fastapi import FastAPI
from pydantic import BaseModel

from app.parser.parser_service import parse_urls

app = FastAPI(title="Parser API")


class ParseRequest(BaseModel):
    urls: list[str] | None = None


@app.post("/parse")
def parse(request: ParseRequest):
    result = parse_urls(request.urls)
    return {
        "status": "completed",
        "items": result
    }