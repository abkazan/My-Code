import tkinter as tk

from pedalboard.io import AudioFile

from . import DbMeter, FRDiagam

root = tk.Tk()

# visulizer = DbMeter(root, __scale=.4)
# visulizer.pack()
# f = AudioFile(open('./dbconn/data/sample2.mp3', 'rb'))
# visulizer.assign(f, 0)
# def show():
#     visulizer.freeze(0)

visualizer = FRDiagam(root, scale=.5)
visualizer.pack()

def go():
    visualizer.assign(AudioFile('./dbconn/data/sample2.mp3'), 0)
    visualizer.freeze(0)

button = tk.Button(root, text = 'go', command = go)
button.pack()
root.mainloop()
