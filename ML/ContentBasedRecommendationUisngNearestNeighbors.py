
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import operator


# In[2]:

movie = pd.read_csv('movies.csv')
rating = pd.read_csv('ratings.csv')
movie.isnull().any()
rating.isnull().any() #check if there are any nulls


# In[3]:

features = pd.concat([movie["genres"].str.get_dummies(sep="|"), rating[["rating"]]],axis=1) #merging the tables and creating dummy values


# In[4]:

features.head()


# In[5]:

features.isnull().any() #to check for nulls


# In[6]:

features.fillna(0, inplace= True) #replace nan with 0


# In[7]:

features.head()


# In[8]:

#featurescaling

from sklearn.preprocessing import MaxAbsScaler
#np.isnan(features)

#np.where(np.isnan(features))

max_abs_scaler = MaxAbsScaler()
features = max_abs_scaler.fit_transform(features) #fitting the class to variable and transforming it


# In[9]:

#nearest neighbor classifier

from sklearn.neighbors import NearestNeighbors
neighbors = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(features)
distances, indices = neighbors.kneighbors(features)


# In[11]:

def index_title(title):
    return movie[movie["title"]== title].index.tolist()[0] #returns row of the movie title where we select the index of the movie and convert it to a list and access the first element of list
index_title("Toy Story (1995)") #output returns the index of the current movie ie. toy story


# In[13]:

title="Toy Story (1995)"
a= movie[movie["title"]== title].index.tolist()[0]
#title="Toy Story (1995)"
#b=movie[movie["title"]== title].index.tolist()[0]
#print(b)
nearest_movies= indices[a] #from the model
print(nearest_movies) #returns of nearest 5 movies indices


# In[14]:

for mov in nearest_movies:
    print(movie.loc[mov]["title"]) #returns titles


# In[ ]:



