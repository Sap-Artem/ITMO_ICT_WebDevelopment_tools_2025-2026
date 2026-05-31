import requests
from bs4 import BeautifulSoup
from sqlalchemy import text
from sqlmodel import Session

from app.db.connection import engine


DEFAULT_URLS = [
    "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    "http://books.toscrape.com/catalogue/soumission_998/index.html",
    "http://books.toscrape.com/catalogue/sharp-objects_997/index.html",
    "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html",
]


def parse_price(price_text: str) -> float:
    return float(
        price_text
        .replace("£", "")
        .replace("Â", "")
        .strip()
    )


def save_transaction(title: str, amount: float, comment: str, user_id: int = 2, category_id: int = 2):
    with Session(engine) as session:
        session.execute(
            text("""
                INSERT INTO "transaction"
                (title, amount, transaction_type, comment, user_id, category_id)
                VALUES (:title, :amount, :transaction_type, :comment, :user_id, :category_id)
            """),
            {
                "title": title[:255],
                "amount": amount,
                "transaction_type": "expense",
                "comment": comment,
                "user_id": user_id,
                "category_id": category_id,
            }
        )
        session.commit()


def parse_one_url(url: str) -> dict:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    book_title = soup.find("h1").get_text(strip=True)
    price_text = soup.find("p", class_="price_color").get_text(strip=True)

    title = f"Покупка книги: {book_title}"
    amount = parse_price(price_text)
    comment = f"Спарсено со страницы: {url}"

    save_transaction(title, amount, comment)

    return {
        "title": title,
        "amount": amount,
        "url": url,
    }


def parse_urls(urls: list[str] | None = None) -> list[dict]:
    urls = urls or DEFAULT_URLS
    return [parse_one_url(url) for url in urls]