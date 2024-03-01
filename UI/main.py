import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np

import logic

FT = logic.Functions_Toolbox()

root = tk.Tk()
root.geometry("1080x720")

root.title("Wildlife and Bird Monitoring System")

Tabs = ttk.Notebook(root)

Overview = ttk.Frame(Tabs)
Counter = ttk.Frame(Tabs)

Tabs.add(Overview, text="Overview")
Tabs.add(Counter, text="Counter")

Tabs.pack(expand = 1, fill="both")

frame = tk.Frame(Overview, width = 600, height= 400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

LatestImage = "Images/Barn_Swallow.jpg"


img = ImageTk.PhotoImage(Image.open(LatestImage))

label = tk.Label(frame, image = img)
label.pack()

root.mainloop()
