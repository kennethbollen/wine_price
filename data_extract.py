#What impacts the price of wine?

#dependent variable (y): Base Price

#independent variables (x): Grape, Country, Region, Vintage

import requests
import bs4
import re
import json

wine_url = []
country_url = []
grape_url = []
regions_url = []
wine_prices = {}
true = 1
false = 0

url = 'https://www.majestic.co.uk/wine'
req = requests.get(url)
req.raise_for_status()
soup = bs4.BeautifulSoup(req.text)

#find all the grapes
for links in soup.find_all('h3'):
    if links.text == 'Browse Wines':
        wines = str("\\") + str(links.findNext('ul'))
        print('Gathering wine URLs...')
        print()
        
soup2 = bs4.BeautifulSoup(wines, "html.parser")
lis = soup2.find_all('a')
for li in lis:
    wine_url.append("https://www.majestic.co.uk" + li['href'])

#find all the countries
for links in soup.find_all('h3'):
    if links.text == 'Popular Countries':
        countries = str("\\") + str(links.findNext('ul'))
        print('Gathering countries URLs...')
        print()
        
soup3 = bs4.BeautifulSoup(countries, 'html.parser')
lis2 = soup3.find_all('a')
for li in lis2:
    country_url.append("https://www.majestic.co.uk" + li['href'])
    
#find all the grapes
for links in soup.find_all('h3'):
    if links.text == 'Popular Grapes':
        grapes = str("\\") + str(links.findNext('ul'))
        print('Gathering grapes URLs...')
        print()
        
soup4 = bs4.BeautifulSoup(grapes, 'html.parser')
lis3 = soup4.find_all('a')
for li in lis3:
    grape_url.append("https://www.majestic.co.uk" + li['href'])
    
#find all the regions
for links in soup.find_all('h3'):
    if links.text == 'Popular Regions':
        regions = str("\\") + str(links.findNext('ul'))
        print('Gathering region URLs...')
        print()
        
soup5 = bs4.BeautifulSoup(regions, 'html.parser')
lis4 = soup5.find_all('a')
for li in lis4:
    regions_url.append("https://www.majestic.co.uk" + li['href'])

#Loop through the wine urls
for wine in wine_url:
    print('Fetching data from ', wine)
    print()
    req = requests.get(wine)
    req.raise_for_status()
    wine_soup = bs4.BeautifulSoup(req.text)
    #create a prices list to help extract unneeded html from the wine data
    prices = []
    #html contains additional json script that needs to be stripped to extract relevant data
    strip_text = "MajesticDataLayer.page.addPageName("+'"PLP");\n      MajesticDataLayer.product.addSearchResultData(['
    print('searching for wine data...')
    print()
    for script in soup.find_all('script'):
        #search the html for the script that contains the wine data
        if re.search('MajesticDataLayer.', script.text) is not None:
            prices.append(script.text)
    #relevant data will be contained in price[1], need to remove other part of the script
    price = prices[1]
    #strip off additional json code from data
    price = price.strip(strip_text)
    price = price.strip('],')
    #breakdown product data into individual datasets to allow it to be processed as a dict
    print('breaking down wine data into individual data sets...')
    print()
    price = price.split(',{')
    split_wines = []
    for x in range(len(price)):
        if x == 0:
            split_wines.append(price[x])
        else:
            split_wines.append('{' + price[x])
    #convert each element of the list into one dict with relevant data (product name and price) 
    for wine in split_wines:
        a = json.loads(wine)
        for k, v in a.items():
            wine_prices[a['productName']] = {'price': a['pricesCurrent']['prices']['basePrice']}
 
#next_page = soup2.find('link', rel='next')['href']
