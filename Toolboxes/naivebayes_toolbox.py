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
        # Seprate classes by their numbers and then pop off the class identifier
        classgroups = self.data.groupby(400775)

        self.Group_One = classgroups.get_group(1)
        self.Group_One.pop(400775)
        self.Group_Two = classgroups.get_group(2)
        self.Group_Two.pop(400775)
        self.Group_Three = classgroups.get_group(3)
        self.Group_Three.pop(400775)
        self.Group_Four = classgroups.get_group(4)
        self.Group_Four.pop(400775)
        self.Group_Five = classgroups.get_group(5)
        self.Group_Five.pop(400775)
        self.Group_Six = classgroups.get_group(6)
        self.Group_Six.pop(400775)
        self.Group_Seven = classgroups.get_group(7)
        self.Group_Seven.pop(400775)
        self.Group_Eight = classgroups.get_group(8)
        self.Group_Eight.pop(400775)
        self.Group_Nine = classgroups.get_group(9)
        self.Group_Nine.pop(400775)
        self.Group_Ten = classgroups.get_group(10)
        self.Group_Ten.pop(400775)
        
        print(self.Group_One.head())
    
    def mean(self):
        self.Mean1 = self.Group_One.mean()
        self.Mean2 = self.Group_Two.mean()
        self.Mean3 = self.Group_Three.mean()
        self.Mean4 = self.Group_Four.mean()
        self.Mean5 = self.Group_Five.mean()
        self.Mean6 = self.Group_Six.mean()
        self.Mean7 = self.Group_Seven.mean()
        self.Mean8 = self.Group_Eight.mean()
        self.Mean9 = self.Group_Nine.mean()
        self.Mean10 = self.Group_Ten.mean() 
