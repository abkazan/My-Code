
import threading
import serial
import time
from . import digitalSampler as ds

class SerialMonitor:

    _com : threading.Thread
    _com_on : bool
    def __init__(self, drumpad, port : str, baud: int = 9600, ) -> None:

        self._drumpad = drumpad

        # Start threading
        self._com_on = True

        self._com = threading.Thread(target = lambda: self.com_connect(port, baud))

        self._com.start()



    def com_connect(self, port : str, baud : int) :

        #Start serial connection
        ser = serial.Serial(
            port=port,\
            baudrate=baud,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=0)
        
        #this will store the line
        seq = []
        count = 1
        
    
        while self._com_on :
            for c in ser.read():
                seq.append(chr(c)) #convert from ANSII
                joined_seq = ''.join(str(v) for v in seq) #Make a string from array
                
                if chr(c) == '\n':
                    self._drumpad.pressButton(joined_seq.strip().lower())
                    time.sleep(0.5)
                    self._drumpad.releaseButton(joined_seq.strip().lower())
                    seq = []
                    count += 1
                    break



        ser.close()

    def close(self) -> None:
        self._com_on = False
