'''
TODO add a multi commit
'''

from .util import get_uid, rand_uid

class Timeline:
    '''
    Memory efficient timeline of commits

    A timeline allows you to keep track of a sequence of commits. Each time the application is updated, a new commit should be added to be tracked.

    Example
    -------
    >>> from timeline import Timeline
    >>> tl = Timeline()
    >>> _ = tl.commit(item1='joshua',item2=23)
    >>> tl.peek()
    {'item1': 'joshua', 'item2': 23}
    
    '''

    def __init__(self):
        '''Initialize a new timeline'''
        self._head: int = -1
        self._history: list = []
        self._resolution: dict = {}
        self._cache: dict = {}

    def __str__(self) -> str:
        '''
        Return a string representation of this object
        
        Examples
        --------
        >>> from timeline import Timeline
        >>> tl = Timeline()
        >>> _ = tl.commit(item1='joshua',item2=23)
        >>> # print(tl)
        
        '''
        return ''
        
    def __repr__(self) -> str:
        '''Return Python code to create self'''
        return 'Timeline()'
    
    def _validate(self):
        '''
        Validate that the internal state representations are in agreement

        If the state is invalid but repairable, the state is corrected silently. Throws an error when state is irreparably desynced.

        Throws
        ------
        KeyError, IndexError : the state is irreparably desynced.
        '''
        
        # check the head is pointing to a valid commit
        if not (-1 <= self._head < (n:=len(self._history))):
            raise IndexError(f'cannot access commit {self._head} for {n} commits')
        
        # verify each commit uid can be resolved...
        for uid in set(self._history):
            if uid not in self._resolution:
                raise KeyError(f'{uid=} cannot be resolved')
            
            # ...and that it's values are cached
            for value_uid in self._resolution[uid].values():
                if value_uid not in self._cache:
                    raise KeyError(f'{value_uid=} is not in cache')
                
        # TODO add state correction
        
        return


    def peek(self, offset: int = 0) -> dict or None:
        '''
        Retrieve a commit relative to current commit

        Calling without any arguments will return the current commit. Requesting a commit outside of the history will return none.

        Parameters
        ----------
        offset : int
            The number of commits to look ahead or behind. A negative offset will look at commits in the past, and positive offsets will look at future commits.

        Returns 
        -------
        dict, None : the requested commit's data

        Example
        -------
        >>> from timeline import Timeline
        >>> tl = Timeline()
        >>> _ = tl.commit(item1='joshua',item2=23)
        >>> tl.peek()
        {'item1': 'joshua', 'item2': 23}
        >>> tl.peek(10) == None
        True
        
        '''

        ptr = self._head + offset
        if not (0 <= ptr < len(self._history)):
            return None
        
        # resolve the commit...
        res_dict = self._resolution[self._history[ptr]]
        
        # ...and pull its data from the cache
        retval = {}
        for key, uid in res_dict.items():
            retval[key] = self._cache[uid][1]
            
        return retval

    def commit(self, **data) -> int:
        '''
        Add a new commit to the timeline

        Paramters
        ---------
        **data : Any
            The data to store in this commit
            
        Returns
        -------
        int : the commit hash

        Exmaples
        --------
        >>> from timeline import Timeline
        >>> tl = Timeline()
        >>> _ = tl.commit(data='my data')
        >>> tl.peek()
        {'data': 'my data'}

        '''

        if __debug__:
            self._validate()
        self.decap()
        
        # enter a new commit into the history
        __hash = rand_uid()
        self._history.append(__hash)
        
        # cache all the data values and create the resolution dict
        res_dict = {}
        for key, value in data.items():
            
            value_uid = get_uid(value)
            res_dict[key] = value_uid
            
            if value_uid in self._cache:    # pre cached, inc ref count
                self._cache[value_uid][0] += 1 
            else:                           # new cache entry
                self._cache[value_uid] = [1, value]
        
        # add resoultion dict, move head
        self._resolution[__hash] = res_dict
        self._head += 1
        
        return __hash
    
    def uncommit(self, __hash: int):
        '''
        Drop a commit from history
        
        All of the commit's data is subject to removal, but not guaranteed to be removed. 
        
        Parameters
        ----------
        __hash : int
            The commit hash to remove
            
        Exmaples
        --------
        >>> from timeline import Timeline
        >>> tl = Timeline()
        >>> __hash = tl.commit(data='my data')
        >>> tl.peek()
        {'data': 'my data'}
        >>> tl.uncommit(__hash)
        >>> tl.peek() == None
        True
        
        '''
        
        if __hash not in self._history:
            return
        
        # remove from history
        loc = self._history.index(__hash)
        del self._history[loc]
        
        # remove from resolution
        res_dict = self._resolution[__hash]
        del self._resolution[__hash]
        
        # dec all ref counts, remove data w/ zero ref count
        for _, data_uid in res_dict.items():
            self._cache[data_uid][0] -= 1
            if not self._cache[data_uid][0]:
                del self._cache[data_uid]
        return
        
    
    def decap(self) -> None:
        '''
        Uncommit all future commits
        '''
        for __hash in self._history[self._head+1:]:
            self.uncommit(__hash)
            
        return
    
    def undo(self) -> None:
        '''
        Undo the last timeline operation

        Exmaples
        --------
        >>> from timeline import Timeline
        >>> tl = Timeline()
        >>> _ = tl.commit(data='my data')
        >>> tl.peek()
        {'data': 'my data'}
        >>> tl.undo()
        >>> tl.peek() == None
        True

        '''
        if -1 < self._head:
            self._head = self._head - 1
        return
    
    def redo(self) -> None:
        '''
        Redo the last timeline operation

        Exmaples
        --------
        >>> from timeline import Timeline
        >>> tl = Timeline()
        >>> _ = tl.commit(data='my data')
        >>> tl.peek()
        {'data': 'my data'}
        >>> tl.undo()
        >>> tl.peek()
        >>> tl.redo()
        >>> tl.peek()
        {'data': 'my data'}
        
        '''
        if self._head < len(self._history) - 1:
            self._head = self._head + 1
        return
    
    def revert(self):
        '''
        Return to the oldest commit

        If you are already on the oldest commit, does nothing
        
        Examples
        --------
        >>> from timeline import Timeline
        >>> tl = Timeline()
        >>> _ = tl.commit(data='my data')
        >>> _ = tl.commit(data='my second')
        >>> tl.peek()
        {'data': 'my second'}
        >>> tl.revert()
        >>> tl.peek()
        {'data': 'my data'}
        
        '''
        
        if self._history and self._history[self._head] != self._history[0]:
            new_uid = rand_uid()
            self._history.append(new_uid)
            self._resolution[new_uid] = self._resolution[self._history[0]]
            self._head = self._head + 1
            
        return
        
    def cull(self) -> int:
        '''
        Drop the oldest commit

        Returns
        -------
        int : size of this timeline in bytes after dropping oldest commit
        
        Examples
        --------
        >>> from timeline import Timeline
        >>> tl = Timeline()
        >>> _ = tl.commit(data='my data')
        >>> _ = tl.commit(data='my second')
        >>> tl.peek(-1)
        {'data': 'my data'}
        >>> tl.cull() # different results on mac vs window
        48
        >>> tl.peek(-1) == None
        True
        
        '''
        import sys
        
        if not self._history:
            return
        
        oldest = self._history[0]
        self.uncommit(oldest)
        self._head = self._head - 1  
        return sys.getsizeof(self)