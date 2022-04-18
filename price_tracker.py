import requests
from bs4 import BeautifulSoup
import unicodedata

from send_email import send_email


HEADERS = ({'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"})


def get_product_info(url):
	page = requests.get(url, headers=HEADERS)
	soup = BeautifulSoup(page.content, features="lxml")

	#print(soup)

	try:
		title = soup.find(id='productTitle').get_text().strip()
		price_str = soup.find(id='priceblock_outprice').get_text()
	except:
		return None, None, None

	try:
		soup.select('#availability .a-color-success')[0].get_text().strip()
		available = True
	except:
		available = False

	try:
		price = unicodedata.normalize("NFKD", price_str)
		price = price.replace(',', '.').replace('$', '')
		price = float(price)
	except:
		return None, None, None

	return title, price, available

if __name__ == '__main__':
	url = "https://www.amazon.com/gp/product/B00YGZACKI"
	products = [(url, 700)]

	#print(get_product_info(url))

	products_below_limit = []
	for product_url, limit in products:
		title, price, available = get_product_info(product_url)
		if title is not None and price < limit and available:
			products_below_limit.append((url, title, price))

	if products_below_limit:
		message = "Subject: Price below limit!\n\n"
		message += "Your tracked products are below the given limit!\n\n"

		for url, title, price in products_below_limit:
			message += f"{title}\n"
			message += f"Price: {price}\n"
			message += f"{url}\n\n"

		send_email(message)
