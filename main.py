from Toolboxes import Predictor_Toolbox as PT
from Toolboxes import Buffer_Toolbox as BT
from Toolboxes import Data_Transmission_Toolbox as DTT
from Toolboxes import Neural_Network_Toolbox as NTT
#from Toolboxes import WandB_Toolbox as WB
#from spidev import SpiDev
#import wiringpi
#import time

#wiringpi.wiringPiSetupSys()

system = PT.RunPredictor()
Data_Transmit = DTT.TransmissionSystem()
Network = NTT.Neural_Networks()


#spi = SpiDev()
Buffers = BT.Buffer(520, 20, 20000)

# Arbitary Pin Value, Change it later!
Pin = 6

def main():
    #WB.run()
    

    Result, _ = system.runClassifier('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow1_split_2.wav', False)
    Data_Transmit.website(Result)
    #system.GenerateConfusion()
    
    #print(Result)
    
    # Send Classification Result to the website
    #Data_Transmit.website(Result)
    
    '''
    wiringpi.pinMode(Pin, 0) # Pin 6 Input Pin
    while True:
        if wiringpi.digitalRead(Pin) == 1:
            # Open SPI Port and Read the Data into the Buffers
            spi.open(5, 1)
            spi.max_speed_hz = 5000
            Buffers.BufferLoad(spi.read_all())
            Buffers.BufferLoad(spi.read_all())
            spi.close()
            
            # Run the Classifier
            Result, _ = system.runClassifier('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Audio/Barnswallow/SplitData/BarnSwallow6_split_1.wav', False)
            
            # Send Classification Result to the website
            Data_Transmit.website(Result)
            
                
            
        else:
            time.sleep(0.1)
            
    '''


if __name__ == "__main__":
    main()
