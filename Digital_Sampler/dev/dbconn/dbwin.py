from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from .conn import Connection
from .cslsshtunnel import *
import traceback
import threading



class DBWindow:
    '''
    This class creates a new window that allows the user
    to search the sample library and retrieve samples from the database
    '''

    _root: Tk
    _search_results: Frame
    _search_frame : Frame
    _import_frame : Frame
    _args : dict
    _start = True
    _file_path : StringVar
    def __init__(self, root : Tk) -> None:
        '''
        A new window is generated when this class is created that allows users to import and export samples from the sample library

        Parameters
        ----------
        root : Tk
            The root of the application. Will be the Music Player in the application
        '''
        # Start thread to access database
        login = threading.Thread(target = logintoserver)
        login.start()

        # Unpack args from json
        import json
        with open("./dbconn/guiconfig.json") as f:
            self._args = json.load(f)

        # TODO: This should become the window when integrated
        self._root = root

        # for testing only
        self._root.title("Sample Library Search")

        # for testing only
        self._root.geometry("810x775")
        self._root.config(**self._args['window_args'])

        self._search_results = Frame(self._root)
        self._search_frame = Frame(self._root)
        self._import_frame = Frame(self._root)

        # Connect button so window doesn't fault on startup
        # User should be told to only press the button once they have completed login
        Label(self._root, text= 'Login to the CSL Machine before you click connect!\nPlease check your terminal, click connect once you have successfully logged in.').place(x=300, y=100)
        connectbutton = Button(self._root, text='Connect', command= self.connect)
        connectbutton.place(x=100, y = 100)
      
    
    def connect(self):
        '''
        Once the user has created a tunnel, they can now connect to the database to search or upload samples.

        Defaults on startup to searching, user can switch between the two with buttons.
        '''
        for widget in self._root.winfo_children():
            widget.destroy()

        try:
            with Connection() as conn:

                # Default to searching open
                # create search frame on startup
                if self._start :
                    self.search_frame(conn)
                    self._start=False

                # Two buttons to switch between Searching and Importing
                search_mode = Button(self._root,
                                     text = 'Search Library',
                                     **self._args["mode_button_args"],
                                     command= lambda : self.search_frame(conn))
                search_mode.grid(row = 0, column = 0, padx= 135, pady= 5)

                import_mode = Button(self._root,
                                     text = 'Add to Library',
                                     **self._args["mode_button_args"],
                                     command= lambda : self.import_frame(conn)
                                     )
                import_mode.grid(row = 0, column = 1, padx= 135, pady= 5)

        except Exception as exe:
            messagebox.showerror("Connection Error", traceback.format_exc())


    def search_frame(self, conn : Connection) -> None :
        '''
        A frame is generated that allows the user to search over the 
        sample library. 
        Includes a box to type in a search term, a dropdown to select the column, and a search button to execute the search

        Parameters
        -----------
        conn : Connection
            The connection object connected to the 

        Returns
        --------
        Frame : the frame that holds the search functionality
        '''

        # Clean the window
        self._import_frame.destroy()
        self._import_frame = Frame(self._root)
        self._search_frame.destroy()

        self._search_frame = Frame(self._root,
                             self._args['search_frame_args'])
        self._search_frame.grid(row = 1, column= 0, columnspan= 2)

        # Title
        search_title = Label(self._search_frame,
                             **self._args['search_title_args'])
        search_title.grid(column= 0, row =0, columnspan= 3)

        # Text box
        search_text = Entry(self._search_frame, 
                           **self._args['search_text_args'])
        
        search_text.grid(row=1, column=0, padx = 20, sticky='W')

        # Set up dropdown box
        search_column = StringVar(self._root)
        search_column.set(self._args['columns'][0])
        select_menu = OptionMenu(self._search_frame, 
                                 search_column,
                                 *self._args['columns'])
        select_menu.config(**self._args['select_menu_args'])
        select_menu.grid(row = 1, column= 1, padx=10)

        # Search Button
        search_button = Button(self._search_frame,
                               **self._args['search_button_args'],
                               command = lambda: self.search(search_text.get(), search_column.get(), conn)
                               )
        
        search_button.grid(row=1, column=3, padx=20, sticky='W')

        return 


    def search(self, search_term: str, column_name: str, conn: Connection) -> None:
        '''
        A search is started when the search button is pressed. The column name is the currently selected option in the drop down menu.

        TODO: Change Theme to match the rest of the app

        TODO: Fix datetime error - probably want ability to search newest - oldest, or oldest-newest rather than searching for a specific date

        Parameters:
        ------------
        search_term : str
            Term the returned files must match to
        column_name: any
            Name of the column being searched over
        conn: Connection
            The connection object connected to the sample library
        '''
        # wipe old search results before printing new ones
        self._search_results.destroy()

        # create a new frame and place it
        self._search_results = Frame(self._root,
                                     borderwidth=2,
                                     relief='sunken')
        self._search_results.grid(row = 3, column= 0, columnspan= 3, pady=5)

        column_name = column_name.replace(' ','_').lower()

        # Call the search function provided by conn
        retrieved = conn.search_audio(column_name, search_term)

        curry = 0

        global export_button
        export_button = PhotoImage(file = f'./{self._module}/export.png').subsample(16,16)
        # If no results, display "No results for your search term"
        if not retrieved:
            no_results = Label(
                        self._search_results,
                        text='No Search Results.'
            )
            no_results.grid(row=0, column=0, padx=3, sticky=W)

        # Parse through results and display them
        else:
            # add a scrollbar in case results go off screen
            Scrollbar(self._search_results,
                      orient=VERTICAL)
            # Column headers
            for col, settings in enumerate(self._args['table_args']):
                Label(self._search_results, 
                      **self._args['table_setup'],
                      font = ["times new roman", 8],
                      **settings).grid(column=col, row=curry)

            curry = curry+1

            # organizes results into a grid
            # TODO: Add a scroll bar when results overflow the frame
            for row in retrieved:
                for col, settings in enumerate(self._args['table_args']):
                    if col % 2 == 0 :
                        bgcolor = "#c3d4c8"
                    else:
                        bgcolor = "#b7c9be"

                    if(settings['text'] == 'Export'):
                        # Export button
                        Button(self._search_results,
                               **self._args['table_setup'], 
                               width=60, # Button width is different from label width ffs
                               height=14, 
                               image=export_button, 
                               bg = bgcolor,
                               command=lambda: self.export(row.primary_key, row.file_name, row.file_ext, conn)).grid(column=col, row=curry)
                    else:
                        # Attributes of the song displayed    
                        Label(self._search_results,
                              **self._args['table_setup'], 
                              width = settings['width'], 
                              bg = bgcolor,
                              font = ["times new roman", 8],
                              text = getattr(row, settings['text'].replace(' ','_').lower())).grid(column=col, row=curry)

                curry = curry + 1
            
            
                
                
    def export(self, pk: int, file_name: str, file_ext: str, conn : Connection):
        '''
        This function is called when the user presses the export button
        Saves the song to a folder the user specifies
        The file name comes from what is saved it the library

        Parameters
        ----------
        pk : int
            the primary key of the song to retrieve from the db
        file_name: str
            the file name of the sample, used to reconstruct the save path
        file_ext : str
            the file extension of the sample, used to reconstruct the save path
        conn : Connection
            the connection object used to access the sample library
        '''
        # let user choose folder to save in
        file_path = filedialog.askdirectory()

        # if they don't choose, we cannot save
        if file_path == None:
            return
        
        # get the file from the library
        file = conn.get_audio_file(pk)

        # write file where the user specifies
        file_path = f'{file_path}/{file_name}{file_ext}'
        with open(file_path, 'wb') as f:
            f.write(file)

    def import_frame(self, conn : Connection):
        '''
        A Frame is created that allows the user to import a sample into the sample library

        Parameters
        ----------
        conn : Connection
            the connection object to access the sample library
        '''
        # Clear search_frame
        self._search_frame.destroy()
        self._search_frame = Frame(self._root)
        self._search_results.destroy()
        self._search_results = Frame(self._root)

        self._import_frame.destroy()
        self._import_frame = Frame(self._root,
                                   self._args['import_frame_args'])
        self._import_frame.grid(row=1, column=0, columnspan=2)

        # Have the user select a file with file explorer

        select_file_button = Button(self._import_frame,
                                 **self._args['select_file_button_args'],
                                 command = lambda : self.getfilepath())
        select_file_button.grid(column=0, row=0, padx = 10, pady=20)
        self._file_path = StringVar(self._root)
        self._file_path.set("No file choosen")
        file_choosen = Label(self._import_frame,
                             textvariable=self._file_path,
                             **self._args['file_path_args'])
        file_choosen.grid(column=1, row=0, padx = 10, pady=20)

        # Pass that file path and other inputed args to the connection function

        import_button = Button(self._import_frame,
                               **self._args['import_button_args'],
                               command= lambda : self.import_file(conn, self._file_path.get()))
        import_button.grid(column=2, row=0, padx = 10, pady= 20)

        # display success message 

    def getfilepath(self):
        self._file_path.set(filedialog.askopenfilename())
        return 
        
    def import_file(self, conn : Connection, filepath : str):

        kwargs = {
            "file_path" : filepath
        }
        
        uploaded = conn.set_audio_file(**kwargs)
        Label(self._import_frame, text=f"{uploaded['file_name']}{uploaded['file_ext']} uploaded to the database.").grid(column=0, row=3)
        Label(self._import_frame, text=f"Title: {uploaded['title']}").grid(column=1, row=3)
        Label(self._import_frame, text=f"Artist: {uploaded['artist']}").grid(column=1, row=4)
        Label(self._import_frame, text=f"Album: {uploaded['album']}").grid(column=1, row=5)



        




                