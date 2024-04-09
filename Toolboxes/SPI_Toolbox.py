import numpy as np
import pyaudio
import os, wave
import matplotlib.pyplot as plt

class IIC_SPI_Communications:
    def __init__(self, format, InDevice, Rate = 48000, Usedchannels = 1, chunks = 512, BufferFormat = np.int16):
        self.Audio = pyaudio.PyAudio()

        self.sampleRate = Rate
        print(self.sampleRate)
        self.Operatingchannels = Usedchannels
        self.InDeviceIndex = InDevice
        self.CHUNK = chunks
        self.BuffFormat = BufferFormat

        if (format == 24):
            self.pyaudioFormat = pyaudio.paInt24
        elif (format == 16):
            self.pyaudioFormat = pyaudio.paInt16
        elif (format == 32):
            self.pyaudioFormat = pyaudio.paInt32
            
    
    def GetDevices(self):
        for ii in range(0, self.Audio.get_device_count()):
            print(self.Audio.get_device_info_by_index(ii))
        
    def AudioStart(self):
        self.stream = self.Audio.open(format = self.pyaudioFormat, rate = self.sampleRate, channels= self.Operatingchannels, input_device_index= self.InDeviceIndex, input= True)
        
        self.stream.stop_stream()
    
    def pyAudio_End(self):
        self.stream.close()
        self.Audio.terminate()
    
    def pyAudio_Start(self):
        self.stream.start_stream()
    
    def pyAudio_Stop(self):
        self.stream.stop_stream()

    def DataCollection(self, LengthOfAudio):
        self.stream.start_stream()
        self.stream.read(self.CHUNK, exception_on_overflow = False)

        # Data Variables
        self.data = [] 
        self.data_frames = []

        print('--- Audio Transfer Starting ---')

        for frame in range(0, int((self.sampleRate * LengthOfAudio) / self.CHUNK)):
            self.stream_data = self.stream.read(self.CHUNK, exception_on_overflow = False)
            self.data_frames.append(self.stream_data)

            self.data.append(np.frombuffer(self.stream_data, dtype= self.BuffFormat))
        
        self.stream.stop_stream()

        print('--- Audio Transfer Completed ---')
    
    def returnBuffer(self):
        return self.data_frames

    def DataSaver(self, NameofFile):
        data_folder = 'Toolboxes/Data/'

        if os.path.isdir(data_folder) == False:
            os.mkdir(data_folder)
        
        wf = wave.open(data_folder+NameofFile+'.wav', 'wb')
        wf.setnchannels(self.Operatingchannels)
        wf.setsampwidth(self.Audio.get_sample_size(self.pyaudioFormat))
        wf.setframerate(self.sampleRate)
        wf.writeframes(b''.join(self.data_frames))
        wf.close()
        
    def SpectoGram(self):
        figure = plt.figure()
        s = figure.add_subplot(111)
        amplitude = np.frombuffer(self.stream_data, dtype=self.BuffFormat)
        s.plot(amplitude)
        
        plt.show()

