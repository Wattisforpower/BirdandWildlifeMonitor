import numpy as np
from Toolboxes import Buffer_Toolbox as BT
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics
import pathlib
import os
import pygad.kerasga
import pygad


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

        df = pd.read_csv('dataset2.csv', low_memory = False)

        df = df.T

        print(df.head())

        class_names = df.pop(400776)
        
        d = dict.fromkeys(df.select_dtypes(object).columns, np.float32)
        df = df.astype(d)

        self.classes = df.pop(400775)

        names = list(i for i in range(0, 400774))
        self.numeric_values = df[names]
        self.numeric_tensors = tf.convert_to_tensor(self.numeric_values)
        self.class_tensors = tf.convert_to_tensor(self.classes)

        # Normalize the data
        self.normalization_layer = tf.keras.layers.Normalization(axis = -1)
        self.normalization_layer.adapt(self.numeric_tensors)


        # Batch the data

        self.numeric_dataset = tf.data.Dataset.from_tensor_slices((self.numeric_tensors, self.class_tensors))

        self.numeric_batches = self.numeric_dataset.shuffle(10).batch(32)

        

    def RunPreprocessing(self) -> None:
        self.__Preprocessing()

    def __DevelopedModel(self):
        model = tf.keras.Sequential([
            self.normalization_layer,
            tf.keras.layers.Dense(4, input_shape = (400774,), activation = tf.nn.elu),
            tf.keras.layers.Dense(16, activation = tf.nn.elu),
            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dense(256, activation = tf.nn.elu),
            tf.keras.layers.Dropout(0.3),

            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dense(256, activation = tf.nn.elu),
            tf.keras.layers.Dropout(0.3),

            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dense(256, activation = tf.nn.elu),
            tf.keras.layers.Dropout(0.3),

            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dense(256, activation = tf.nn.elu),
            tf.keras.layers.Dense(128, activation = tf.nn.elu),
            tf.keras.layers.Dropout(0.3),
                                  
            tf.keras.layers.Dense(11, activation = tf.nn.softmax)
        ])

        return model
    
    def __Train(self) -> None:
        self.epochs = 20
        self.Optimizer = tf.keras.optimizers.Adam()

        self.Model = self.__DevelopedModel()      
        
        self.Model.compile(
            optimizer = self.Optimizer,
            loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
            metrics = ['accuracy']
        )

        self.Model.summary()

        self.History = self.Model.fit(
            self.numeric_batches.repeat(),
            steps_per_epoch = 100,
            epochs = self.epochs
        )
    
    def __PlotResults(self):
        acc = self.History.history['accuracy']
        #val_acc = self.History.history['val_accuracy']

        loss = self.History.history['loss']
        #val_loss = self.History.history['val_loss']

        epochs_range = range(self.epochs)

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        #plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        #plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.savefig('FIGURE.png')
        plt.show()
        
    def fitness_func(self, ga_instance, solution, sol_idx):
        model = self.__DevelopedModel()

        model_weights_matrix = pygad.kerasga.model_weights_as_matrix(model=model, weights_vector=solution)
        model.set_weights(weights=model_weights_matrix)

        predictions = model.predict(self.numeric_batches)

        scce = tf.keras.losses.CategoricalCrossentropy()
        loss = scce(self.Data_Outputs, predictions).numpy()

        fitness_value = 1.0 / loss

        return fitness_value

    def callback_generation(self, ga_instance):
        print("Generation = {generation}".format(generation=ga_instance.generations_completed))
        print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))

    def GAHead(self):
        self.__Preprocessing()
        model = self.__DevelopedModel()
        self.Data_Outputs = tf.keras.utils.to_categorical(self.classes.to_numpy())

        Keras_ga = pygad.kerasga.KerasGA(model = model, num_solutions = 10)

        initial_population = Keras_ga.population_weights

        num_generations = 10
        num_parents_mating = 5

        Ga_Instance = pygad.GA(num_generations= num_generations,
                               num_parents_mating= num_parents_mating,
                               initial_population= initial_population,
                               mutation_type= "random",
                               fitness_func= self.fitness_func,
                               on_generation= self.callback_generation)
        
        Ga_Instance.run()
        
        Ga_Instance.plot_result(title="PyGAD & Keras - Iteration vs. Fitness", linewidth=4)

        solution, solution_fitness, solution_idx = Ga_Instance.best_solution()

        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx))

        best_solution_weights = pygad.kerasga.model_weights_as_matrix(model=model, weights_vector=solution)
        model.set_weights(best_solution_weights)
        predictions = model.predict(self.numeric_batches)
        print("Predictions : \n", predictions)

        scce = tf.keras.losses.SparseCategoricalCrossentropy()
        absolute_loss = scce(self.classes, predictions).numpy()

        print(f"Abosulte Error : {absolute_loss}")



    def SaveModel(self, ModelName):
        converter = tf.lite.TFLiteConverter.from_keras_model(self.Model)
        tflite_model = converter.convert()

        with open(ModelName, 'wb') as f:
            f.write(tflite_model)

    def run(self):
        self.__Preprocessing()
        self.__Train()
        self.__PlotResults()