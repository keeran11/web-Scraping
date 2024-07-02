from playwright.sync_api import sync_playwright  #importing the playwright library for synchronous operation.
import json

# Search query and configuration
search_query = "Sneakers"  
total_pages = 4             # 4 pages  scrape garnu xa hami lai
Headless = False            # Set to True for headless browsing

# Prepare search query for URL
search_query = '+'.join(search_query.split())

finalData = []

# Function to parse results and extract title and price
def parsing_results(page):
    products = page.query_selector_all('.gridItem--Yd0sa')  # Update class based on Daraz's HTML structure
    for product in products:
        try:
            title_element = product.query_selector('.title-wrapper--IaQ0m')  # Update class based on Daraz's HTML structure for title
            title = title_element.inner_text()
        except Exception as e:
            title = None
        
        try:
            price_element = product.query_selector('.current-price--Jklkc')  # Update class based on Daraz's HTML structure for price
            price = price_element.inner_text()
        except Exception as e:
            price = None
        
        finalData.append({
            'Title': title,
            'Price': price
        })

# Launch Playwright and start scraping
with sync_playwright() as p:
    browser = p.chromium.launch(headless=Headless)
    page = browser.new_page()

    try:
        for page_number in range(1, total_pages + 1):
            link = f"https://www.daraz.com.np/catalog/?q={search_query}&from=input&spm=a2a0e.searchlistcategory.search.go.46a9e54asrpwYL&page={page_number}"
            
            try:
                # Attempt to navigate to the page with extended timeout
                page.goto(link, timeout=100000)
            except Exception as e:
                print(f"Error navigating to {link}: {e}")
                continue
            
            # Wait for the page content to be fully loaded
            try:
                page.wait_for_load_state('domcontentloaded')
            except Exception as e:
                print(f"Timeout waiting for page to load: {e}")
                continue
            
            # Parse and collect data
            parsing_results(page)

    finally:
        # Save collected data to a JSON file
        output_file = 'output2.json'
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(finalData, json_file, ensure_ascii=False, indent=4)

        # Close browser after scraping is done
        try:
            browser.close()
        except Exception as e:
            print(f"Error closing browser: {e}")
        else:
            print(f"Data saved to {output_file} successfully.")
