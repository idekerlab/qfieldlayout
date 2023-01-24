import numpy as np
import sklearn
from sklearn.neighbors import KernelDensity


# create a 2d dataset with 100 points
X = np.random.rand(100, 2)


# In this example, the mean function is used to calculate
# the centroid of the dataset, and the linalg.norm function
# is used to calculate the Euclidean distance of each point
# from the centroid. The var function is then used to
# compute the variance of the distances.

def coordinate_variance(point_array):
    # calculate the centroid of the dataset
    centroid = np.mean(X, axis=0)
    # calculate the distance of each point from the centroid
    distances = np.linalg.norm(X - centroid, axis=1)

    # calculate the variance of the distances
    variance = np.var(distances)
    return variance


def coordinate_density(point_array):
    # calculate the centroid of the dataset
    centroid = np.mean(point_array, axis=0)

    # create a kernel density estimator
    kde = KernelDensity(kernel='gaussian', bandwidth=0.2)

    # fit the estimator to the data
    kde.fit(point_array)

    # evaluate the density at the centroid
    density = np.exp(kde.score_samples([centroid]))
    return density


