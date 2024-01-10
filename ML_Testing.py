import ML_Model
import ML_Model_Test


BC = ML_Model_Test.BirdClassifier_Test('Data', 200, 200, 32)

BC.LoadinImages(0.2)

BC.ConfigureDataset()

BC.AugmentData('horizontal', 0.1, 0.1)

BC.Model('relu', 'relu', 'same', 0.2)
#BC.Model_MultiLayerPerceptron()

BC.TrainModel(400, 'adam')

BC.PlotResults('relureluAdamV2.png')

BC.SaveModel('MLP_V1.tflite')