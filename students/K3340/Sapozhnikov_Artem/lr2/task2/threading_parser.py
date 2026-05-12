import threading
import time
import requests

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

def parse_and_save(url):
    response = requests.get(url, timeout=10)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    title = f"Покупка книги: {soup.find("h1").get_text(strip=True)}"

    price_text = soup.find("p", class_="price_color").get_text(strip=True)
    amount = parse_price(price_text)

    comment = f"Спарсено со страницы: {url}"

    save_transaction(title, amount, comment)

    print(f"[threading] {title} — {amount}")


if __name__ == "__main__":
    start_time = time.time()

    threads = []

    for url in URLS:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Threading time:", time.time() - start_time)