#What impacts the price of wine?

#dependent variable (y): Base Price

#independent variables (x): Grape, Country, Region, Vintage


import requests
import bs4


url = 'https://www.majestic.co.uk/wine'
req = requests.get(url)
req.raise_for_status()
soup = bs4.BeautifulSoup(req.text)

for link in soup.find_all('a', href=True):
		if re.search("Maternity Services Monthly Statistics, England.", link.text) is not None:
			maternity_hyplink.append(link['href'])
			print("Collecting Hyperlink: %s" %link.text)
			print()
