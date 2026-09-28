
import csv
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/catalogue/page-{}.html"
PAGES = range(1, 6)
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_page(page_html, page_url):
    soup = BeautifulSoup(page_html, "html.parser")
    books = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        # Full title is in the link's title attribute (the visible text is truncated)
        title = link["title"]

        # Keep only the number, e.g. "£51.77" -> 51.77
        price_text = card.select_one("p.price_color").get_text()
        price = float(re.search(r"[0-9.]+", price_text).group())

        # <p class="star-rating Three"> -> 3
        rating_classes = card.select_one("p.star-rating")["class"]
        rating = next(RATINGS[c] for c in rating_classes if c in RATINGS)

        availability = card.select_one("p.availability").get_text(strip=True)
        in_stock = availability.startswith("In stock")

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "in_stock": "true" if in_stock else "false",
            "url": urljoin(page_url, link["href"]),  # relative link -> full URL
        })
    return books


def main():
    books = []
    with requests.Session() as session:
        for page in PAGES:
            url = BASE.format(page)
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            books.extend(parse_page(resp.text, url))
            print(f"page {page}: {len(books)} books so far")

    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "in_stock", "url"])
        writer.writeheader()
        writer.writerows(books)
    print(f"Saved {len(books)} books to books.csv")


if __name__ == "__main__":
    main()
