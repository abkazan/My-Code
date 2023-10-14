'''
Display a frequency diagram in a tkinter app

Displays a pedalboard.io.AudioFile object
'''

import tkinter as tk
from time import time_ns

import numpy as np
from pedalboard.io import AudioFile

MIN_FREQ: int = 20
MAX_FREQ: int = 20_000

# implementation detail
LOG10_MIN_FREQ: float = np.log10(MIN_FREQ)
LOG10_MAX_FREQ: float = np.log10(MAX_FREQ)

FREQ_SAMPLES: int = 256
DISPLAYED_FREQS: list[int] = list()

for i in range(FREQ_SAMPLES):
    power = LOG10_MIN_FREQ + (LOG10_MAX_FREQ - LOG10_MIN_FREQ) * i / FREQ_SAMPLES
    freq = int(np.power(10, power))
    while freq in DISPLAYED_FREQS:
        freq += 1
    DISPLAYED_FREQS.append(freq)
    
LEFT_EDGE: float = 0.0
RIGHT_EDGE: float = 1.0

DEFAULT_HZ: int = 44_100

NATIVE_WIDTH: int = 1308
NATIVE_HEIGHT: int = 686

CHANNEL_COUNT: int = 16

# colors
C_FREQ_EDGE: str = '#778892'
C_BACKGROUND: str = '#253741'
C_GRID_LINE: str = '#32424f'
C_GRID_LINE_MINOR: str = '#2A3C47'

H_GRID_GAP: float =  1.0 / 36.0

FREQ_WINDOW: int = 1024

SPECTRAGRAM_DECAY_RATE: float = 0.01

class FRDiagam(tk.Canvas):
    '''
    A tkinter canvas that displays a frequency response diagram
    '''
    
    _audio: list[AudioFile]
    _frozen: list[bool]
    _frame: list[int]
    _freq_levels: list[int]
    _prev_time: float
    
    def __init__(self, master: tk.Misc or None = None, scale: float = 1.0, 
                 *args, **kwargs) -> None:
        '''
        Create a new displayable frequency response diagram

        Parameters
        ----------
        master : tk.Misc | None, optional
            The tkinter root, by default None
        scale : float
            positive number that multiplies the canvas size
        '''
        
        
        self.__width = NATIVE_WIDTH * scale
        self.__height = NATIVE_HEIGHT * scale
        super().__init__(master, width = self.__width, height = self.__height, 
                         *args, **kwargs)
        
        
        # initialize state, all paused no audio
        self._audio = [None] * CHANNEL_COUNT
        self._frozen = [True] * CHANNEL_COUNT
        self._frame = [0] * CHANNEL_COUNT
        self._freq_levels = np.zeros(22051)
        self._prev_time = time_ns() / 1_000_000_000
        
        # -------------------------drawing---------------------------- #
        
        # background
        self.create_rectangle(self._abs(0, 0, 1, 1), 
                              fill = C_BACKGROUND, outline= '')
            
        # gridlines vertical
        for magnitude in range(1, 5): # 1, 2, 3
            for k in range(1, 11): # 1, 2, ..., 10
                line_freq = 10 ** magnitude * k
                x = self._freq_x_pos(line_freq)
                self.create_line(self._abs(x, 0, x, 1), 
                                 fill = C_GRID_LINE)
                
        # gridlines horizontal
        for y in range(1, 36): 
            y_ = H_GRID_GAP * y
            c = C_GRID_LINE_MINOR 
            if not (y) % 6:
                c = C_GRID_LINE
                
                # dbs = 20 * np.log10(y_ * 2)
                # self.create_text(*self._abs((RIGHT_EDGE + 1) / 2, y_), 
                #              text = f'{dbs:.2} db', fill = C_FREQ_EDGE)
            
            self.create_line(self._abs(LEFT_EDGE, y_, RIGHT_EDGE, y_), fill = c)
    
        
        # draw freq spec
        points = []
        for freq in DISPLAYED_FREQS:
            x = self._freq_x_pos(freq)
            points += [x, 0]
            
        #  bottom right, bottom left
        points += [1, -3, 0, -3]
        points_abs = self._abs(*points)
        
        # freq spec
        self._freq_diag = self.create_polygon(points_abs,
            smooth = True, outline = C_FREQ_EDGE, fill = '')
        
        # launch display loop
        self._draw_frame()
    
    
    def assign(self, audio: AudioFile, channel: int) -> None:
        '''
        Assign an audio file to a display channel

        this docstring sucks lol
        
        TODO improve

        Parameters
        ----------
        audio : AudioFile
            The audio to display
        channel : int
            The channnel
        '''
        self._audio[channel] = audio
        self._frozen[channel] = True
        self._frame[channel] = 0
        
    def freeze(self, channel: int):
        '''
        Toggle the freeze status of a channel

        Nah

        Parameters
        ----------
        channel : int
            the channel
        ''' 
        self._frozen[channel] = not self._frozen[channel]

    
    def _fourier(self, signal: np.ndarray, rate: int = DEFAULT_HZ
                  ) -> np.ndarray:
        '''
        Compute the FFT audio-style

        Something something something IDK man the math just works

        Parameters
        ----------
        signal : np.ndarray
            The signal to decompose
        rate : int, optional
            The sample rate of the audio, by default DEFAULT_HZ

        Returns
        -------
        np.ndarray
            The computed frequency breakdown in decibles
        '''
        
        # for complex values (re + im*j), find (re^2 + im^2) as freq
        
        return (
            np.abs(np.fft.rfft(signal, rate)),
            np.fft.rfftfreq(FREQ_WINDOW, d = 1.0 / rate)
        )
    
    def _abs(self, *coords) -> list[float]:
        '''
        Convert relative coords to absolute coordinates

        Relative coords place 0,0 in the bottom left and 1,1 in the top
        right

        Parameters
        ----------
        coords : list[float]
            The coordinates -> x, y, x, y, ...

        Returns
        -------
        list[float]
            The absolute coordinates
        '''
        coords = list(coords)
        for i in range(len(coords)):
            if i % 2: # odd (y)
                coords[i] = (-coords[i] + 1) * self.__height
            else: # even (x)
                coords[i] *= self.__width
        return coords

        
    def _rel(self, *coords: list[float]) -> list[float]:
        '''
        Get the relative coordinate from a list of absolute coordinates

        relative coords place 0,0 in the bottom left and 1,1 in the top
        right

        Parameters
        ----------
        coords : list[float]
            The coordinates -> x, y, x, y, ...

        Returns
        -------
        list[float]
            relative coords
        '''
        coords = list(coords)
        for i in range(len(coords)):
            if i % 2: # odd (y)
                coords[i] = -(coords[i] / self.__height - 1)
            else: # even (x)
                coords[i] /= self.__width
        return coords
        
    def _freq_x_pos(self, freq: int) -> float:
        '''
        Get the relative x value to display a given frequency
        
        Based on config parameters such as MAX_FREQ, LEFT_EDGE, etc.

        Parameters
        ----------
        freq : int
            a freq in [MIN_FREQ, MAX_FREQ]

        Returns
        -------
        float
            the relative x coordinate
        '''
        
        if freq < MIN_FREQ or MAX_FREQ < freq:
            return -1
        
        log = np.log10(freq)
        
        return (log  - LOG10_MIN_FREQ) / (LOG10_MAX_FREQ - LOG10_MIN_FREQ) * \
            (RIGHT_EDGE - LEFT_EDGE) + LEFT_EDGE
    
    def _update_state(self):
        '''
        Update the internal state of the FRD

        Do not call this function, it will be called for you
        '''
        
        # elapsed time
        delta = time_ns() / 1_000_000_000 - self._prev_time
        
        # record time
        self._prev_time = time_ns() / 1_000_000_000
        
        
        prev_freq_levels = self._freq_levels
        self._freq_levels = np.zeros(22051)
        
        for chan in range(CHANNEL_COUNT):
    
            # check that we have audio
            audio = self._audio[chan]
            if not audio or self._frozen[chan]:
                continue
        
            # retrieve the audio data
            elapsed_frames = int(audio.samplerate * delta)
            
            # if the audio is exhasted, get last bit and remove
            total = self._audio[chan].frames
            exhausted = total <= (elapsed_frames + self._frame[chan])
            n_frames = FREQ_WINDOW
            if exhausted:
                n_frames = total - self._frame[chan]
            
            
            try:
                # read portion of audio
                audio.seek(max(self._frame[chan] - FREQ_WINDOW // 2, 0))
                data = audio.read(n_frames)
                self._frame[chan] = self._frame[chan] + elapsed_frames
            
            
                # remove
                if exhausted:
                    self._audio[chan] = None
                    self._frame[chan] = 0
                    self._frozen[chan] = True
                
                # transform and update levels
                four, _ = self._fourier(data[1], rate = int(audio.samplerate))

                four = four + np.full(four.shape, 0.0000001)

                self._freq_levels = np.log10(four)
                
                dd = self._freq_levels[100:10_000]

            
                # Fix for divide by 0 error
                if (np.max(dd) - np.min(dd)) == 0: 
                    pass
                else:
                    self._freq_levels = self._freq_levels * 0.2 + 0.8 * (self._freq_levels - np.min(dd)) / (np.max(dd) - np.min(dd))
            except Exception:
                pass 
        
        self._freq_levels = np.maximum(
            self._freq_levels,
            prev_freq_levels - SPECTRAGRAM_DECAY_RATE
        )
        
        
        
    def _draw_frame(self) -> None:
        '''
        Draws the frame based on internal state

        Do not call this function, it will be called internally for you
        '''
        
        self._update_state()

        # update displays
        coord_list = self.coords(self._freq_diag)
        for i in range(FREQ_SAMPLES):
            freq = DISPLAYED_FREQS[i]
            coord_list[1+i*2] = (1 - self._freq_levels[freq]/2) * \
                self.__height
            
        
        self.coords(self._freq_diag, coord_list)
        
        # # roughly 60 FPS
        self.after(16, self._draw_frame)
        