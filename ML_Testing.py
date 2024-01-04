import ML_Model

# all relu model

BC = ML_Model.BirdClassifier('Data', 200, 200, 32)

BC.LoadinImages(0.2)

BC.ConfigureDataset()

BC.AugmentData('horizontal', 0.1, 0.1)

BC.Model('relu', 'relu', 'same', 0.2)

BC.TrainModel(400, 'adam')

BC.PlotResults('relureluAdamV2.png')

BC.SaveModel('modelV2.tflite')