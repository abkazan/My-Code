from pedalboard import Pedalboard, Chorus, Reverb, Distortion, Delay
from pedalboard.io import AudioFile

def applyEffects(params,songName):
    # Make a Pedalboard object, containing audio plugins:
    print(params)
    reverb,delay,chorus,distortion = params
    board = Pedalboard([Reverb(room_size=reverb/100),Delay(delay_seconds = delay/100), Chorus(rate_hz = chorus/100), Distortion(drive_db = distortion/10)])
    #board = Pedalboard([Chorus(depth = 0.25, centre_delay_ms = 10, feedback = 0.1), Reverb(room_size=0.25)])
    #board = Pedalboard([Chorus(depth = 5, centre_delay_ms = 50, feedback = .9), Reverb(room_size=0.5), Distortion(drive_db = 15)])

    # Open an audio file for reading:
    with AudioFile(songName) as f:
    
    #TODO: Re-applying effects only works when you play the sample and then stop it again
    # Open an audio file to write to:
        with AudioFile('output' + songName + '.mp3', 'w', f.samplerate, f.num_channels) as o:
        
            # Read one second of audio at a time, until the file is empty:
            while f.tell() < f.frames:
                chunk = f.read(int(f.samplerate))
                
                # Run the audio through pedalboard:
                effected = board(chunk, f.samplerate, reset=False)
                
                # Write the output to output file:
                o.write(effected)
    