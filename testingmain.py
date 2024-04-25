import tensorflow as tf
import numpy as np
import pandas as pd
import librosa
import matplotlib
from Toolboxes import Predictor_Toolbox

System = Predictor_Toolbox.RunPredictor()

def LoadAudio(audiopath):
    LoadingBuffer, sr = librosa.load(audiopath, sr = 48000)

    X_STFT = librosa.stft(LoadingBuffer)

    X_db = librosa.amplitude_to_db(np.abs(X_STFT))

    return X_db.flatten()

System.runClassifier('BIRD_RECORDINGS/BlackheadedGull/BlackheadedGull1_split_2_SNR_50.wav', False)

'''
df = pd.read_csv('dataset2.csv', low_memory = False)

df = df.T

print(df.head())

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