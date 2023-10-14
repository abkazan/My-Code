# stdlib
import os
import copy
from tkinter import *
from tkinter import (
    messagebox, # demo for message box
    filedialog,
    simpledialog, # demo for naming song
    ) 

# 3rd party
from tkdial import Dial


from .vis import DbMeter
from .vis import FRDiagam
from .timeline import Timeline

try:
    import pygame
    from pygame.mixer import Sound, Channel
    
except (ImportError, ModuleNotFoundError) as error:
    USING_PYGAME: bool = False
    from sys import stderr
    stderr.writelines(f'Could not import pygame. No sound will be played. {error.msg = }, {error.args = }')
    
except Exception as error:
    error.add_note('Failed to import pygame with fatal error')
    raise 

else:
    USING_PYGAME: bool = True
    
# package
from .backend import *
from .btn_frame import *
from .effects import *
from .drumpad import *
from .dbwin import *
from .serialaccess import *

global delay_img
global reverb_img
global chorus_img
global distortion_img

# Color names to be used for frames and widgets
COLOR_DEEP_PURPLE: str = "#450939"
COLOR_LIGHT_PURPLE: str = "#701e60"
COLOR_DEEP_BLUE: str  = "#08525e"
COLOR_BRIGHT_PINK: str = "#d661b8"
COLOR_HOT_PINK: str = "#dc22b6"
COLOR_LAVENDER: str = "#c89cd7"
COLOR_MINT: str = "#a6f8b0"
COLOR_CYAN: str = "#0edcfa"
COLOR_GRAYISH_GREEN: str = "#b7c9be"
COLOR_DARK_GRAYISH_GREEN: str = "#535c56"
COLOR_LIGHT_GRAYISH_GREEN: str = "#c3d4c8"
COLOR_WHITE: str = "#ffffff"
COLOR_SUPER_DARK_GRAY: str = "#282e33"
COLOR_DARK_GRAY: str = "#3c464d"
COLOR_MEDIUM_GRAY: str = "#40555d"
COLOR_LIGHT_GRAY: str = "#8599a1"
COLOR_NEON_GREEN: str = "#A5DE1A"


class track_frame:
    '''
    Composes the top left area of the main window where
    the sample title and status are shown.

    Widgets
    -------
    trackframe : LabelFrame  
            Placed in main window.
            Holds all other widgets in this class
    track_name : Label 
        displaying name of sample
    track_status : Label 
        displaying status of selected sample 
    '''
    def __init__(self, mp):
        '''
        Constructor called by MusicPlayer class

        Parameters
        ----------
        mp: MusicPlayer object
        '''
        label_frame_args = {
            "text": "Sample",
            "font": ("Terminal", 16),
            "bg": COLOR_LIGHT_PURPLE, 
            "fg": COLOR_WHITE,
            "bd": 5,
            "relief": FLAT,
        }
        trackframe = LabelFrame(mp.root, **label_frame_args)
        trackframe.place(x=0, y=0, width=600, height=100)
        
        # Inserting Song Track Label
        track_name_args = {
            "textvariable": mp.track,
            "width": 35,
            "font": ("Fixedsys", 18),
            "bg": COLOR_BRIGHT_PINK,
            "bd": 5,
            "fg": COLOR_NEON_GREEN,
            "relief":RIDGE,
            "padx": 5,
            "pady": 10
        }
        track_name = Label(trackframe, **track_name_args)

        # organizing in grid of 'trackframe'
        track_name.grid(row=1, column=1, padx=5, pady=5)
        


        
class playlist_frame:
    
    def __init__(self, mp):
        songs_frame_args = {
            "text": "Loaded Samples",
            "font": ("Terminal", 15),
            "bg": COLOR_LIGHT_PURPLE,
            "fg": COLOR_WHITE,
            "bd": 5,
            "relief": FLAT,
        }
        
        songsframe = LabelFrame(mp.root, **songs_frame_args)
        songsframe.place(x=600, y=0, width=400, height=275)

        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        scrol_x = Scrollbar(songsframe, orient=HORIZONTAL)

        # Inserting Playlist listbox
        playlist_args = {
            "yscrollcommand": scrol_y.set,
            "xscrollcommand": scrol_x.set,
            "selectbackground": COLOR_NEON_GREEN,
            "selectforeground": COLOR_HOT_PINK,
            "selectmode": SINGLE,
            "font": ("Terminal", 12, "bold"),
            "bg": COLOR_GRAYISH_GREEN,
            "fg": COLOR_DEEP_PURPLE,
            "bd": 5,
            "relief": GROOVE,
            "height": 50,
        }
        mp.playlist = Listbox(songsframe, **playlist_args)
        mp.playlist.bind("<<ListboxSelect>>", mp.on_listbox_select)
        #mp.playlist.bind("<Double-1>", mp.on_double_click)
        # Applying Scrollbars to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=mp.playlist.yview)
        scrol_x.pack(side=BOTTOM, fill=X)
        scrol_x.config(command=mp.playlist.xview)
        mp.playlist.pack(fill=BOTH)
        # Changing Directory for fetching Songs
        # make this the song folder in your directory
        curr_dir = os.getcwd()
        os.chdir("./digital-sampler/sounds")

        # Fetching Songs
        songtracks = os.listdir()
        #print(f"songtracks: {songtracks}\n")
        # Inserting Songs into Playlist
        mp.songs = []
        for track in songtracks:
            mp.user_songs[track] = convertAudioFile(track)
            mp.songs.append(track)
            mp.playlist.insert(END, track)
        os.chdir(curr_dir)
        
class MusicPlayer:

    _visualizer : DbMeter
    _spectogram: FRDiagam
    _channel : Channel
    _timeline : Timeline
    def __init__(self, root):

        self.root = root
        # Title of the window
        self.root.title("Beats by L35")
        # Window Geometry
        self.root.geometry("1000x775+25+25") #plus values are coordinates where window opens on user's screen
        ico = PhotoImage(file = "./digital-sampler/photos/scottyBOYYYYYYYYYYYY.png")
        root.wm_iconphoto(False, ico)
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()

        self._channel = Channel(1)
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()
        self.status.set("--")  # default status is empty
        # Declaring Effects Variable - TODO - change effect label for each effect
        self.effects = StringVar()
        self.effects.set("(0, 0, 0, 0)")  # default

        self.reverb_vals_label = StringVar()
        self.reverb_vals_label.set("(0, 0, 0, 0)")

        self.distortion_vals_label = StringVar()
        self.distortion_vals_label.set("(0)")

        self.delay_vals_label = StringVar()
        self.delay_vals_label.set("(0, 0, 0)")

        self.chorus_vals_label = StringVar()
        self.chorus_vals_label.set("(0, 0, 0, 0)")

        self.connected = False

        #variables to hold for each dial that can be used to re-establish dial states
        #default is 0 for all
        #TODO - each window will have separate saved values - these are only for the delay window which currently adjusts all effects 
        # for debugging purposes
        self.reverbVal = 0
        self.delayVal = 0
        self.chorusVal = 0
        self.distortionVal = 0
        self.key_bindings = {}
        
        #storing reverb vals 
        #storing delay vals
        #storing chorus vals
        #storing distortion vals


        #===============================================#
        timeline = Timeline()

        # ============= Creating the Track Frame for Song label & status label =========
        track_frame(self)
        
        #dictionary for user songs
        self.user_songs = {}
        # ======================== Creating Button Frame =============================
        self.bf = btn_frame(self)
        # ===================== Creating Pad Frame ===========================
        self.drumpad = drumpad(self)
        # ======================== Playlist Frame ===========================
        playlist_frame(self)

        self.create_menu()


        #===============================================#
        self._timeline = Timeline()
        self._timeline.commit(**self.user_songs)

        self.root.bind_all("<Control-y>", self.redo)
        self.root.bind_all("<Control-z>", self.undo)


    def redo(self, _):
        '''
        Timeline helper function
        Tied to Control Y
        
        Restores the next future version of the user_songs dictionary'''
        self._timeline.redo()
        redo_state = self._timeline.peek()

        self.playlist.delete(0, END)
        self.user_songs = redo_state

        for song in self.user_songs:
            self.playlist.insert(END, song)
        
    
    def undo(self, _):
        '''
        Timeline helper function
        Tied to Control Z

        Restores the previous version of the user_songs dictionary
        '''
        self._timeline.undo()
        undo_state = self._timeline.peek()
        
        self.playlist.delete(0, END)

        self.user_songs = undo_state
        for song in self.user_songs:
            self.playlist.insert(END, song)



    def create_menu(self) :

        menubar = Menu(self.root)

        # File import and export as drop down menus
        File = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = 'File', menu = File)
        File.add_command(label = 'Import', command = self.add_song)
        File.add_command(label = 'Export', command = self.export)

        # Database library access
        Library = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = 'Library', menu = Library)
        Library.add_command(label = 'Open', command = self.create_db_window)

        # Serial port device access
        Devices = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = 'Devices', menu = Devices)
        Devices.add_command(label = 'Connect', command = self.connect_to_serial)
        Devices.add_command(label = 'Disconnect', command = self.disconnect_from_serial)

        self.root.config(menu = menubar)


    def connect_to_serial(self):
        #print(self.connected)
    
        if not self.connected:
            port = simpledialog.askstring("COM Select", "Enter the serial port to connect to: ")
            self.com = SerialMonitor(drumpad = self.drumpad, port = port)
            self.connected = True


    def disconnect_from_serial(self):
        #print(self.connected)

        if self.connected:
            self.com.close()
            self.connected = False
            del self.com

        

    def play_new_song(self):
        #print("in play_new_song")
        self._channel.stop()
        song_to_play = self.playlist.get(self.playlist.curselection())
        self.track.set(song_to_play)
        self.status.set("--Playing")
        if song_to_play in self.user_songs.keys():
            self.user_songs[song_to_play].seek(0)
            song = copy.copy(self.user_songs[song_to_play])
            self._channel = Sound(song).play()
            self._channel.set_volume(self._volume)
            
            self._visualizer.assign(AudioFile(copy.copy(self.user_songs[song_to_play])), 0)
            self._visualizer.freeze(0)
            self._spectogram.assign(AudioFile(copy.copy(self.user_songs[song_to_play])), 0)
            self._spectogram.freeze(0)
            
        self.bf.play_img_btn.config(text="||")
        
    def play_pause(self):
        #print("in play_pause")
        if self.status.get() == "--":
            song_to_play = self.playlist.get(ACTIVE)
            self.track.set(song_to_play)
            self.status.set("--Playing")
            if song_to_play in self.user_songs.keys():
                try:
                    # Make a copy of the song to play so it doesn't get closed
                    song = copy.copy(self.user_songs[song_to_play])
                    self._channel = Sound(song).play()
                    self._channel.set_volume(self._volume)
                    self._visualizer.assign(copy.copy(self.user_songs[song_to_play]), 0)
                    self._visualizer.freeze(0)
                    self._spectogram.assign(copy.copy(self.user_songs[song_to_play]), 0)
                    self._spectogram.freeze(0)
                except pygame.error:
                    messagebox.showinfo("Info", "File Not Found")
            self.bf.play_img_btn.config(text="||")
            return    
        elif self.status.get() == "--Paused":
            self.status.set("--Playing")
            # Playing back Song
            self.bf.play_img_btn.config(text="||")
            self._visualizer.freeze(0)
            self._spectogram.freeze(0)
            self._channel.unpause()
            return
        elif self.status.get() == "--Playing":
            self.status.set("--Paused")
            # Paused Song
            self.bf.play_img_btn.config(text=">")
            self._visualizer.freeze(0)
            self._spectogram.freeze(0)
            self._channel.pause()
            return
            
        # Loading Selected Song

    def add_song(self):
        #print(self.songs)
        file_path = filedialog.askopenfilename(
            initialdir="./digital-sampler/songs",
            title="Select file",
            filetypes=(("Audio Files", ["*.mp3", "*.wav", "*.flac"]), ("mp3 files", "*.mp3"), ("wav files", "*.wav"), ("flac files", "*.flac"))
        )

        #print(file_path)
        if file_path:
            song_name = simpledialog.askstring("Song Name", "Enter a name for your sound: ")
            if song_name:
                song_bytes = convertAudioFile(file_path)
            else:
                messagebox.showerror("Failed to add Song", "No Name Given")
        else:
            messagebox.showerror("Failed to add Song", "No file selected")
        #dictionary of the user-named songs as keys and their corresponding file_paths as values
        self.user_songs[song_name] = song_bytes # TODO: try replicating this bug
        self.playlist.insert(END, song_name)
        
    def on_listbox_select(self, event):
        selected_item = self.playlist.get(self.playlist.curselection())
        self.play_new_song()
    
    def on_bind_btn_click(self):
        #selected_item = self.playlist.get(self.playlist.curselection())
        selection = self.playlist.get(self.playlist.curselection())

        
        
        
        new_window = Toplevel()
        new_window.geometry("200x200+1025+50")
        #new_window.geometry(f"+{event.widget.winfo_rootx() + event.widget.winfo_width()}+{event.widget.winfo_rooty()}")
        new_window.title(selection)
        #print(f"geometry: {new_window.winfo_reqwidth()} x {new_window.winfo_reqheight()} ")
        
        
        
        options_frame = LabelFrame(new_window, text="Options", bg = COLOR_LIGHT_PURPLE, fg= COLOR_WHITE, bd=5, relief=RIDGE)
        options_frame.place(x=0, y = 0, width=200, height=200)
        
        
        
        window_btn_args = {
            "width": 10,
            "height": 2,
            "font": ("Terminal", 12, "bold"),
            "fg": ds.COLOR_DEEP_PURPLE,
            "bg": ds.COLOR_LAVENDER,
            "relief": ds.RIDGE,
        }
        
        #export_button = Button(options_frame, text="Export", **window_btn_args )
        bind_to_key_button = Button(options_frame, text="Choose Key", **window_btn_args, command= lambda: self.bind_to_key(parent=new_window, selection=selection))
        #export_button.grid(row=0, column=0, padx=10, pady=10)
        bind_to_key_button.grid(row=1, column=0, padx=10, pady=10)
    
    
    def bind(self, key, sound, window, parent):
        #print(f"binding key {key} to sound {sound}")
        self.key_bindings[key] = sound
        messagebox.showinfo("Info", f"Key {key} has been bounded to sound {sound}")
        window.destroy()
        parent.destroy()
    
    def bind_to_key(self, parent, selection):
        #print("In bind_to_key")
        new_window = Toplevel()
        new_window.geometry("200x200+1025+50")
        options_frame = LabelFrame(new_window, text="Select from the available keys: ", bg = COLOR_LIGHT_PURPLE, fg= COLOR_WHITE, bd=5, relief=RIDGE)
        options_frame.place(x=0, y = 0, width=200, height=200)
        row = 0
        col = 0
        
        
        for key in self.key_bindings:
            if self.key_bindings[key] == None:
                key_btn_args = {
                    "text": key,
                    "height": 2,
                    "width": 2,
                    "command": lambda key=key: self.bind(key=key, sound=selection, window=new_window, parent = parent),
                }
                key_btn = Button(options_frame, **key_btn_args)
                key_btn.grid(row=row, column=col)
            col += 1
            if col == 4:
                col = 0
                row += 1
            if row == 4:
                break
        
        
    def adjust_volume(self, var):
        self._volume = float(var)/100
        self._channel.set_volume(self._volume)

    def create_delay_window(self):
        global delay_window
        delay_window = Toplevel(self.root)
        delay_window.title("DELAY")
        delay_window.geometry("850x775+1025+25")
        delay_frame(window=delay_window, mp=self)

    def create_reverb_window(self):
        global reverb_window
        reverb_window = Toplevel(self.root)
        reverb_window.title("REVERB")
        reverb_window.geometry("850x775+1025+25")
        reverb_frame(window=reverb_window, mp=self)

    def create_chorus_window(self):
        global chorus_window
        chorus_window = Toplevel(self.root)
        chorus_window.title("CHORUS")
        chorus_window.geometry("850x775+1025+25")
        chorus_frame(window=chorus_window, mp=self)

    def create_distortion_window(self):
        global distortion_window
        distortion_window = Toplevel(self.root)
        distortion_window.title("DISTORTION")
        distortion_window.geometry("850x775+1025+25")
        distortion_frame(window=distortion_window, mp=self)
    
    def create_db_window(self):
        global dbwin
        dbwin = Toplevel(self.root)
        DBWindow(root = dbwin, mp = self)


    # ==================== Function for Collecting Dial Values =============

        
    def apply_reverb(self):
        self._channel.stop()
        reverb_vals = [self.reverbEffectsList[i].get() for i in range(len(self.reverbEffectsList))]
        self.reverb_vals_label.set(f"({int(reverb_vals[0])}, {int(reverb_vals[1])}, {int(reverb_vals[2])}, {int(reverb_vals[3])})")
        #send call to backend
        file_out = createReverbPedalboard(reverb_vals, self.user_songs[self.playlist.get(ACTIVE)])
        self.user_songs[self.playlist.get(ACTIVE)] = file_out
        self._timeline.commit(**self.user_songs)


    def export(self):
        self._channel.stop()
        file = filedialog.asksaveasfilename(initialdir= "./../output", defaultextension='.mp3', filetypes=(("mp3 files", ".mp3"), ("wav files", ".wav"), ("flac files", ".flac")))
        bytes = self.user_songs[self.playlist.get(ACTIVE)]
        #print(file)
        export(file,bytes)

    def apply_distortion(self):
        self._channel.stop()
        distortion_vals = [self.distortionEffectsList[i].get() for i in range(len(self.distortionEffectsList))]
        self.distortion_vals_label.set(f"({int(distortion_vals[0])})")
        #send call to backend
        file_out = createDistortionPedalboard(distortion_vals, self.user_songs[self.playlist.get(ACTIVE)])
        self.user_songs[self.playlist.get(ACTIVE)] = file_out
        self._timeline.commit(**self.user_songs)


    def apply_delay(self):
        self._channel.stop()
        delay_vals = [self.delayEffectsList[i].get() for i in range(len(self.delayEffectsList))]
        self.delay_vals_label.set(f"({int(delay_vals[0])}, {int(delay_vals[1])}, {int(delay_vals[2])})")
        #send call to backend
        file_out = createDelayPedalboard(delay_vals, self.user_songs[self.playlist.get(ACTIVE)])
        self.user_songs[self.playlist.get(ACTIVE)] = file_out
        self._timeline.commit(**self.user_songs)

        
    def apply_chorus(self):
        self._channel.stop()
        chorus_vals = [self.chorusEffectsList[i].get() for i in range(len(self.chorusEffectsList))]
        self.chorus_vals_label.set(f"({int(chorus_vals[0])}, {int(chorus_vals[1])}, {int(chorus_vals[2])}, {int(chorus_vals[3])})")
        #send call to backend
        file_out = createChorusPedalboard(chorus_vals, self.user_songs[self.playlist.get(ACTIVE)])
        self.user_songs[self.playlist.get(ACTIVE)] = file_out
        self._timeline.commit(**self.user_songs)
