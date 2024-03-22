import numpy as np
import pyaudio

class IIC_SPI_Communications:
    def __init__(self):
        self.Audio = pyaudio.PyAudio()
    
    def GetDevices(self):
        for ii in range(0, self.Audio.get_device_count()):
            print(self.Audio.get_device_info_by_index(ii))
        
    def AudioStart(self):
        pass

# Testing

AudioDevice = IIC_SPI_Communications()

AudioDevice.GetDevices()
        
