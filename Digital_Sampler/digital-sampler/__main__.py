'''
Main for the Digital Sampler Application

To run, execute python -m digital-sampler
'''


from .digitalSampler import MusicPlayer
from tkinter import Tk

root = Tk()
MusicPlayer(root)
root.mainloop()
