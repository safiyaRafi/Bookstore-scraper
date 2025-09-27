import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

books = []

for page in range(1, 6):  # scrape first 5 pages
    url = BASE_URL.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    for book in soup.select("article.product_pod"):
        title = book.h3.a['title']
        price = book.select_one("p.price_color").text
        availability = book.select_one("p.instock.availability").text.strip()
        books.append({
            "Title": title,
            "Price": price,
            "Availability": availability
        })

# Save to CSV
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(books)
df.to_csv("data/books.csv", index=False)
print("✅ Scraping completed. Data saved to data/books.csv")
