#https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/

import numpy as np
import pandas as pd

class NaiveBayes:
    def __init__(self) -> None:
        pass

    def LoadData(self, source) -> None:
        print("Loading Data")
        # Load the Data
        self.data = pd.read_csv(source, low_memory=False)
        print("Loaded Data")

        # Transpose the data
        self.data = self.data.T
        self.classnames = self.data.pop(400776)

        print(self.data.head())

    def SeperateClasses(self) -> None:
        classgroups = self.data.groupby(400775)

        self.Group_One = classgroups.get_group(1)
        self.Group_Two = classgroups.get_group(2)
        self.Group_Three = classgroups.get_group(3)
        self.Group_Four = classgroups.get_group(4)
        self.Group_Five = classgroups.get_group(5)
        self.Group_Six = classgroups.get_group(6)
        self.Group_Seven = classgroups.get_group(7)
        self.Group_Eight = classgroups.get_group(8)
        self.Group_Nine = classgroups.get_group(9)
        self.Group_Ten = classgroups.get_group(10)

        print(self.Group_One.head())
    
    def __mean(self, num)
        
