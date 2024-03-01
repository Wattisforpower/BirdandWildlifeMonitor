# This program will decifer the results from the receiver and then add it to the system
import serial


class Functions_Toolbox:
    def __init__(self) -> None:
        pass

    def Create_Connection(self, port = '/dev/ttyUSB0', baudrate = 115200) -> None:
        self.Terminal = serial.Serial()
        self.Terminal.baudrate = baudrate
        self.Terminal.port = port

    def Start(self) -> None:
        try:
            self.Terminal.open()
        except:
            print("ERROR; Could not open terminal, closing and trying again")
            self.Terminal.close()
            self.Terminal.open()


    def Read(self) -> str:
        if (self.Terminal.is_open):
            self.read = self.Terminal.readline()
        else:
            print("ERROR; Terminal not opened!")
        
        return self.read
    
    def Write(self, input = 'Hello World!') -> None:
        try:
            self.Terminal.write(input)
        except:
            print("ERROR; Could not send data")
    
    def DecodeData(self) -> str:
        # Data will come in the form of:
        # <Indicator>:<data>:<endline>
        # Indicatiors Include
        # RES -> Producing a result
            # This will be the data for the results of the classification
        # ERR -> Producing an Error
            # This will produce the error for example when a system goes down
        # SYS -> Generic System data communication
            # This includes data about the battery levels*, system operations
        
        # Read the incoming data, if any
        Data = self.Read()

        datasplit = Data.split(":")

        if (datasplit[0] == "RES"):
            return datasplit[1]
        
        elif (datasplit[0] == "ERR"):
            print("ERROR: " + str(datasplit[1]))
            return datasplit[1]
        
        elif (datasplit[0] == "SYS"):
            print("System Data: " + str(datasplit[1]))
            return datasplit[1]
        
