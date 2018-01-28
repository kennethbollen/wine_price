from data_extract import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

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

#is the data normally distributed
mu = df_country['rating_score'].mean()
sigma = df_country['rating_score'].std()
samples = np.random.normal(mu, sigma, size=10000)
plt.hist(samples, normed=True, bins=100, histtype='step')
plt.show()
#Yes - data is normally ditributed

#what's the probability of someone buying non french wine again
country_mean = pd.DataFrame(df_country.groupby('country')['rating_score'].mean())
french_mean = country_mean.filter(like='french', axis=0)['rating_score'].values
prob = np.sum(samples >= french_mean) / len(samples)
print('Probability of being better than french wine: ', prob)

#Hypothesis test does the origin of wine make a difference to whether someone will buy the wine again
#Null Hypothesis: Country of origin has no impact on whether someone will buy wine again
#Alternative Hypothesis: Country of origin has an impact on whether someone will buy wine again

#sample mean
world_mean = pd.DataFrame(df_country.groupby('world')['rating_score'].mean())
new_mean = world_mean.filter(like='new world', axis=0)['rating_score'].values
old_mean = world_mean.filter(like='old world', axis=0)['rating_score'].values

#sample variance
world_var = pd.DataFrame(df_country.groupby('world')['rating_score'].std())
new_var = world_var.filter(like='new world', axis=0)['rating_score'].values
old_var = world_var.filter(like='old world', axis=0)['rating_score'].values

#sample size
world_cnt = pd.DataFrame(df_country.groupby('world')['rating_score'].count())
new_cnt = world_cnt.filter(like='new world', axis=0)['rating_score'].values
old_cnt = world_cnt.filter(like='old world', axis=0)['rating_score'].values

#samples
rvs_new = stats.norm.rvs(loc=new_mean, scale=new_var, size=new_cnt)
rvs_old = stats.norm.rvs(loc=old_mean, scale=old_var, size=old_cnt)

#t-test and p value
t_test, p_value = stats.ttest_ind(rvs_new, rvs_old, equal_var = False)
sig_level = 0.05

if p_value > sig_level:
  print('p value: ', p_value, ' is greater than the significance level of ', sig_level)
  print('Cannot reject null hypothesis, country of origin has no impact on sales')
else:
  print('p value: ', p_value, ' is less than the significance level of ', sig_level)
  print('Reject null hypothesis, country of origin has an impact on sales')

