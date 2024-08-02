class KNNTransform:
    def transformData(lifter):
        metricsArr = []
        for point in lifter.positional_points:
            vectorString = ""
            vectorString += point.points + point.distances + str(lifter.weight)
            metricsArr.append(vectorString.split())

        return metricsArr