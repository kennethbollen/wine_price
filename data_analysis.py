from data_extract import *
import seaborn as sns
from stats_functions import draw_perm_reps

#EDA on the wine's country of origin and rating score
_ = sns.swarmplot(x='country', y='rating_score', data=df_country)

#are the zero rating's outliers skewing the data?
print(df_country.loc[df_country['rating_score'] == 0,:])
#no, they have been bought before

#numerical analysis on the wine's country of origin and rating score
country_pr = df_country.groupby('country')[['price', 'rating_score']].mean()
#highest ratings
print(country_pr.sort_values(['rating_score'],ascending=False))
#highest prices
print(country_pr.sort_values(['price'],ascending=False))

#EDA on the wine world and rating
_ = sns.swarmplot(x='world', y='rating_score', data = df_country)

#numerical analysis on the wine's world of origin and rating score
print(df_country.groupby('world')[['price','rating_score']].mean())

