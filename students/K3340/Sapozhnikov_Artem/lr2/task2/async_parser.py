import asyncio
import time
import aiohttp

from bs4 import BeautifulSoup
from db import save_transaction


URLS = [
    "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    "https://books.toscrape.com/catalogue/soumission_998/index.html",
    "https://books.toscrape.com/catalogue/sharp-objects_997/index.html",
    "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html",
]


def parse_price(price_text):
    cleaned = (
        price_text
        .replace("£", "")
        .replace("Â", "")
        .strip()
    )

    return float(cleaned)


async def parse_and_save(session, url):
    async with session.get(url, timeout=10) as response:
        html = await response.text(encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")

    book_title = soup.find("h1").get_text(strip=True)
    title = f"Покупка книги: {book_title}"

    price_text = soup.find("p", class_="price_color").get_text(strip=True)
    amount = parse_price(price_text)

    comment = f"Спарсено со страницы: {url}"

    save_transaction(title, amount, comment)

    print(f"[async] {title} — {amount}")


async def main():
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [
            parse_and_save(session, url)
            for url in URLS
        ]

        await asyncio.gather(*tasks)

    print("Async time:", time.time() - start_time)


if __name__ == "__main__":
    asyncio.run(main())