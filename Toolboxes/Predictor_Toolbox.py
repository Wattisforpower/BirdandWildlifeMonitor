from Toolboxes import Neural_Network_Toolbox
import tensorflow as tf
import numpy as np
import PIL
import pathlib
import random
from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd

# Multithreading
import threading
import os

class RunPredictor:
    def __init__(self) -> None:
        self.nn = Neural_Network_Toolbox.Neural_Networks()
        self.TF_MODEL_FILE_PATH = 'DNN_V3.1.tflite'

    def runClassifier(self, source):
        # Define the interpreter and the location of the neural network model
        interpreter = tf.lite.Interpreter(model_path=self.TF_MODEL_FILE_PATH)

        print(interpreter.get_signature_list())

        # Collect the signature of the inputs and outputs of the neural network
        classify_lite = interpreter.get_signature_runner('serving_default')

        # convert the data into something readable by the neural network
        Input = self.nn.Buffers.ConverttoData(False, source)

        # Run the prediction
        predictions_lite = classify_lite(normalization_input=Input[:-1])['dense_14']
        score_lite = tf.nn.softmax(predictions_lite)

        # Class names for the conversion back from numeric classes to string classes
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
            "This Source most likely to be a {} with a {:.2f} percent confidence."
            .format(self.class_names[np.argmax(score_lite) - 1], 100 * np.max(score_lite))
        )
        
        return np.argmax(score_lite)

    def __convertToClass(self, selection):
        # convert to numeric class
        if selection == 'Barnswallow':
            return 1
        elif selection == 'BlackheadedGull':
            return 2
        elif selection == 'CommonGuillemot':
            return 3
        elif selection == 'CommonStarling':
            return 4
        elif selection == 'Dunlin':
            return 5
        elif selection == 'EurasianOysterCatcher':
            return 6
        elif selection == 'EuropeanGoldenPlover':
            return 7
        elif selection == 'HerringGull':
            return 8
        elif selection == 'NorthernLapwing':
            return 9
        elif selection == 'Redwing':
            return 10


    def GenerateConfusion(self):
        # Generates the Confusion Matrix

        # Define the actual and predicted as empty numpy arrays
        actual = np.empty(0)
        predicted = np.empty(0)

        # Collect all of the possible audio options and present them in a list
        path = pathlib.Path('Audio').with_suffix('')
        ListOfItems = list(path.glob('*/SplitData/*.wav'))
        NumberofItems = len(ListOfItems)

        # select 20 of the audio options
        for i in range(20):
            # random selection
            selection_Number = random.randint(0, NumberofItems - 1)
            selection = ListOfItems[selection_Number]

            # discover the class name based on the folder name
            filename = os.path.dirname(selection)
            filename = filename.split('\\')

            # convert to a numeric value
            selection_class = self.__convertToClass(filename[1])

            # add to actual array
            actual = np.append(actual, selection_class)

            # run the prediction on the selection
            prediction = self.runClassifier(selection)

            # add the prediction to the prediction array
            predicted = np.append(predicted, prediction)

        # Testing purposes only
        print(actual)

        print(predicted)
        
        # Generate the confusion matrix based on the actual and predicted
        confusionMat = metrics.confusion_matrix(actual, predicted)

        # convert the Matrix into a displayable version
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix= confusionMat)
        
        # Plot and save the confusion matrix
        cm_display.plot()
        plt.savefig('Confusion_Matrix')
        plt.show()
    
    def ShowPlotsOfData(self) -> None:
        data = pd.read_csv('dataset2.csv', low_memory = False)

        data = data.T

        counts = data[400775].value_counts().reset_index().rename(columns={"index": "value", 0: "count"})

        print(counts)

        plt.pie(counts[400775], labels = counts['value'], autopct = '%1.1f%%')
        plt.show()
 
    def GainData(self) -> None:
        pass
