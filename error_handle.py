import requests  # Fetch website content
from bs4 import BeautifulSoup  # Extract structured data from webpages
import pandas as pd  # Store data and save to CSV
import logging  # Log errors instead of stopping execution

# Setup logging to track errors
logging.basicConfig(filename="scraping_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to safely fetch webpage content and handle errors
def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)  # Fetch the page with a timeout
        response.raise_for_status()  # Check if the request was successful
        return response  # Return the page content if everything is fine
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")  # Log the error instead of stopping
        return None  # Return None so the program doesn’t crash

# Function to process each book entry, ensuring missing data is handled
def process_books(book_list, books):
    for book in book_list:
        try:
            # Extract book details safely
            title_tag = book.h3.a
            price_tag = book.select_one('p.price_color')
            rating_tag = book.select_one('p.star-rating')
            availability_tag = book.select_one('p.instock.availability')
            product_url_tag = book.h3.a

            # If any data is missing, log the error and skip the book
            if None in [title_tag, price_tag, rating_tag, availability_tag, product_url_tag]:
                logging.warning("Skipping a book due to missing data.")
                continue  # Move to the next book without crashing

            # Extract and format price correctly, ensuring proper encoding
            price_text = price_tag.text.strip().encode('latin1').decode('utf-8')  # Fix encoding issues
            price = price_text.replace("Â", "").replace("�", "").replace("£", "").strip()

            # Convert to float safely
            try:
                price = float(price)
            except ValueError:
                logging.warning(f"Skipping book due to invalid price format: {price_text}")
                continue

            # Extract remaining details
            title = title_tag['title']
            rating_class = rating_tag['class'][1]  # Gets rating as a word (One, Two, etc.)
            availability = availability_tag.text.strip()
            product_url = product_url_tag['href']

            # Store book data in a list
            books.append({
                'Title': title,
                'Price': price,  # Numeric price
                'Currency': '£',  # Store currency separately
                'Rating': rating_class,
                'Availability': 'In stock' if 'In stock' in availability else 'Out of stock',
                'Product URL': product_url
            })
        except Exception as e:
            logging.error(f"Skipping book due to error: {e}")  # Logs error instead of stopping execution

# Main function that integrates error handling and book extraction
def scrape():
    books = []
    page_number = 1

    while len(books) < 1000:  # Stop once ~1000 books are collected
        url = f"http://books.toscrape.com/catalogue/page-{page_number}.html"

        response = fetch_page(url)  # Fetch the page safely

        if response is None:
            break  # Stop if the page couldn't be retrieved

        soup = BeautifulSoup(response.text, 'html.parser')
        book_list = soup.select('article.product_pod')  # Find all books on the page

        if not book_list:
            print("No more books found.")
            break  # Exit loop if no more books exist

        process_books(book_list, books)  # Extract book details and handle errors

        page_number += 1  # Move to the next page

    return books  # Return final book list

# Convert book data into a structured format and save to CSV
df = pd.DataFrame(scrape())

if not df.empty:
    df.to_csv('books_data.csv', index=False)
    print("Data saved successfully.")
else:
    print("No data found. Check logs for errors.")
