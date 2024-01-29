import librosa
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import scipy.signal as sig

class Buffer:
    def __init__(self, buffersize, timeframe, samplerate) -> None:
        self.MaxSize = buffersize * timeframe * samplerate
        self.samplerate = samplerate
        self.BuffOne = np.empty(0)
        self.BuffTwo = np.empty(0)
        self.LoadingBuffer = np.empty(0)
        
    def BufferLoad(self, data):
        self.BuffTwo = self.BuffOne

        self.BuffOne = data


    def __BufferOffload(self):
        self.LoadingBuffer = self.BuffTwo

    def ConverttoSpectograph(self):
        self.__BufferOffload()

        X_STFT = librosa.stft(self.LoadingBuffer)

        X_db = librosa.amplitude_to_db(np.abs(X_STFT))

        plt.figure(figsize=(120, 10))
        librosa.display.specshow(X_db, sr = self.samplerate, x_axis = 'time', y_axis = 'hz', shading = 'auto')
        plt.axis('off')
        plt.show()

    def RandomDataGenerator(self):
        TempData = np.empty(0)
        for x in range(0, self.MaxSize):
            y = rd.randint(0, 1048576)
            TempData = np.append(TempData, y)
        
        return TempData
    
    def SineWave(self)