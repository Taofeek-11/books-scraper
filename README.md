# 📚 Books E-Commerce Scraper

## Overview
A Selenium web scraper that extracts 1000 books
from books.toscrape.com across 50 pages.

## Tools Used
- Python 3.13
- Selenium WebDriver
- ChromeDriver (via webdriver-manager)
- Pandas
- CSV

## Data Collected
| Column | Description |
|---|---|
| title | Book title |
| categories | Breadcrumb category path |
| upc | Universal Product Code |
| price | Price in GBP |
| stock | Availability and count |
| rating | Star rating (One-Five) |
| type | Product type |

## How to Run
1. Clone the repository
2. Install dependencies:
pip install -r requirements.txt
3. Run the scraper:
python scraper.py

## Project Structure
books-scraper/
├── scraper.py
├── requirements.txt
├── README.md
└── Scraped_books.csv
