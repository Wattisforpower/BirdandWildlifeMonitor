import ML_Model_Test


BC = ML_Model_Test.BirdClassifier_Test('Data', 200, 200, 32)

BC.LoadinImages(0.2)

BC.ConfigureDataset()

BC.AugmentData('horizontal', 0.4, 0.3)

BC.Model('elu', 'elu', 'same', 0.25)
#BC.Model_MultiLayerPerceptron()


BC.TrainModel(400, 'adam', 0.001)

BC.PlotResults('CNN_LearningRateChange_V10.png')

BC.SaveModel('CNN_ELU_V10.tflite')