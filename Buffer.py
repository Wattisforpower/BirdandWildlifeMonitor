
class Buffer:
    def __init__(self, buffersize, timeframe) -> None:
        self.BuffOne[(buffersize * timeframe)]
        self.BuffTwo[(buffersize * timeframe)]

    def BufferLoad(self, data):
        self.BuffTwo = self.BuffOne

        self.BuffOne = data


    def BufferOffload(self):
        pass

    def ConverttoSpectograph(self):
        pass
