
class Buffer:
    def __init__(self, buffersize, timeframe) -> None:
        self.BuffOne[(buffersize * timeframe)]
        self.BuffTwo[(buffersize * timeframe)]
        self.LoadingBuffer[(buffersize * timeframe)]

    def BufferLoad(self, data):
        self.BuffTwo = self.BuffOne

        self.BuffOne = data


    def __BufferOffload(self):
        self.LoadingBuffer = self.BuffTwo

    def ConverttoSpectograph(self):
        X_STFT = librosa.stft(self.LoadingBuffer)
        X_db = librosa.amplitufe_to_db(abs(X_STFT))

        
