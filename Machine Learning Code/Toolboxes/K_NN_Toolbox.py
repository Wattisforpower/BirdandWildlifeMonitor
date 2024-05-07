from sklearn.neighbors import KNeighborsClassifier
from Toolboxes import Neural_Network_Toolbox as NNT


class KNN:
    def __init__(self) -> None:
        self.Neural = NNT.Neural_Networks()
    
    def runclassification(self) -> None:
        self.Neural.RunPreprocessing()
        
        classes = self.Neural.classes
        Datapoints = self.Neural.numeric_values

        knn = KNeighborsClassifier(n_neighbors=1)

        knn.fit(Datapoints, classes)

        



