from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os

# Lock file removal
lock_file = r'C:\Users\USER\.wdm\.wdm-lock-chromedriver-win64'
if os.path.exists(lock_file):
    os.remove(lock_file)
    print("Lock file cleared ✅")

url           = 'https://books.toscrape.com'
scraped_books = []
page_scraped  = 1
max_page      = 50
driver        = None

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    while url and page_scraped <= max_page:
        print(f"\nScraping page {page_scraped}/{max_page}: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product_pod')))

        # Collect links and next_href BEFORE navigating away
        book_elements = driver.find_elements(By.CSS_SELECTOR, 'div.image_container a')
        book_links    = [el.get_attribute('href') for el in book_elements]

        try:
            next_href = driver.find_element(By.CSS_SELECTOR, 'ul.pager li.next a').get_attribute('href')
        except:
            next_href = None

        # Visit each book detail page
        for link in book_links:
            driver.get(link)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product_main h1')))

            title        = driver.find_element(By.CSS_SELECTOR, 'div.product_main h1').text
            price        = driver.find_element(By.CSS_SELECTOR, 'div.product_main p').text
            rating       = driver.find_element(By.CSS_SELECTOR, 'p.star-rating').get_attribute('class').split()[-1]  # ✅ word only
            stock        = driver.find_element(By.CSS_SELECTOR, 'p.instock.availability').text.strip()
            upc_code     = driver.find_element(By.CSS_SELECTOR, 'table tr:nth-child(1) td').text  
            product_type = driver.find_element(By.CSS_SELECTOR, 'table tr:nth-child(2) td').text  

            breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.breadcrumb li a')
            breadcrumb = ' > '.join([t.text for t in breadcrumb_elements])

            scraped_books.append({
                'title':      title,
                'categories': breadcrumb,
                'upc':        upc_code,
                'price':      price,
                'stock':      stock,
                'rating':     rating,
                'type':       product_type
            })

            if len(scraped_books) % 10 == 0:
                print(f"Progress: {len(scraped_books)} books scraped so far")


        url = next_href if next_href else None
        page_scraped += 1


    print(f"\nScraping complete! Total books: {len(scraped_books)}")

    for idx, book in enumerate(scraped_books, start=1):
        print(f"Book {idx}: {book['title']}")
        print(f"  Categories: {book['categories']}")
        print(f"  UPC:        {book['upc']}")
        print(f"  Price:      {book['price']}")
        print(f"  Stock:      {book['stock']}")
        print(f"  Rating:     {book['rating']}")

    with open('Scraped_books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'categories', 'upc', 'price', 'stock', 'rating', 'type'])
        writer.writeheader()
        writer.writerows(scraped_books)

    print("Saved to Scraped_books.csv ✅")

finally:
    if driver:
        driver.quit()