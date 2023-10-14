'''
Util for funning tests
'''

import functools

def _color(text: str, color: str) -> str:
    '''
    Color a string for printing to the console. 

    Parameters
    ----------
    text : str
        The string to color for printing
    color : str
        The color code for the string

    Returns
    -------
    str : the colored string
    '''

    colors = {
        'HEADER': '\033[95m',
        'OKBLUE': '\033[94m',
        'OKCYAN': '\033[96m',
        'OKGREEN': '\033[92m',
        'WARNING': '\033[93m',
        'FAIL': '\033[91m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m'
    }

    return f'{colors[color]}{text}\033[0m'


class Test:
    '''
    A testing instance that keeps track of statistics
    '''

    total: int = 0
    n_pass: int = 0
    n_fail: int = 0

    def __call__(self, func: callable) -> callable:
        '''
        Test functions should return `None` if they pass, else a message about why they failed.
        '''

        self.total += 1
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(_color(f'running {func.__name__}', 'WARNING'))
            try:
                status = func(*args, **kwargs)
            except Exception as exe:
                print(_color('FAILED', 'FAIL'), *exe.args)
                self.n_fail += 1
            else:
                if status:
                    print(_color('FAILED', 'FAIL'), status)
                    self.n_fail += 1
                else:
                    print(_color('PASSED', 'OKGREEN'))
                    self.n_pass += 1
        return wrapper
    
    def done(self) -> None:
        '''
        Print testing statistics
        '''
        print(f'Ran {self.total} tests with {_color(self.n_pass, "OKGREEN")} passed and {_color(self.n_fail, "FAIL")} failed.')