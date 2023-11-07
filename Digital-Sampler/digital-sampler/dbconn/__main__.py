'''
Tests for module dbconn

To Run:  python -m dbconn
Run cslsshtunnel.py in a separate terminal to tunnel into the csl machine

To wipe and run your mysql database, look in src-server->scripts and pick the files that match your operating system

Table Schema is as follows
sample
--------------------------
primary_key  | INT
upload_date  | DATETIME
file_data    | MEDIUMBLOB
file_name    | VARCHAR(255)
file_ext     | VARCHAR(5)
duration     | INT
title        | VARCHAR(255)
artist       | VARCHAR(255)
album        | VARCHAR(255)
genre        | VARCHAR(255)
instrument   | VARCHAR(255)
album_art    | BLOB
album_art_ext| VARCHAR(5)
bpm          | INT
key_signature| VARCHAR(15)
--------------------------

  /\   __   /\  
 //\\_//\\_//\\
 \_          _/
 //   ͡° ͜ʖ ͡°  \\ 
  \          /
   \\      //
     '----'

     

To run the tests, uncomment the line 
<<< testsuite()

To run the UI, uncomment these 3 lines
<<< root = Tk()
<<< DBWindow(root)
<<< root.mainloop()
    
'''

from .cslsshtunnel import *

from testpy import (
    Test as TestContext # Just thought 'Test' was a bit unclear
)

from .conn import Connection
from .dbwin import DBWindow
from tkinter import *

test = TestContext()

@test
def test_creating_connection():

    from .conn import Connection
    with Connection() as conn:
        pass
    return None


@test
def simple_test_pushing_file():
    '''
    Send one file to the db with some parameters
    Data from testdata/testnum1.json
    '''
    from .conn import Connection
    with Connection() as conn:
        import json
        with open("./dbconn/test-data/testnum1.json") as f:
            qargs = json.load(f)
        sent = conn.set_audio_file(**qargs)

    return None



@test
def simple_test_pulling_file():
    '''
    Test pulling the audio file that was stored in previous test

    Check that bytes are the same, otherwise fail
    '''
    from .conn import Connection
    with Connection() as conn:
        retrieved = conn.get_audio_file(1)
        with open('dbconn/test-data/lo-fi-violin.mp3', 'rb') as f:
            file = f.read()
        if (retrieved != file):
            raise Exception("retrieved file does not match original")
    return None

@test
def simple_test_search():
    '''
    Search on the entry that was added in 
    simple_test_pushing_file
    '''
    from .conn import Connection
    with Connection() as conn:
        retrieved = conn.search_audio('bpm', 80)

    row = retrieved[0]
    if (row.primary_key != 1):
        raise Exception(f"Retreived primary key: '{row.primary_key}' does not match expected: 1 ")

    if (row.upload_date == None):
        raise Exception(f"Retreived date time '{row.upload_date}' does not have a value")
    
    if(row.file_name != 'lo-fi-violin'):
         raise Exception(f"Retreived file name: '{row.file_name}' does not match expected: lo-fi-violin")
    
    if(row.file_ext != '.mp3'):
         raise Exception(f"Retreived file extension: '{row.file_ext}' does not match expected: .mp3")
    
    if(row.duration != 9):
        raise Exception(f"Retreived duration: '{row.duration}' does not match expected: 9")
    
    if(row.artist != 'k'):
        raise Exception(f"Retreived duration: '{row.artist}' does not match expected: k")
    
    if(row.genre != 'Lo-Fi'):
        raise Exception(f"Retreived duration: '{row.genre}' does not match expected: Lo-Fi")
    
    if(row.instrument != 'Violin'):
        raise Exception(f"Retreived instrument: '{row.instrument}' does not match expected: Violin")
    
    try:
        row.file_data
        raise Exception(f"Retreived file data when expecting None")
    except Exception as exe:
        pass
    

def testsuite():
    test_creating_connection()
    simple_test_pushing_file()
    simple_test_pulling_file()
    simple_test_search()

    test.done()

    import doctest
    doctest.testmod()

#testsuite()


root = Tk()
DBWindow(root)
root.mainloop()
    