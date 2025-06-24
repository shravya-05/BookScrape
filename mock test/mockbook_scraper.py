import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/"

# utility function to convert rating class to number
def rating(rating_class):
    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    for r in ratings:
        if r in rating_class:
            return ratings[r]
    return 0

# function to scrape all available book data
def scrape():
    books = []
    page_number = 1

    while True:
        url = f"{BASE_URL}page-{page_number}.html"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"No more pages to scrape. Total pages scraped: {page_number - 1}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        book_list = soup.select('article.product_pod')

        # if no books found on the page, stop scraping
        if not book_list:
            print(f"No more books found on page {page_number}.")
            break

        for book in book_list:
            title = book.h3.a['title']
            price = book.select_one('p.price_color').text.strip()
            rating_class = book.select_one('p.star-rating')['class']
            rate = rating(rating_class)
            availability = book.select_one('p.instock.availability').text.strip()
            product_relative_url = book.h3.a['href']
            product_url = urljoin(BASE_URL, product_relative_url)

            books.append({
                'Title': title,
                'Price': price,
                'Rating': rate,
                'Availability': 'In stock' if 'In stock' in availability else 'Out of stock',
                'Product URL': product_url
            })

        page_number += 1

    return books



# scrape and save to CSV
book_data = scrape()
df = pd.DataFrame(book_data)
#remove the index assigned by to_csv operation by default
df.to_csv('books_data.csv', index=False)