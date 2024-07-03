from playwright.sync_api import sync_playwright
import json
import time
import random

# Search query and configuration
search_query = "Sneakers"
total_pages = 4
Headless = False

# Prepare search query for URL
search_query = '+'.join(search_query.split())

finalData = []

# Function to parse results and extract title, price, and sold
def parsing_results(page):
    products = page.query_selector_all('.gridItem--Yd0sa')
    for product in products:
        try:
            title_element = product.query_selector('.title-wrapper--IaQ0m')
            title = title_element.inner_text()
        except Exception as e:
            print(f"Error fetching title: {e}")
            title = None
        
        try:
            price_element = product.query_selector('.current-price--Jklkc')
            price = price_element.inner_text()
        except Exception as e:
            print(f"Error fetching price: {e}")
            price = None
        
        try:
            sold_element = product.query_selector('div[class*=rating-wrapper] > div:nth-child(3)')
            if sold_element:
                sold = sold_element.inner_text()
            else:
                print("sold_element not found")
                sold = None
        except Exception as e:
            print(f"Error fetching sold: {e}")
            sold = None
        
        finalData.append({
            'Title': title,
            'Price': price,
            'sold': sold
        })

# Launch Playwright and start scraping
with sync_playwright() as p:
    browser = p.chromium.launch(headless=Headless)
    page = browser.new_page()

    try:
        for page_number in range(1, total_pages + 1):
            link = f"https://www.daraz.com.np/catalog/?q={search_query}&from=input&spm=a2a0e.searchlistcategory.search.go.46a9e54asrpwYL&page={page_number}"
            
            try:
                # Increase timeout and use 'networkidle' wait condition
                page.goto(link, timeout=200000)
                page.wait_for_load_state('networkidle')
            except Exception as e:
                print(f"Error navigating to {link}: {e}")
                continue
            
            # Parse and collect data
            parsing_results(page)

    finally:
        # Save collected data to a JSON file
        output_file = 'output4.json'
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(finalData, json_file, ensure_ascii=False, indent=4)

        # Close browser after scraping is done
        try:
            browser.close()
        except Exception as e:
            print(f"Error closing browser: {e}")
        else:
            print(f"Data saved to {output_file} successfully.")
