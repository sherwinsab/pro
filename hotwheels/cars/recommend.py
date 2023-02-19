from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from .models import Order, DETAILS
import numpy as np
import pandas as pd

class Recommedations():

    def process_recom(self,car_id):

        # Get the ratings and cars from the database
        ratings = Order.objects.all().values('customerid','carnameid','average_rating')
        # cars = DETAILS.objects.all()

        # Convert the ratings to a Pandas DataFrame
        ratings_data = list(ratings.values('customerid','carnameid','average_rating'))
        
        ratings = pd.DataFrame(ratings_data)
        # Convert the cars to a Pandas DataFrame
        # cars_data = list(cars.values())
        # cars = pd.DataFrame(cars_data)

        X, user_mapper, car_mapper, user_inv_mapper, car_inv_mapper = self.create_matrix(ratings)

        # car_make = dict(zip(cars['id'], cars['make']))



        # Find similar cars and print their makes
        similar_ids = self.find_similar_cars(car_id, car_mapper, car_inv_mapper, X, k=3)
        # car_title = car_make[car_id]
        return similar_ids
        

# # Calculate the number of ratings, unique cars, and unique users
# n_ratings = len(ratings)
# n_cars = len(ratings['car_id'].unique())
# n_users = len(ratings['user_id'].unique())

# # Calculate the average number of ratings per user and per car
# avg_ratings_per_user = round(n_ratings / n_users, 2)
# avg_ratings_per_car = round(n_ratings / n_cars, 2)

# # Create a user frequency table
# user_freq = ratings[['user_id', 'car_id']].groupby('user_id').count().reset_index()
# user_freq.columns = ['user_id', 'n_ratings']

# # Create a car statistics table
# car_stats = ratings.groupby('car_id')[['rating']].agg(['count', 'mean'])

# Create a sparse matrix for the ratings data
    def create_matrix(self, df):
        
        N = len(df['customerid'].unique())
        M = len(df['carnameid'].unique())
        
        user_mapper = dict(zip(np.unique(df["customerid"]), list(range(N))))
        car_mapper = dict(zip(np.unique(df["carnameid"]), list(range(M))))

        user_inv_mapper = dict(zip(list(range(N)), np.unique(df["customerid"])))
        car_inv_mapper = dict(zip(list(range(M)), np.unique(df["carnameid"])))

        user_index = [user_mapper[i] for i in df['customerid']]
        car_index = [car_mapper[i] for i in df['carnameid']]

        X = csr_matrix((df["average_rating"], (car_index, user_index)), shape=(M, N))

        return X, user_mapper, car_mapper, user_inv_mapper, car_inv_mapper



# Find similar cars using k-nearest neighbors
    def find_similar_cars(self, car_id, car_mapper, car_inv_mapper, X, k, metric='cosine', show_distance=False):
        neighbour_ids = []
        car_ind = car_mapper[car_id]
        car_vec = X[car_ind]
        k += 1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
        kNN.fit(X)
        car_vec = car_vec.reshape(1, -1)
        neighbour = kNN.kneighbors(car_vec, return_distance=show_distance)

        for i in range(0, k):
            n = neighbour.item(i)
            neighbour_ids.append(car_inv_mapper[n])
        neighbour_ids.pop(0)
        return neighbour_ids

rec_obj = Recommedations()