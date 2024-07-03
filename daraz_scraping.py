# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup
# import pandas as pd

# # Search query and configuration
# search_query = "Sneakers"  # Enter the product you want to search
# total_pages = 5             # Total pages you want to scrape
# Headless = False            # Set to True for headless browsing

# # Prepare search query for URL
# search_query = '+'.join(search_query.split())

# finalData = []

# # Function to parse results from BeautifulSoup object
# def parsing_results(soup):
#     allResults = soup.find_all('div', class_='c3e8SH')  # Update class based on Daraz's HTML structure
#     for card in allResults:
#         try:
#             cardLink = card.find('a', class_='c16H9d').get('href')  # Update class based on Daraz's HTML structure
#         except:
#             cardLink = None
        
#         try:
#             heading = card.find('div', class_='c16H9d').get_text(strip=True)  # Update class based on Daraz's HTML structure
#         except:
#             heading = None
        
#         try:
#             price = card.find('div', class_='c16H9d').get_text(strip=True)  # Update class based on Daraz's HTML structure
#         except:
#             price = None
        
#         finalData.append({
#             'Item link': cardLink,
#             'Heading': heading,
#             'Price': price
#         })

# # Launch Playwright and start scraping
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=Headless)
#     page = browser.new_page()

#     for page_number in range(1, total_pages + 1):
#         link = f"https://www.daraz.com.np/catalog/?q={search_query}&from=input&spm=a2a0e.searchlistcategory.search.go.46a9e54asrpwYL&page={page_number}"
#         page.goto(link, timeout=100000)
        
#         # Get page content as HTML
#         html_content = page.content()
#         soup = BeautifulSoup(html_content, 'html.parser')
#         parsing_results(soup)

# # Convert data to DataFrame and save to Excel
# df = pd.DataFrame(finalData)
# df.to_excel('output.xlsx', index=False)

# # Close browser after scraping is done
# browser.close()


from playwright.sync_api import sync_playwright
import json

# Search query and configuration
search_query = "Sneakers"  # Enter the product you want to search
total_pages = 4            # Total pages you want to scrape
Headless = False            # Set to True for headless browsing

# Prepare search query for URL
search_query = '+'.join(search_query.split())

finalData = []

# Function to parse results and extract title and price
def parsing_results(page):
    products = page.query_selector_all('.title-wrapper--IaQ0m')  # Update class based on Daraz's HTML structure
    for product in products:
        title = product.inner_text()
        price_element = product.parent().query_selector('.current-price--Jklkc')  # Update class based on Daraz's HTML structure
        price = price_element.inner_text()
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
        output_file = 'output1.json'
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(finalData, json_file, ensure_ascii=False, indent=4)

        # Close browser after scraping is done
        try:
            browser.close()
        except Exception as e:
            print(f"Error closing browser: {e}")
        else:
            print(f"Data saved to {output_file} successfully.")

