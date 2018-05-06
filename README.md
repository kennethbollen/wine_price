Drivers of wine consumption in the U.K
=======================================
Project used wine data from the U.K retailer Majestic Wine (majestic.co.uk) to analyse wine consumption trends and drivers.

Overview
----------
Languages: Python 3
Source: https://majestic.co.uk
Time period: April 2018
Time of analysis: January 2018 - April 2018
Packages used: pandas, numpy, requests, re, bs4, sklearn, matplotlib, seaborn, scipy.stats and json

Data Extract (data_extract.py)
-------------------------------
File provides code used to web scrap over 500 bottles of wine from majestic wine's e-commerce website. Data collection was focused on collecting data on wine producer's country, region, price and grap variety.

Data Analysis (data_analysis.py)
--------------------------------
File provides code used to conduct hypothesis analysis on whether the origin of wine make a difference to whether someone will buy the wine again. 

Predictive Analysis (predict.py)
--------------------------------
File provides code used to conduct predictive analysis. Code includes data-set splitting, parameter tuning, model training and precision-recall tuning. Additionally, a function to predict wine satisfaction with the arguments price, country and grape. 
