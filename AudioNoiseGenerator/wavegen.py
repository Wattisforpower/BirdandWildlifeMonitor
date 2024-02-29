# https://www.codeproject.com/Articles/5323200/On-How-to-Mix-Two-Signals-by-using-Spectral-Foreca

from scipy.io import wavfile
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import librosa
import random
<<<<<<< Updated upstream
=======
import sounddevice as sd
>>>>>>> Stashed changes

SampleRate = 20000
Length = 10
amplitude = 0.001

audiopath = 'Audio/Barnswallow/SplitData/BarnSwallow2_split_1.wav'

# Original Signal
LoadingBuffer, sr = librosa.load(audiopath, sr = SampleRate)

# Noise Generator
noise = np.empty(0)

def GenNoise():
    global LoadingBuffer, noise

    for i in range(len(LoadingBuffer)):
        temp = random.uniform(-1, 1)

        noise = np.append(noise, temp)
GenNoise()

<<<<<<< Updated upstream
    d = random.randint(0, MaxAB)
=======
OutNoise = 0.1*noise
>>>>>>> Stashed changes

Result = LoadingBuffer + OutNoise

print("playingAudio")

sd.play(Result, 20000)

plt.figure()
plt.subplot(1, 3, 1)
plt.plot(noise)
plt.plot(OutNoise)
plt.title("Noise")
plt.subplot(1, 3, 2)
plt.plot(LoadingBuffer)
plt.title("Unprocessed Signal")
plt.subplot(1, 3, 3)
plt.plot(Result)
plt.title("Combined Signal")
plt.show()

