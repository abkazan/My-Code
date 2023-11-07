import tkinter as tk
from time import sleep

from pedalboard.io import AudioFile

from . import DbMeter

root = tk.Tk()
visulizer = DbMeter(root, __scale=.4)

visulizer.pack()


f = AudioFile(open('./dbconn/data/sample2.mp3', 'rb'))
visulizer.assign(f, 0)

def show():
    visulizer.freeze(0)

button = tk.Button(root, text='play pause', command=show)
button.pack()
root.mainloop()
