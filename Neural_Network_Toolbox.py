import numpy as np
import Buffer_Toolbox as BT
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import os


class Neural_Networks:
    def __init__(self) -> None:
        self.Buffers = BT.Buffer(520, 20, 20000)


    def PrepData(self) -> None:
        # Barnswallow
        path = pathlib.Path('Audio').with_suffix('')
        ListOfItems = list(path.glob('*/SplitData/*.wav'))
        self.Dataframe = pd.DataFrame()

        for item in ListOfItems:
            data = self.Buffers.ConverttoData(False, item)

            filename = os.path.dirname(item)
            filename = filename.split('\\')
            print(filename[1])

            Class_Value = 0

            if filename[1] == 'BarnswallowMB':
                Class_Value = 1

            elif filename[1] == 'BlackheadedGullMB':
                Class_Value = 2
            
            elif filename[1] == 'CommonGuillemotMB':
                Class_Value = 3

            elif filename[1] == 'CommonStarlingMB':
                Class_Value = 4

            elif filename[1] == 'DunlinMB':
                Class_Value = 5

            elif filename[1] == 'EurasianOysterCatcherMB':
                Class_Value = 6

            elif filename[1] == 'EuropeanGoldenPloverMB':
                Class_Value = 7

            elif filename[1] == 'HerringGullMB':
                Class_Value = 8

            elif filename[1] == 'NorthernLapwingMB':
                Class_Value = 9

            elif filename[1] == 'RedwingMB':
                Class_Value = 10

            series = pd.Series(data, name = item)
            file_data = {filename[1]}
            series.loc[len(series)] = Class_Value

            series = pd.to_numeric(series, errors = 'coerce').astype('float32')

            series.loc[len(series)] = file_data
            

            self.Dataframe = pd.concat([self.Dataframe, series.to_frame()], axis = 1)
        
               
        self.Dataframe.to_csv('dataset2.csv', index = False, encoding = 'utf-8')
            

    def __Preprocessing(self) -> None:
        # Load the Data

        df = pd.read_csv('dataset.csv', low_memory = False, skiprows = 1)

        df = df.T

        class_names = df.pop(400775)
        self.classes = df.pop(400774)
        
        print(df.dtypes)

        names = list(i for i in range(0, 400773))
        numeric_values = df[names]
        self.numeric_tensors = tf.convert_to_tensor(numeric_values)
        self.class_tensors = tf.convert_to_tensor(self.classes)

        #self.numeric_dataset = tf.data.Dataset.from_tensor_slices((self.numeric_tensors, self.class_tensors))

        #self.numeric_batches = self.numeric_dataset.shuffle(10).batch(32)
        

    def RunPreprocessing(self) -> None:
        self.__Preprocessing()

    def __DevelopedModel(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(4, input_shape = (400773,), activation = tf.nn.elu),
            tf.keras.layers.Dense(16, activation = tf.nn.elu),
            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dense(256, activation = tf.nn.elu),
            tf.keras.layers.Dense(128, activation = tf.nn.elu),
                                  
            tf.keras.layers.Dense(10, activation = tf.nn.softmax)
        ])

        return model
    
    def __Train(self) -> None:
        self.epochs = 100
        self.Optimizer = tf.keras.optimizers.Adam()

        Model = self.__DevelopedModel()      
        
        Model.compile(
            optimizer = self.Optimizer,
            loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
            metrics = ['accuracy']
        )

        Model.summary()

        self.History = Model.fit(
            self.numeric_tensors,
            self.class_tensors,
            epochs = self.epochs
        )
    
    def __PlotResults(self, SaveName):
        acc = self.History.history['accuracy']
        val_acc = self.History.history['val_accuracy']

        loss = self.History.history['loss']
        val_loss = self.History.history['val_loss']

        epochs_range = range(self.Epochs)

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.savefig(SaveName)
        plt.show()


    def run(self):
        self.__Preprocessing()
        self.__Train()
        self.__PlotResults()