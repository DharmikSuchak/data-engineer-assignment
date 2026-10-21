"""Print products from the first MD Computers search results page as CSV."""

import argparse
import csv
import sys

from bs4 import BeautifulSoup
from curl_cffi import requests


SEARCH_URL = "https://mdcomputers.in/"


def extract_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for card in soup.select("#content .all-product-wrapper .product-grid-item"):
        link = card.select_one("h3.product-entities-title a[href]")
        price = card.select_one(".price .ins .amount") or card.select_one(
            ".price .amount"
        )
        if link:
            products.append(
                (
                    link.get_text(" ", strip=True),
                    price.get_text(" ", strip=True) if price else "",
                    link["href"],
                )
            )
    return products


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("search_term", help="product search term")
    args = parser.parse_args()

    try:
        response = requests.get(
            SEARCH_URL,
            params={"route": "product/search", "search": args.search_term},
            impersonate="chrome",
            timeout=20,
        )
        if "<title>Attention Required! | Cloudflare" in response.text:
            raise ValueError("MD Computers blocked this automated request")
        response.raise_for_status()
        products = extract_products(response.text)
    except (requests.exceptions.RequestException, ValueError) as error:
        parser.exit(1, f"Could not read search results: {error}\n")

    if not products and "no product that matches" not in response.text.lower():
        parser.exit(1, "No product cards found; the page layout may have changed.\n")

    writer = csv.writer(sys.stdout)
    writer.writerow(("name", "price", "url"))
    writer.writerows(products)


if __name__ == "__main__":
    main()
