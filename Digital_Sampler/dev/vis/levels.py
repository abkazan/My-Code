import math
import tkinter as tk
from time import time_ns
from typing import NoReturn

import numpy as np
from pedalboard.io import AudioFile

NUMBER_CHANNELS: int = 1 << 4  # 16 channelss

# overall component dimensions
NATIVE_WIDTH: int = 404
NATIVE_HEIGHT: int = 1172

# control where 0 db is displayed. 0 -> no clip levels displayed
REL_ZERO_DB: int = 0.25

# style dicts to quickly color shapes
# 2nd grays are lighter than their 1st gray counterparts
LIGHT_GREEN: dict = {'fill': '#a5de1a', 'outline': ''}
LIGHT_ORANGE: dict = {'fill': '#f9c228', 'outline': ''}
GRAY_1: dict = {'fill': '#2d373e', 'outline': ''}
GRAY_2: dict = {'fill': '#3c464d', 'outline': ''}
BLUE_GRAY_1: dict = {'fill': '#40555d', 'outline': ''}
BLUE_GRAY_2: dict = {'fill': '#8599a1', 'outline': ''}

LABEL_HEIGHT: float = 0.03
LABEL_WIDTH: float = 0.3
LABEL_SPACING: float = 0.10

LEFT_BAR_START: float = 0.4
RIGHT_BAR_START: float = 0.7

BAR_DECAY: float = 0.013

CAP_HEIGHT: float = 0.004
CAP_DECAY: float = 0.005


class DbMeter(tk.Canvas):
    '''
    A custom tkinter.Canvas that displays the levels of an audio 
    file    
    '''
    
    class __Channel:
        '''Track the audio file and data in each channel'''
        
        audio: AudioFile
        t_requested: float
        frozen: bool
        frame_num: int
    
        def __init__(self, audio: AudioFile):
            '''Populate a Channel object. For internal use only'''
            self.audio = audio
            self.t_requested = None
            self.frozen = True
            self.frame_num = 0
            

    def __init__(self, master: tk.Misc | None = None, __scale: float = 0.5,
                 *args, **kwargs):
        '''
        Initialize a new levels meter

        This method works the same as a tkinter.Canvas.__init__ with 
        the exception that you cannot spec the width or height. If you 
        do, they will be overridden.

        Parameters
        ----------
        master : tk.Misc | None
            The root of this component. Default is None.
        __scale : float
            The relative size of this component. Default is 0.5.

        Examples
        --------
        >>> import tkinter as tk
        >>> from vis import DbMeter
        >>> meter = DbMeter(tk.Tk())

        '''

        # README: this method is REALLY long because it is creating lots
        # of custom shape elements that need to be set ONCE. please do
        # not move the draw calls to sub methods; it will just make
        # drawing things in the correct order harder...

        # get overall scaling
        if kwargs.get('__scale'):
            __scale = kwargs['__scale']
            del kwargs['__scale']

        # create canvas
        self.__width = NATIVE_WIDTH * __scale
        self.__height = NATIVE_HEIGHT * __scale
        kwargs['width'] = self.__width
        kwargs['height'] = self.__height
        super().__init__(master, *args, **kwargs)

        # track volume
        self.left_volume: float = 0
        self.right_volume: float = 0
        
        self.right_cap_lvl: float = 0
        self.left_cap_lvl: float = 0

        # track the channels    
        self.__channels: list[self.__Channel] = [None] * NUMBER_CHANNELS

        # draw all the elements. to people looking to update this
        # section, please make sure you are drawing the elements in the
        # correct order. elements defined later will be drawn on top of
        # all previous elements. there are a lot of magic numbers in
        # this section just to spec how things look. they don't affect
        # the function of the meter, and COULD be put into constants if
        # you'd like

        # REFFERENCE https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/img_plug/dbmeter.png

        # background and sidebar
        self.create_rectangle(*self._get_abs(0, 0, 1, 1), **GRAY_2)
        self.create_rectangle(*self._get_abs(0, 0, 0.4, 1), **BLUE_GRAY_1)

        # draw ticks and labels
        for i in range(-10, 10):

            # lable's y values all in relative coords
            y_mid = REL_ZERO_DB + i * LABEL_SPACING
            y_top = y_mid - LABEL_HEIGHT / 2
            y_bot = y_mid + LABEL_HEIGHT / 2

            # decible label's background
            self.create_rectangle(
                *self._get_abs(0, y_top, LABEL_WIDTH, y_bot),
                **BLUE_GRAY_2,
            )

            # calculate decibles
            lvl = 1 - (y_mid - REL_ZERO_DB)
            db = -math.inf
            if lvl > 0:
                db = int(40 * math.log(lvl))

            # write out decibles (label)
            self.create_text(
                LABEL_WIDTH / 2 * self.__width,
                y_mid * self.__height,
                text=f'{"+" if db > 0 else ""}{db}',
                fill='black',
            )

            # draw major tick at label
            self.create_line(
                *self._get_abs(LABEL_WIDTH + 0.05, y_mid, 0.4, y_mid),
                fill=BLUE_GRAY_2['fill'],
                width=2,
            )

            # draw 5 (really it's 4) subticks
            for j in range(5):
                y_sub = y_mid + j * LABEL_SPACING / 5
                self.create_line(
                    *self._get_abs(LABEL_WIDTH + 0.075, y_sub, 0.4, y_sub),
                    fill=BLUE_GRAY_2['fill'],
                    width=1,
                )

        # create and track the bars (level displays)
        # list layout = [left norm, left clip, right norm, right clip]
        self.__bars = [None] * 4

        # clipped bars first for correct draw order
        # left channel clipped
        self.__bars[1] = self.create_rectangle(
            *self._get_abs(LEFT_BAR_START, 0, RIGHT_BAR_START, 1),
            **LIGHT_ORANGE,
        )
        # right channel clipped
        self.__bars[3] = self.create_rectangle(
            *self._get_abs(RIGHT_BAR_START, 0, 1, 1),
            **LIGHT_ORANGE,
        )
        # left channel unclipped
        self.__bars[0] = self.create_rectangle(
            *self._get_abs(LEFT_BAR_START, REL_ZERO_DB, RIGHT_BAR_START, 1),
            **LIGHT_GREEN,
        )
        # right channel unclipped
        self.__bars[2] = self.create_rectangle(
            *self._get_abs(RIGHT_BAR_START, REL_ZERO_DB, 1, 1),
            **LIGHT_GREEN,
        )

        #TODO for a different day...
        #create and track caps
        self.__caps = [None] * 2
        self.__caps[0] = self.create_rectangle(
            *self._get_abs(
                LEFT_BAR_START,
                1 - CAP_HEIGHT / 2,
                RIGHT_BAR_START,
                1 + CAP_HEIGHT / 2
                ),
            **LIGHT_ORANGE
            )
        self.__caps[1] = self.create_rectangle(
            *self._get_abs(
                RIGHT_BAR_START,
                1 - CAP_HEIGHT / 2,
                1,
                1 + CAP_HEIGHT / 2),
            **LIGHT_ORANGE
            )

        # vertical line seperating channels
        self.create_line(
            *self._get_abs(0.7, 0, 0.7, 1.1),
            fill=GRAY_1['fill'],
            width=4,
        )

        # launch display loop
        self._update_display()

    def _update_volumes(self):
        '''
        Update the volume fields for this object

        Do not call this function, it will be called for you.
        '''
        
        prev_vol_left = self.left_volume
        prev_vol_right = self.right_volume
        
        self.left_volume = 0
        self.right_volume = 0
        
        for i, chan in enumerate(self.__channels):
            
            # no meta, not playing
            if chan is None or chan.frozen or chan.t_requested is None:
                continue
            
            # how long since the request?
            secs = time_ns() / 1_000_000_000.0
            delta = secs - chan.t_requested

            # check for completion
            elapsed_frames = int(chan.audio.samplerate * delta)
            if chan.audio.frames <= chan.frame_num:
                self.__channels[i] = None
                break 
            
            # get everything since we last displayed, and display the 
            # max
            chan.audio.seek(chan.frame_num)
            frame_data = chan.audio.read(elapsed_frames)
            self.left_volume += np.max(frame_data[0])
            self.right_volume += np.max(frame_data[1])

            # request to display again
            chan.frame_num += elapsed_frames
            chan.t_requested = secs
            
        if not self.left_volume and not self.right_volume:
            self.left_volume = prev_vol_left - BAR_DECAY
            self.right_volume = prev_vol_right - BAR_DECAY
            
        self.left_cap_lvl = max(self.left_cap_lvl - CAP_DECAY, self.left_volume)
        self.right_cap_lvl = max(self.right_cap_lvl - CAP_DECAY, self.right_volume)
                        
            

    def _update_display(self):
        '''
        Update the levels displayed in this db meter

        Don't call this method. It will be called internally for you.
        '''

        self._update_volumes()

        # see https://docs.google.com/drawings/d/1hxiXEKo_MK5b-BL1-ymEVadC7wOR22N8oGeKiqpsXZk/edit?usp=sharing

        for i in range(4):
            # first two indicies are the left bars
            vol = self.left_volume if i < 2 else self.right_volume
            # second and fourth are uncapped
            vol = vol if i % 2 else min(1, vol)

            # which bar?
            id = self.__bars[i]
            
            # update the first y value to display volume
            rel_coords = self._get_rel(*self.coords(id))
            rel_coords[1] = 1 - vol * (1 - REL_ZERO_DB)
            self.coords(id, self._get_abs(*rel_coords))
            
        for i in range(2):
            # first two indicies are the left cap
            vol = self.left_cap_lvl if not i else self.right_cap_lvl
            
            # which caps?
            id = self.__caps[i]
            
            # update the first y value to display volume
            rel_coords = self._get_rel(*self.coords(id))
            rel_coords[1] = 1 - vol * (1 - REL_ZERO_DB) - CAP_HEIGHT / 2
            rel_coords[3] = 1 - vol * (1 - REL_ZERO_DB) + CAP_HEIGHT / 2
            self.coords(id, self._get_abs(*rel_coords))
                

        # update at ~ 60 tps
        self.master.after(16, self._update_display)

    def _get_abs(self, x1: float, y1: float, x2: float,
                 y2: float) -> list[float]:
        '''
        Convert relative coords into absolute coords

        Relative coords are coords given in range [0, 1]

        Parameters
        ----------
        x1 : float
            relative x coord of upper left
        y1 : float
            relative y coord of upper left
        x2 : float
            relative x coord of bottom right
        y2 : float
            relative y coord of bottom right

        Returns
        -------
        list[float] : the corresponding absolute coordinates

        Examples
        --------
        >>> # TODO

        '''
        return [
            x1 * self.__width,
            y1 * self.__height,
            x2 * self.__width,
            y2 * self.__height,
        ]

    def _get_rel(self, x1: float, y1: float, x2: float,
                 y2: float) -> list[float]:
        '''
        Convert absolute coords to relative ones

        Absolute coords for height are given in range 
        [0, self.__height], and absolute coords for width are given in 
        range [0, self.__width]

        Parameters
        ----------
        x1 : float
            absolute x coord of upper left
        y1 : float
            absolute y coord of upper left
        x2 : float
            absolute x coord of bottom right
        y2 : float
            absolute y coord of bottom right

        Returns
        -------
        list[float] : the corresponding relative coordinates

        Examples
        --------
        >>> # TODO

        '''
        return [
            x1 / self.__width,
            y1 / self.__height,
            x2 / self.__width,
            y2 / self.__height,
        ]

    def assign(self, audio: AudioFile, channel_num: int) -> None:
        '''
        Assign a channel to diplay an audio file

        Assigning an occupied channel will override previous contents. 

        Parameters
        ----------
        audio : AudioFile
            The audio file to display. 
        channel : int
            The audio channel to display in. In range 
            [0, NUMBER_CHANNELS-1].

        Examples
        --------
        '''

        if NUMBER_CHANNELS <= channel_num or channel_num < 0:
            raise ValueError(f'{channel_num = } is out of bounds')
        
        self.__channels[channel_num] = self.__Channel(audio)

    def freeze(self, channel_num: int, frozen: bool = ...):
        '''
        Toggle or set the display settings of a channel

        A frozen channel will not display any levels. When the channel
        is unfrozen, it will begin displaying where it left off. 

        Parameters
        ----------
        channel : int
            The channel to change the frozen status of
        frozen : bool
            Forcibly set the channel to frozen or not. Default value 
            toggles the status of this channel.
        '''

        if NUMBER_CHANNELS <= channel_num or channel_num < 0:
            raise ValueError(f'{channel_num = } is out of bounds')

        chan: self.__Channel = self.__channels[channel_num]

        if not chan:
            return

        # decide to toggle or force
        frozen = not chan.frozen if frozen is ... else frozen
        
        secs = time_ns() / 1_000_000_000.0
        chan.t_requested = secs

        
        chan.frozen = frozen
