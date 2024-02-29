import serial

class TransmissionSystem:
    def __init__(self):
        self.SerialPort = serial.Serial('/dev/ttyUSB0')
        self.SerialPort.baudrate = 115200
        

    def website(self, result):
        with open('/home/pi/Documents/GitHub/BirdandWildlifeMonitor/Toolboxes/Website/data.csv', 'a') as datafile:
            datafile.write(str(result) + "\n")
            
            datafile.close()
    
    def SendSerial(self, result):
        try:
            self.SerialPort.open()
        except:
            self.SerialPort.close()
            self.SerialPort.open()
            
        #self.SerialPort.write(result.encode('utf-8'))
        
        self.SerialPort.write(result.encode('utf-8'))
        
        self.SerialPort.close()
        
        print('sent')
        

