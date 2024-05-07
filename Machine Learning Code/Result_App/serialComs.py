import serial

class SerialComs:
    def __init__(self, ComPort, BaudRate) -> None:
        self.ser = serial.Serial(ComPort, BaudRate, timeout=1)

    def Open(self) -> None:
        try:
            self.ser.open()
        except:
            self.ser.close()
            self.ser.open()
    
    def Close(self) -> None:
        try:
            self.ser.close()
        except:
            print("Serial Already Closed")
        
    def ReadLine(self) -> str:
        return self.ser.readline()
    
    def WriteLine(self, writeable) -> None:
        self.ser.write(b'{}}'.format(writeable))
    