import ML_Model
import ML_Model_Test


BC = ML_Model_Test.BirdClassifier_Test('Data', 200, 200, 16)

BC.LoadinImages(0.2)

BC.ConfigureDataset()

BC.AugmentData('horizontal', 0.1, 0.1)

BC.Model('elu', 'elu', 'same', 0.25, 0.5)
#BC.Model_MultiLayerPerceptron()


BC.TrainModel(10, 20, 'adam')

BC.PlotResults('regularizationCNNV6.png')

BC.SaveModel('CNN_ELU_V6.tflite')