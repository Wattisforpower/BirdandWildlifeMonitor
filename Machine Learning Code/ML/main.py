import spidev
import numpy as np
import time
import os, wave
import struct
import tensorflow as tf
import librosa
import RPi.GPIO as GPIO
import serial

###################################################
SPI = spidev.SpiDev(0, 0)
i = 0;
SampleRate = 12000000
SPI.mode = 0b01
SPI.max_speed_hz = SampleRate
SPI.no_cs = True
###################################################
SerialPort = serial.Serial('/dev/ttyUSB0')
SerialPort.baudrate = 115200

def Send(result):
    try:
        SerialPort.open()
    except:
        SerialPort.close()
        SerialPort.open()
    
    SerialPort.write(result.encode('utf-8'))
    
    
    print('sent')

###################################################
# TENSORFLOW
model = 'SavedModel/variables'
loadOptions = tf.saved_model.LoadOptions(experimental_io_device = "/job:localhost")

def Convert(source):
    LoadingBuffer, sr = librosa.load(source, sr = 20000)
    
    X_stft = librosa.stft(LoadingBuffer)
    return librosa.amplitude_to_db(np.abs(X_stft)).flatten()

def Classify(source):
    interpreter = tf.saved_model.load('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/saved_model_20khz')
    
    Classify_Lite = interpreter.signatures["serving_default"]
    
    Input = tf.convert_to_tensor(Convert(source))
    
    predictions = Classify_Lite(normalization_input=Input[:-1])['dense_14']
    # Class names for the conversion back from numeric classes to string classes
    class_names = ['BarnSwallow',
                'BlackheadedGull',
                'CommonGuillemot',
                'CommonStarling',
                'Dunlin',
                'EurasianOysterCatcher',
                'EuropeanGoldenPlover',
                'HerringGull',
                'NorthernLapwing',
                'Redwing']

    # Print the result
    print(
        "This Source most likely to be a {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(predictions) - 1], 100 * np.max(predictions))
    )
    
    return class_names[np.argmax(predictions) - 1], np.argmax(predictions)

def Instream_Classify(Val):
    # Val = ##/##/-
    Val = Val.decode('utf-8')
    # Split the Value
    Input = Val.split('/')
    Track = ""
    
    
    
    if (str(Input[0]) == str("00")):
        # Barnswallow
        if (str(Input[1]) == str("01")):
            #Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow1_split_1.wav'
            Track = '/home/pi/Downloads/HerringGullMB1_split_1_SNR_-5.wav'
    elif (Pre == 1):
        # BlackheadedGull
        pass
    elif (Pre == 2):
        # CommonGuillemot
        pass
    elif (Pre == 3):
        # Common Starling
        pass
    elif (Pre == 4):
        # Dunlin
        pass
    elif (Pre == 5):
        # Eurasian OysterCatcher
        pass
    elif (Pre == 6):
        # European Golden Plover
        pass
    elif (Pre == 7):
        # Herring Gull
        pass
    elif (Pre == 8):
        # Northern Lapwing
        pass
    elif (Pre == 9):
        #Redwing
        pass
    
    Result, score = Classify(Track)
    
    return Result, score

def CheckStream():
    try:
        SerialPort.open()
    except:
        SerialPort.close()
        SerialPort.open()
    print("R")
    Data = SerialPort.readline()
    
    print(Data)

    return Data

def main():
    while True:
        val = CheckStream()
        
        result, score = Instream_Classify(val)
        
        print(result)
                
        if (score > 60):
            Send(result)
        
    
main()