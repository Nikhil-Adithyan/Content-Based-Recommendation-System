# Importing packages

import pandas as pd
from termcolor import colored as cl

# Importing the Movies Data

movies = pd.read_csv('movies.csv')
print(movies.head())

# Data Processing - Movies data

movies['title'] = movies.title.str.replace('(\(\d\d\d\d\))', '')
movies['title'] = movies['title'].apply(lambda x: x.strip())

movies['genres'] = movies.genres.str.split('|')

movies_genres = movies.copy()

for index, row in movies_genres.iterrows():
    for genres in row['genres']:
        movies_genres.at[index, genres] = 1

movies_genres = movies_genres.fillna(0)
print(movies_genres.head())

# Creating a personal list

myList = [
            {'title':'Breakfast Club, The', 'rating':5},
            {'title':'Toy Story', 'rating':3.5},
            {'title':'Jumanji', 'rating':2},
            {'title':"Pulp Fiction", 'rating':5},
            {'title':'Akira', 'rating':4.5}
         ]

print(myList)

# Creating the algorithm

def find_recommendations(myList, n):
    
    myMovies = pd.DataFrame(myList) # converting the given list to a dataframe
    myMoviesId = movies[movies['title'].isin(myMovies['title'].tolist())] # extracting the movieId from the movies data
    myMovies = pd.merge(myMoviesId, myMovies) # joining the movieId with the personal data
    myMovies.drop(['genres'], axis = 1, inplace = True) # processing the personal data
    
    myGenres = movies_genres[movies_genres['movieId'].isin(myMovies['movieId'].tolist())] # extracting genres
    myGenresTable = myGenres.reset_index(drop = True) # resetting the index of the extracted genres data
    myGenresTable.drop(['movieId', 'title', 'genres'], axis = 1, inplace = True) # processing the new genres data
    
    myProfile = myGenresTable.T.dot(myMovies['rating']) # generating a profile with personal ratings for genres
    genreTable = movies_genres.set_index('movieId') # new genre data with movieId as the index
    genreTable.drop(['title', 'genres'], axis = 1, inplace = True) # processing the newly created genre data
    
    recommendationDf = ((genreTable * myProfile).sum(axis = 1)) / (myProfile.sum()) # weighted average for each movie
    recommendationTable = recommendationDf.sort_values(ascending = False) # ranking the values in descending order
    
    final_recommends = movies.loc[movies['movieId'].isin(recommendationTable.head(n).keys())] # recommended movies data
    
    return final_recommends

find_recommendations(myList, 10)

# Importing the Ratings Data

ratings = pd.read_csv('ratings.csv')
ratings = ratings.drop(['timestamp', 'userId'], axis = 1)
print(ratings.head())

def recommend_movies(genre):
    
    genre_movies = movies[movies_genres[genre] == 1] # extracting movies data 
    genre_ratings = ratings[ratings['movieId'].isin(genre_movies['movieId'].tolist())] # extracting ratings data
    ratings_ranking = genre_ratings.nlargest(10, 'rating') # ranking top 10 movies based on the ratings
    final_recommends = movies[movies['movieId'].isin(ratings_ranking['movieId'])] # recommended movies data
    
    # Output format
    
    print(cl('TOP 10 RECOMMENDED MOVIES FOR YOU IN {}'.format(genre), attrs = ['bold']))
    
    print('-------------------------------------------------------')
    
    print(cl('1. {}'.format(final_recommends['title'].values[0]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('2. {}'.format(final_recommends['title'].values[1]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('3. {}'.format(final_recommends['title'].values[2]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('4. {}'.format(final_recommends['title'].values[3]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('5. {}'.format(final_recommends['title'].values[4]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('6. {}'.format(final_recommends['title'].values[5]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('7 {}'.format(final_recommends['title'].values[6]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('8. {}'.format(final_recommends['title'].values[7]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('9. {}'.format(final_recommends['title'].values[8]), attrs = ['bold']))
    print('-------------------------------------------------------')
    print(cl('10. {}'.format(final_recommends['title'].values[9]), attrs = ['bold']))
    
    print('-------------------------------------------------------')

recommend_movies('Sci-Fi')