import librosa
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import scipy.signal as sig

class Buffer:
    def __init__(self, buffersize, timeframe, samplerate) -> None:
        self.MaxSize = buffersize * timeframe * samplerate
        self.samplerate = samplerate
        self.timeframe = timeframe
        self.BuffOne = np.empty(0)
        self.BuffTwo = np.empty(0)
        self.LoadingBuffer = np.empty(0)
        
    def BufferLoad(self, data):
        self.BuffTwo = self.BuffOne

        self.BuffOne = data


    def __BufferOffload(self):
        self.LoadingBuffer = self.BuffTwo

    def __LoadAudio(self, audiopath):
        self.LoadingBuffer, sr = librosa.load(audiopath, sr = 20000)


    def ConverttoData(self, Pin_Audio = True, audiopath = ''):
        
        if Pin_Audio:
            self.__BufferOffload()
        else:
            self.__LoadAudio(audiopath= audiopath)

        X_STFT = librosa.stft(self.LoadingBuffer)

        X_db = librosa.amplitude_to_db(np.abs(X_STFT))

        return X_db.flatten()

        
    def RandomDataGenerator(self):
        TempData = np.empty(0)
        for x in range(0, self.MaxSize):
            y = rd.randint(0, 1048576)
            TempData = np.append(TempData, y)
        
        return TempData
