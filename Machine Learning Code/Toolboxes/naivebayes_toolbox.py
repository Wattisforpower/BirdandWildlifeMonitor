#https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import scipy
from joblib import dump, load
import pandas as pd
import numpy as np

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
        self.classes = self.data.pop(400775)

        # Convert from objects to floats
        d = dict.fromkeys(self.data.select_dtypes(object).columns, np.float32)
        self.data = self.data.astype(d)

        self.numeric_input = self.data[list(i for i in range(0, 400774))]

    def TrainClassifier(self) -> None:
        # Absolute the data
        Input = np.abs(self.numeric_input.to_numpy())
        
        # Scale the Data
        X_train = preprocessing.MinMaxScaler().fit_transform(Input)


        clf = MultinomialNB()
        clf.fit(X_train, self.classes)

        dump(clf, 'MultiClassNaiveBayesClassifierV1.joblib')
    
    def RunClassifier(self, source) -> None:
        # convert source to a numpy array
        Input = source.reshape(1, -1)
        Input = np.abs(Input)

        # Scale the Data
        X_train = preprocessing.MinMaxScaler().fit_transform(Input)
        

        clf = load('MultiClassNaiveBayesClassifierV1.joblib')

        result = clf.predict(X_train)

        self.class_names = ['BarnSwallow',
                    'BlackheadedGull',
                    'CommonGuillemot',
                    'CommonStarling',
                    'Dunlin',
                    'EurasianOysterCatcher',
                    'EuropeanGoldenPlover',
                    'HerringGull',
                    'NorthernLapwing',
                    'Redwing']
        
        # Print the result
        print(
            "This Source most likely to be a {}."
            .format(self.class_names[int(float(result) - 1.0)])
        )
