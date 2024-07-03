from autoscraper import AutoScraper


daraz_url = "https://www.daraz.com.np/catalog/?q=Sneakers"

wanted_list = ["Rs.446","Black Ankle Cut Printed Bandana Synthetic Round Toe Lace-Up Closure Medium Width Casual/Sport Sneakers For Men And Women" ]
scraper = AutoScraper()
result = scraper.build(daraz_url,wanted_list)
print(result)