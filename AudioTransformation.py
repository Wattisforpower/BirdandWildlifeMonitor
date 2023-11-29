import matplotlib.pyplot as plt

#for loading and visualizing audio files
import librosa
import librosa.display


audioPath = "Audio\BarnSwallow.wav"

x, sr = librosa.load(audioPath, sr = 48000)

plt.figure(figsize=(14, 5))
librosa.display.waveshow(x, sr = sr)
plt.show()

X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X))

plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr = sr, x_axis='time', y_axis='hz')
#plt.colorbar()
plt.set_cmap('gray_r')
plt.axis('off')
plt.savefig('output.png', bbox_inches= 'tight', pad_inches = 0)
plt.show()
