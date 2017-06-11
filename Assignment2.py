
# coding: utf-8


# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on
# [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning.
#
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[ ]:

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index)
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')

# ### Question 0 (Example)
# What is the first country in df?
# *This function should return a Series.*

# In[ ]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
# answer_zero()


# ### Question 1
# Which country has won the most gold medals in summer games?
#
# *This function should return a single string value.*

# In[ ]:

def answer_one():
    return df.sort_values('Gold', ascending=False).iloc[0].name


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
#
# *This function should return a single string value.*

# In[ ]:

def answer_two():
    temp_df = df.copy()
    temp_df['diff'] = abs(temp_df['Gold'] - temp_df['Gold.1'])
    return temp_df.sort_values('diff', ascending=False).iloc[0].name
print("TWO")
print(answer_two())

# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count?
#
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
#
# Only include countries that have won at least 1 gold in both summer and winter.
#
# *This function should return a single string value.*

# In[ ]:

def answer_three():
    dff = df.copy()
    dff['rel_diff'] = (dff['Gold'] - dff['Gold.1']) / dff['Gold.2']
    return dff[(dff['Gold.2'] >= 1) & (dff['Gold.1'] >= 1)].sort_values('rel_diff', ascending=False)[['Gold', 'Gold.1', 'Gold.2', 'rel_diff']].iloc[0].name
print("THREE")
print(answer_three())


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
#
# *This function should return a Series named `Points` of length 146*

# In[ ]:

def answer_four():
    dff = df.copy()
    dff['points'] = dff['gold.2'].apply(lambda x: x * 3) + dff['silver.2'].apply(lambda x: x * 2) + dff['bronze.2']
    return dff['points']

# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
#
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
#
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
#
# *This function should return a single string value.*

# In[ ]:

census_df = pd.read_csv('census.csv')
county_df = census_df[census_df['SUMLEV'] == 50]
county_df = county_df.set_index(['STNAME', 'CTYNAME'])
print(county_df.loc['Delaware'])
print('--------------- END CENSUS HEAD -----------')


# In[ ]:

def answer_five():
    dff = county_df.copy()
    dff = dff.groupby(level=[0]).size().sort_values()
    biggest = dff.iloc[-1]
    return dff[dff == biggest].index.values[0]
print(answer_five())

# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
#
# *This function should return a list of string values.*

# In[ ]:

def answer_six():
    dff = county_df.copy()
    # group them, them for each dataframe given with the apply sort it as hell
    dff = dff.groupby(level=0).apply(lambda x: x.sort_values('CENSUS2010POP', ascending=False).head(3))
    # sum everything because we can, do not even bother that we only need to filter by CENSUS2010POP
    dff = dff.groupby(level=0).apply(sum)
    # now sort the bigger dataset by the already summed up census2010pop
    return list(dff.sort_values('CENSUS2010POP', ascending=False).head(3).index.values)

print(answer_six())


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
#
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
#
# *This function should return a single string value.*

# In[ ]:

def answer_seven():
    dff = census_df.copy()
    dff = dff[dff['SUMLEV'] == 50]
    columns = dff[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012',
                   'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015'
               ]]
    dff['ABS_CHANGE'] = abs(columns.max(axis=1) - columns.min(axis=1))
    return dff.sort_values('ABS_CHANGE', ascending=False).iloc[0]['CTYNAME']


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column.
#
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
#
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[ ]:

def answer_eight():
    dff = census_df.copy()
    dff = dff[(dff['SUMLEV'] == 50) & (dff['REGION'] <= 2) & (dff['CTYNAME'].str.startswith('Washington')) & (dff['POPESTIMATE2015'] > dff['POPESTIMATE2014'])]
    return dff[['CTYNAME', 'STNAME']].sort_index()
