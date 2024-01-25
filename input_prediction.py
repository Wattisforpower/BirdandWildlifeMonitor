# need to change to following to the appropriate libraries for raspberry pi
import tensorflow as tf


# Convert the audio file to a temporary Spectograph, when pulse is high
def Convert(item, savename):
    x, sr = librosa.load(item, sr = 48000)

    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))

    plt.figure(figsize=(120, 10))
    librosa.display.specshow(Xdb, sr = sr, x_axis='time', y_axis='hz')
    plt.set_cmap('gray_r')
    plt.axis('off')
    plt.savefig(savename, bbox_inches= 'tight', pad_inches = 0)



if (INPUT_INDICATOR == 1):
    Convert()