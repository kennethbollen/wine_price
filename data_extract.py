#What impacts the price of wine?

#dependent variable (y): Base Price

#independent variables (x): Grape, Country, Region, Vintage

import requests
import bs4

wine_url = []
country_url = []
grape_url = []
regions_url = []

url = 'https://www.majestic.co.uk/wine'
req = requests.get(url)
req.raise_for_status()
soup = bs4.BeautifulSoup(req.text)

#find all the grapes
for links in soup.find_all('h3'):
    if links.text == 'Browse Wines':
        wines = str("\\") + str(links.findNext('ul'))
        
soup2 = bs4.BeautifulSoup(wines, "html.parser")
for li in lis:
    wine_url.append("https://www.majestic.co.uk" + li['href'])

#find all the countries
for links in soup.find_all('h3'):
    if links.text == 'Popular Countries':
        countries = str("\\") + str(links.findNext('ul'))
        
soup3 = bs4.BeautifulSoup(countries, 'html.parser')
lis2 = soup3.find_all('a')
for li in lis2:
    country_url.append("https://www.majestic.co.uk" + li['href'])
    
#find all the grapes
for links in soup.find_all('h3'):
    if links.text == 'Popular Grapes':
        grapes = str("\\") + str(links.findNext('ul'))
        
soup4 = bs4.BeautifulSoup(grapes, 'html.parser')
lis3 = soup4.find_all('a')
for li in lis3:
    grape_url.append("https://www.majestic.co.uk" + li['href'])
    
#find all the regions
for links in soup.find_all('h3'):
    if links.text == 'Popular Regions':
        regions = str("\\") + str(links.findNext('ul'))
        
soup5 = bs4.BeautifulSoup(regions, 'html.parser')
lis4 = soup5.find_all('a')
for li in lis4:
    regions_url.append("https://www.majestic.co.uk" + li['href'])

#Loop through the wine urls
for wine in wine_ur:
    req = requests.get(wine)
    req.raise_for_status()
    wine_soup = bs4.BeautifulSoup(req.text)
    prices = []
    strip_string = "MajesticDataLayer.page.addPageName("+'"PLP");\n      MajesticDataLayer.product.addSearchResultData(['
    for script in soup.find_all('script'):
        if re.search('MajesticDataLayer.', script.text) is not None:
            prices.append(script.text)
    price = prices[1]
    price = price.strip(strip_text)
    #next trick is to convert string into dict
