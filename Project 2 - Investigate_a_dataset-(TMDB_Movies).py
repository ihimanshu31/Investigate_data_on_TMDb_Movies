#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a Dataset (TMDB Movies)
# The TMDb movie dataset provide many information on all movies. 
# The TMDb movie dataset provide many information on all movies. The data contains information that are provided from The Movie Database (TMDb). It collects 5000+ movies basic move information and movie matrices, including user ratings, popularity and revenue data. These metrics can be seen as how successful these movies are. The movie basic information contained like cast, director, keywords, runtime, genres, etc.
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
#     
# <li><a href="#wrangling">Data Wrangling</a></li>
# 
# <li><a href="#eda">Exploratory Data Analysis</a></li>
#         
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>
# 
# **In this report I am going to explore following questions : **
#     
#     Question 1: Which movies are the most profitable to the market?
#     Question 2: Which movie has the Least and maximum profit , budget, runtime?
#     Question 3: Top 10 movies by profit , budget, runtime?
#     Question 4: Which years do movies made the most profits ?
#     Question 5: Movie Release years vs Total budget made by movies ?
#     Question 6: No. of movies release in every month of a year?
#     Question 7: Find the top casts, directors and genres?
#     Question 8: What is the Average Budget of the movies?
#     Question 9: What is the Average Revenue earned by the movies?
#     Question 10: What is the Average duration of the movies?

# <a id='intro'></a>
# ## Introduction
#  The primary goal of the project is to go through the general data analysis process — using basic data analysis technique with NumPy, pandas, and Matplotlib. 
#  
#  

# In[1]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# In this process the main idea is to take a quick glance on the data set, find the potential unreasonable data value, unnecessary variables for my research question, null data or duplicates, and then make data clearing decisions.
# •	Basic Exploration
# 
# •	Null values and zero values:
# 	
#     Zero Values in Budget and Revenue Columns
# 	Zero Values in Runtime Columns
#     
# •	Data Cleaning 
# 	
#     Drop Duplicates
# 	Replace zero values with null values
# 
# 
# 

# In[2]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.

tmdb_df = pd.read_csv("tmdb-movies.csv")
tmdb_df.info()


# In[3]:


tmdb_df.shape


# #### 1. Deleting the columns that is not required

# In[4]:


#Deleting the columns that is not required
# list of columns that are to be deleted/dropped

tmdb_df.drop(['id', 'imdb_id', 'budget_adj', 'revenue_adj', 'homepage',  'tagline', 'keywords', 
              'production_companies','vote_average','vote_count','overview'], axis=1, inplace=True)


# In[5]:


#print two rows of data set
tmdb_df.head(2)


# In[12]:


#print summary of the data set
tmdb_df.describe()


# In[6]:


# count no. of rows containing null values
tmdb_df.isnull().sum()


# #### 2. Delete duplicate rows in the dataset
# 
# 

# In[7]:


#Need to remove duplicate rows from the dataset
#to check duplicate  values
tmdb_df.duplicated().sum()


# In[9]:


#delete duplicates values 
tmdb_df.drop_duplicates(inplace=True)
tmdb_df.shape


# #### 3. Changing Format Of Release Date Into Datetime Format

# In[10]:


#Changing Format Of Release Date Into Datetime Format
tmdb_df['release_date']= pd.to_datetime(tmdb_df['release_date'])
tmdb_df['release_date'].head()


# In[11]:


#change budget and revenue into integer
tmdb_df['budget'] = tmdb_df['budget'].astype(int)
tmdb_df['revenue'] = tmdb_df['revenue'].astype(int)


# #### 4. Check Zero and Null values in Budget and revenue and drop them

# In[18]:


# I see lot of values is zero in budget and revenue column
#lets ee how many zeros they have
print (tmdb_df[tmdb_df['budget']==0].shape)
print (tmdb_df[tmdb_df['revenue']==0].shape)


# In[12]:


#drop null values
tmdb_df['budget'] = tmdb_df['budget'].replace(0, np.NaN)
tmdb_df['revenue'] = tmdb_df['revenue'].replace(0, np.NaN)

tmdb_df.dropna(inplace =True)


# In[13]:


tmdb_df.isnull().sum()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. Compute statistics and create visualizations with the goal of addressing the research questions that you posed in the Introduction section. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables.
# 
# ### Question 1. Which movies are the most profitable to the market? 

# In[14]:


# Create a Profit column to check the most profitable movie

tmdb_df['profit'] = tmdb_df['revenue'] - tmdb_df['budget']
tmdb_df['revenue'] = tmdb_df['revenue'].astype(int)
tmdb_df.head(1)


# In[22]:


#top 10 movies

tmdb_df.sort_values(['profit'], ascending = False).head(10)


# In[15]:


#sort the 'Profit' column in decending order and store it in the new dataframe,
info = pd.DataFrame(tmdb_df['profit'].sort_values(ascending = False))
info['original_title'] = tmdb_df['original_title']
data = list(map(str,(info['original_title'])))
x = list(data[:10])
y = list(info['profit'][:10])

#make a plot usinf pointplot for top 10 profitable movies.
ax = sns.pointplot(x=y,y=x)


#setup the title and labels of the plot.
ax.set_title("Top 10 Profitable Movies",fontsize = 15)
ax.set_xlabel("Profit",fontsize = 13)
sns.set_style("darkgrid")


# ### Question 2  : Which movie has the Least and maximum profit , budget, runtime?

# In[16]:


def max_min_data(column_name):
    
    # Find the max from the index number in the column, store to df
    highest_movie = tmdb_df[column_name].idxmax()
    highest = pd.DataFrame(tmdb_df.loc[highest_movie])
    
    # Find the min from the index number in the column, store to df
    lowest_movie = tmdb_df[column_name].idxmin()
    lowest = pd.DataFrame(tmdb_df.loc[lowest_movie])
    
    #concatenating two dfs
    max_min_data = pd.concat([highest, lowest], axis = 1)
    
    return max_min_data




# In[17]:


max_min_data('profit')


# In[18]:


max_min_data('budget')


# In[19]:


max_min_data('runtime')


# ### Question 3  : Top 10 movies by profit , budget, runtime 

# In[20]:


# Create a bar graph for the top 10 most profitable movies 


# First sort the raw data by the profit.
sorted_profit = tmdb_df['profit'].sort_values(ascending=False)[:10]

# Create title and profit lists which will be used as X-axis and Y-axis values in bar graph.
high_profit=pd.DataFrame()
titles=[]
profit=[]

# Fill the vallues from raw data to the lists.
for i in sorted_profit.index:
    titles.append(tmdb_df.loc[i,'original_title'])
    profit.append(sorted_profit.loc[i])
high_profit['Titles']=titles
high_profit['Profit']=profit
high_profit.set_index('Titles',inplace=True)

# Plot
high_profit.plot(kind ='bar',figsize=(8,5))
plt.title('Top 10 movies with the most Profit');
plt.ylabel('Profit in billions ($)');


# In[21]:


#top 10 movies by budget

sorted_budget = tmdb_df['budget'].sort_values(ascending=False)[:10]
high_budget=pd.DataFrame()
titles_exp=[]
budgets=[]
for i in sorted_budget.index:
    titles_exp.append(tmdb_df.loc[i,'original_title'])
    budgets.append(sorted_budget.loc[i])
high_budget['Titles']=titles_exp
high_budget['Budgets']=budgets
high_budget.set_index('Titles',inplace=True)
high_budget.plot(kind ='bar',figsize=(8,6), color='orange')
plt.title('Top 10 movies with the most budget ');
plt.ylabel('Budget in 100\'s of million');


# In[22]:


# Create a histogram for movie runtimes.
plt.figure(figsize=(5,3), dpi=100)
tmdb_df['runtime'].hist(rwidth = 0.9, bins =35)
plt.xlabel('Runtime')
plt.ylabel('Number of Movies')
plt.title('Runtime distribution of all the movies');


# #### Question 4: Which years do movies made the most profits ?

# In[24]:


# First group total profit by each years
profit_yr = tmdb_df.groupby('release_year')['profit'].sum()
profit_yr.tail(5)


# In[35]:


# plot 

profit_yr.plot(figsize = (12,6), color="purple")
plt.xlabel('Movies released year')
plt.ylabel('Total Profits made by Movies')
plt.title('Total Profits vs Movie Years');


# #### Question 5: Movie Release years vs Total budget made by movies ?

# In[36]:


# Totaal buget vs movie years
budget_yr = tmdb_df.groupby('release_year')['budget'].sum()
budget_yr.head(5)

# plot the above query
profit_yr.plot(figsize = (10,6), color='green')
plt.xlabel('Movies released year')
plt.ylabel('Total budgets made by Movies')
plt.title('Total budgets vs Movie Years');


# #### Question 6. No. of movies release in every month of a year?

# In[42]:


#extract the month number from the release date.
month_release = tmdb_df['release_date'].dt.month

#count the movies in each month using value_counts().
number_of_release = month_release.value_counts().sort_index()
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
number_of_release = pd.DataFrame(number_of_release)
number_of_release['month'] = months

number_of_release


# In[43]:


#change the column name of the new dataframe 'number_of_release'
number_of_release.rename(columns = {'release_date':'number_of_release'},inplace=True)


#plot the bar graph using plot.
number_of_release.plot(x='month',kind='bar',fontsize = 11,figsize=(10,6))

#set the labels and titles of the plot.
plt.title('Months vs Number Of Movie Releases',fontsize = 15)
plt.xlabel('Month',fontsize = 12)
plt.ylabel('Number of movie releases',fontsize = 12)


# In[ ]:





# #### Question 7. Find the top casts, directors and genres?

# In[207]:


# to study about cast, we will separate each all people in each movie into every individuals.
tmdb_df.loc[:,['original_title', 'cast', 'director', 'genres']].head()


# In[208]:


def extract_data(column_name):
    tmdb_df['cast']=tmdb_df['cast'].astype(str)
    tmdb_df['director']=tmdb_df['director'].astype(str)
    
    # From the column entered, eparate the string by '|'
    all_data = tmdb_df[column_name].str.cat(sep = '|')
    
    # StorE the values separately as series
    all_data = pd.Series(all_data.split('|'))
    
    # Read the descending order, starts with highest number
    count = all_data.value_counts(ascending = False)
    
    return count


# #### Most Frequent Cast

# In[209]:


# Use the function for the casts.

cast_count = extract_data('cast')
cast_count = pd.DataFrame(data=cast_count)

top_cast = cast_count.head(10)
top_cast


# ####  Most Succesful Directors

# In[210]:


# Use the function for the directors

director_count = extract_data('director')
director_count = pd.DataFrame(data=director_count)

top_director = director_count.head(10)
top_director


# ####  Most Succesful genres

# In[211]:


# Use the function for the genres

genres_count = extract_data('genres')
genres_count = pd.DataFrame(data=genres_count)

top_genres = genres_count.head(10)
top_genres


# #### Question 8 : What is the  Average Budget of the movies?

# In[202]:


#New function to find average 
def profit_avg(column):
    return profit_data[column].mean()


# In[201]:


profit_avg('budget')


# #### Question 9 : What is the  Average Revenue earned by the movies?

# In[203]:


profit_avg('revenue')


# #### Question 10 : What is the Average duration of the movies?
# 
# 

# In[205]:


profit_avg('runtime')


# <a id='conclusions'></a>
# ## Conclusions
# 
# >The TMDb movie dataset provide many information on all movies. After Data Wrangling, null values, duplicated values and 0 values were removed to provide more accurate results.  
# We came out with some very interesting facts about movies. After this analysis we can conclude following:
# >
# >**For a Movie to be in successful criteria**
# 
#     •	Average Budget must be around 60 millon dollar
#     •	Average duration of the movie must be 113 minutes (1 hr 53min)
#     •	Profits: profits has positive relationship with budget and popularity
#     •	Any one of these should be in the cast: Robert De Niro , Bruce Willis,  Sylvester Stallone, Samuel L. Jackson
#     •	Genre must be: Comedy, Drama., Action, Thriller.
#     •	Director must be: Steven Spielberg, Clint Eastwood, Ridley Scott, Woody Allen
# 
# >**Limitation:**
# >Although we successfully predited the above properties on TMDb movie dataset, there are many infomation removed such as rows contained 0 values and null values. The dataset was cut by few thousand rows of movies, which would definitly affect the result.
# 
# 
# 
