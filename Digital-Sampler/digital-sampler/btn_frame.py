from . import digitalSampler as ds
class btn_frame:
    '''
    Composed the middle left area of the main window.
    Holds all the buttons for controlling sample playback
    as well as the buttons for opening new windows to apply
    effects to the currently selected sample. This class
    also opens and sets as global the images to be used 
    in the main window as well as new windows opened by the
    commands that the buttons defined in this class specify.

    *_args : dictionaries
        hold the arguments passed into the
        ds.Button() constructor to customize the buttons
    *_args : dictionaries
        hold the arguments passed into the
        ds.Button() constructor to customize the buttons

    Widgets
    -------
    buttonframe: LabelFrame
        Frame containing all other components of this class
    self.play_img_btn : ds.Button  
        Displays either a play or pause image.
        Based on user interaction
    add_file_btn : ds.Button 
        when clicked calls mp.add_song
    add_delay_btn: ds.Button
        onclick calls mp.create_delay_window
    add_reverb_btn: ds.Button
        onclick calls mp.create_reverb_window
    add_chorus_btn: ds.Button
        onclick calls mp.create_chorus_window
    add_distortion_btn: ds.Button
        onclick calls mp.create_distortion_window
    '''
    def __init__(self, mp) -> None:
        button_frame_args = {
            "text": "Control Panel",
            "font": ("Terminal", 15),
            "bg": ds.COLOR_LIGHT_PURPLE,
            "fg": ds.COLOR_WHITE,
            "bd": 5,
            "relief": ds.RIDGE,
        }
        
        buttonframe = ds.LabelFrame(mp.root, **button_frame_args)
        buttonframe.place(x=0, y=100, width=600, height=175)

        add_effect_btn_args = {
            "width": 15,
            "height": 2,
            "font": ("Terminal", 16, "bold"),
            "fg": ds.COLOR_DEEP_PURPLE,
            "bg": ds.COLOR_LAVENDER,
            "relief": ds.RIDGE
        }

        play_pause_btn_args = {
            "width": 5,
            "height": 1,
            "font": ("Terminal", 24, "bold"),
            "fg": ds.COLOR_DEEP_PURPLE,
            "bg": ds.COLOR_LAVENDER,
            "relief": ds.RIDGE,
            "pady": 26,
            "text": ">"
        }

        '''
        #Images for play/pause
        global play_img
        play_img = PhotoImage(file = "./digital-sampler/icons/play.png")
        global pause_img
        pause_img = PhotoImage(file = "./digital-sampler/icons/pause.png")
        '''

        '''
        global images: 
        image to be used inside dial frame of new window
        images used in seperate windows must be declared global,
        and must be brought in before the new window command can be triggered.
        (i.e. - before the effects buttons that open new windows are created)
        '''
        
        ds.delay_img = ds.PhotoImage(file = "./digital-sampler/photos/dolphin.png")
        
        ds.reverb_img = ds.PhotoImage(file = "./digital-sampler/photos/warehouse.png")
        
        ds.chorus_img = ds.PhotoImage(file = "./digital-sampler/photos/churchChoir.png")
        
        ds.distortion_img = ds.PhotoImage(file = "./digital-sampler/photos/distortionMan.png")
        
        self.play_img_btn = ds.Button(buttonframe, command=mp.play_pause, **play_pause_btn_args)
        add_delay_btn = ds.Button(buttonframe, **add_effect_btn_args, command=mp.create_delay_window, text="Delay")
        add_reverb_btn = ds.Button(buttonframe, **add_effect_btn_args, command=mp.create_reverb_window, text="Reverb")
        add_chorus_btn = ds.Button(buttonframe, **add_effect_btn_args, command=mp.create_chorus_window, text="Chorus")
        add_distortion_btn = ds.Button(buttonframe, **add_effect_btn_args, command=mp.create_distortion_window, text="Distortion")
        bind_btn = ds.Button(buttonframe,fg=ds.COLOR_DEEP_PURPLE, bg=ds.COLOR_NEON_GREEN, command=mp.on_bind_btn_click , text='Bind', font=("Terminal", 12, "bold"))

        # organizing in grid of 'buttonframe'
        padding_args = {
            "padx": 4,
            "pady": 3,
        }
        
        self.play_img_btn.grid(row=0, column=0, rowspan=2, **padding_args)
        add_delay_btn.grid(row=0, column=1, **padding_args)
        add_reverb_btn.grid(row=0, column=2, **padding_args)
        add_chorus_btn.grid(row=1, column=1,  **padding_args)
        add_distortion_btn.grid(row=1, column=2, **padding_args)
        bind_btn.grid(row=0, column=3, **padding_args, rowspan=2)
        
        """_summary_
        
        #create and grid 16 buttons used for loading samples into the drum pad
        #TODO - can we make this global? this is 2nd. spot its used
        #Used for text var for each little button.
        nameList = ['1', '2', '3', '4',
                    'q', 'w', 'e', 'r',
                    'a', 's', 'd', 'f',
                    'z', 'x', 'c', 'v',]
        
        
        #frame to hold 16 little buttons inside of. This frame is inside buttonFrame
        drumpad_loader_frame = ds.LabelFrame(buttonframe, bg=ds.COLOR_SUPER_DARK_GRAY)
        #grid underneath play/pause and effects buttons
        drumpad_loader_frame.grid(row=2, column=0, columnspan=3, pady=5, padx=5)

        drumpad_loader_btn_list = []

        for i in range(16):
            drumpad_loader_btn_list.append(ds.Button(drumpad_loader_frame, text=nameList[i], font=("Terminal", 10), bg=ds.COLOR_DEEP_PURPLE, fg="red"))
            drumpad_loader_btn_list[-1].grid(pady=3, padx=8, row=0, column=i)
        """