import librosa
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import scipy.signal as sig
import spidev

class Buffer:
    def __init__(self, buffersize, timeframe, samplerate) -> None:
        self.BuffOne = np.empty(0)
        self.BuffTwo = np.empty(0)

        
        
    def BufferLoad(self, data):
        self.BuffTwo = self.BuffOne

        self.BuffOne = data


    def __BufferOffload(self):
        self.LoadingBuffer = self.BuffTwo

    def __LoadAudio(self, audiopath):
        self.LoadingBuffer, sr = librosa.load(audiopath, sr = 20000)
    

    
    def ClearBuffers(self):
        self.BuffOne = np.empty(0)
        self.BuffTwo = np.empty(0)
    

    def ConverttoData(self, Pin_Audio = True, audiopath = ''):
        
        if Pin_Audio:
            self.CollectingData()
        else:
            self.__LoadAudio(audiopath= audiopath)

        X_STFT = librosa.stft(self.LoadingBuffer)

        X_db = librosa.amplitude_to_db(np.abs(X_STFT))

        return X_db.flatten()

        
   