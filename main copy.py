#https://www.youtube.com/watch?v=YdJY65uXopw

import tensorflow as tf
import os
import numpy as np

model = tf.saved_model.load('saved_model')

converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model(model)
tflite_model = converter.convert()

with open("SGD_Model.tflite", 'w') as f:
  f.write(tflite_model)

  