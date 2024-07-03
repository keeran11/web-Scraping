import requests
from bs4 import BeautifulSoup

baseurl = "https://www.daraz.com.np/catalog/?q=Sneakers&_keyori=ss&from=input&spm=a2a0e.searchlistcategory.search.go.46a9e54asrpwYL"
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

r  = requests.get(baseurl, headers=headers)
soup = BeautifulSoup(r.text, "lxml")

productlinks = []

# Loop through the first 4 pages
for x in range(1, 5):
    r = requests.get(f"https://www.daraz.com.np/catalog/?q=Sneakers&page={x}", headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    
    productlist = soup.find_all("div", class_="gridItem--Yd0sa")
    
    for item in productlist:
        link = item.find('a', href=True)['href']
        productlinks.append("https:" + link)

darazlist = []

for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    
    # Print out the soup to verify the HTML structure
    # print(soup.prettify())

    try:
        name = soup.find('div', class_='title-wrapper--IaQ0m').text.strip()
    except AttributeError:
        name = None
    try:
        price = soup.find('div', class_='current-price--Jklkc').text.strip()
    except AttributeError:
        price = None

    if name and price:
        daraz = {
            'name': name,
            'price': price
        }
        darazlist.append(daraz)
        print('saving:', name, price)

# Save data to CSV file in the current directory
output_file_path = 'daraz_products.csv'
df = id.DataFrame(darazlist)
df.to_csv(output_file_path, index=False)
print(df.head(5))
