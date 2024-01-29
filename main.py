import tensorflow as tf
import numpy as np
import PIL

TF_MODEL_FILE_PATH = 'TfliteModels/CNN_ELU_V3.tflite'

interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)

print(interpreter.get_signature_list())

classify_lite = interpreter.get_signature_runner('serving_default')

Input = 'PredictiveData/Icelandic_Redwing-1.jpeg'


img = tf.keras.utils.load_img(
    Input, 
    target_size=(200, 200)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

predictions_lite = classify_lite(sequential_input=img_array)['dense_1']
score_lite = tf.nn.softmax(predictions_lite)

class_names = ['BarnSwallow',
               'BlackheadedGull',
               'CommonGuillemot',
               'CommonStarling',
               'Dunlin',
               'EurasianOysterCatcher',
               'EuropeanGoldenPlover',
               'HerringGull',
               'NorthernLapwing',
               'Redwing']


print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score_lite)], 100 * np.max(score_lite))
)

