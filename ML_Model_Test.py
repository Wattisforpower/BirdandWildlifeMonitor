import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
from sklearn.model_selection import train_test_split

import pathlib

class BirdClassifier_Test:
    def __init__(self, PathToData, MaxWidth, MaxHeight, Batch) -> None:
        # Data file
        self.DataDirectory = pathlib.Path(PathToData).with_suffix('')
        self.ImageCount =  len(list(self.DataDirectory.glob('*/*.*')))
        
        # Image Size and Batch Size
        self.BatchSize = Batch
        self.Image_Height = MaxHeight
        self.Image_Width = MaxWidth

    def LoadinImages(self, ValidationSplit):
        self.train_dataset = tf.keras.utils.image_dataset_from_directory(
            self.DataDirectory,
            validation_split = ValidationSplit,
            subset="training",
            seed=123,
            image_size=(self.Image_Height, self.Image_Width),
            batch_size=self.BatchSize
        )

        self.Validation_Dataset = tf.keras.utils.image_dataset_from_directory(
            self.DataDirectory,
            validation_split = ValidationSplit,
            subset= "validation",
            seed=123,
            image_size=(self.Image_Height, self.Image_Width),
            batch_size=self.BatchSize
        )

        self.classNames_training = self.train_dataset.class_names
        self.classNames_Validate = self.Validation_Dataset.class_names
        self.Num_Classes = len(self.classNames_training)

        self.X_Train, X_test = train_test_split(self.train_dataset, test_size= 0.2)

    def ConfigureDataset(self):
        self.Autotune = tf.data.AUTOTUNE

        self.train_dataset = self.train_dataset.cache().shuffle(10).prefetch(buffer_size = self.Autotune)
        self.Validation_Dataset = self.Validation_Dataset.cache().prefetch(buffer_size = self.Autotune)

    def AugmentData(self, FlipDirection, RotationProbability, ZoomProbability):
        self.Data_Augmentation = tf.keras.Sequential(
            [
                tf.keras.layers.RandomFlip(
                    FlipDirection,
                    input_shape = (self.Image_Height, self.Image_Width, 3)
                ),
                tf.keras.layers.RandomRotation(RotationProbability),
                tf.keras.layers.RandomZoom(ZoomProbability)
            ]
        )

    def Model(self, InternalActivation, activation, Padding, InternalDropOutValue):
        self.BirdClassifierModel = tf.keras.Sequential([
            self.Data_Augmentation,
            tf.keras.layers.Rescaling(1./255, input_shape=(self.Image_Height, self.Image_Width, 3)),

            tf.keras.layers.Conv2D(16, 3, padding=Padding, activation=InternalActivation),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),
            #tf.keras.layers.Dropout(InternalDropOutValue),

            tf.keras.layers.Conv2D(32, 3, padding=Padding, activation=InternalActivation),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),
            #tf.keras.layers.Dropout(InternalDropOutValue),

            # Added Conv2D layers

            tf.keras.layers.Conv2D(64, 3, padding=Padding, activation=InternalActivation),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),


            tf.keras.layers.Conv2D(64, 3, padding=Padding, activation=InternalActivation),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),

            tf.keras.layers.Conv2D(64, 3, padding=Padding, activation=InternalActivation),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),

            tf.keras.layers.Conv2D(128, 3, padding=Padding, activation=InternalActivation),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),

            # End of Added Conv2D layers

            tf.keras.layers.Dropout(InternalDropOutValue),
            tf.keras.layers.Flatten(),

            tf.keras.layers.Dense(128, activation = activation),
            tf.keras.layers.Dropout(InternalDropOutValue),
            tf.keras.layers.Dense(self.Num_Classes) 
        ])
    
    def Model_MultiLayerPerceptron(self):
        self.BirdClassifierModel = tf.keras.Sequential([
            self.Data_Augmentation,
            tf.keras.layers.Rescaling(1./255, input_shape=(self.Image_Height, self.Image_Width, 3)),
            tf.keras.layers.Flatten(input_shape = (32, 32)),

            tf.keras.layers.Dense(64, activation = 'relu'),
            tf.keras.layers.Dense(128, activation = 'relu'),
            tf.keras.layers.Dense(256, activation = 'relu'),
            tf.keras.layers.Dense(128, activation = 'relu'),
            tf.keras.layers.Dense(10, activation = 'relu'),
            tf.keras.layers.BatchNormalization()
            
        ])
    
    
    def TrainModel(self, Epochs, Optimizer):
        self.Epochs = Epochs

        self.BirdClassifierModel.compile(
            optimizer = Optimizer,
            loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
            metrics = ['accuracy']
        )

        self.BirdClassifierModel.summary()

        self.History = self.BirdClassifierModel.fit(
            self.train_dataset,
            validation_data = self.Validation_Dataset,
            epochs = Epochs
        )
    
    def PlotResults(self, SaveName):
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

    def Test(self, image, PercentageLimiter):
        img = tf.keras.utils.load_img(
            image, target_size = (self.Image_Height, self.Image_Width)
        )

        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # create a batch

        predictions = self.BirdClassifierModel.predict(img_array)
        self.score = tf.nn.softmax(predictions[0])

        self.percentage_Confidence = 100 * np.max(self.score)

        self.Result(PercentageLimiter)
    
    def Result(self, PercentageLimiter):
        if (self.percentage_Confidence < PercentageLimiter):
            print("Unknown Bird type!")
            print("This Bird is most likely a {} with a {:.2f} percent confidence." .format(self.classNames[np.argmax(self.score)], 100 * np.max(self.score)))
        else:
            print("This Bird is most likely a {} with a {:.2f} percent confidence." .format(self.classNames[np.argmax(self.score)], 100 * np.max(self.score)))
    
    def SaveModel(self, ModelName):
        converter = tf.lite.TFLiteConverter.from_keras_model(self.BirdClassifierModel)
        tflite_model = converter.convert()

        with open(ModelName, 'wb') as f:
            f.write(tflite_model)