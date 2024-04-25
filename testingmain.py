import tensorflow as tf
import numpy as np
import pandas as pd
import librosa
import matplotlib
from Toolboxes import Predictor_Toolbox
import pathlib
import os

#https://huggingface.co/blog/audio-datasets

System = Predictor_Toolbox.RunPredictor()

def LoadAudio(audiopath):
    LoadingBuffer, sr = librosa.load(audiopath, sr = 48000)

    X_STFT = librosa.stft(LoadingBuffer)

    X_db = librosa.amplitude_to_db(np.abs(X_STFT))

    return X_db.flatten()


def PrepData(self) -> None:
        # Barnswallow
        path = pathlib.Path('BIRD_RECORDINGS').with_suffix('')
        ListOfItems = list(path.glob('*/*.wav'))
        Dataframe = pd.DataFrame()

        for item in ListOfItems:
            data = self.Buffers.ConverttoData(False, item)

            filename = os.path.dirname(item)
            filename = filename.split('\\')
            print(filename[1])

            Class_Value = 0

            if filename[1] == 'Barnswallow':
                Class_Value = 1

            elif filename[1] == 'BlackheadedGull':
                Class_Value = 2
            
            elif filename[1] == 'CommonGuillemot':
                Class_Value = 3

            elif filename[1] == 'CommonStarling':
                Class_Value = 4

            elif filename[1] == 'Dunlin':
                Class_Value = 5

            elif filename[1] == 'EurasianOysterCatcher':
                Class_Value = 6

            elif filename[1] == 'EuropeanGoldenPlover':
                Class_Value = 7

            elif filename[1] == 'HerringGull':
                Class_Value = 8

            elif filename[1] == 'NorthernLapwing':
                Class_Value = 9

            elif filename[1] == 'Redwing':
                Class_Value = 10

            series = pd.Series(data, name = item)
            file_data = {filename[1]}
            series.loc[len(series)] = Class_Value

            series = pd.to_numeric(series, errors = 'coerce').astype('float32')

            series.loc[len(series)] = file_data
            

            self.Dataframe = pd.concat([self.Dataframe, series.to_frame()], axis = 1)
        
               
        self.Dataframe.to_csv('dataset2.csv', index = False, encoding = 'utf-8')



df = pd.read_csv('datasetWavFiles.csv', low_memory = False)

df = df.T

print(df.head())


'''

class_names = df.pop(400776)

d = dict.fromkeys(df.select_dtypes(object).columns, np.float32)
df = df.astype(d)

classes = df.pop(400775)

names = list(i for i in range(0, 400774))
numeric_values = df[names]
numeric_tensors = tf.convert_to_tensor(numeric_values)
class_tensors = tf.convert_to_tensor(classes)

# Normalize the data
normalization_layer = tf.keras.layers.Normalization(axis = -1)
normalization_layer.adapt(numeric_tensors)


# Batch the data

numeric_dataset = tf.data.Dataset.from_tensor_slices((numeric_tensors,class_tensors))

numeric_batches = numeric_dataset.shuffle(10).batch(32)



model = tf.keras.Sequential([
    normalization_layer,
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


epochs = 20
Optimizer = tf.keras.optimizers.Adam()

Model.compile(
    optimizer = Optimizer,
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
    metrics = ['accuracy']
)

model.summary()

History = model.fit(
    numeric_batches.repeat(),
    steps_per_epoch = 100,
    epochs = epochs
)
'''