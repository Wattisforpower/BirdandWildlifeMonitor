# https://www.codeproject.com/Articles/5323200/On-How-to-Mix-Two-Signals-by-using-Spectral-Foreca

from scipy.io import wavfile
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import librosa
import random

SR = 20000
Length = 10
amplitude = 0.001

audiopath = 'Audio/Barnswallow/SplitData/BarnSwallow2_split_1.wav'

# Noise Generator
noise = stats.truncnorm(-1, 1, scale=min(2**16, 2**amplitude)).rvs(SR * Length)
#wavfile.write('noise.wav', SR, noise.astype(np.int16))

# Original Signal
LoadingBuffer, sr = librosa.load(audiopath, sr = SR)

Result = np.empty(0)

def SpectralForecast():
    global LoadingBuffer, noise, Result

    MaxA = 1 #int(np.max(LoadingBuffer))
    MaxB = int(np.max(noise))

    MaxAB = np.max([MaxA, MaxB])

    d = random.randint(0, MaxAB)

    for i in range(0, len(LoadingBuffer)):
        temp = ((d / MaxA) * LoadingBuffer[i]) + (((MaxAB - d) / MaxB) * noise[i])

        Result = np.append(Result, temp)

SpectralForecast()

plt.figure()
plt.subplot(1, 3, 1)
plt.plot(noise)
plt.title("Noise")
plt.subplot(1, 3, 2)
plt.plot(LoadingBuffer)
plt.title("Unprocessed Signal")
plt.subplot(1, 3, 3)
plt.plot(Result)
plt.title("Combined Signal")
plt.show()


