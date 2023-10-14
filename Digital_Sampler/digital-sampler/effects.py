from . import digitalSampler as ds

class delay_frame:
    '''
    Contains the components to be placed
    in a separate window, which is passed in when
    constructing a delay_frame. The widgets in this class
    are manipulated to apply desired delay effects to a sample.

    Widgets
    -------
    df : ds.LabelFrame
        frame containing all other components of this class
    reverb_dial :
    ''' 
    def __init__(self, window, mp):
        '''
        Constructor called by MusicPlayer class

        Parameters
        ----------
        mp : MusicPlayer
        window : Toplevel 
            the window where the components of this class
            will be placed/gridded
        '''
        df_args = {
            "text": "Echolocation-DELAY",
            "fg":ds.COLOR_DEEP_BLUE,
            "font":("Terminal", 24),
            "bd":7,
            "relief": ds.FLAT,
            "bg": ds.COLOR_BRIGHT_PINK, 
        }
       
        df = ds.LabelFrame(window, **df_args)
        df.place(x=0, y=0, width=900, height=775)

        # ----------- Dials for ds.Dial Frame ----------
        dial_args = {
            "start": 0,
            "end": 100,
            "text_color": ds.COLOR_DEEP_PURPLE,
            "color_gradient": (ds.COLOR_MINT, ds.COLOR_CYAN),
            "bg": ds.COLOR_BRIGHT_PINK,
            "needle_color": ds.COLOR_DEEP_PURPLE,
            "unit_width": 5,
            "unit_length": 7,
            "unit_color": ds.COLOR_DEEP_BLUE,
            "radius": 50,
            "scroll_steps": 5
        }
        
        delay_time_dial = ds.Dial(df, text="Delay Time: ", **dial_args)
        delay_feedback_dial = ds.Dial(df, text="Feedback: ", **dial_args)
        delay_drywet_dial = ds.Dial(df, text="Dry/Wet: ", **dial_args)

        DEFAULT_DRY_VALUE: int = 50
        delay_drywet_dial.set(DEFAULT_DRY_VALUE)
        
        # list with each dial - used for keeping track of dial values
        mp.delayEffectsList = [delay_time_dial, delay_feedback_dial, delay_drywet_dial]

        # label showing the recorded
        # values in all dials when 'Apply Effects' button is clicked
        effects_vars_label_args = {
            "textvariable": mp.delay_vals_label,
            "font": ("Terminal", 12, "bold"),
            "bd": 5,
            "bg": ds.COLOR_BRIGHT_PINK,
            "fg": ds.COLOR_DEEP_PURPLE,
            "relief": ds.SUNKEN
        }
        delay_vars_label = ds.Label(df, **effects_vars_label_args)
        
        apply_btn_args = {
            "text": "Apply Delay",
            "command": mp.apply_delay,
            "font": ("Terminal", 16, "bold"),
            "fg": ds.COLOR_DEEP_PURPLE,
            "bg": ds.COLOR_LAVENDER,
            "bd": 3,
            "padx": 50,
            "pady": 25
        }
        apply_delay_btn = ds.Button(df, **apply_btn_args)

        #creating image label inside dial frame
        delay_img_label = ds.Label(df, image=ds.delay_img)
        
        # organizing in grid of dial frame (df)
        delay_time_dial.grid(row=0, column=0, padx=30, pady=15)
        delay_feedback_dial.grid(row=0, column=1, padx=30, pady=15)
        delay_drywet_dial.grid(row=1, column=0, padx=30, pady=15, columnspan=2)

        # padding for button on outside of button goes here
        apply_delay_btn.grid(row=2, column=0, columnspan=2, padx=15, pady=25)
        delay_vars_label.grid(row=3, column=0, columnspan=2, padx=5, pady=15)
        delay_img_label.grid(row=0, column=2, rowspan=4)
        
class reverb_frame:
    def __init__(self, window, mp):
        df_args = {
            "text": "Desolate-Warehouse-REVERB",
            "fg": ds.COLOR_DEEP_BLUE,
            "font":("Terminal", 24),
            "bd":7,
            "relief":ds.FLAT,
            "bg": ds.COLOR_BRIGHT_PINK, 
        }
       
        df = ds.LabelFrame(window, **df_args)
        df.place(x=0, y=0, width=900, height=775)

        # ----------- Dials for ds.Dial Frame ----------
        dial_args = {
            "start": 0,
            "end": 100,
            "text_color": ds.COLOR_DEEP_PURPLE,
            "color_gradient": (ds.COLOR_MINT, ds.COLOR_CYAN),
            "bg": ds.COLOR_BRIGHT_PINK,
            "needle_color": ds.COLOR_DEEP_PURPLE,
            "unit_width": 5,
            "unit_length": 7,
            "unit_color": ds.COLOR_DEEP_BLUE,
            "radius": 50,
            "scroll_steps": 5
        }
        
        reverb_roomsize_dial = ds.Dial(df, text="Room Size: ", **dial_args)
        reverb_damping_dial = ds.Dial(df, text="Damping: ", **dial_args)
        reverb_dry_dial = ds.Dial(df, text="Dry: ", **dial_args)
        reverb_wet_dial = ds.Dial(df, text="Wet: ", **dial_args)

        # TODO move these up top to the constants section
        DEFAULT_DRY_VALUE: int = 50
        DEFAULT_WET_VALUE: int = 50
        reverb_dry_dial.set(DEFAULT_DRY_VALUE)
        reverb_wet_dial.set(DEFAULT_WET_VALUE)

        # list with each dial - used for keeping track of dial values
        mp.reverbEffectsList = [reverb_roomsize_dial, reverb_damping_dial, reverb_dry_dial, reverb_wet_dial]

        # label showing the recorded
        # values in all dials when 'Apply Effects' button is clicked
        effects_vars_label_args = {
            "textvariable": mp.reverb_vals_label,
            "font": ("Terminal", 12, "bold"),
            "bd": 5,
            "bg": ds.COLOR_BRIGHT_PINK,
            "fg": ds.COLOR_DEEP_PURPLE,
            "relief": ds.FLAT
        }
        effect_vars_label = ds.Label(df, **effects_vars_label_args)
        
        apply_btn_args = {
            "text": "Apply Reverb",
            "command": mp.apply_reverb,
            "font": ("Terminal", 16, "bold"),
            "fg": ds.COLOR_DEEP_PURPLE,
            "bg": ds.COLOR_LAVENDER,
            "bd": 3,
            "padx": 50,
            "pady": 25
        }
        apply_reverb_btn = ds.Button(df, **apply_btn_args)

        #creating image label inside dial frame
        reverb_img_label = ds.Label(df, image=ds.reverb_img)
        
        # organizing in grid of dial frame (df)
        reverb_roomsize_dial.grid(row=0, column=0, padx=30, pady=15)
        reverb_damping_dial.grid(row=0, column=1, padx=30, pady=15)
        reverb_dry_dial.grid(row=1, column=0, padx=30, pady=15)
        reverb_wet_dial.grid(row=1, column=1, padx=30, pady=15)
        # padding for button on outside of button goes here
        apply_reverb_btn.grid(row=2, column=0, columnspan=2, padx=15, pady=25)
        effect_vars_label.grid(row=3, column=0, columnspan=2, padx=5, pady=15)
        reverb_img_label.grid(row=0, column=2, rowspan=4)
        
class chorus_frame:
    def __init__(self, window, mp):
        df_args = {
            "text": "Church-Choir-CHORUS",
            "fg":ds.COLOR_DEEP_BLUE,
            "font":("Terminal", 24),
            "bd":7,
            "relief":ds.FLAT,
            "bg":ds.COLOR_BRIGHT_PINK, 
        }
       
        df = ds.LabelFrame(window, **df_args)
        df.place(x=0, y=0, width=900, height=775)

        # ----------- Dials for ds.Dial Frame ----------
        dial_args = {
            "start": 0,
            "end": 100,
            "text_color": ds.COLOR_DEEP_PURPLE,
            "color_gradient": (ds.COLOR_MINT, ds.COLOR_CYAN),
            "bg": ds.COLOR_BRIGHT_PINK,
            "needle_color": ds.COLOR_DEEP_PURPLE,
            "unit_width": 5,
            "unit_length": 7,
            "unit_color": ds.COLOR_DEEP_BLUE,
            "radius": 50,
            "scroll_steps": 5
        }
        
        chorus_rate_dial = ds.Dial(df, text="Rate: ", **dial_args)
        chorus_depth_dial = ds.Dial(df, text="Depth: ", **dial_args)
        chorus_feedback_dial = ds.Dial(df, text="Feedback: ", **dial_args)
        chorus_drywet_dial = ds.Dial(df, text="Dry/Wet: ", **dial_args)

        DEFAULT_DRY_VALUE: int = 50
        chorus_drywet_dial.set(DEFAULT_DRY_VALUE)

        # list with each dial - used for keeping track of dial values
        mp.chorusEffectsList = [chorus_rate_dial, chorus_depth_dial, chorus_feedback_dial, chorus_drywet_dial]

        # label showing the recorded
        # values in all dials when 'Apply Effects' button is clicked
        effects_vars_label_args = {
            "textvariable": mp.chorus_vals_label,
            "font": ("Terminal", 12, "bold"),
            "bd": 5,
            "bg": ds.COLOR_BRIGHT_PINK,
            "fg": ds.COLOR_DEEP_PURPLE,
            "relief": ds.FLAT
        }
        effect_vars_label = ds.Label(df, **effects_vars_label_args)
        
        apply_btn_args = {
            "text": "Apply Chorus",
            "command": mp.apply_chorus,
            "font": ("Terminal", 16, "bold"),
            "fg": ds.COLOR_DEEP_PURPLE,
            "bg": ds.COLOR_LAVENDER,
            "bd": 3,
            "padx": 50,
            "pady": 25
        }
        apply_chorus_btn = ds.Button(df, **apply_btn_args)

        #creating image label inside dial frame
        chorus_img_label = ds.Label(df, image=ds.chorus_img)
        
        # organizing in grid of dial frame (df)
        chorus_rate_dial.grid(row=0, column=0, padx=30, pady=15)
        chorus_depth_dial.grid(row=0, column=1, padx=30, pady=15)
        chorus_feedback_dial.grid(row=1, column=0, padx=30, pady=15)
        chorus_drywet_dial.grid(row=1, column=1, padx=30, pady=15)
        # padding for button on outside of button goes here
        apply_chorus_btn.grid(row=2, column=0, columnspan=2, padx=15, pady=25)
        effect_vars_label.grid(row=3, column=0, columnspan=2, padx=5, pady=15)
        chorus_img_label.grid(row=0, column=2, rowspan=4)
        
class distortion_frame:
    def __init__(self, window, mp):
        df_args = {
            "text": "Inconvenient-Headache-DISTORTION",
            "fg": ds.COLOR_DEEP_BLUE,
            "font":("Terminal", 24),
            "bd":7,
            "relief":ds.FLAT,
            "bg":ds.COLOR_BRIGHT_PINK, 
        }
       
        df = ds.LabelFrame(window, **df_args)
        df.place(x=0, y=0, width=900, height=775)

        # ----------- Dials for ds.Dial Frame ----------
        dial_args = {
            "start": 0,
            "end": 100,
            "text_color": ds.COLOR_DEEP_PURPLE,
            "color_gradient": (ds.COLOR_MINT, ds.COLOR_CYAN),
            "bg": ds.COLOR_BRIGHT_PINK,
            "needle_color": ds.COLOR_DEEP_PURPLE,
            "unit_width": 5,
            "unit_length": 7,
            "unit_color": ds.COLOR_DEEP_BLUE,
            "radius": 150,
            "scroll_steps": 5
        }
        
        distortion_drive_dial = ds.Dial(df, text="Drive: ", **dial_args)
        

        # list with each dial - used for keeping track of dial values
        mp.distortionEffectsList = [distortion_drive_dial]

        # label showing the recorded
        # values in all dials when 'Apply Effects' button is clicked
        effects_vars_label_args = {
            "textvariable": mp.distortion_vals_label,
            "font": ("Terminal", 12, "bold"),
            "bd": 5,
            "bg": ds.COLOR_HOT_PINK,
            "fg": ds.COLOR_DEEP_PURPLE,
            "relief": ds.FLAT
        }
        effect_vars_label = ds.Label(df, **effects_vars_label_args)
        
        apply_btn_args = {
            "text": "Apply Distortion",
            "command": mp.apply_distortion,
            "font": ("Terminal", 16, "bold"),
            "fg": ds.COLOR_DEEP_PURPLE,
            "bg": ds.COLOR_LAVENDER,
            "bd": 3,
            "padx": 50,
            "pady": 25
        }
        apply_distortion_btn = ds.Button(df, **apply_btn_args)

        #creating image label inside dial frame
        distortion_img_label = ds.Label(df, image=ds.distortion_img)
        
        # organizing in grid of dial frame (df)
        distortion_drive_dial.grid(row=0, column=0, padx=30, pady=15)
        # padding for button on outside of button goes here
        apply_distortion_btn.grid(row=2, column=0, columnspan=2, padx=15, pady=25)
        effect_vars_label.grid(row=3, column=0, columnspan=2, padx=5, pady=15)
        distortion_img_label.grid(row=0, column=2, rowspan=4)