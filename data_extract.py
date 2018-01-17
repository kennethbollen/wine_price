#What impacts the price of wine?

#dependent variable (y): Base Price

#independent variables (x): Grape, Country, Region, Vintage


import requests
import bs4


url = 'https://www.majestic.co.uk/wine'
req = requests.get(url)
req.raise_for_status()
soup = bs4.BeautifulSoup(req.text)

for link in soup.find_all('h3'):
    if link.text == 'Browse Wines':
        for tag in link.findNext('ul'):
            tag = str(tag)
            wines.append(tag)
