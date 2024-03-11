import tkinter as tk
import random
import numpy as np
import librosa
import sounddevice as sd
from scipy.io import wavfile
from scipy import stats

root = tk.Tk()

root.geometry("720x520")
root.title("Noise Generation and Machine Testing Lab")

# Slider
slider_label = tk.Label(root, text = "Percentage of Noise")
slider_label.place(x = 100, y = 300)

slider = tk.Scale(root, from_=0, to=100, orient= "horizontal")
slider.place(x = 100, y = 320)

# Load in the noise
Noise, _ = librosa.load("AudioNoiseGenerator/Noise2.wav", sr = 20000)

# Drop down for each species
Track = ''
SpeciesSelection = ''

def Store1():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow1_split_1.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull1_split_1.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = 'Audio/CommonGuillemot/SplitData/CommonGuillemot1_split_1.wav'

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling1_split_1.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin2_split_1.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = 'Audio/EurasianOysterCatcher/SplitData/Dunlin1_split_1.wav'
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = 'Audio/EuropeanGoldenPlover/SplitData/Dunlin1_split_1.wav'

    elif SpeciesSelection == 'Herring Gull':
        Track = 'Audio/HerringGull/SplitData/HerringGullMB1_split_1.wav'
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing1_split_1.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = 'Audio/Redwing/SplitData/Redwing1_split_1.wav'

def Store2():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow1_split_2.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull1_split_2.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = 'Audio/CommonGuillemot/SplitData/CommonGuillemot1_split_2.wav'

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling1_split_2.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin3_split_1.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = 'Audio/EurasianOysterCatcher/SplitData/Dunlin2_split_1.wav'
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = 'Audio/EuropeanGoldenPlover/SplitData/Dunlin2_split_1.wav'

    elif SpeciesSelection == 'Herring Gull':
        Track = 'Audio/HerringGull/SplitData/HerringGullMB1_split_2.wav'
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing1_split_2.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = 'Audio/Redwing/SplitData/Redwing1_split_2.wav'

def Store3():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow2_split_1.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull1_split_3.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = 'Audio/CommonGuillemot/SplitData/CommonGuillemot2_split_1.wav'

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling1_split_3.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin4_split_1.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = 'Audio/EurasianOysterCatcher/SplitData/Dunlin2_split_2.wav'
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = 'Audio/HerringGull/SplitData/HerringGullMB2_split_1.wav'
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing1_split_3.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = 'Audio/Redwing/SplitData/Redwing1_split_3.wav'

def Store4():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow2_split_2.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull2_split_1.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = 'Audio/CommonGuillemot/SplitData/CommonGuillemot2_split_2.wav'

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling2_split_1.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin4_split_2.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = 'Audio/EurasianOysterCatcher/SplitData/Dunlin2_split_3.wav'
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = 'Audio/HerringGull/SplitData/HerringGullMB3_split_1.wav'
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing2_split_1.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = 'Audio/Redwing/SplitData/Redwing2_split_1.wav'

def Store5():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow2_split_3.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull2_split_2.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = 'Audio/CommonGuillemot/SplitData/CommonGuillemot3_split_1.wav'

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling2_split_2.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin5_split_1.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = 'Audio/HerringGull/SplitData/HerringGullMB4_split_1.wav'
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing2_split_2.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = 'Audio/Redwing/SplitData/Redwing2_split_2.wav'

def Store6():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow3_split_1.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull3_split_1.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = 'Audio/CommonGuillemot/SplitData/CommonGuillemot3_split_2.wav'

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling2_split_3.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin5_split_2.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = 'Audio/HerringGull/SplitData/HerringGullMB5_split_1.wav'
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing2_split_3.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = 'Audio/Redwing/SplitData/Redwing2_split_3.wav'

def Store7():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow4_split_1.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull4_split_1.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling2_split_4.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin6_split_1.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = 'Audio/HerringGull/SplitData/HerringGullMB6_split_1.wav'
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing3_split_1.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = 'Audio/Redwing/SplitData/Redwing3_split_1.wav'

def Store8():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow4_split_2.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull4_split_2.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling3_split_1.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin6_split_2.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = 'Audio/HerringGull/SplitData/HerringGullMB6_split_2.wav'
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing4_split_1.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def Store9():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow5_split_1.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = 'Audio/BlackheadedGull/SplitData/BlackheadedGull5_split_1.wav'

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling3_split_2.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin7_split_1.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = '  '
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing5_split_1.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def Store10():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow6_split_1.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = '  '

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling3_split_3.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin7_split_2.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = '  '
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing5_split_2.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def Store11():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = 'Audio/Barnswallow/SplitData/BarnSwallow7_split_1.wav'

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = '  '

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling3_split_4.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin8_split_1.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = '  '
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing6_split_1.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def Store12():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = '  '

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = '  '

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling4_split_1.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = 'Audio/Dunlin/SplitData/Dunlin8_split_2.wav'

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = '  '
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing6_split_2.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def Store13():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = '  '

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = '  '

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling4_split_2.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = '  '

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = '  '
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing7_split_1.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def Store14():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = '  '

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = '  '

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling5_split_1.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = '  '

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = '  '
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = 'Audio/NorthernLapwing/SplitData/NorthernLapwing7_split_2.wav'
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def Store15():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = '  '

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = '  '

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling6_split_1.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = '  '

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = '  '
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = '  '
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def Store16():
    global SpeciesSelection, Track
    if SpeciesSelection == 'Barnswallow':
        Track = '  '

    elif SpeciesSelection == 'Blackheaded Gull':
        Track = '  '

    elif SpeciesSelection == 'Common Guillemot':
        Track = '  '

    elif SpeciesSelection == 'Common Starling':
        Track = 'Audio/CommonStarling/SplitData/CommonStarling7_split_1.wav'
    
    elif SpeciesSelection == 'Dunlin':
        Track = '  '

    elif SpeciesSelection == 'Eurasian Oyster Catcher':
        Track = '  '
    
    elif SpeciesSelection == 'European Golden Plover':
        Track = '  '

    elif SpeciesSelection == 'Herring Gull':
        Track = '  '
    
    elif SpeciesSelection == 'Northern Lapwing':
        Track = '  '
    
    elif SpeciesSelection == 'Redwing':
        Track = '  '

def UpdateButtonNames():
    global SpeciesSelection
    selection = clicked.get()
    SpeciesSelection = selection


    if selection == 'Barnswallow':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("05")
        Btn6Text.set("06")
        Btn7Text.set("07")
        Btn8Text.set("08")
        Btn9Text.set("09")
        Btn10Text.set("10")
        Btn11Text.set("11")
        Btn12Text.set("  ")
        Btn13Text.set("  ")
        Btn14Text.set("  ")
        Btn15Text.set("  ")
        Btn16Text.set(" ")
    
    elif selection == 'Blackheaded Gull':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("05")
        Btn6Text.set("06")
        Btn7Text.set("07")
        Btn8Text.set("08")
        Btn9Text.set("09")
        Btn10Text.set("  ")
        Btn11Text.set("  ")
        Btn12Text.set("  ")
        Btn13Text.set("  ")
        Btn14Text.set("  ")
        Btn15Text.set("  ")
        Btn16Text.set("  ")
    
    elif selection == 'Common Guillemot':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("05")
        Btn6Text.set("06")
        Btn7Text.set("  ")
        Btn8Text.set("  ")
        Btn9Text.set("  ")
        Btn10Text.set("  ")
        Btn11Text.set("  ")
        Btn12Text.set("  ")
        Btn13Text.set("  ")
        Btn14Text.set("  ")
        Btn15Text.set("  ")
        Btn16Text.set("  ")
    
    elif selection == 'Common Starling':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("05")
        Btn6Text.set("06")
        Btn7Text.set("07")
        Btn8Text.set("08")
        Btn9Text.set("09")
        Btn10Text.set("10")
        Btn11Text.set("11")
        Btn12Text.set("12")
        Btn13Text.set("13")
        Btn14Text.set("14")
        Btn15Text.set("15")
        Btn16Text.set("16")
    
    elif selection == 'Dunlin':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("05")
        Btn6Text.set("06")
        Btn7Text.set("07")
        Btn8Text.set("08")
        Btn9Text.set("09")
        Btn10Text.set("10")
        Btn11Text.set("11")
        Btn12Text.set("12")
        Btn13Text.set("  ")
        Btn14Text.set("  ")
        Btn15Text.set("  ")
        Btn16Text.set("  ")

    elif selection == 'Eurasian Oyster Catcher':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("  ")
        Btn6Text.set("  ")
        Btn7Text.set("  ")
        Btn8Text.set("  ")
        Btn9Text.set("  ")
        Btn10Text.set("  ")
        Btn11Text.set("  ")
        Btn12Text.set("  ")
        Btn13Text.set("  ")
        Btn14Text.set("  ")
        Btn15Text.set("  ")
        Btn16Text.set("  ")
    
    elif selection == 'European Golden Plover':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("  ")
        Btn4Text.set("  ")
        Btn5Text.set("  ")
        Btn6Text.set("  ")
        Btn7Text.set("  ")
        Btn8Text.set("  ")
        Btn9Text.set("  ")
        Btn10Text.set("  ")
        Btn11Text.set("  ")
        Btn12Text.set("  ")
        Btn13Text.set("  ")
        Btn14Text.set("  ")
        Btn15Text.set("  ")
        Btn16Text.set("  ")

    elif selection == 'Herring Gull':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("05")
        Btn6Text.set("06")
        Btn7Text.set("07")
        Btn8Text.set("08")
        Btn9Text.set("  ")
        Btn10Text.set("  ")
        Btn11Text.set("  ")
        Btn12Text.set("  ")
        Btn13Text.set("  ")
        Btn14Text.set("  ")
        Btn15Text.set("  ")
        Btn16Text.set("  ")
    
    elif selection == 'Northern Lapwing':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("05")
        Btn6Text.set("06")
        Btn7Text.set("07")
        Btn8Text.set("08")
        Btn9Text.set("09")
        Btn10Text.set("10")
        Btn11Text.set("11")
        Btn12Text.set("12")
        Btn13Text.set("13")
        Btn14Text.set("14")
        Btn15Text.set("  ")
        Btn16Text.set("  ")
    
    elif selection == 'Redwing':
        Btn1Text.set("01")
        Btn2Text.set("02")
        Btn3Text.set("03")
        Btn4Text.set("04")
        Btn5Text.set("05")
        Btn6Text.set("06")
        Btn7Text.set("07")
        Btn8Text.set("  ")
        Btn9Text.set("  ")
        Btn10Text.set("  ")
        Btn11Text.set("  ")
        Btn12Text.set("  ")
        Btn13Text.set("  ")
        Btn14Text.set("  ")
        Btn15Text.set("  ")
        Btn16Text.set("  ")
    


Btn1Text = tk.StringVar()
Btn1Text.set("  ")
btn1 = tk.Button(root, textvariable=Btn1Text, command=Store1)
btn1.place(x = 20, y = 30)

Btn2Text = tk.StringVar()
Btn2Text.set("  ")
btn2 = tk.Button(root, textvariable=Btn2Text, command=Store2)
btn2.place(x = 50, y = 30)

Btn3Text = tk.StringVar()
Btn3Text.set("  ")
btn3 = tk.Button(root, textvariable=Btn3Text, command=Store3)
btn3.place(x = 80, y = 30)

Btn4Text = tk.StringVar()
Btn4Text.set("  ")
btn4= tk.Button(root, textvariable=Btn4Text, command=Store4)
btn4.place(x = 110, y = 30)

Btn5Text = tk.StringVar()
Btn5Text.set("  ")
btn5 = tk.Button(root, textvariable=Btn5Text, command=Store5)
btn5.place(x = 140, y = 30)

Btn6Text = tk.StringVar()
Btn6Text.set("  ")
btn6 = tk.Button(root, textvariable=Btn6Text, command=Store6)
btn6.place(x = 170, y = 30)

Btn7Text = tk.StringVar()
Btn7Text.set("  ")
btn7 = tk.Button(root, textvariable=Btn7Text, command=Store7)
btn7.place(x = 200, y = 30)

Btn8Text = tk.StringVar()
Btn8Text.set("  ")
btn8 = tk.Button(root, textvariable=Btn8Text, command=Store8)
btn8.place(x = 230, y = 30)

Btn9Text = tk.StringVar()
Btn9Text.set("  ")
btn9 = tk.Button(root, textvariable=Btn9Text, command=Store9)
btn9.place(x = 260, y = 30)

Btn10Text = tk.StringVar()
Btn10Text.set("  ")
btn10 = tk.Button(root, textvariable=Btn10Text, command=Store10)
btn10.place(x = 290, y = 30)

Btn11Text = tk.StringVar()
Btn11Text.set("  ")
btn11 = tk.Button(root, textvariable=Btn11Text, command=Store11)
btn11.place(x = 320, y = 30)

Btn12Text = tk.StringVar()
Btn12Text.set("  ")
btn12 = tk.Button(root, textvariable=Btn12Text, command=Store12)
btn12.place(x = 350, y = 30)

Btn13Text = tk.StringVar()
Btn13Text.set("  ")
btn13 = tk.Button(root, textvariable=Btn13Text, command=Store13)
btn13.place(x = 380, y = 30)

Btn14Text = tk.StringVar()
Btn14Text.set("  ")
btn14 = tk.Button(root, textvariable=Btn14Text, command=Store14)
btn14.place(x = 410, y = 30)

Btn15Text = tk.StringVar()
Btn15Text.set("  ")
btn15 = tk.Button(root, textvariable=Btn15Text, command=Store15)
btn15.place(x = 440, y = 30)

Btn16Text = tk.StringVar()
Btn16Text.set("  ")
btn16 = tk.Button(root, textvariable=Btn16Text, command=Store16)
btn16.place(x = 470, y = 30)

Speciesoptions = [
    "Barnswallow",
    "Blackheaded Gull",
    "Common Guillemot",
    "Common Starling",
    "Dunlin",
    "Eurasian Oyster Catcher",
    "European Golden Plover",
    "Herring Gull",
    "Northern Lapwing",
    "Redwing"
]

clicked = tk.StringVar()

clicked.set("Barnswallow")

dropSpecies = tk.OptionMenu(root, clicked, *Speciesoptions)
dropSpecies.place(x = 100, y = 70)

ConfirmBtn = tk.Button(root, text="Confirm Species", command = UpdateButtonNames)
ConfirmBtn.place(x = 100, y= 170)

# Command for Button Press
def Play():
    global Noise, Track

    #audiopath = 'Audio/Barnswallow/SplitData/BarnSwallow2_split_1.wav'
    Audio, _ = librosa.load(Track, sr = 20000)

    PercentageOfNoise = slider.get() / 100

    Result = Audio + PercentageOfNoise * Noise

    sd.play(Result, 20000)
    sd.wait()
    

Play_Button = tk.Button(root, text= "Play Sound", command = Play)
Play_Button.place(x = 220, y = 360)


root.mainloop()

