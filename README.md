# BookScrape
Web scraping project using Python (Team: Auryn, Shravya, Shreenidhi)

## Overview  
This project scrapes book details from [Books to Scrape](http://books.toscrape.com/) using Python to analyze trends in pricing, ratings, and stock availability.  

## Objective  
- Extract **Title, Pricing, Availability, and Product URL** for approximately 1,000 books.  
- Store data in a structured CSV file (`books_data.csv`).  
- Implement error handling to manage missing data and HTTP failures.  
- Validate extracted data using a testing framework.  

## Technologies Used  
- **Programming Language**: Python  
- **Web Scraping**: Requests, BeautifulSoup  
- **Data Handling**: Pandas  
- **Logging**: Python’s logging module  
- **Storage**: CSV  

## Business Flow  
1. **Initiate Scraping** – Start from page one.  
2. **Send HTTP Request** – Validate the status code.  
3. **Extract Data** – Scrape the following details:  
   - Title  
   - Pricing  
   - Rating  
   - Availability  
   - Product URL  
4. **Handle Pagination** – Iterate through multiple pages.  
5. **Log Errors** – Manage missing fields and HTTP issues.  
6. **Store Data** – Save structured output into `books_data.csv`.  
7. **Perform Testing** – Verify data integrity and format.  

## Implementation and Code Structure  
### Key Functions  
- `fetch_page(url)`  
   - Sends an HTTP request  
   - Validates response success  
   - Handles exceptions  
- `process_books(book_list, books)`  
   - Extracts book details  
   - Structures data into a dictionary  
   - Manages rating conversion  
- `scrape()`  
   - Iterates through all pages  
   - Calls helper functions  
   - Stops execution on failure  
- `save_to_csv(books)`  
   - Converts data into a **structured DataFrame** using Pandas  
   - Saves output into `books_data.csv`  

## Error Handling  
- **Missing Data** – Logs error and skips invalid books.  
- **HTTP Errors** – Retries requests and records failures in `scraping_errors.log`.  
- **Unexpected Rating Format** – Defaults to `None` and logs the issue.  
- **Empty Response** – Stops pagination process.  

## Data Storage Structure (`books_data.csv`)  
| Title                   | Price  | Rating | Availability | Product URL                     |  
|-------------------------|--------|--------|--------------|---------------------------------|  
| A Light in the Attic    | 51.77  | Three  | In stock     | `a-light-in-the-attic_1000/index.html` |  

## Testing and Validation  
### Test Cases Covered  
1. **Verify CSV File Exists** (`os.path.isfile("books_data.csv")`).  
2. **Confirm Correct File Format** (`.csv`).  
3. **Validate Column Structure** (Title, Price, Rating, Availability, URL).  
4. **Ensure Correct Data Types** (Price stored as `float`).  
5. **Handle Missing or Invalid Data** (`df.isnull().sum()`).  

## Challenges and Solutions  
1. **Handling Timeouts** – Added request timeout (`timeout=10`).  
2. **Rating Conversion Errors** – Used dictionary mapping (`One -> 1, Two -> 2`).  
3. **Avoiding Crashes** – Wrapped functions in try-except blocks to prevent failures.  
