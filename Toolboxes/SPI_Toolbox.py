import numpy as np
import pyaudio
import os, wave
import matplotlib.pyplot as plt
import scipy
import spidev
import time

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

class SPI_Communications:
    def __init__(self):
        self.deserialize_Buffer = [0,0,0,0]
        self.deserialize_buffer_head = 0
        self.SPI = spidev.SpiDev(0, 0)
        self.AudioBuffer = np.empty(0, dtype = np.int32)
        self.SampleRate = 12000000

    def deserialize(self, byte_):
        if (byte_ == 10):
            self.deserialize_buffer_head = 0 # reset head pointer
            output = (self.deserialize_Buffer[0] << 24) | (self.deserialize_Buffer[1] << 16) | (self.deserialize_Buffer[2] << 8) | (self.deserialize_Buffer[3])
            return output
        else:
            self.deserialize_Buffer[self.deserialize_buffer_head] = byte_
            self.deserialize_buffer_head += 1
            return 0
    
    def Init_SPI(self):
        self.SPI.mode = 0b01
        self.SPI.max_speed_hz = self.SampleRate
        self.SPI.no_cs = True
        #self.SPI.lsbfirst = True
        #self.SPI.no_cs = True

    def ReverseBits(self, byte):
        byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
        byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
        byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)

        return byte

    def readbytes_and_deserialize(self):
        #self.SPI.writebytes([0x80, 0x00])
        #time.sleep(0.1)
        instream = np.ones((4, 1), dtype = np.uint8)
        instream = self.SPI.xfer2([0x00, 0x00, 0x00, 0x00, 0x00])
        #instream = self.SPI.readbytes(5)
        #print(instream)
        output = np.ones((1,1), dtype = np.int32)        
        output = (instream[0] << 24) | (instream[1] << 16) | (instream[2] << 8) | (instream[3])

        if (output >= 2**31):
            output = output - 2**32

        if (output != 0):
            #print(instream)
            print(output)
        
            self.AudioBuffer = np.append(self.AudioBuffer, output)

        return output

    def Convert_to_wav(self, filename):

        data_folder = 'Toolboxes/Data/'

        if os.path.isdir(data_folder) == False:
            os.mkdir(data_folder)

        
        File = data_folder + filename

        # Write to file
        wf = wave.open(data_folder + filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(4800)
        wf.writeframes(b''.join(self.AudioBuffer))
        wf.close()

        # Clear AudioBuffer
        self.AudioBuffer = np.empty(0)
    
    def GenerateGraph(self):
               
        fig = plt.figure(1)
        plt.plot(self.AudioBuffer)
        plt.show()

    def RecordAudio(self, lengthofAudio = 10):
        timeNow = time.time()

        while True:
            self.readbytes_and_deserialize()

            timeNew = time.time()

            timeDelta = timeNew - timeNow # work out the change in time

            if timeDelta >= lengthofAudio:
                break



# Testing that code works
SPI = SPI_Communications()

SPI.Init_SPI()



SPI.RecordAudio(10)

SPI.GenerateGraph()
SPI.Convert_to_wav('TempSingle')
