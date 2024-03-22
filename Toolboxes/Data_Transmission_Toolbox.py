import serial
import time

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
    
    def LoRa_Setup(self):
        self.LoRa = serial.Serial('/dev/ttyUSB1')
        self.LoRa.baudrate = 9600
        
        # ensure that the serial port is open for the tranmission of data
        try:
            self.LoRa.open()
        except:
            self.LoRa.close()
            self.LoRa.open()
        
        self.LoRa.write("AT+MODE=OTAA".encode('utf-8'))
        
        time.sleep(1)
        
        self.LoRa.write("AT+JOIN".encode('utf-8'))
        
        time.sleep(10)
        
        self.LoRa.write("AT+MODE=TEST".encode('utf-8'))
        
        time.sleep(1)
        
        # send test message
        
        self.LoRa.write("AT+TEST=TXLRSTR,\"Hello World!\"".encode('utf-8'))
        
        time.sleep(1)
    
    def LoRa_Send(self, message):
        EncodedMsg = "AT+TEST=TXLRSTR,\"" + message + "\""
        self.LoRa.write(EncodedMsg.encode('utf-8'))
        time.sleep(5)
        print('Sent over LoRa')
    
# Testing
#LoRaTest = TransmissionSystem()

#LoRaTest.LoRa_Setup()

#LoRaTest.LoRa_Send("Hi")
        
        
        
        
        

