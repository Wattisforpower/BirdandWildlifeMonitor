import ML_Model
import ML_Model_Test


BC = ML_Model_Test.BirdClassifier_Test('Data', 200, 200, 16)

BC.LoadinImages(0.2)

BC.ConfigureDataset()

BC.AugmentData('horizontal', 0.4, 0.3)

BC.Model('elu', 'elu', 'same', 0.25, 0.5)
#BC.Model_MultiLayerPerceptron()


BC.TrainModel(200, 'adam')

BC.PlotResults('CNNV7.png')

BC.SaveModel('CNN_ELU_V7.tflite')