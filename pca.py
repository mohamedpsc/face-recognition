import numpy
from sklearn.neighbors import KNeighborsClassifier
import database_reader as reader
import logging 
logging.basicConfig(level=logging.INFO)

def deviationMatrix(matrix):
    ones = numpy.ones((1, matrix.shape[0]))
    devMatrix = matrix - ((ones * matrix)/matrix.shape[0])
    return devMatrix

def covariance(matrix):
    covMatrix = matrix.getT() * matrix
    return covMatrix / matrix.shape[0]

def pca(matrix, threshold, eigValues=None, eigVectors=None):
    # eigen Values and Vectors Calculated For first Time
    if eigValues is None or eigVectors is None:
        devMatrix = deviationMatrix(matrix)
        covMatrix = covariance(devMatrix)
        eigValues, eigVectors = numpy.linalg.eigh(covMatrix)
        # Saving eigen Values and Vectors into Files
        # numpy.save('eigValues', eigValues)
        # numpy.save('eigVectors', eigVectors)
    # Finding Number Of Dimensions To Project Data on
    sum = eigValues.sum()
    num = 0
    count = eigValues.shape[0]
    while num/sum < threshold:
        count -= 1
        num += eigValues[count]
    # Return Projection Matrix
    return eigVectors[:, count:eigValues.shape[0]]

def classify(alpha):
    global train_data, test_data, train_labels, test_labels
    global eigValues, eigVectors
    projection_matrix = pca(train_data, alpha, eigValues, eigVectors)
    projected_data = test_data * projection_matrix
    print(projection_matrix.shape)
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(train_data * projection_matrix, train_labels.flat)
    logging.debug(projected_data.shape)
    return neigh.score(projected_data, test_labels.flat)

'''
loading constants 
'''
train_data, train_labels, test_data, test_labels = reader.load_non_human(100)

from os import path
# if path.exists('eigValues.npy') and path.exists('eigVectors.npy'):
#     logging.info("Found eigen...loading...")
#     eigValues = numpy.load('eigValues.npy')
#     eigVectors = numpy.load('eigVectors.npy')
# else:

logging.info("Recomputing eigen..")
eigValues = None
eigVectors = None


if __name__ == '__main__':
    from os import path

    # For alpha = 0.8
    for i in [0.8, 0.85, 0.9, 0.95]:
         print(classify(i))
