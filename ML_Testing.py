import ML_Model_Test


BC = ML_Model_Test.BirdClassifier_Test('Data', 200, 200, 32)

BC.LoadinImages(0.2)

BC.ConfigureDataset()

BC.AugmentData('horizontal', 0.4, 0.3)

BC.Model('elu', 'elu', 'same', 0.25)
#BC.Model_MultiLayerPerceptron()


BC.TrainModel(200, 'adam')

BC.PlotResults('CNN_L2_V7.png')

BC.SaveModel('CNN_ELU_V7.tflite')