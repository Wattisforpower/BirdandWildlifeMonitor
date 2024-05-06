import numpy as np
import tensorflow as tf
import pandas as pd
import random
import wandb
from wandb.keras import WandbMetricsLogger, WandbModelCheckpoint, WandbCallback

wandb.login()


sweep_configuration = {
    'method': 'random',
    'metric': {
        'name': 'accuracy',
        'goal': 'maximize'
    },
    'parameters': {
        'batch_size': {
            'values': [10, 21, 32, 43, 54]
        },
        'learning_rate': {
            'values': [0.01, 0.005, 0.001, 0.0005, 0.0001]
        },
        'dropout': {
            'values': [0.2, 0.3, 0.4, 0.5]
        }
    }
}

# Load the Data
df = pd.read_csv('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/dataset2.csv', low_memory = False)

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

numeric_dataset = tf.data.Dataset.from_tensor_slices((numeric_tensors, class_tensors))

numeric_batches = numeric_dataset.shuffle(10).batch(32)

# load Training Data

df = pd.read_csv('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/training_dataset4.csv', low_memory = false)

df = df.T

print(df.head())

class_names = df.pop(400776)
        
d = dict.fromkeys(df.select_dtypes(object).columns, np.float32)
df = df.astype(d)

training_classes = df.pop(400775)

names = list(i for i in range(0, 400774))
training_numeric_values = df[names]
training_numeric_tensors = tf.convert_to_tensor(training_numeric_values)
training_class_tensors = tf.convert_to_tensor(training_classes)

# Normalize the data
training_normalization_layer = tf.keras.layers.Normalization(axis = -1)
training_normalization_layer.adapt(training_numeric_tensors)

# Batch the data

training_numeric_dataset = tf.data.Dataset.from_tensor_slices((training_numeric_tensors, training_class_tensors))

training_numeric_batches = training_numeric_dataset.shuffle(10).batch(32)

def run():
    # Initialized wandb

    wandb.init(
        config = {
            "layer_1" : 4,
            "activation_1" : "tf.nn.elu",
            "dropout" : random.uniform(0.01, 0.8),
            "layer_2": 128,
            "layer_3" : 256,
            "output_layer" : 11,
            "activation_2": "tf.nn.softmax",
            "optimizer": "tf.keras.optimizers.Adam",
            "loss": "tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True)",
            "metric": "accuracy",
            "dropout": 0.2,
            "epoch": 20,
            "batch_size": 32,
            "learning_rate": 0.01
        }
    )

    config = wandb.config

    

    model = tf.keras.Sequential([
        normalization_layer,
        tf.keras.layers.Dense(config.layer_1, input_shape = (400774,), activation = tf.nn.elu),
        tf.keras.layers.Dense(16, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_2, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_3, activation = tf.nn.elu),
        tf.keras.layers.Dropout(config.dropout),

        tf.keras.layers.Dense(config.layer_2, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_2, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_3, activation = tf.nn.elu),
        tf.keras.layers.Dropout(config.dropout),

        tf.keras.layers.Dense(config.layer_2, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_2, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_3, activation = tf.nn.elu),
        tf.keras.layers.Dropout(config.dropout),

        tf.keras.layers.Dense(config.layer_2, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_2, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_3, activation = tf.nn.elu),
        tf.keras.layers.Dense(config.layer_2, activation = tf.nn.elu),
        tf.keras.layers.Dropout(config.dropout),
                                    
        tf.keras.layers.Dense(config.output_layer, activation = tf.nn.softmax)
    ])
        
    model.compile(
        optimizer = tf.keras.optimizers.Adam(),
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
        metrics = [config.metric]
    )

    model.summary()
    epochs = config.epoch

    History = model.fit(
        numeric_batches.repeat(),
        validation_data = training_numeric_batches.repeat(),
        steps_per_epoch = 100,
        validation_steps= 50,
        epochs = epochs,
        callbacks = [
            WandbMetricsLogger(log_freq= 5),
            WandbModelCheckpoint("models"),
            WandbCallback()
        ]
    )

sweep_id = wandb.sweep(sweep_configuration, project="BirdWildlifeMonitor-Sweep-Accuracy-WithValidation")

wandb.agent(sweep_id=sweep_id, function=run, count = 20)


wandb.finish()
