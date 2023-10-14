from . import digitalSampler as ds
from .vis import FRDiagam
from pedalboard.io import AudioFile
import pygame
from pedalboard.io import AudioFile

import copy
class drumpad:
    '''
    Composes the bottom ~third of the main window.
    Contains 20 buttons corresponding to 20 keyboard keys - q through l
    on a standard qwerty keyboard. The class also contains all
    the methods to execute when one of these 20 keys is pressed.
    For each button, the user selects one of their loaded samples
    to associate with the button. When the button is then pressed, 
    the associated sample plays. Every button has its own channel,
    which is displayed along the very bottom of the frame. A master-
    volume slider is located along the far left side.

    Widgets
    -------
    drumpad_frame : LabelFrame
        Holds all the other components of this class

    '''
    def keyboard_trigger(self, e):
        # this is a really bad shallow method whoops
        self.pressButton(e.char)
    
            
    
    def pressButton(self, key: str):
        if (self.mp.key_bindings[key]):
            for button in self.button_list:
                if key == button.cget("text"):
                    #print(f"button {e.char} pressed")
                    button.configure(state=ds.ACTIVE, relief=ds.RAISED)
                    if (self.mp.user_songs[self.mp.key_bindings[key]]):
                            sound_to_play = self.mp.user_songs[self.mp.key_bindings[key]]
                            sound_to_play.seek(0)
                            copy_of_sound = copy.copy(sound_to_play)
                            self.mp._channel = pygame.mixer.Sound(copy_of_sound).play()
                            self.mp._channel.set_volume(self.mp._volume)

                            # Open file here
                            self.mp._visualizer.assign(AudioFile(copy.copy(self.mp.user_songs[self.mp.key_bindings[key]])), 0)
                            self.mp._visualizer.freeze(0)
                            self.mp._spectogram.assign(AudioFile(copy.copy(self.mp.user_songs[self.mp.key_bindings[key]])), 0)
                            self.mp._spectogram.freeze(0)

                        # Close file here
                        
                    #mp.play_new_song()

    def keyboard_release(self, e) : 
        self.releaseButton(e.char)
    
    def releaseButton(self, key :str):
        for button in self.button_list:
            if key == button.cget("text"):
                button.configure(state=ds.NORMAL, relief=ds.RAISED)
    
    def __init__(self, mp) -> None:
        self.mp = mp
        drumpad_frame_args = {
            #"text": "Drum Pad",
            "fg": ds.COLOR_DARK_GRAY,
            "font": ("Terminal", 20),
            "bd": 7,
            "relief": ds.FLAT,
            "bg": ds.COLOR_GRAYISH_GREEN,
        }

        #shared fields between drum pad buttons
        drumpad_btn_args = {
            "fg": ds.COLOR_NEON_GREEN,
            "bg": ds.COLOR_MEDIUM_GRAY,
            "padx": 20,
            "pady": 20,
            "font": ("Terminal", 12),
            "relief": ds.RAISED,
            "bd": 5,
            "activebackground": ds.COLOR_SUPER_DARK_GRAY,
            "activeforeground": ds.COLOR_NEON_GREEN
        }

        # -if we want, scale can have variable=volumeValue (where volNum has been declared as an IntVar)
        volume_slider_args = {
            "width": 60,
            "length": 460,
            "orient": ds.HORIZONTAL,
            "relief": ds.RAISED,
            "bg":ds.COLOR_LIGHT_GRAY,
            "command": mp.adjust_volume,
            "fg": ds.COLOR_NEON_GREEN,
            "label": "MASTER VOLUME"
        }

        #create label frame
        drumpad_frame = ds.LabelFrame(mp.root, **drumpad_frame_args)
        
        self.button_list = []
        list_of_chars = ['1', '2', '3', '4',
                         'q', 'w', 'e', 'r',
                         'a', 's', 'd', 'f',
                         'z', 'x', 'c', 'v']
        
        for character in list_of_chars:
            self.button_list.append(ds.Button(drumpad_frame, **drumpad_btn_args, text=character))
            mp.key_bindings[character] = None

       
        txt = "text"
        for button in self.button_list:
            #print(f"binding button {button.cget(txt)}")
            mp.root.bind(f"<KeyPress-{button.cget(txt)}>", self.keyboard_trigger)
            mp.root.bind(f"<KeyRelease-{button.cget(txt)}>", self.keyboard_release)

        drumpad_frame.place(x=0, y=275, width=1000, height=500)
        
        #Currently the placeholder image for audio wav visual

        dp_pad_args = {
            "padx": 5,
            "pady": 5,
        }
        
        #grid drum pad buttons in 4 rows of 4 cols each
        button_counter = 0
        for row in range(4):
            for column in range(4):
                self.button_list[button_counter].grid(row=row, column=column, **dp_pad_args)
                button_counter += 1


        #adding master volume slider to drumpad-frame on LHS
        volumeSlider = ds.Scale(drumpad_frame, **volume_slider_args, font="Terminal")
        volumeSlider.set(50) #default value to 50, 
        volumeSlider.grid(row=4, column=0, padx=5, pady=15, columnspan = 5)

        #holds list of all the small dbmeters associated with drum pad
        #db_meter_list = []
        
        '''
        #create and grid 16 meters, adding them to list and gridding
        for r in range (4):
            for c in range(5,9):
                db_meter_list.append(DbMeter(drumpad_frame, __scale = .065))
                db_meter_list[-1].grid(row=r, column=c, padx=15, pady=5)
        '''

        #main dbmeter for entire app
        mp._visualizer = ds.DbMeter(drumpad_frame, __scale = .275)
        mp._visualizer.grid(row=0, column=4, rowspan=4, padx=5)
        
        # visualizer = FRDiagam(root, scale=.5)
        # visualizer.pack()
        # visualizer.assign(AudioFile('./dbconn/data/sample2.mp3'), 0)
        # visualizer.freeze(0)

        mp._spectogram = FRDiagam(drumpad_frame, scale=0.38)
        mp._spectogram.grid(row=0, column=5, rowspan=4, padx=5, pady=10)

        teamLabel = ds.Label(drumpad_frame, font=("Terminal", 36, "bold"), fg=ds.COLOR_SUPER_DARK_GRAY, bg=ds.COLOR_GRAYISH_GREEN, text="Beats by L35")
        teamLabel.grid(row=4, column=5, padx=5) 
        
        # ------------ Adding Image to Drum Pad Frame on LHS Below Buttons ------------------
        #myImageLabel = Label(drumpad_frame,image=wav_view_img, bg=color_grayish_green).grid(row=2, column=0, columnspan=10)