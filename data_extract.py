#!python3

import requests
import bs4
import re
import json
import pandas as pd
import numpy as np

#all the relevant urls containting the data
wine_url = []
country_url = []
grape_url = []
regions_url = []
#used to transform j-query code into python dicts
split_wines = []
wine_prices = {}
split_country = []
country_prices = {}
split_grape = []
grape_prices = {}
split_region = []
region_prices = {}
#category of wine country for further analysis
old_world = ['spanish', 'portuguese', 'french', 'italian']
new_world = ['australian','argentinian', 'new-zealand', 'south-african','chilean']
world = []
country_to_world = []
#datasets scrapped contain true and false variables that need to be handled in order to import the data
true = 1
false = 0
#set the target variable
y = []
#transform continous data price into cat
price_cat = []

url = 'https://www.majestic.co.uk/wine'
req = requests.get(url)
req.raise_for_status()
soup = bs4.BeautifulSoup(req.text, 'lxml')

#find all the grapes
for links in soup.find_all('h3'):
    if links.text == 'Browse Wines':
        wines = str("\\") + str(links.findNext('ul'))
        print('Gathering wine URLs...')
        print()
        
soup2 = bs4.BeautifulSoup(wines, "html.parser")
lis = soup2.find_all('a')
for li in lis:
    #avoid dupilication and overwrite of data
    if li['href'] == '/wine':
        continue
    else:
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
    #avoid dupilication and overwrite of data
    if li['href'] == '/wine':
        continue
    else:
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
    #count how many web pages to loop
    num_pages = []
    for line in wine_soup.find_all('a', {'class': 'button button--small'}):
        #this will grab a few non-int items and therefore need to handle for it
        try:
            a = int(line.text)
            num_pages.append(a)
        except:
            print()
    #some pages will only have one page and the max function won't work, this is a error handle for that        
    try:        
        last_page = max(num_pages)
    except:
        last_page = 1
    #loop through all the web pages    
    for i in range(last_page):
        sub_url = wine + '?pageNum=%s&pageSize=12' % str(i)
        sub_req = requests.get(sub_url)
        sub_req.raise_for_status()
        sub_soup = bs4.BeautifulSoup(sub_req.text)
        prices = []
        #html contains additional json script that needs to be stripped to extract relevant data
        strip_text = "MajesticDataLayer.page.addPageName("+'"PLP");\n      MajesticDataLayer.product.addSearchResultData(['
        print('searching for wine data...')
        print()
        for script in sub_soup.find_all('script'):
            #search the html for the script that contains the wine data
            if re.search('MajesticDataLayer.', script.text) is not None:
                prices.append(script.text)
        #relevant data will be contained in price[1], need to remove other part of the script
        prices = prices[1]
        #strip off additional json code from data
        prices = prices.strip(strip_text)
        prices = prices.strip('],')
        #breakdown product data into individual datasets to allow it to be processed as a dict
        print('breaking down wine data into individual data sets...')
        print()
        prices = prices.split(',{')
        for i in range(len(prices)):
            #remove the the end curly bracket in order to append extra data
            prices[i] = prices[i][:-1]
        #add a data tag to know what type of wine this is
        tag_wine = wine.replace('https://www.majestic.co.uk/','')
        try:
            tag_wine = tag_wine.replace('-',' ')
        except:
            print('no hypen to remove...')
            print()
        print('adding data tag...')
        print()
        for x in range(len(prices)):
            #all the dicts in the list will have a opening curly bracket missing because of the split except the first dict
            if x == 0:
                prices[x] = prices[x] + ', "wine_type":"' + tag_wine + '"}'
            else:
                prices[x] = '{' + prices[x] + ', "wine_type":"' + tag_wine + '"}'
        print('Creating wine list with prices...')
        print()
        #Using two different lists to capture the wine data as one list will be used to prep the data and the other to store the data
        for x in prices:
            split_wines.append(x)
            
#convert each element of the list into one dict with relevant data (product name and price) 
for wine_str in split_wines:
    print('Converting wine list into dict...')
    print()
    try:
        a = json.loads(wine_str)
        for k, v in a.items():
            wine_prices[a['productName']] = {'price': a['pricesCurrent']['prices']['basePrice'],'positive_rating': a['productFamily']['positiveRatings'],'num_ratings': a['productFamily']['allRatings'],'wine_type': a['wine_type']}
    except:
        print()

#Loop through the country urls
for country in country_url:
    print('Fetching data from ', country)
    print()
    req = requests.get(country)
    req.raise_for_status()
    country_soup = bs4.BeautifulSoup(req.text)
    #count how many web pages to loop
    num_pages = []
    for line in country_soup.find_all('a', {'class': 'button button--small'}):
        #this will grab a few non-int items and therefore need to handle for it
        try:
            a = int(line.text)
            num_pages.append(a)
        except:
            print()
    #some pages will only have one page and the max function won't work, this is a error handle for that        
    try:        
        last_page = max(num_pages)
    except:
        last_page = 1
    #loop through all the web pages    
    for i in range(last_page):
        sub_url = country + '?pageNum=%s&pageSize=12' % str(i)
        sub_req = requests.get(sub_url)
        sub_req.raise_for_status()
        sub_soup = bs4.BeautifulSoup(sub_req.text)
        prices = []
        #html contains additional json script that needs to be stripped to extract relevant data
        strip_text = "MajesticDataLayer.page.addPageName("+'"PLP");\n      MajesticDataLayer.product.addSearchResultData(['
        print('searching for country data...')
        print()
        for script in sub_soup.find_all('script'):
            #search the html for the script that contains the country data
            if re.search('MajesticDataLayer.', script.text) is not None:
                prices.append(script.text)
        #relevant data will be contained in price[1], need to remove other part of the script
        prices = prices[1]
        #strip off additional json code from data
        prices = prices.strip(strip_text)
        prices = prices.strip('],')
        #breakdown product data into individual datasets to allow it to be processed as a dict
        print('breaking down country data into individual data sets...')
        print()
        prices = prices.split(',{')
        for i in range(len(prices)):
            #remove the the end curly bracket in order to append extra data
            prices[i] = prices[i][:-1]
        #add a data tag to know what type of country this is
        tag_country = country.replace('https://www.majestic.co.uk/','')
        try:
            tag_country = tag_country.replace('-wine',' ')
        except:
            print('no hypen to remove...')
            print()
        print('adding data tag...')
        print()
        for x in range(len(prices)):
            #all the dicts in the list will have a opening curly bracket missing because of the split except the first dict
            if x == 0:
                prices[x] = prices[x] + ', "country":"' + tag_country + '"}'
            else:
                prices[x] = '{' + prices[x] + ', "country":"' + tag_country + '"}'
        print('Creating country list with prices...')
        print()
        #Using two different lists to capture the country data as one list will be used to prep the data and the other to store the data
        for x in prices:
            split_country.append(x)
            
#convert each element of the list into one dict with relevant data (product name and price) 
for country_str in split_country:
    print('Converting country list into dict...')
    print()
    try:
        a = json.loads(country_str)
        for k, v in a.items():
            country_prices[a['productName']] = {'price': a['pricesCurrent']['prices']['basePrice'],'positive_rating': a['productFamily']['positiveRatings'],'num_ratings': a['productFamily']['allRatings'],'country': a['country']}
    except:
        print()
        
#Loop through the grape urls
for grape in grape_url:
    print('Fetching data from ', grape)
    print()
    req = requests.get(grape)
    req.raise_for_status()
    grape_soup = bs4.BeautifulSoup(req.text)
    #count how many web pages to loop
    num_pages = []
    for line in grape_soup.find_all('a', {'class': 'button button--small'}):
        #this will grab a few non-int items and therefore need to handle for it
        try:
            a = int(line.text)
            num_pages.append(a)
        except:
            print()
    #some pages will only have one page and the max function won't work, this is a error handle for that        
    try:        
        last_page = max(num_pages)
    except:
        last_page = 1
    #loop through all the web pages    
    for i in range(last_page):
        sub_url = grape + '?pageNum=%s&pageSize=12' % str(i)
        sub_req = requests.get(sub_url)
        sub_req.raise_for_status()
        sub_soup = bs4.BeautifulSoup(sub_req.text)
        prices = []
        #html contains additional json script that needs to be stripped to extract relevant data
        strip_text = "MajesticDataLayer.page.addPageName("+'"PLP");\n      MajesticDataLayer.product.addSearchResultData(['
        print('searching for grape data...')
        print()
        for script in sub_soup.find_all('script'):
            #search the html for the script that contains the grape data
            if re.search('MajesticDataLayer.', script.text) is not None:
                prices.append(script.text)
        #relevant data will be contained in price[1], need to remove other part of the script
        prices = prices[1]
        #strip off additional json code from data
        prices = prices.strip(strip_text)
        prices = prices.strip('],')
        #breakdown product data into individual datasets to allow it to be processed as a dict
        print('breaking down grape data into individual data sets...')
        print()
        prices = prices.split(',{')
        for i in range(len(prices)):
            #remove the the end curly bracket in order to append extra data
            prices[i] = prices[i][:-1]
        #add a data tag to know what type of grape this is
        tag_grape = grape.replace('https://www.majestic.co.uk/','')
        try:
            tag_grape = tag_grape.replace('-',' ')
        except:
            print('no hypen to remove...')
            print()
        print('adding data tag...')
        print()
        for x in range(len(prices)):
            #all the dicts in the list will have a opening curly bracket missing because of the split except the first dict
            if x == 0:
                prices[x] = prices[x] + ', "grape":"' + tag_grape + '"}'
            else:
                prices[x] = '{' + prices[x] + ', "grape":"' + tag_grape + '"}'
        print('Creating grape list with prices...')
        print()
        #Using two different lists to capture the grape data as one list will be used to prep the data and the other to store the data
        for x in prices:
            split_grape.append(x)
            
#convert each element of the list into one dict with relevant data (product name and price) 
for grape_str in split_grape:
    print('Converting grape list into dict...')
    print()
    try:
        a = json.loads(grape_str)
        for k, v in a.items():
            grape_prices[a['productName']] = {'price': a['pricesCurrent']['prices']['basePrice'],'positive_rating': a['productFamily']['positiveRatings'],'num_ratings': a['productFamily']['allRatings'],'grape': a['grape']}
    except:
        print()
        
#Loop through the regions urls
for region in regions_url:
    print('Fetching data from ', region)
    print()
    req = requests.get(region)
    req.raise_for_status()
    region_soup = bs4.BeautifulSoup(req.text)
    #count how many web pages to loop
    num_pages = []
    for line in region_soup.find_all('a', {'class': 'button button--small'}):
        #this will grab a few non-int items and therefore need to handle for it
        try:
            a = int(line.text)
            num_pages.append(a)
        except:
            print()
    #some pages will only have one page and the max function won't work, this is a error handle for that        
    try:        
        last_page = max(num_pages)
    except:
        last_page = 1
    #loop through all the web pages    
    for i in range(last_page):
        sub_url = region + '?pageNum=%s&pageSize=12' % str(i)
        sub_req = requests.get(sub_url)
        sub_req.raise_for_status()
        sub_soup = bs4.BeautifulSoup(sub_req.text)
        prices = []
        #html contains additional json script that needs to be stripped to extract relevant data
        strip_text = "MajesticDataLayer.page.addPageName("+'"PLP");\n      MajesticDataLayer.product.addSearchResultData(['
        print('searching for region data...')
        print()
        for script in sub_soup.find_all('script'):
            #search the html for the script that contains the region data
            if re.search('MajesticDataLayer.', script.text) is not None:
                prices.append(script.text)
        #relevant data will be contained in price[1], need to remove other part of the script
        prices = prices[1]
        #strip off additional json code from data
        prices = prices.strip(strip_text)
        prices = prices.strip('],')
        #breakdown product data into individual datasets to allow it to be processed as a dict
        print('breaking down region data into individual data sets...')
        print()
        prices = prices.split(',{')
        for i in range(len(prices)):
            #remove the the end curly bracket in order to append extra data
            prices[i] = prices[i][:-1]
        #add a data tag to know what type of region this is
        tag_region = region.replace('https://www.majestic.co.uk/','')
        try:
            tag_region = tag_region.replace('-',' ')
        except:
            print('no hypen to remove...')
            print()
        print('adding data tag...')
        print()
        for x in range(len(prices)):
            #all the dicts in the list will have a opening curly bracket missing because of the split except the first dict
            if x == 0:
                prices[x] = prices[x] + ', "region":"' + tag_region + '"}'
            else:
                prices[x] = '{' + prices[x] + ', "region":"' + tag_region + '"}'
        print('Creating region list with prices...')
        print()
        #Using two different lists to capture the region data as one list will be used to prep the data and the other to store the data
        for x in prices:
            split_region.append(x)
            
#convert each element of the list into one dict with relevant data (product name and price) 
for region_str in split_region:
    print('Converting region list into dict...')
    print()
    try:
        a = json.loads(region_str)
        for k, v in a.items():
            region_prices[a['productName']] = {'price': a['pricesCurrent']['prices']['basePrice'],'positive_rating': a['productFamily']['positiveRatings'],'num_ratings': a['productFamily']['allRatings'],'region': a['region']}
    except:
        print()

#convert data into dataframes 

df_wines = pd.DataFrame(wine_prices)
#transpose data
df_wines = df_wines.T
#convert to floats
df_wines[['num_ratings', 'positive_rating', 'price']] = df_wines[['num_ratings', 'positive_rating', 'price']].astype('float')
#trim the white space
df_wines['wine_type'] = df_wines['wine_type'].str.strip()
#add a rating score
#df_wines['rating_score'] = df_wines['positive_rating'] / df_wines['num_ratings']

df_country = pd.DataFrame(country_prices)
#transpose data
df_country = df_country.T
#convert to floats
df_country[['num_ratings', 'positive_rating', 'price']] = df_country[['num_ratings', 'positive_rating', 'price']].astype('float')
#trim the white space
df_country['country'] = df_country['country'].str.strip()
#add a rating score
df_country['rating_score'] = df_country['positive_rating'] / df_country['num_ratings']
#add a column to the dataframe to categorise wines into new world and old world
for index, row in df_country.iterrows():
	country_to_world.append(row['country'])
for i in country_to_world:
	if i in old_world:
		world.append('old world')
	else:
		world.append('new world')       
df_country['world'] = world

#create grapes dataframe
df_grapes = pd.DataFrame(grape_prices)
#transpose data
df_grapes = df_grapes.T
#convert to floats
df_grapes[['num_ratings', 'positive_rating', 'price']] = df_grapes[['num_ratings', 'positive_rating', 'price']].astype('float')
#remove the whitespace
df_grapes['grape'] = df_grapes['grape'].str.strip()
#add a rating score
df_grapes['rating_score'] = df_grapes['positive_rating'] / df_grapes['num_ratings']

#create regions dataframe
df_regions = pd.DataFrame(region_prices)
#transpose data
df_regions = df_regions.T
#convert to floats
df_regions[['num_ratings', 'positive_rating', 'price']] = df_regions[['num_ratings', 'positive_rating', 'price']].astype('float')
#remove the whitespace
df_regions['region'] = df_regions['region'].str.strip()
#add a rating score
df_regions['rating_score'] = df_regions['positive_rating'] / df_regions['num_ratings']

#consolidate the datasets
print('Joining wine and country datasets...')
print()
df_all = df_wines.join(df_country, how='left', rsuffix='_country')
print('Adding grapes dataset...')
print()
df_all = df_all.drop(['num_ratings_country','positive_rating_country', 'rating_score' ,'price_country'], axis=1)

df_all = df_all.join(df_grapes, how='left', rsuffix='_grapes')
df_all = df_all.drop(['num_ratings_grapes', 'positive_rating_grapes', 'rating_score','price_grapes'], axis=1)
print('Adding regions dataset...')
print()

df_all = df_all.join(df_regions, how='left', rsuffix='_regions')
df_all = df_all.drop(['num_ratings_regions', 'positive_rating_regions', 'rating_score' ,'price_regions'], axis=1)

#remove the wines where there were no ratings - not using this with the rationale that no ratings indicate no order = no demand, still a relevant data point
#df_all = df_all[df_all.num_ratings != 0]

#add aggregate rating score
df_all['rating_score'] = df_all['positive_rating'] / df_all['num_ratings']

print('number of blanks')
print(df_all.isnull().sum())

#remove grape and region from the initial analysis 
df_2 = df_all.drop(['grape','region'], axis=1)

#transform price into category
for k, v in df_2['price'].items():
    if v <= 10:
        price_cat.append('£0 - £10')
    elif v <= 30:
        price_cat.append('£11 - £30')
    elif v <= 50:
        price_cat.append('£31 - £50')
    elif v <= 100:
        price_cat.append('£51 - £100')
    elif v <= 250:
        price_cat.append('£101 - £250')
    else:
        price_cat.append('£251 - £500')

df_2['price_cat'] = price_cat

#fill na of the rating score attribute with 0s
df_2['rating_score'] = df_2['rating_score'].fillna(0)

#turn categorial data into numerical
df_dumb = pd.get_dummies(df_2)

#create the independent variables and dependent variable
X = np.array(df_dumb.drop(['rating_score', 'num_ratings', 'positive_rating', 'world_new world', 'world_old world', 'price'], axis=1).values)

#for catergorial learning
#Catergories Fav is > 50% repurchase Unfav < 50% purchases
for index, row in df_2.iterrows():
	if row['rating_score'] > 0.5:
		y.append(1)
	else:
		y.append(0)

y = np.array(y)
print('target variable set...')
print('a score of 1 = Favourable')
print('a score of 0 = Unfavourable')

#for linear learning
y_rating = np.array(df_dumb['rating_score'].values)



