'''
Really horrible procedural programming to show off reading in and 
writing out pedalboard AudioFiles to BytesIO objects. BytesIO objects 
are like files that live in memory. They havea a buffer that can be read 
from and written to.

This apporach enables a few things:
 - In memory files do not need to be cleaned up after the program exits
 - In memory files are faster to read and write from
 - In memory files can be easily tracked by the state manager
 
Downsides:
 - You need to rewind buffers when you read an write to them. You'll 
   see that I call the .seek(0) method a lot to send the buffer back to
   its beginning. If you do not do this, you will get all kind of crazy
   bugs. 
 - These bad boys are memory HOGS if you use .wav, .ogg, or .flac. 
   Please just stick to mid to high quality .mp3... It's honestly good 
   enough. (You can still read in .wav obviously).
   
Notes about this demo: I am only demonstrating IO and memory management.
I am not applying any effects though I will indicate the spot that you 
would to so.
'''

import os
import io

# stop pygame from greeting us... it's annoying
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pedalboard.io import AudioFile
from pygame.mixer import Sound, Channel, init
from pygame.time import delay

# setup pygame env
init()

# The sample we will analyze
SAMPLE_PATH = r'./dbconn/data/sample1.wav'
if not os.path.exists(SAMPLE_PATH):
    print('change the sample path on line 40... i cant read it.')
    exit(1)

with open(SAMPLE_PATH, 'rb') as f, AudioFile(f) as audio_in:
    
    # reset file stream from initilization. AudioFile(f) just read the whole 
    # buffer... now we need to read it again. 
    f.seek(0) 
    
    print(f'''Raw bytes info: 
    {f.name = }
    {f.read(32).hex() = :s}...
    {f.mode = }
    ''')
    
    # reset stream from f.read(32). Remember, this stream is tied to audio_in,
    # so we have to be careful not to let it get out of whack
    f.seek(0) 
    
    # Lets see some numbers
    print(f'''Pedalboard AudioFile info: 
    {audio_in.name = } (None b/c opened from file-like object)
    {type(audio_in) = }
    {audio_in.file_dtype = }
    {audio_in.duration = } seconds
    {audio_in.samplerate = } samples/second
    {audio_in.num_channels = }
    {audio_in.closed = }
    {audio_in.frames = }
    {audio_in.exact_duration_known = }
    ''')

    # look at the Numpy representation. we need this for things like the freq 
    # diagram and the db meter
    data = audio_in.read(audio_in.frames) 
    print(f'''Pedalboard AudioFile as Numpy array
    {data.shape = }
    {data[:,-10:] = }
    ''')
    
    # audio_in.read( ... ) just read from the buffer, we need to rewind it
    audio_in.seek(0)
    
    # <----------------------------------------------------------------------->
    # put effects here ...
    # <----------------------------------------------------------------------->
    
    # configure how to write out file
    settings = {
        'samplerate': audio_in.samplerate, # copy input settings
        'num_channels': audio_in.num_channels, 
        'format': 'mp3', # wav, ogg, flac, mp3, etc.
        'quality': 'V0' # highest quality mp3
        }
    
    # create a new BytesIO for output. this replaces the temp files
    buffer = io.BytesIO() 
    
    # show empty buffer
    print(f'''Buffer prior to write
    {buffer.getbuffer()[:32].hex() = :s}
    {len(buffer.getbuffer()) = }
    ''') # no .seek() because .getbuffer() is just a view
    
    # Writing out to `buffer`
    with AudioFile(buffer, 'w', **settings) as audio_out:
        
        # cursed indenting for better printing (see dedent())
        print(f'''Pedalboard AudioFile info:
    {type(audio_out) = }
    {audio_out.closed = }
    {audio_out.file_dtype = }
    {audio_out.frames = }
    {audio_out.num_channels = }
    {audio_out.quality = }
    {audio_out.samplerate = } samples/second
        ''')
        
        # writing out data 1024 frames at a time. A frame is like 1 of the 
        # 44100 samples per second.
        while audio_in.tell() < audio_in.frames:
            audio_out.write(audio_in.read(1024)) 
        
        
    # we just wrote to `buffer` (through `audio_out`), so we should rewind it.
    # we do this after the `audio_out` context closes to ensure the data is 
    # flushed
    buffer.seek(0)

    # take a look at what we got
    print(f'''Buffer after the write
    {buffer.getbuffer()[:32].hex() = :s}...
    {len(buffer.getbuffer()) = }
    ''')
    
# here is the recovered sound
song = Sound(buffer)
channel = song.play()
delay(10)
channel.pause()
delay(10000000)
channel.play(song)
while channel.get_busy():
    delay(10)
    
# could now take `buffer` and save it in timeline. This lets us keep a copy of 
# the processed audio in memory. We can easily 'undo' back to it, and it will 
# die when the app dies. If you want to export it, just write it to a file.