import matplotlib.pyplot as plt
import pathlib

import os

#for loading and visualizing audio files
import librosa
import librosa.display
import soundfile as sf

def Convert(item, savename):
    x, sr = librosa.load(item, sr = 48000)

    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))

    plt.figure(figsize=(120, 10))
    librosa.display.specshow(Xdb, sr = sr, x_axis='time', y_axis='hz')
    plt.set_cmap('gray_r')
    plt.axis('off')
    plt.savefig(savename, bbox_inches= 'tight', pad_inches = 0)

def BatchConvert(path, DefineBatchName):
    Path = pathlib.Path(path).with_suffix('')

    ListOfValues = list(Path.glob('*.wav'))

    i = 1
    for item in ListOfValues:

        GenName = DefineBatchName + '-' + str(i) + '_MB'
        Convert(item, GenName)

        i += 1

def Split_Audio(Max_Length, file, savename):
    try:
        # Calculate Maximum split amount
        audio, sr = librosa.load(file, sr = 48000)

        Total_Samples = len(audio)
        buffer = Max_Length * sr
        Samples_Wrote = 0
        counter = 1

        while Samples_Wrote < Total_Samples:
            # generate buffer
            if buffer > (Total_Samples - Samples_Wrote) : buffer = Total_Samples - Samples_Wrote

            # create audio block
            block = audio[Samples_Wrote : (Samples_Wrote + buffer)]

            # create filename
            outfile = savename + "_split_" + str(counter) + ".wav"

            #write audio
            sf.write(outfile, block, sr)

            # update system
            counter += 1
            Samples_Wrote += buffer

            

    except Exception as e:
        print(f'Error Processing File: {e}')

def Batch_split(path, BatchName):
    Path = pathlib.Path(path).with_suffix('')

    ListOfValues = list(Path.glob('*.wav'))

    i = 1

    for item in ListOfValues:
        GenName = BatchName + str(i)

        Split_Audio(10, item, GenName)

        i += 1

Batch_split("Audio/RedwingMB", "Audio/RedwingMB/SplitData/Redwing")
BatchConvert("Audio/RedwingMB/SplitData", "Data/Redwing/Redwing_Split")
