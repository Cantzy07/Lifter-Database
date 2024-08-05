import numpy as np
from sklearn.neighbors import NearestNeighbors

class KNNTransform:
    def transformData(lifter):
        metricsArr = []
        for point in lifter.positional_points:
            vectorString = ""
            vectorString += point.points + " " + point.distances + " " +  str(lifter.weight)
            temp_array = vectorString.split()
            string_to_int_array = [float(value) for value in temp_array]
            metricsArr.append(string_to_int_array)
            # metricsArr.append(vectorString.split())

        return metricsArr
    
    def findKNN(individual, data):
        individual_array = np.array(individual).reshape(1, -1)
        data_array = np.array(data)

        knn = NearestNeighbors(n_neighbors=1, metric='euclidean')
        knn.fit(data_array)

        distances, indices = knn.kneighbors(individual_array)

        most_similar_metric = data[indices[0][0]]

        return most_similar_metric