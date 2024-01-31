import Buffer_Toolbox
import Neural_Network_Toolbox

NN = Neural_Network_Toolbox.Neural_Networks()



'''
Buff = Buffer_Toolbox.Buffer(520, 20, 1)

Data = Buff.RandomDataGenerator()

Buff.BufferLoad(Data)
Buff.BufferLoad(Data)

Buff.ConverttoData(False, 'Audio/BarnswallowMB/BarnSwallow.wav')
'''

import tensorflow as tf
import numpy as np
import PIL

TF_MODEL_FILE_PATH = 'DNN_V3.1.tflite'

interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)

print(interpreter.get_signature_list())

classify_lite = interpreter.get_signature_runner('serving_default')

Input = NN.Buffers.ConverttoData(False, 'Audio/BarnswallowMB/SplitData/BarnSwallow1_split_1.wav')

predictions_lite = classify_lite(normalization_input=Input[:-1])['dense_14']
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
    "This Source most likely to be a {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score_lite) - 1], 100 * np.max(score_lite))
)

'''

##################

import tensorflow as tf
import numpy as np
import PIL

TF_MODEL_FILE_PATH = 'TfliteModels/CNN_ELU_V3.tflite'

interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)

print(interpreter.get_signature_list())

classify_lite = interpreter.get_signature_runner('serving_default')

Input = 'unclassified_image.jpeg'


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


#NN.PrepData()

NN.run()

NN.SaveModel('DNN_V2.tflite')
'''