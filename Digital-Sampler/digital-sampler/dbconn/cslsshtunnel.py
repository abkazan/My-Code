
'''
Run this in a separate terminal before attempting to connect to the db!!!
'''


import subprocess

def logintoserver():
    '''
    Calls a tunnel to the database on the csl machine
    This should be called in a separate thread, once the tunnel is created, subsequent python code will not be executed
    '''
    username = input("Username: ")
    
    subprocess.call(f'ssh -L  localhost:39954:localhost:39954 {username}@cs506-team-35.cs.wisc.edu')


