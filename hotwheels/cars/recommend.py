import numpy as np
import pandas as pd

ratings = pd.read_csv("ratings.csv")
ratings.head()

cars = pd.read_csv("cars.csv")
cars.head()

n_ratings = len(ratings)
n_cars = len(ratings['carId'].unique())
n_users = len(ratings['userId'].unique())

print(f"Number of ratings: {n_ratings}")
print(f"Number of unique carId's: {n_cars}")
print(f"Number of unique users: {n_users}")
print(f"Average ratings per user: {round(n_ratings / n_users, 2)}")
print(f"Average ratings per cars: {round(n_ratings / n_cars, 2)}")

user_freq = ratings[['userId', 'carId']].groupby('userId').count().reset_index()
user_freq.columns = ['userId', 'n_ratings']
# user_freq.head()
# print(user_freq.head(101))


car_stats = ratings.groupby('carId')[['rating']].agg(['count', 'mean'])
# print(car_stats)

from scipy.sparse import csr_matrix
def create_matrix(df):
    N = len(df['userId'].unique())
    M = len(df['carId'].unique())
    # print(N)
    # print(M)

    user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
    car_mapper = dict(zip(np.unique(df["carId"]), list(range(M))))
    # print(user_mapper)
    # print(car_mapper)

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
    car_inv_mapper = dict(zip(list(range(M)), np.unique(df["carId"])))
    # print(user_inv_mapper)
    # print(car_inv_mapper)

    user_index = [user_mapper[i] for i in df['userId']]
    car_index = [car_mapper[i] for i in df['carId']]

    X = csr_matrix((df["rating"], (car_index, user_index)), shape=(M, N))
    # print(X)

    return X, user_mapper, car_mapper, user_inv_mapper, car_inv_mapper


X, user_mapper, car_mapper, user_inv_mapper, car_inv_mapper = create_matrix(ratings)


from sklearn.neighbors import NearestNeighbors


def find_similar_cars(car_id, X, k, metric='cosine', show_distance=False):

    neighbour_ids = []
    car_ind = car_mapper[car_id]
    car_vec = X[car_ind]
    k += 1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    car_vec = car_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(car_vec, return_distance=show_distance)
    # print(neighbour)

    for i in range(0, k):
        n = neighbour.item(i)
        # print(n)
        neighbour_ids.append(car_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids


car_make = dict(zip(cars['carId'], cars['make']))
# print(car_make)

car_id = int(input("Enter the car id you have : "))
# print(car_id)

similar_ids = find_similar_cars(car_id, X, k=5)
car_title = car_make[car_id]
print(f"Since you are looking for car : {car_title}")
print("Recommend Cars are : ")

for i in similar_ids:
    print(car_make[i])

