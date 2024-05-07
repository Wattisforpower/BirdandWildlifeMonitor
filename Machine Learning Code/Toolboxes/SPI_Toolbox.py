import numpy as np
import pyaudio
import os, wave
import matplotlib.pyplot as plt
import spidev
import time
import struct

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
        self.SPI = spidev.SpiDev(0, 0)
        self.AudioBuffer = np.empty(0, dtype = np.int32)

        self.instream2 = np.ones((2, 1), dtype = np.uint8)
        self.output_buffer = [None] * 480000
        self.deserialise_buffer = [0] * 3
        self.deserialise_buffer_head = 0

        self.SampleRate = 12000000

    def deserialize(self, byte_):
        if (byte_ == 10):
            self.deserialize_buffer_head = 0 # reset head pointer
            output = (self.deserialize_Buffer[0] << 24) | (self.deserialize_Buffer[1] << 16) | (self.deserialize_Buffer[2] << 8) | (self.deserialize_Buffer[3])
            return output
        else:
            self.deserialize_buffer[self.deserialize_buffer_head] = byte_
            self.deserialize_buffer_head += 1
            return 0
    
    def deserialise_2(self, input_byte):
        if input_byte == 10:
            self.deserialise_buffer_head = 0
            output = (self.deserialise_buffer[0] << 8) | (self.deserialise_buffer[1])
            return output
        else:
            self.deserialise_buffer[self.deserialise_buffer_head] = input_byte
            self.deserialise_buffer_head += 1
            if self.deserialise_buffer_head >= 3:
                self.deserialise_buffer_head = 0
    
    def read_bytes_2(self):
        instream2 = self.SPI.xfer2([0x00, 0x00, 0x00])

        if (not((instream2[0] == 0x00) and (instream2[1] == 0x00) and (instream2[2]))):
            for m in range(3):
                deserialised_data = self.deserialise_2(instream2[m])

                if deserialised_data != None:
                    if (deserialised_data >= 2**15):
                        deserialised_data = deserialised_data - 2**16
                    return deserialised_data
    
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
        prev_Val = 0
        instream = np.ones((4, 1), dtype = np.uint8)
        instream = self.SPI.xfer2([0x00, 0x00, 0x00, 0x00, 0x00])
        instream = self.SPI.readbytes(5)
        #print(instream)
        output = np.ones((1,1), dtype = np.int32)        
        output = (instream[0] << 24) | (instream[1] << 16) | (instream[2] << 8) | (instream[3])

        if (output >= 2**31):
            output = output - 2**32

        if prev_Val != int(output):
            if (output != 0):
                print(output)
                self.AudioBuffer = np.append(self.AudioBuffer, int(output))
                prev_Val = int(output)
                #print(self.AudioBuffer)
        

                return output
    
        return 0

    def Convert_to_wav(self, filename):

        data_folder = 'Toolboxes/Data/'

        if os.path.isdir(data_folder) == False:
            os.mkdir(data_folder)

        
        File = data_folder + filename

        Data = self.AudioBuffer

        # Write to file
        sample_rate = 48000
        duration = 10
        wf = wave.open(data_folder + filename, 'w') 
        wf.setnchannels(1)
        wf.setsampwidth(4)
        wf.setframerate(sample_rate)
        #for i in range(sample_rate * duration):
        for i in range(len(self.AudioBuffer)):
            value = int(self.AudioBuffer[i]) *1000000
            if(value > 2147483647):
                value = 2147483647
            elif(value < -2147483647):
                value = -2147483647
            #print(value)
            data = struct.pack('<i',value)
            wf.writeframesraw(data)
        #wf.writeframes(b''.join(Data))
        wf.close()

        # Clear AudioBuffer
        self.AudioBuffer = np.empty(0)
    
    def convert_to_wav_2(self, filename):
        data_folder = 'Toolboxes/Data/'

        if os.path.isdir(data_folder) == False:
            os.mkdir(data_folder)
        
        File = data_folder + filename

        # Write to file
        sample_rate = 48000
        duration = 10

        wf = wave.open(File, 'w')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        for i in range(sample_rate * duration):
            value = int(self.output_buffer[i])

            if (value > (2**15)):
                value = (2**15)
            elif (value < -(2**15)):
                value = -(2**15)
            
            data = struct.pack('<h', value)
            wf.writeframesraw(data)
        
        wf.close()
    
    def GenerateGraph(self):
               
        fig = plt.figure(1)
        plt.plot(self.AudioBuffer)
        plt.show()

    def RecordAudio(self, lengthofAudio = 10):
        Max_Samples = 48000 * lengthofAudio
        i = 0
        while (len(self.AudioBuffer) < Max_Samples):
            self.readbytes_and_deserialize()

    def RecordAudio_2(self):
        idx = 0

        while (idx < 480000):
            self.output_buffer[idx] = self.read_bytes_2()
            
            if (self.output_buffer[idx] != None):
                idx += 1
