import numpy as np
import pandas as pd

# Not possible as it is not a binary classification!

class Hebbnet:
    def __init__(self) -> None:
        self.Weights = np.zeros((400774, 1))

    def OpenData(self):
        # Load the Data

        df = pd.read_csv('dataset2.csv', low_memory = False)

        df = df.T

        print(df.head())

        class_names = df.pop(400776)
        
        d = dict.fromkeys(df.select_dtypes(object).columns, np.float32)
        df = df.astype(d)

        self.classes = df.pop(400775)

        names = list(i for i in range(0, 400774))
        self.numeric_values = df[names]
    
    def preprocessing(self) -> pd.DataFrame:
        # Normalize the data using mean normalization

        self.NormalizedData = (self.numeric_values - self.numeric_values.min()) / (self.numeric_values.std())

        return self.NormalizedData
    
    def trainData(self):
        arr = self.NormalizedData.to_numpy()
        classes_train = self.classes.to_numpy()

        for i in range(0, 89):
            x = arr[:, i]
            y = classes_train[:, i]

            self.Weights = self.Weights + x * y




