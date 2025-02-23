# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO AUTOLAB

from collections import defaultdict
from collections import Counter

# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    # WRITE YOUR CODE BELOW
    ratings = defaultdict(list)
    with open(f, 'r') as file:
        for line in file:
            parts = line.strip().split('|') #strip whitespace 
            name = parts[0].strip() #extract movie name
            rating = float(parts[1]) #extract rating and convert to float
            ratings[name].append(rating) #add rating to corresponding movie
    return dict(ratings)    

# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    # WRITE YOUR CODE BELOW
    genres = {}
    with open(f, 'r') as file:
        for line in file:
            parts = line.strip().split('|') 
            genre = parts[0].strip()
            name = parts[2].strip()
            genres[name] = genre
    return genres

# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    # WRITE YOUR CODE BELOW
    genre_to_movies = defaultdict(list)
    for movie, genre in d.items():
        genre_to_movies[genre].append(movie)
    return dict(genre_to_movies)
    
# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    ratings = {}
    for movie, ratings_list in d.items():
        ratings[movie] = sum(ratings_list)/len(ratings_list)
    return ratings
    
# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating, 
    #         in ranked order from highest to lowest average rating
    # WRITE YOUR CODE BELOW
    sorted_movies = sorted(d.items(), key = lambda x: x[1], reverse=True)
    top = dict(sorted_movies)
    return top
    
# 3.2
def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    filtered_movies = {
        movie: rating for movie, rating in d.items() if rating >= thres_rating
    }
    return filtered_movies
    
# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    if genre not in genre_to_movies:
        return {}
    genre_movies = genre_to_movies[genre]
    genre_ratings = {
        movie: movie_to_average_rating[movie] for movie in genre_movies if movie in movie_to_average_rating
    }
    return get_popular_movies(genre_ratings, n)
    
# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # return: average rating of movies in genre
    # WRITE YOUR CODE BELOW
    if genre not in genre_to_movies:
        return 0
    genre_movies = genre_to_movies[genre]
    genre_ratings = [
        movie_to_average_rating[movie] for movie in genre_movies if movie in movie_to_average_rating
    ]
    return sum(genre_ratings) / len(genre_ratings) if genre_ratings else 0
    
# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    # WRITE YOUR CODE BELOW
    genre_ratings = {
        genre: get_genre_rating(genre, genre_to_movies, movie_to_average_rating) for genre in genre_to_movies
    }
    return get_popular_movies(genre_ratings, n)

# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(f):
    # parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
    # return: dictionary that maps user to list of (movie,rating)
    # WRITE YOUR CODE BELOW
    user_movies = defaultdict(list)
    with open(f, 'r') as file:
        for line in file:
            movie, rating, user_id = line.strip().split('|')
            user_id = user_id.strip()
            movie_name = movie.strip()
            rating = float(rating)
            
            user_movies[user_id].append((movie_name, rating))
    return dict(user_movies)

# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    # WRITE YOUR CODE BELOW
    if user_id not in user_to_movies:
        return None
    genre_ratings = defaultdict(list)
    for movie, rating in user_to_movies[user_id]:
        if movie in movie_to_genre:
            genre = movie_to_genre[movie]
            genre_ratings[genre].append(rating)
    genre_averages = {}
    for genre, ratings in genre_ratings.items():
        genre_averages[genre] = sum(ratings) / len(ratings)
    if len(genre_averages) == 0:
        return None
    top_genre = max(genre_averages, key = genre_averages.get)
    return top_genre
# 4.3    
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    if user_id not in user_to_movies:
        return {}
    top_genre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    if top_genre is None:
        return {}
    rated_movies = set()
    for movie, _ in user_to_movies[user_id]:
        rated_movies.add(movie)
    genre_movies = {}
    for movie, rating in movie_to_average_rating.items():
        if movie not in movie_to_genre:
            continue
        if movie_to_genre[movie] != top_genre:
            continue
        if movie in rated_movies:
            continue
        genre_movies[movie] = rating
    recommend_movies = get_popular_movies(genre_movies, 3)
    return recommend_movies

# -------- main function for your testing -----
def main():
    # write all your test code here
    # this function will be ignored by us when grading
    pass
    
# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions
    
# program will start at the following main() function call
# when you execute hw1.py
main()