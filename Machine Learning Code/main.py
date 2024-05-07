from Toolboxes import Predictor_Toolbox as PT
from Toolboxes import Buffer_Toolbox as BT
from Toolboxes import Data_Transmission_Toolbox as DTT
#from Toolboxes import Neural_Network_Toolbox as NTT
from Toolboxes import File_Management_Toolbox as FMT
from Toolboxes import SPI_Toolbox
import RPi.GPIO as GPIO
import time

# --- Setup GPIO ---
GPIO.setmode(GPIO.BCM)

pin = 25

GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# --- Setup Classes --- 
system = PT.RunPredictor()
Buffers = BT.Buffer(520, 10, 48000)
Data_Transmit = DTT.TransmissionSystem()
#Network = NTT.Neural_Networks()
#AudioStream = SPI_Toolbox.IIC_SPI_Communications(24, 3, 48000)
SPI = SPI_Toolbox.SPI_Communications()
Files = FMT.FileManagement()


FileI = 0
def main():
    
    #AudioStream.GetDevices() # Used to get the correct audio input for pyAudio
    #AudioStream.AudioStart()
    SPI.Init_SPI()
    #Result, score = system.runClassifier('/home/pi/Downloads/BarnSwallow6_SNR_-10-[AudioTrimmer.com].wav', False)
    
    
    while True:
        #if GPIO.input(pin): # check if the pin is high
            Start = time.time()
            #SPI.RecordAudio(1)
            SPI.RecordAudio_2()
            Stop = time.time()

            delta = Stop - Start
            print(delta)

            #SPI.GenerateGraph()
            SPI.convert_to_wav_2('tempWav.wav')
            #SPI.Convert_to_wav('tempWav.wav') # save the collected data as a wav file

            
            # try, except clause to protect the system from crashing
            try:
                # Try and classify the wav file and return the result and score of the confidence of the result
                Result, score = system.runClassifier('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Toolboxes/Data/tempWav.wav', False)
                #Result, score = system.runClassifier('/home/pi/Downloads/BarnSwallow6_SNR_-10.wav', False)
                
                # if, elif, else clause to filter the score and if it is confident or not.
                if (score > 19):
                    Data_Transmit.SendSerial(Result)
                elif (score < 19):
                    # Print Unknown Species on the GUI
                    Data_Transmit.SendSerial('Unknown Species')
                    # Generate a Name
                    Name = 'Unknown_' + str(FileI) + '.wav'
                    # Save the WAV file to another location
                    Files.CopyAndRenameFile('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Toolboxes/Data/tempWav.wav', '/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Unknown_Species_Folder', Name)
                    # increase FileI by 1
                    FileI += 1
                else:
                    print("No species detected")
            
            except:
                # return 'No Data or Error Occured' if it could not classify correctly, which could be due to many reasons
                print("No Data or Error Occurred")

            
            
            time.sleep(10) # remove when finished testing
        #else:
            #time.sleep(0.1)
    

if __name__ == "__main__":
    main()