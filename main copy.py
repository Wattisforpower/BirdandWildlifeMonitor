#https://www.youtube.com/watch?v=YdJY65uXopw

import tensorflow as tf
from tflite_support import metadata as md
from tflite_support import metadata_schema_py_generated as mds
import os
import numpy as np

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

TF_MODEL_FILE_PATH = 'TfliteModels/CNN_InternalDropout_V1.tflite'
TF_MODEL_JSON_FILE = 'TfliteModels/CNN_InternalDropout_V1.json'

Input = 'PredictiveData/BarnSwallow-1.jpeg'


img = tf.keras.utils.load_img(
    Input, target_size=(200, 200)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

interpreter = tf.lite.Interpreter(model_path= TF_MODEL_FILE_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#print(input_details, output_details)

interpreter.set_tensor(input_details[0]['index'], img_array)

interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])

print(output_data)
print(output_data.shape)

maxval = np.argmax(output_data)

prediction = tf.nn.softmax(output_data)

probability = prediction[0][maxval]

preds = list(prediction[0])
preds.sort(reverse = True)


print(preds[0])

# metadata
displayer = md.MetadataDisplayer.with_model_file(TF_MODEL_FILE_PATH)
json_file = displayer.get_metadata_json(TF_MODEL_JSON_FILE)

with open(TF_MODEL_JSON_FILE, 'w') as f:
  f.write(json_file)

  