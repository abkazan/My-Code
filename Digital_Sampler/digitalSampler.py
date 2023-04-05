from tkinter import *
from tkinter import filedialog
from tkinter import messagebox # * demo for message boxx
from PIL import ImageTk,Image
from tkdial import Dial
import pygame
import os
import shutil
import backend as back
#TODO - Put in list of all colors used
#with their description as actual var name

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("Beats by L35")
        # Window Geometry
        self.root.geometry("1000x975+500+500") #figure out what +500+500
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()
        self.status.set("--")  # default status is empty
        # Declaring Effects Variable
        self.effects = StringVar()
        self.effects.set("(0, 0, 0, 0)")  # default
        # ============= Creating the Track Frame for Song label & status label =========
        trackframe = LabelFrame(
            self.root,
            text="Sample",
            font=("times new roman", 15, "bold"),
            bg="#450939",
            fg="white",
            bd=5,
            relief=GROOVE,
        )

        trackframe.place(x=0, y=0, width=600, height=100)

        # Inserting Song Track Label
        track_name = Label(
            trackframe,
            textvariable=self.track,
            width=20,
            font=("times new roman", 20, "bold"),
            bg="#d661b8",
            bd=5,
            fg="#a6f8b0",
            relief=SUNKEN,
        )

        # Inserting Status Label
        track_status = Label(
            trackframe,
            textvariable=self.status,
            font=("times new roman", 24, "bold"),
            bd=5,
            bg="#d661b8",
            fg="#a6f8b0",
            relief=SUNKEN
        )

        # organizing in grid of 'trackframe'
        track_name.grid(row=0, column=0, padx=10, pady=5)
        track_status.grid(row=0, column=1, padx=10, pady=5)

        # ======================== Creating Button Frame =============================
        #TODO  - Add vars to a dictionary to cut out redundancy
        buttonframe = LabelFrame(
            self.root,
            text="Control Panel",
            font=("times new roman", 15, "bold"),
            bg="#08525e",
            fg="white",
            bd=5,
            relief=GROOVE,
        )
        buttonframe.place(x=0, y=100, width=600, height=175)

        # Inserting Play Button
        play_btn = Button(
            buttonframe,
            text="PLAY",
            command=self.playsong,
            width=10,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="#450939",
            bg="#c89cd7",
        )

        # Inserting Pause Button
        pause_btn = Button(
            buttonframe,
            text="PAUSE",
            command=self.pausesong,
            width=8,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="#450939",
            bg="#c89cd7",
        )

        # Inserting Unpause Button
        unpause_btn = Button(
            buttonframe,
            text="UNPAUSE",
            command=self.unpausesong,
            width=10,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="#450939",
            bg="#c89cd7",
        )

        # Inserting Stop Button
        stop_btn = Button(
            buttonframe,
            text="STOP",
            command=self.stopsong,
            width=10,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="#450939",
            bg="#c89cd7",
        )

        # Inserting an add File Button
        addFile_btn = Button(
            buttonframe,
            text="ADD FILE",
            command=self.add_song,
            width=10,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="#450939",
            bg="#c89cd7",
        )
        # Inserting an add effects Button
        add_effects_btn = Button(
            buttonframe,
            text="ADD EFFECTS",
            command=self.new_window,
            width=10,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="#450939",
            bg="#c89cd7",
        )
        

        # organizing in grid of 'buttonframe'
        play_btn.grid(row=0, column=0, padx=10, pady=10)
        pause_btn.grid(row=0, column=1, padx=10, pady=10)
        unpause_btn.grid(row=0, column=2, padx=10, pady=10)
        stop_btn.grid(row=0, column=3, padx=10, pady=10)
        addFile_btn.grid(row=1, column=0, padx=10, pady=10)
        add_effects_btn.grid(row=1, column=1, padx=10,pady=10)

        # ===================== Creating Dial Frame ===========================
        dial_frame = LabelFrame(
            self.root,
            text="Effects",
            fg="white",
            font=("times new roman", 15, "bold"),
            bd=7,
            relief=GROOVE,
            bg="#d661b8",
        )
        dial_frame.place(x=0, y=275, width=1000, height=200)

        # ----------- Dials for Dial Frame ----------

        reverb_dial = Dial(
            dial_frame,
            start=0,
            end=100,
            text="Reverb: ",
            text_color="#450939",
            color_gradient=("#a6f8b0", "#0edcfa"),
            bg="#d661b8",
            needle_color="#450939",
            unit_width=5,
            unit_length=7,
            unit_color="#08525e",
            radius=50,
            scroll_steps=5
        )

        delay_dial = Dial(
            dial_frame,
            start=0,
            end=100,
            text="Delay: ",
            text_color="#450939",
            color_gradient=("#a6f8b0", "#0edcfa"),
            bg="#d661b8",
            needle_color="#450939",
            unit_width=5,
            unit_length=7,
            unit_color="#08525e",
            radius=50,
            scroll_steps=5
        )

        chorus_dial = Dial(
            dial_frame,
            start=0,
            end=100,
            text="Chorus: ",
            text_color="#450939",
            color_gradient=("#a6f8b0", "#0edcfa"),
            bg="#d661b8",
            needle_color="#450939",
            unit_width=5,
            unit_length=7,
            unit_color="#08525e",
            radius=50,
            scroll_steps=5
        )

        distortion_dial = Dial(
            dial_frame,
            start=0,
            end=100,
            text="Distortion: ",
            text_color="#450939",
            color_gradient=("#a6f8b0", "#0edcfa"),
            bg="#d661b8",
            needle_color="#450939",
            unit_width=5,
            unit_length=7,
            unit_color="#08525e",
            radius=50,
            scroll_steps=5
        )

        # list with each dial - used for keeping track of dial values
        self.effectsList = [reverb_dial, delay_dial, chorus_dial, distortion_dial]

        # label showing the recorded
        # values in all dials when 'Apply Effects' button is clicked
        effect_vars_label = Label(
            dial_frame,
            textvariable=self.effects,
            font=("times new roman", 12, "bold"),
            bd=5,
            bg="#d661b8",
            fg="#450939",
            relief=SUNKEN,
        )

        apply_btn = Button(
            dial_frame,
            text="Apply Effects",
            command=self.apply_effects,
            font=("times new roman", 16, "bold"),
            fg="#450939",
            bg="#c89cd7",
            bd=3,
            padx=50,  # padding for inside of button (aka size of button)
            pady=25,
        )

        # organizing in grid of dial_frame
        reverb_dial.grid(row=0, column=0, padx=10, pady=10)
        delay_dial.grid(row=0, column=1, padx=10, pady=10)
        chorus_dial.grid(row=0, column=2, padx=10, pady=10)
        distortion_dial.grid(row=0, column=3, padx=10, pady=10)
        # padding for button on outside of button goes here
        apply_btn.grid(row=0, column=4, padx=15, pady=10)
        effect_vars_label.grid(row=0, column=5, padx=5, pady=10)


        # ===================== Creating Pad Frame ===========================
        sequencer_frame = LabelFrame(
            self.root,
            text="Sequencer Pad",
            fg="white",
            font=("times new roman", 15, "bold"),
            bd=7,
            relief=GROOVE,
            bg="#b7c9be",
        )
        sequencer_frame.place(x=0, y=475, width=1000, height=500)

        # ----------- Buttons for Pad Frame -----------------------

        #image for each button
        #global declaration is necessary because since we're in a different frame  ***
        #other than root, python garbage collector thinks its trash otherwise
        global pad_btn_img
        global active_btn_img
        global wav_view_img

        pad_btn_img = ImageTk.PhotoImage(Image.open("glossyButtonResized.png"))
        active_btn_img = ImageTk.PhotoImage(Image.open("greenActiveButton.png"))
        inactive_btn_img = ImageTk.PhotoImage(Image.open("greyInactiveButton.png"))
        wav_view_img = ImageTk.PhotoImage(Image.open("audioWav.png"))
        

        #for loop to create and grid 16 radio buttons. rows are alternating to save room for indicator buttons
        myRow = 0
        for r in range(4): #TODO - Combine statements to simplify
            for c in range(4):
                Button(sequencer_frame, image=pad_btn_img, highlightthickness=0, borderwidth=0, bd=0).grid(row=myRow,column=c, padx=20, pady=2)
            myRow = myRow + 2

        #for loop to create and grid 16 more buttons for indicating which step the sequence is on
        myRow = 1
        for r in range(4):
            for c in range(4):
                Button(sequencer_frame,image=active_btn_img, bg="#b7c9be",
                       activebackground="#b7c9be", relief=FLAT, highlightthickness=0, borderwidth=0, bd=0).grid(row=myRow, column=c)
            myRow = myRow + 2
        
        # ------------ Adding Image to Sequencer Frame on RHS ------------------
        myImageLabel = Label(sequencer_frame,image=wav_view_img, bg="#b7c9be").grid(row=0, column=4, rowspan=7)

        # ======================== Playlist Frame ===========================
        songsframe = LabelFrame(
            self.root,
            text="Loaded Samples",
            font=("times new roman", 15, "bold"),
            bg="#08525e",
            fg="white",
            bd=5,
            relief=GROOVE,
        )
        songsframe.place(x=600, y=0, width=400, height=275)

        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        scrol_x = Scrollbar(songsframe, orient=HORIZONTAL)

        # Inserting Playlist listbox
        self.playlist = Listbox(
            songsframe,
            yscrollcommand=scrol_y.set,
            xscrollcommand=scrol_x.set,
            selectbackground="#a6f8b0",
            selectforeground="#dc22b6",
            selectmode=SINGLE,
            font=("times new roman", 18, "bold"),
            bg="#b7c9be",
            fg="#450939",
            bd=5,
            relief=GROOVE,
            height=50
        )
        # Applying Scrollbars to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        scrol_x.pack(side=BOTTOM, fill=X)
        scrol_x.config(command=self.playlist.xview)
        self.playlist.pack(fill=BOTH)
        # Changing Directory for fetching Songs
        # make this the song folder in your directory
        os.chdir("./songs")

        # Fetching Songs
        songtracks = os.listdir()

        # Inserting Songs into Playlist
        self.songs = []
        for track in songtracks:
            self.songs.append(track)
            self.playlist.insert(END, track)

    def playsong(self):
        # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))

        # Displaying Status
        self.status.set("--Playing")

        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get(ACTIVE))

        # Playing Selected Song
        pygame.mixer.music.play()

    def stopsong(self):
        # Displaying Status
        self.status.set("--Stopped")
        # Stopped Song
        pygame.mixer.music.stop()

    def pausesong(self):
        # Displaying Status
        self.status.set("--Paused")

        # Paused Song
        pygame.mixer.music.pause()

    def unpausesong(self):
        # It will Display the  Status
        self.status.set("--Playing")

        # Playing back Song
        pygame.mixer.music.unpause()
    #TODO - less copying songs into directory
    def add_song(self):
        file_path = filedialog.askopenfilename(
            initialdir="./songs",
            title="Select file",
            filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*"))
        )
        dest_dir = "./songs"
        file_name, file_ext = os.path.splitext(file_path)
        dest_file_path = os.path.join(dest_dir, os.path.basename(file_name) + file_ext)
        shutil.copy2(file_path, dest_file_path)
        self.update_songs()

    def update_songs(self):
        os.chdir("./songs")
        # Fetching Songs
        songtracks = os.listdir()
        # Inserting Songs into Playlist
        for track in songtracks:
            if track not in self.songs:
                self.playlist.insert(END, track)
            else:
                continue

    # ==================== Function for Collecting Dial Values =============
    #TODO - FOrmat string !!!!
    def apply_effects(self):
        self.effects.set(
            "("
            + str(int(self.effectsList[0].get()))
            + ", "
            + str(int(self.effectsList[1].get()))
            + ", "
            + str(int(self.effectsList[2].get()))
            + ", "
            + str(int(self.effectsList[3].get()))
            + ")"
        )
        back.applyEffects([self.effectsList[0].get(),self.effectsList[1].get(),self.effectsList[2].get(),self.effectsList[3].get()],self.playlist.get(ACTIVE))
    def new_window(self):
        new_window = Toplevel(self.root)
        new_window.title("EFFECTS")
        new_window.geometry("500x500")
        dial_frame = LabelFrame(
            self.new_window,
            text="Effects",
            fg="white",
            font=("times new roman", 15, "bold"),
            bd=7,
            relief=GROOVE,
            bg="#d661b8",
        )
        dial_frame.place(x=0, y=275, width=1000, height=200)
        """_summary_
        
        
        Label(new_window, text ="This is a new window").pack()
        

        # ----------- Dials for Dial Frame ----------

        reverb_dial = Dial(
            dial_frame,
            start=0,
            end=100,
            text="Reverb: ",
            text_color="#450939",
            color_gradient=("#a6f8b0", "#0edcfa"),
            bg="#d661b8",
            needle_color="#450939",
            unit_width=5,
            unit_length=7,
            unit_color="#08525e",
            radius=50,
            scroll_steps=5
        )

        delay_dial = Dial(
            dial_frame,
            start=0,
            end=100,
            text="Delay: ",
            text_color="#450939",
            color_gradient=("#a6f8b0", "#0edcfa"),
            bg="#d661b8",
            needle_color="#450939",
            unit_width=5,
            unit_length=7,
            unit_color="#08525e",
            radius=50,
            scroll_steps=5
        )

        chorus_dial = Dial(
            dial_frame,
            start=0,
            end=100,
            text="Chorus: ",
            text_color="#450939",
            color_gradient=("#a6f8b0", "#0edcfa"),
            bg="#d661b8",
            needle_color="#450939",
            unit_width=5,
            unit_length=7,
            unit_color="#08525e",
            radius=50,
            scroll_steps=5
        )

        distortion_dial = Dial(
            dial_frame,
            start=0,
            end=100,
            text="Distortion: ",
            text_color="#450939",
            color_gradient=("#a6f8b0", "#0edcfa"),
            bg="#d661b8",
            needle_color="#450939",
            unit_width=5,
            unit_length=7,
            unit_color="#08525e",
            radius=50,
            scroll_steps=5
        )
        reverb_dial.grid(row=0, column=0, padx=10, pady=10)
        delay_dial.grid(row=0, column=1, padx=10, pady=10)
        chorus_dial.grid(row=0, column=2, padx=10, pady=10)
        distortion_dial.grid(row=0, column=3, padx=10, pady=10)
        """


root = Tk()
MusicPlayer(root)
root.mainloop()
