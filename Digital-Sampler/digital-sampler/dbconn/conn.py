'''
Methods for creating and managing a connection to the MySQL database
'''

import sqlalchemy
from tinytag import TinyTag
import io


class Connection:
    '''
    A `connection` is a wrapper on a MySQL connection to make sending and loading audio files and their meta data easier. 

    Create a connection by diong the following

    >>> with Connection() as conn:
    ...     conn
    ... 
    Connection to 127.0.0.1:39954
    '''

    _engine: sqlalchemy.Engine
    _conn: sqlalchemy.Connection
    _meta: sqlalchemy.MetaData
    
    def __init__(self, host: str = 'cs506-team-35.cs.wisc.edu', port: int = 3306, table: str = 'sample'):
        '''
        A new connection to the MySQL database containing .wav files.

        Parameters
        ----------
        host : str
            The host location for the database. Defaults to '127.0.0.1'
        port : int
            The port of the database. Defaults to 39954
        table : str
            The table of samples to link to. Defaults to 'sample'

        Returns
        -------
        Connection : connection to MySQL database
        '''

        # for __repr__ and __str__
        self._host = host
        self._port = port

        # TODO These arguments as dummies THEY WILL NOT WORK :D
        url = sqlalchemy.engine.URL.create (
            drivername = "mysql",
            username = "root",
            password = "admin",
            host = host,
            port = port,
            database = "sample_lib"
        )

        try:
            self._engine = sqlalchemy.create_engine(url)
        except Exception as exe:
            exe.args = (f'Issues creating database engine with url "{url}"', *exe.args)
            raise

        self._meta = sqlalchemy.MetaData()
        self.change_table(table)

    def __repr__(self) -> str:
        return f'Connection to {self._host}:{self._port}'
    
    def __str__(self) -> str:
        return self.__repr__

    def __enter__(self):
        '''
        Allow this object to be used in a with block.
        '''

        self._conn = self._engine.begin()
        self._conn.__enter__()
        return self
 
    def __exit__(self, *args):
        '''
        TODO Doc comment
        '''

        self._conn.__exit__(*args)


    def change_table(self, table_name: str) -> None:
        '''
        Change the table that is currently being accessed
        
        Parameters
        ----------
        table_name: str
            The table to be access next time a query is called

        Throws
        ----------
        NoSuchTableError
            Trying to access a table that doesn't exist
        '''
        try:
            self._table = sqlalchemy.Table(table_name, self._meta, autoload_with = self._engine)

        except Exception as exe:
            exe.args = (f'Issues with table lookup for table "{table_name}"', *exe.args)
            raise

    def get_audio_file(self, pk: int) -> bytes:
        '''
        Returns a bytearray of a audio file by primary key

        TODO Generalize this. What if I want to lookup by artist, genre, etc.?

        TODO Is it actually a bytearray, or are you just guessing?

        Parameters
        ----------
        file_name : str
            The name of the file to return

        Returns
        -------
        bytearray : the audio file representation in bytes


        Throws
        ------
        TODO This guy throws so much stuff

        '''

        
        # search for the audio file that matches the primary key
        query = sqlalchemy \
            .select(self._table.c.file_data) \
            .where(self._table.c.primary_key == pk)
        
        try: 
            with self._engine.begin() as c:
                for row in c.execute(query):
                    query_retval = row.file_data

            # Bytes IO supports just native bytes conversion
            # Very cool!
            buffer = io.BytesIO(query_retval)
            buffer.seek(0)

        except Exception as exe: 
            exe.args = exe.args + (f'Issues running lookup query for primary key "{pk}"', *exe.args)
            raise


        # Turn bytes into an audio buffer  

        return buffer

    # TODO the returns none annotation might be useless... investigate
    def set_audio_file(self, *args, **kwargs) -> dict:
        '''
        Store information about an audio file by name. 
        
        If the name does not exist in the database, a new record will be created. 

        Parameters
        ----------
        file_name : str
            The name of the file to update
        *args
            Not used
        **kwargs 
            The properties to update
            At a minimum, there must be either
            - file_path OR
            - The file_data and file_ext and duration
                - if the file name is not provided, it will become the default
            - getting duration sucks, will default to 0 if not passed in
                - TODO: Come back to this when it works
            Other optional fields:
            - *title
            - *artist
            - *album
            - *genre
            - instrument
            - bpm
            - key signature
            *auto generated from file
        '''

        # TODO: Check if name already exists in database, if so don't readd it?


        if 'file_path' in kwargs:

            # Use tinytag to retreive as much metadata as possible
            # This shit doesn't work except for duration ;.;
            metadata = TinyTag.get(kwargs["file_path"])
            if 'title' not in kwargs: 
                kwargs['title'] = metadata.title
            if 'artist' not in kwargs: 
                kwargs['artist'] = metadata.artist
            if 'duration' not in kwargs: 
                kwargs['duration'] = metadata.duration
            if 'genre' not in kwargs:
                kwargs['genre'] = metadata.genre
            if 'album' not in kwargs: 
                kwargs['album'] = metadata.album
            

            # retrieving the file name and extension from the path
            import os
            filename = kwargs["file_path"].rsplit('/', 1)[1]
            split_name = os.path.splitext(filename)

            kwargs['file_name'] = split_name[0]
            kwargs['file_ext'] = split_name[1]


            # charge to match audio format in main app
            # get data from the file

            with open(kwargs["file_path"], 'rb') as f:
                        
                file = f.read()

            del kwargs['file_path']

            # add retreived data to the kwargs
            
            kwargs['file_data'] = file

            # If title is still null, make it file_name
            if not kwargs['title']:
                kwargs['title'] = kwargs['file_name']

        
        search_results = self.search_audio('title', kwargs['title'])

        if search_results:
            kwargs['primary_key'] = search_results['primary_key']
            return self.update_entry(kwargs)


        elif((kwargs['file_data'] != None) & (kwargs['file_ext'] != None)):
            if(kwargs['file_name'] == None):
                kwargs['file_name'] = 'sample'


        else:
            raise Exception("Error in input, please make sure you have either 1)the path to the file or 2) the file data and extension")

        # add current datetime to kwargs        
        from datetime import datetime
        kwargs['upload_date'] = datetime.now()


        if(kwargs['duration'] == None):
            kwargs['duration'] = 0

        #generate the query based on the kwargs
        query = sqlalchemy \
            .insert(self._table) \
            .values(*args,**kwargs)
        
        try:
            stmt = query.compile()
            with self._engine.begin() as c:
                query_retval = c.execute(query) 
            
        except Exception as exe: 
            exe.args = (f'Issues running record insert query for file name "{kwargs["file_name"]}" with arguments "{args}" and properties "{kwargs}"', *exe.args)
            raise
        kwargs['primary_key'] = query_retval.inserted_primary_key
        return kwargs
    
    def update_entry(self, pk: int, *args, **kwargs) -> dict:
        '''
        Updates the entry for the audio file of the
        provided primary key

        If no primary key, nothing happens

        Parameters
        ----------
        *args
            Not used
        **kwargs 
            The properties to update
            At a minimum, there must be
            - primary key
                used to find the specific entry
            Other optional fields:
            - title
            - artist
            - album
            - genre
            - instrument
            - bpm
            - duration
            - key signature
        '''
        # can not upadte without primary key
        if not pk:
            return
        
        # update upload date to reflect       
        from datetime import datetime
        kwargs['upload_date'] = datetime.now()

        #generate the query based on the kwargs
        query = sqlalchemy \
            .update(self._table) \
            .where(self._table.c.primary_key == pk)\
            .values(**kwargs)
        

        try:
            stmt = query.compile()
            with self._engine.begin() as c:
                query_retval = c.execute(query) 
            
        except Exception as exe: 
            exe.args = (f'Issues running record update query for primary key "{pk}" with arguments "{args}" and properties "{kwargs}"', *exe.args)
            raise

        return kwargs
    

    
    # TODO check the return typing of this 
    def search_audio(self, column_name: str, search_term) -> list[tuple]:
        '''
        Search for audio files that match the search term
        
        Return all information about these files
        
        Parameters
        ----------
        column_name : str
            The name of the column being searched over
        search_term : any
            The term the returned files must match to. Type is dependant on the type store in that column
        
        Returns
        -------
        A list of all the files that match that search term. Keep characteristic fields of the audio files, but do not return the binary data itself so the user can make a selection

        Fields that will be returned:
        -primary_key
        -upload_date
        -file_name
        -file_ext
        -duration
        -title
        -artist
        -album
        -genre
        -instrument
        -bpm
        -key_signature

        Throws
        ------
        TODO
        '''


        if not search_term :
            query = sqlalchemy \
                .select(self._table.c.primary_key, \
                        self._table.c.upload_date, \
                        self._table.c.file_name, \
                        self._table.c.file_ext, \
                        self._table.c.duration, \
                        self._table.c.title,\
                        self._table.c.artist, \
                        self._table.c.genre, \
                        self._table.c.album, \
                        self._table.c.instrument, \
                        self._table.c.album_art, \
                        self._table.c.album_art_ext,
                        self._table.c.bpm, \
                        self._table.c.key_signature)
            
        elif column_name == 'upload_date':
            query = sqlalchemy \
                .select(self._table.c.primary_key, \
                        self._table.c.upload_date, \
                        self._table.c.file_name, \
                        self._table.c.file_ext, \
                        self._table.c.duration, \
                        self._table.c.title,\
                        self._table.c.artist, \
                        self._table.c.genre, \
                        self._table.c.album, \
                        self._table.c.instrument, \
                        self._table.c.album_art, \
                        self._table.c.album_art_ext,
                        self._table.c.bpm, \
                        self._table.c.key_signature).\
                        order_by(self._table.c.upload_date)

        else :

            query = sqlalchemy \
                .select(self._table.c.primary_key, \
                        self._table.c.upload_date, \
                        self._table.c.file_name, \
                        self._table.c.file_ext, \
                        self._table.c.duration, \
                        self._table.c.title,\
                        self._table.c.artist, \
                        self._table.c.genre, \
                        self._table.c.album, \
                        self._table.c.instrument, \
                        self._table.c.album_art, \
                        self._table.c.album_art_ext,
                        self._table.c.bpm, \
                        self._table.c.key_signature) \
                .where(self._table.c[column_name]==search_term)
        
        try:
            with self._engine.begin() as c:
                query_retval = c.execute(query).all()
            
        except Exception as exe:
            exe.args = (f'Issues looking for audio files from "{column_name}" that match "{search_term}"', *exe.args)
            raise
        return query_retval
