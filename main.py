from Toolboxes import Predictor_Toolbox as PT
from Toolboxes import Buffer_Toolbox as BT
from Toolboxes import Data_Transmission_Toolbox as DTT
#from Toolboxes import Neural_Network_Toolbox as NTT
from Toolboxes import SPI_Toolbox
import RPi.GPIO as GPIO
import time

# --- Setup GPIO ---
GPIO.setmode(GPIO.BCM)

pin = 6

GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# --- Setup Classes --- 
system = PT.RunPredictor()
Buffers = BT.Buffer(520, 10, 48000)
Data_Transmit = DTT.TransmissionSystem()
#Network = NTT.Neural_Networks()
AudioStream = SPI_Toolbox.IIC_SPI_Communications(24, 3, 20000)


def main():
    
    #AudioStream.GetDevices() # Used to get the correct audio input for pyAudio
    AudioStream.AudioStart()
    
    while True:
        if GPIO.input(pin):
            AudioStream.DataCollection(10)
            AudioStream.DataSaver('Temp')
            try:
                Result, score = system.runClassifier('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Toolboxes/Data/Temp.wav', False)
            except:
                print("No Data!")

            if (score >  20):
                Data_Transmit.SendSerial(Result)
            elif (score < 15):
                Data_Transmit.SendSerial('Unknown Species')
            else:
                Data_Transmit.SendSerial('No Species Detected')
            
            time.sleep(10) # Remove when not testing!
        
        else:
            print("No Data!")
    



if __name__ == "__main__":
    main()
