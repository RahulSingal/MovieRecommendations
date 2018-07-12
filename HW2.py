# Assignment: Cpts 315 HW 2 - Movie Recommendations
# Programmer: Rahul Singal (11471764)
# Date Created: 2/20/19
# Date Last Edited: 2/27/18
# Description: Use the item-item collaborative filtering algorithm to 
#               provide movie recommendations for users
# Collaborators: Prof. Doppa in class pseduocode & slides

from numpy import dot
from numpy.linalg import norm
from itertools import combinations
from itertools import permutations


"""
Steps:
Import movieId and corresponding 
Make each item (Moviqe) have an array representing the ratings for each user from id ? to id ? (total of 671 users)
    All user`s who have not rated the movie will be put to zero

Make a centered_cosine_similarity function that calculates given two movie vectors
    Store in a variable that holds are scores...

Make a function that finds the top N neighborhood movies based on score above

Find users who did not rate the movie in the neighborhood set and estimate a rating based on ???

Compute the recommended movies for each user...



"""
def intersection(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

# Read ratings.csv
filename = open('ratings.csv', 'r')
dataset = filename.read().splitlines()
filename.close()

# Read movies.csv
filename1 = open('movies.csv', 'r')
dataset1 = filename1.read().splitlines()
filename1.close()

# 9125 movies, 671 users
num_movies, num_users = 9126, 672

#Initialize Item_profile to a Matrix with 671 users and 9125 corresponding users
item_profile = [[0 for x in range(num_users)] for y in range(num_movies)]

#Temporary for converting movieId to numeric value incrementing by 1
temp_Movie_Id = {}

#Get rid of the first line in each dataset
dataset = dataset[1:] 
dataset1 = dataset1[1:] 

#For incremental purposes
i = 1

#Used for converting MovieId to value incrementing by 1
for line in dataset1:
    temp = line.split(',') #temp contains movieId, title, genre
    temp_Movie_Id[int(temp[0])] = i
    i = i + 1

indexing_Id = 0

#Creating item_profile which will include zeros for no ratings
for line in dataset:
    temp = line.split(',') # temp contains [userId, movieId, rating, timestamp]
    userId = int(temp[0])
    movieId = int(temp[1])
    indexing_Id = temp_Movie_Id[movieId]
    rating = float(temp[2])
    item_profile[indexing_Id][userId] = rating
    
#Will be a dict of dict to store only users who have given a rating for the movie    
movie_vectors = {}

#Initializing the dict of dict with 9126 movies 
for x in range(0, 9126):
    movie_vectors[x] = {}    
  
#Going through every movie and corresponding user and only putting the non-zero value in the movie_vector dict      
for movie in range(0, 9126):
    for user in range(0, 672):
        if (item_profile[movie][user] != 0):
            #Store in a dict of dicts
            movie_vectors[movie][user] = item_profile[movie][user]

#Normalizing the Matrix, since we have to eventually calcualte Centered-Cosine Similarity
for movie in range(0, 9126):
    keys = (list) (movie_vectors[movie].keys())
    size = len(movie_vectors[movie])
    if (size != 0):
        list_of_ratings = (list) (movie_vectors[movie].values())
        sum_ratings = 0
        mean = 0
        for x in range(0, size):
            sum_ratings = sum_ratings + list_of_ratings[x]
        mean = sum_ratings / size
        for user in keys:
            movie_vectors[movie][user] = movie_vectors[movie][user] - mean
    else:
        #Size is zero so do nothing...
        mean = 0
        
#Storing movies which are "irrelevant"
irrelevant_movies = []

#Find "irrelevant" movies.. if empty dict or normalized rating of 0.0, then it will not be used for cosine similarity
for movie in range(0, 9126):
    if (movie_vectors[movie] == {}):
        #Disregard this movie
        irrelevant_movies.append(movie)
    elif (len(movie_vectors[movie]) == 1):
        #Disregard this movie
        irrelevant_movies.append(movie)

#Now set a placeholder for irrelevant movies
for movie in irrelevant_movies:
    del movie_vectors[movie]
    #movie_vectors[movie] = {}

x = (list) (movie_vectors.keys())
pairs = (list) (permutations(x, 2))    

#Key is the movie, value is the corresponding users who have given a rating as a list
movie_users_dict = {}

#Key is the movie, value is the norm for that movie
movie_norm_dict = {}

for movie in x:
    movie_users_dict[movie] = (list) (movie_vectors[movie].keys())  
    list_of_ratings = (list) (movie_vectors[movie].values())   
    movie_norm_dict[movie] = (norm(list_of_ratings))

index = 0

""" REMOVING EVERYTHING WITH TEST LATER ON..... """

#Add the cosine similarity for each pair tuple...
for pair in pairs:
    Movie1_User_Ratings = []
    Movie2_User_Ratings = []
    Movie1 = pair[0]
    Movie2 = pair[1]
    Movie1_Users = movie_users_dict[Movie1]
    Movie2_Users = movie_users_dict[Movie2]
    User_Intersection = intersection(Movie1_Users, Movie2_Users)
    if (len(User_Intersection) > 0):
        for user in User_Intersection:
            Movie1_User_Ratings.append(movie_vectors[Movie1][user])
            Movie2_User_Ratings.append(movie_vectors[Movie2][user]) 
        numerator = dot(Movie1_User_Ratings, Movie2_User_Ratings)
        denominator = (movie_norm_dict[Movie1]) * (movie_norm_dict[Movie2])
        if (denominator != 0):    
            cosine_similarity = numerator / denominator
        else:
            cosine_similarity = 0
        pairs[index] = list(pairs[index])
        pairs[index].append(cosine_similarity)
        #print(test_pairs[index][0])
    else:
        cosine_similarity = 0
        pairs[index] = list(pairs[index])
        pairs[index].append(cosine_similarity)
    index = index + 1


""" IT TAKE APPROXIMATELY 240 SECONDS (4 minutes) TO RUN THE ABOVE"""




    


 

    
    


  
