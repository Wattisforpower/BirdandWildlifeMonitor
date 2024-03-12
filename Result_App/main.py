import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import serialComs

print("Loading")

PySer = serialComs.SerialComs("COM7", "115200")
PySer.Open()

print("1")
root = tk.Tk()

root.geometry("720x520")
Tabs = tk.ttk.Notebook(root)

CurrentObservation = ttk.Frame(Tabs)
PreviousObservations = ttk.Frame(Tabs)

Tabs.add(CurrentObservation, text = "Current Observation")
Tabs.pack(expand = 1, fill = "both")

# Tab 1 Program
ImageList = [
    "BarnSwallow\n",
    "BlackheadedGull\n",
    "CommonGuillemot\n",
    "CommonStarling\n",
    "Dunlin\n",
    "EurasianOysterCatcher\n",
    "EuropeanGoldenPlover\n",
    "HerringGull\n",
    "NorthernLapwing\n",
    "Redwing\n",
    "questionmark\n"
]

tk.Label(CurrentObservation, text = "Current Species Detected: ").place(x = 10, y = 20)#
SpeciesLabel = tk.Label(CurrentObservation, text = "Unknown")
SpeciesLabel.place(x = 150, y = 20)

Load = Image.open('Result_App/Images/questionmark.jpg')
Render = None
PreviousResult = "Unknown"
Result = "Unknown"

print("2")

'''
def RenderResults():
    global PreviousResult
    try:
        Instream = PySer.ReadLine()
        Result = Instream.decode("utf-8")
    except:
        pass
    
    if Result in ImageList:
        with open("Result_App/Results.csv", "a") as f:
            f.write(Result)
            f.close()

    root.after(10)

RenderResults()
'''

def GetResults():
    global Result, PreviousResult
    Instream = PySer.ReadLine()
    print(Instream)
    Instream_Decoded = Instream.decode("utf-8", errors = 'ignore')

    if Instream_Decoded in ImageList:
        Result = Instream_Decoded
    elif Instream_Decoded == 'Unknown\n':
        Result = Instream_Decoded
    else:
        Result = PreviousResult
    
    #CurrentObservation.after(10, GetResults)

#GetResults()


def Update():
    global Load, Render, PreviousResult, Result

    GetResults()

    SpeciesLabel.config(text = Result)

    if Result == ImageList[0]:
        Load = Image.open('Result_App/Images/BarnSwallow.jpg')
    elif Result == ImageList[1]:
        Load = Image.open('Result_App/Images/BlackheadedGull.jpg')
    elif Result == ImageList[2]:
        Load = Image.open('Result_App/Images/CommonGuillemot.jpg')
    elif Result == ImageList[3]:
        Load = Image.open('Result_App/Images/CommonStarling.jpg')
    elif Result == ImageList[4]:
        Load = Image.open('Result_App/Images/Dunlin.jpg')
    elif Result == ImageList[5]:
        Load = Image.open('Result_App/Images/EurasianOysterCatcher.jpg')
    elif Result == ImageList[6]:
        Load = Image.open('Result_App/Images/EuropeanGoldenPlover.jpg')
    elif Result == ImageList[7]:
        Load = Image.open('Result_App/Images/HerringGull.jpg')
    elif Result == ImageList[8]:
        Load = Image.open('Result_App/Images/NorthernLapwing.jpg')
    elif Result == ImageList[9]:
        Load = Image.open('Result_App/Images/Redwing.jpg')
    else:
        Load = Image.open('Result_App/Images/questionmark.jpg')
    

    Render = ImageTk.PhotoImage(Load.resize((300, 300)))

    Img = tk.Label(CurrentObservation, image = Render)
    Img.place(x = 10, y = 40)

    if Result != PreviousResult:
        PreviousResult = Result


    CurrentObservation.after(1000, Update)


Update()

root.mainloop()
