from pedalboard import Pedalboard, Chorus, Reverb, Distortion, Delay
from pedalboard.io import AudioFile
import io

def createReverbPedalboard(params, audioBytes):
    room_size, damping, dry, wet = params
    board = Pedalboard([Reverb(room_size=room_size/100, damping=damping/100, dry_level=dry/100, wet_level=wet/100)])
    return applyEffects(board, audioBytes)
def createDistortionPedalboard(params, audioBytes):
    drive = params[0]
    board = Pedalboard([Distortion(drive_db = drive)])
    return applyEffects(board, audioBytes)
def createDelayPedalboard(params, audioBytes):
    delay_seconds, feedback, dry_wet_mix = params
    board = Pedalboard([Delay(delay_seconds = delay_seconds/100, feedback=feedback/100, mix=dry_wet_mix/100)])
    return applyEffects(board, audioBytes)
def createChorusPedalboard(params, audioBytes):
    rate, depth, feedback, dry_wet_mix = params
    board = Pedalboard([Chorus(rate_hz = rate/100, depth=depth/100, feedback=feedback/100, mix=dry_wet_mix/100)])
    return applyEffects(board, audioBytes)


def applyEffects(board, audioBytes) -> io.BytesIO :
    # Make a Pedalboard object, containing audio plugins:
    #print(params)
    #reverb,delay,chorus,distortion = params
    #board = Pedalboard([Reverb(room_size=reverb/100),Delay(delay_seconds = delay/100), Chorus(rate_hz = chorus/100), Distortion(drive_db = distortion/10)])
    #board = Pedalboard([Chorus(depth = 0.25, centre_delay_ms = 10, feedback = 0.1), Reverb(room_size=0.25)])
    #board = Pedalboard([Chorus(depth = 5, centre_delay_ms = 50, feedback = .9), Reverb(room_size=0.5), Distortion(drive_db = 15)])
    #store in temp directory
    audioBytes.seek(0)
    with AudioFile(audioBytes) as f:     
       

        settings = {
            'samplerate': f.samplerate, # copy input settings
            'num_channels': f.num_channels, 
            'format': 'mp3', # wav, ogg, flac, mp3, etc.
            'quality': 'V0' # highest quality mp3
        }


        buffer = io.BytesIO()
        with AudioFile(buffer, 'w', **settings) as o:
            
        # Read one second of audio at a time, until the file is empty:
            while f.tell() < f.frames:

                chunk = f.read(int(f.samplerate))
                    
                    # Run the audio through pedalboard:
                effected = board(chunk, f.samplerate, reset=False)
                    
                    # Write the output to output file:
                o.write(effected)
   
    return buffer
    # Open an audio file for reading:



def export(file_path : str, bytes: io.BytesIO):
    with AudioFile(bytes) as f:
        settings = {
            'samplerate': f.samplerate, # copy input settings
            'num_channels': f.num_channels, 
            
            }
        
        with AudioFile(file_path,'w',**settings) as o :
            while f.tell() < f.frames:

                chunk = f.read(int(f.samplerate))
                        
                o.write(chunk)
    
    return bytes
            

def convertAudioFile(file_path : str) -> io.BytesIO :

    with open(file_path, 'rb') as f, AudioFile(f) as audio_in:
                        
        # configure how to write out file
        settings = {
            'samplerate': audio_in.samplerate, # copy input settings
            'num_channels': audio_in.num_channels, 
            'format': 'mp3', # wav, ogg, flac, mp3, etc.
            'quality': 'V0' # highest quality mp3
            }
        
        # create a new BytesIO for output. this replaces the temp files
        buffer = io.BytesIO() 

        # Writing out to `buffer`
        with AudioFile(buffer, 'w', **settings) as audio_out:
            # writing out data 1024 frames at a time. A frame is like 1 of the 
            # 44100 samples per second.
            while audio_in.tell() < audio_in.frames:
                audio_out.write(audio_in.read(1024)) 
    # we just wrote to `buffer` (through `audio_out`), so we should rewind it.
    # we do this after the `audio_out` context closes to ensure the data is 
    # flushed
    buffer.seek(0)
    return buffer
    

  

