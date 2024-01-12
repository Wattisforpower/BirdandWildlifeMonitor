import ML_Model
import ML_Model_Test


BC = ML_Model_Test.BirdClassifier_Test('Data', 200, 200, 32)

BC.LoadinImages(0.2)

BC.ConfigureDataset()

BC.AugmentData('horizontal', 0.1, 0.1)

BC.Model('elu', 'elu', 'same', 0.25, 0.5)
#BC.Model_MultiLayerPerceptron()

BC.printclassnames()

BC.TrainModel(400, 'adam')

BC.PlotResults('elueluAdamV1.png')

BC.SaveModel('CNN_ELU_V2.tflite')