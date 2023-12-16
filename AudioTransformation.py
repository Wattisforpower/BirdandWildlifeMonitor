import matplotlib.pyplot as plt
import pathlib

#for loading and visualizing audio files
import librosa
import librosa.display
from pydub import AudioSegment

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

def convert_to_wav(PathName, BatchName):
    Path = pathlib.Path(PathName).with_suffix('')

    ListOfValues = list(Path.glob('*.m4a'))

    i = 1
    for item in ListOfValues:
        GenName = BatchName + str(i)
        sound = AudioSegment.from_file(item, format='m4a')

        file_Handle = sound.export(GenName, format='wav')

        i += 1

convert_to_wav('Audio/CommonStarlingMB', 'Audio/CommonStarlingMB/CommonStarling')

BatchConvert('Audio/CommonStarlingMB', 'Data/CommonStarling/CommonStarling')