import librosa
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import scipy.signal as sig
import spidev

class Buffer:
    def __init__(self, buffersize, timeframe, samplerate) -> None:
        Bus = 0
        Device = 0

        self.SPI = spidev.SpiDev()
        self.SPI.open(Bus, Device)
        
        self.SPI.max_speed_hz = samplerate
        self.SPI.mode = 0
        
        
        self.MaxSize = buffersize * timeframe * samplerate
        self.samplerate = samplerate
        self.timeframe = timeframe
        self.BuffOne = np.empty(0)
        self.BuffTwo = np.empty(0)
        self.LoadingBuffer = np.empty(0)
        self.InstreamBuffer = np.empty(0)
        
        
    def BufferLoad(self, data):
        self.BuffTwo = self.BuffOne

        self.BuffOne = data


    def __BufferOffload(self):
        self.LoadingBuffer = self.BuffTwo

    def __LoadAudio(self, audiopath):
        self.LoadingBuffer, sr = librosa.load(audiopath, sr = 20000)
    
    def ReverseBits(self, byte):
        byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
        byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
        byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
        
        return byte
    
    def CollectingData(self):
        #data = self.SPI.readbytes(1)
        data = self.SPI.xfer2([0x80, 0x00], self.samplerate, 0)
        
        #data = self.ReverseBits(data)
        
        self.BuffOne = np.append(self.BuffOne, data)
    
    def PrintContentsOfBuffer(self):
        print(self.BuffOne)
    
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

        
    def RandomDataGenerator(self):
        TempData = np.empty(0)
        for x in range(0, self.MaxSize):
            y = rd.randint(0, 1048576)
            TempData = np.append(TempData, y)
        
        return TempData
        
