from typing import Any
from random import getrandbits

def get_uid(obj: Any) -> int:
    '''
    Get a unique ID for a given object

    Wrapper on hash() to 'hash' things like lists, dicts, etc. 
    
    Object uids with change between Python instances. 

    Parameters
    ----------
    obj : Any
        An object that implements __hash__(), __str__(), or __repr__()

    Returns
    -------
    int : the unique ID of this key
    
    Examples
    --------
    >>> from timeline.util import get_uid
    >>> get_uid(object()) == get_uid(object())
    True

    '''

    if hasattr(obj, '__hash__'):
        return hash(obj)
    return hash(str(obj))

def rand_uid() -> int:
    '''
    Get a random uid
    
    Returns
    -------
    int : random uid
    '''
    return getrandbits(64)