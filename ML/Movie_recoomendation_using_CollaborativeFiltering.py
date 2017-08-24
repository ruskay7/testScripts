
# coding: utf-8

# In[1]:

import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
#from scipy.spatial.distance import cosine
import operator
import pandas as pd


# In[2]:

#reading the csv files using pandas
#reading only 5000 rows to save memory
movie = pd.read_csv('movies.csv',nrows=5000)

rating = pd.read_csv('ratings.csv')


# In[3]:

#merging the two csv on the common column movieId
merged = rating.merge(movie, left_on = 'movieId', right_on = 'movieId')

#selecting only the columns that we need
merged=merged[['userId', 'title', 'rating']]


# In[4]:

merged.head()


# In[5]:

#creating pivot table which inverts the table. ie. users become the index column and each movie title becomes a separate column with ratings as values
pivot = merged.pivot_table(index=['userId'], columns=['title'], values='rating')


# In[6]:

pivot.head()


# In[7]:

#replacing all Nan values as 0
pivot.fillna(0, inplace= True)
pivot.head()


# In[8]:

"""create a new dataframe from the old
Using the lambda function, we standardize the ratings. We find the mean and subtract the mean from the rating in each row. 
That way all the users with only one rating and all the users with same ratings will be removed
np is numpy library that can be used for mathematical computaitons. The function loops through each row, finds the mean rating of a user and subracts that rating to get the deviation
divides the rating by range)
We standardize the ratings in such a way to avoid fake reviews/ratings whcih will help build a better model"""

pivot_std = pivot.apply(lambda x: (x-np.mean(x))/(np.max(x)-np.min(x)), axis=1)
"""standardScalar implementation trial
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
pivot_std = sc_X.fit_transform(pivot)"""
pivot_std.head()


# In[9]:

#transpose the pivot_std table to have each movie as the index and users in separate column

pivot_std = pivot_std.T
#selecting all rows where standardized rating is not zero
pivot_std = pivot_std.loc[:, (pivot_std != 0).any(axis=0)]
pivot_std.head()


# In[10]:

# In order for us to use the sklearn cosine similarity function, we need to transorm our df to a sparse matrix
pivot_sparse = sp.sparse.csr_matrix(pivot_std.values)


# In[11]:

#calculating item and user similarity using sklearn library
item_similarity = cosine_similarity(pivot_sparse)


# In[12]:

#we are transposing again because we want the user similarity and the users need to be the index column
user_similarity = cosine_similarity(pivot_sparse.T)


# In[13]:

#Our similarities are calculated. Now to fit them to our model
#fitting the variables to separate dataframe objects. We are creating new df and applying the similarity values to the ratings in their respective columns
item_sim = pd.DataFrame(item_similarity, index = pivot_std.index, columns = pivot_std.index) #index column has user
user_sim = pd.DataFrame(user_similarity, index = pivot_std.columns, columns = pivot_std.columns) #columns has movie names


# In[14]:

def movies_similar_to(movie_name):
    count = 1
    print('Similar movies to {} include:\n'.format(movie_name))
    for item in item_sim.sort_values(by = movie_name, ascending = False).index[1:6]: #sort descending value by similarity
        print('No. {}: {}'.format(count, item))
        count +=1  #increment count after each result to show ranking order
movies_similar_to('Toy Story (1995)') #enter a movie from the dataset


# In[15]:

# This function will return the top 5 users with the highest similarity value 

def users_similar_to (user):
    
    if user not in pivot_std.columns:
        return('userId is incorrect {}'.format(user))
    
    print('Most Similar Users:\n')
    sim_values = user_sim.sort_values(by=user, ascending=False).loc[:,user].tolist()[1:6] #using .loc to specify column name as moviename and transforming the results to a list in descending order
    sim_users = user_sim.sort_values(by=user, ascending=False).index[1:6] #sort by index
    zipped = zip(sim_users, sim_values) #using zip to pack key and values
    for user, sim in zipped:
        print('User #{0}, Similarity value: {1:.2f}'.format(user, sim)) 
users_similar_to(7) #user index


# In[16]:

"""we now define a function which returns the highest rated shows by similar users to our input user and the number of times the movies is rated by fellow similar users"""

def users_similar_to_you_also_liked(user):
    
    if user not in pivot_std.columns:
        return('incorrect_userId {}'.format(user))
    
    sim_users = user_sim.sort_values(by=user, ascending=False).index[1:11] #take 10 similar users
    best = [] #list
    most_common = {} #dictionary
    
    for i in sim_users:
        max_score = pivot_std.loc[:, i].max() #get max rating from user using max fn
        best.append(pivot_std[pivot_std.loc[:, i]==max_score].index.tolist()) #append movie to list
    for i in range(len(best)): #loop through length of the movies list
        for j in best[i]:
            if j in most_common:
                most_common[j] += 1 # copying key, value to dictionary if already present and incrementing value
            else:
                most_common[j] = 1 #copying key, value to dictionary
    sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True) #sorting dictionary
    return sorted_list[:6]    #top 5
    
users_similar_to_you_also_liked(7) #user index


# In[ ]:



