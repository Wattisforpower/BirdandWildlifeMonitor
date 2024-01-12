from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

import numpy as np
from scipy.io import wavfile
import sounddevice as sd

root = Tk()
root.geometry("1080x720")

def Play_BS():
    sr, samples = wavfile.read("UI_Audio/Audio/BarnswallowMB/BarnSwallow.wav")
    sd.play(samples, sr)

    sd.wait()

def Play_BS1():
    sr, samples = wavfile.read("UI_Audio/Audio/BarnswallowMB/BarnSwallow1.wav")
    sd.play(samples, sr)

    sd.wait()

def Play_BS2():
    sr, samples = wavfile.read("UI_Audio/Audio/BarnswallowMB/BarnSwallow2.wav")
    sd.play(samples, sr)

    sd.wait()

def Play_BS3():
    sr, samples = wavfile.read("UI_Audio/Audio/BarnswallowMB/BarnSwallow3.wav")
    sd.play(samples, sr)

    sd.wait()

def Play_BS4():
    sr, samples = wavfile.read("UI_Audio/Audio/BarnswallowMB/BarnSwallow4.wav")
    sd.play(samples, sr)

    sd.wait()

def Play_BS5():
    sr, samples = wavfile.read("UI_Audio/Audio/BarnswallowMB/BarnSwallow5.wav")
    sd.play(samples, sr)

    sd.wait()

def Play_BS6():
    sr, samples = wavfile.read("UI_Audio/Audio/BarnswallowMB/BarnSwallow6.wav")
    sd.play(samples, sr)

    sd.wait()

BarnSwallow_Button = Button(root, text= "Barn Swallow 1", command = Play_BS)
BarnSwallow_Button.pack()

BarnSwallow_Button = Button(root, text= "Barn Swallow 2", command = Play_BS1)
BarnSwallow_Button.pack()

BarnSwallow_Button = Button(root, text= "Barn Swallow 3", command = Play_BS2)
BarnSwallow_Button.pack()

BarnSwallow_Button = Button(root, text= "Barn Swallow 4", command = Play_BS3)
BarnSwallow_Button.pack()

BarnSwallow_Button = Button(root, text= "Barn Swallow 5", command = Play_BS4)
BarnSwallow_Button.pack()

BarnSwallow_Button = Button(root, text= "Barn Swallow 6", command = Play_BS5)
BarnSwallow_Button.pack()

BarnSwallow_Button = Button(root, text= "Barn Swallow 7", command = Play_BS6)
BarnSwallow_Button.pack()

root.mainloop()