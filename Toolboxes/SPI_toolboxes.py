import numpy as np
import pyaudio
import os, wave, csv

class IIC_SPI_Communications:
    def __init__(self, format, InDevice, Rate = 48000, Usedchannels = 1, chunks = 512, BufferFormat = np.int16):
        self.Audio = pyaudio.PyAudio()
        self.pyaudioFormat = format
        self.sampleRate = Rate
        self.Operatingchannels = Usedchannels
        self.InDeviceIndex = InDevice
        self.CHUNK = chunks
        self.BuffFormat = BufferFormat
    
    def GetDevices(self):
        for ii in range(0, self.Audio.get_device_count()):
            print(self.Audio.get_device_info_by_index(ii))
        
    def AudioStart(self):
        self.stream = self.Audio.open(format = self.pyaudioFormat, rate = self.sampleRate, channels= self.Operatingchannels, input_device_index= self.InDeviceIndex, input= True, frames_per_buffer= self.CHUNK)
        
        self.stream.stop_stream()
    
    def pyserial_End(self):
        self.stream.close()
        self.Audio.terminate()

    def DataCollection(self, LengthOfAudio):
        self.stream.start_stream()
        self.stream.read(self.CHUNK, exception_on_overflow = False)

        # Data Variables
        self.data = [] 
        self.data_frames = []

        print('--- Audio Transfer Starting ---')

        for frame in range(0, int((self.sampleRate * LengthOfAudio) / self.CHUNK)):
            stream_data = self.stream.read(self.CHUNK, exception_on_overflow = False)
            self.data_frames.append(stream_data)

            self.data.append(np.frombuffer(stream_data, dtype= self.BuffFormat))
        
        self.stream.stop_stream()

        print('--- Audio Transfer Completed ---')

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


# Testing

AudioDevice = IIC_SPI_Communications(pyaudio.paInt24, 1)

#AudioDevice.GetDevices()

AudioDevice.AudioStart()

AudioDevice.DataCollection(10)

AudioDevice.DataSaver('test')
