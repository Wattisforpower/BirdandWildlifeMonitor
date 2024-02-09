#https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/

import numpy as np
import pandas as pd

class NaiveBayes:
    def __init__(self) -> None:
        pass

    def LoadData(self, source) -> None:
        # Load the Data
        self.data = pd.read_csv(source, low_memory=False)

        # Transpose the data
        self.data = self.data.T
        self.classnames = self.data.pop(400776)

    def SeperateClasses(self) -> None:

