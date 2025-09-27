import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Base URL of the website to scrape
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

# List to store scraped books
books = []

# Scrape first 5 pages
for page in range(1, 6):
    url = BASE_URL.format(page)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request fails
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch page {page}: {e}")
        continue
    
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

# Ensure 'data' folder exists
os.makedirs("data", exist_ok=True)

# Save scraped data to CSV
df = pd.DataFrame(books)
df.to_csv("data/books.csv", index=False)

print("✅ Scraping completed. Data saved to data/books.csv")
