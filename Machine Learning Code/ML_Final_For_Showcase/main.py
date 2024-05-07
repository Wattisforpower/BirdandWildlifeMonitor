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
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow1_split_2.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow2_split_1.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow2_split_2.wav'
        elif (str(Input[1]) == str("05")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow2_split_3.wav'
        elif (str(Input[1]) == str("06")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow3_split_1.wav'
        elif (str(Input[1]) == str("07")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow4_split_1.wav'
        elif (str(Input[1]) == str("08")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow4_split_2.wav'
        elif (str(Input[1]) == str("09")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow5_split_1.wav'
        elif (str(Input[1]) == str("10")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow6_split_1.wav'
        elif (str(Input[1]) == str("11")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow7_split_1.wav'
    elif (str(Input[0]) == str("01")):
        # BlackheadedGull
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull1_split_2.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull1_split_3.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull2_split_1.wav'
        elif (str(Input[1]) == str("05")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull2_split_2.wav'
        elif (str(Input[1]) == str("06")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull3_split_1.wav'
        elif (str(Input[1]) == str("07")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull4_split_1.wav'
        elif (str(Input[1]) == str("08")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull4_split_2.wav'
        elif (str(Input[1]) == str("09")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/BlackheadedGull/SplitData/BlackheadedGull5_split_1.wav' 
    elif (str(Input[0]) == str("02")):
        # CommonGuillemot
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonGuillemot/SplitData/CommonGuillemot1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonGuillemot/SplitData/CommonGuillemot1_split_2.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonGuillemot/SplitData/CommonGuillemot2_split_1.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonGuillemot/SplitData/CommonGuillemot2_split_2.wav'
        elif (str(Input[1]) == str("05")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonGuillemot/SplitData/CommonGuillemot3_split_1.wav'
        elif (str(Input[1]) == str("06")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonGuillemot/SplitData/CommonGuillemot3_split_2.wav'
    elif (str(Input[0]) == str("03")):
        # Common Starling
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling1_split_2.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling1_split_3.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling2_split_1.wav'
        elif (str(Input[1]) == str("05")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling2_split_2.wav'
        elif (str(Input[1]) == str("06")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling2_split_3.wav'
        elif (str(Input[1]) == str("07")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling2_split_4.wav'
        elif (str(Input[1]) == str("08")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling3_split_1.wav'
        elif (str(Input[1]) == str("09")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling3_split_2.wav'
        elif (str(Input[1]) == str("10")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling3_split_3.wav'
        elif (str(Input[1]) == str("11")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling3_split_4.wav'
        elif (str(Input[1]) == str("12")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling4_split_1.wav'
        elif (str(Input[1]) == str("13")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling4_split_2.wav'
        elif (str(Input[1]) == str("14")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling5_split_1.wav'
        elif (str(Input[1]) == str("15")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling6_split_1.wav'
        elif (str(Input[1]) == str("16")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/CommonStarling/SplitData/CommonStarling7_split_1.wav'
    elif (str(Input[0]) == str("04")):
        # Dunlin
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin2_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin3_split_1.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin4_split_2.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin4_split_2.wav'
        elif (str(Input[1]) == str("05")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin5_split_1.wav'
        elif (str(Input[1]) == str("06")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin5_split_2.wav'
        elif (str(Input[1]) == str("07")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin6_split_1.wav'
        elif (str(Input[1]) == str("08")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin6_split_2.wav'
        elif (str(Input[1]) == str("09")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin7_split_1.wav'
        elif (str(Input[1]) == str("10")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin7_split_2.wav'
        elif (str(Input[1]) == str("11")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin8_split_1.wav'
        elif (str(Input[1]) == str("12")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Dunlin/SplitData/Dunlin8_split_2.wav'
    elif (str(Input[0]) == str("05")):
        # Eurasian OysterCatcher
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/EurasianOysterCatcher/SplitData/Dunlin1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/EurasianOysterCatcher/SplitData/Dunlin2_split_1.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/EurasianOysterCatcher/SplitData/Dunlin2_split_2.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/EurasianOysterCatcher/SplitData/Dunlin2_split_3.wav'
    elif (str(Input[0]) == str("06")):
        # European Golden Plover
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/EuropeanGoldenPlover/SplitData/Dunlin1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/EuropeanGoldenPlover/SplitData/Dunlin2_split_1.wav'
    elif (str(Input[0]) == str("07")):
        # Herring Gull
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/HerringGull/SplitData/HerringGullMB1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/HerringGull/SplitData/HerringGullMB1_split_2.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/HerringGull/SplitData/HerringGullMB2_split_1.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/HerringGull/SplitData/HerringGullMB3_split_1.wav'
        elif (str(Input[1]) == str("05")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/HerringGull/SplitData/HerringGullMB4_split_1.wav'
        elif (str(Input[1]) == str("06")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/HerringGull/SplitData/HerringGullMB5_split_1.wav'
        elif (str(Input[1]) == str("07")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/HerringGull/SplitData/HerringGullMB6_split_1.wav'
        elif (str(Input[1]) == str("08")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/HerringGull/SplitData/HerringGullMB6_split_2.wav'
    elif (str(Input[0]) == str("08")):
        # Northern Lapwing
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing1_split_2.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing1_split_3.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing2_split_1.wav'
        elif (str(Input[1]) == str("05")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing2_split_2.wav'
        elif (str(Input[1]) == str("06")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing2_split_3.wav'
        elif (str(Input[1]) == str("07")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing3_split_1.wav'
        elif (str(Input[1]) == str("08")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing4_split_1.wav'
        elif (str(Input[1]) == str("09")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing5_split_1.wav'
        elif (str(Input[1]) == str("10")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing5_split_2.wav'
        elif (str(Input[1]) == str("11")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing6_split_1.wav'
        elif (str(Input[1]) == str("12")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing6_split_2.wav'
        elif (str(Input[1]) == str("13")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing7_split_1.wav'
        elif (str(Input[1]) == str("14")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/NorthernLapwing/SplitData/NorthernLapwing7_split_2.wav'
    elif (str(Input[0]) == str("09")):
        #Redwing
        if (str(Input[1]) == str("01")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Redwing/SplitData/Redwing1_split_1.wav'
        elif (str(Input[1]) == str("02")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Redwing/SplitData/Redwing1_split_2.wav'
        elif (str(Input[1]) == str("03")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Redwing/SplitData/Redwing1_split_3.wav'
        elif (str(Input[1]) == str("04")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Redwing/SplitData/Redwing2_split_1.wav'
        elif (str(Input[1]) == str("05")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Redwing/SplitData/Redwing2_split_2.wav'
        elif (str(Input[1]) == str("06")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Redwing/SplitData/Redwing2_split_3.wav'
        elif (str(Input[1]) == str("07")):
            Track = '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Redwing/SplitData/Redwing3_split_1.wav'
    
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
        #val = CheckStream()
        val = b'00/01/'
        
        result, score = Instream_Classify(val)
        
        print(result)
                
        if (score > 60):
            Send(result)
        
    
main()