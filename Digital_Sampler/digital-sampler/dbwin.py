from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from .dbconn import Connection
import traceback
import os
from . import digitalSampler as ds

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
    _search_box: Entry
    def __init__(self, root : Tk, mp) -> None:
        '''
        A new window is generated when this class is created that allows users to import and export samples from the sample library

        Parameters
        ----------
        root : Tk
            The root of the application. Will be the Windos in the application
        mp : Music Player
            The main module of the application.
        '''
        # Start thread to access database
        #login = threading.Thread(target = logintoserver)
        #login.start()

        # Unpack args from json
        import json
        with open (os.path.join(os.path.dirname(__file__),os.path.join("config","dbconfig.json"))) as f:
            self._args = json.load(f)


        self._root = root
        self._mp = mp

        # for testing only
        self._root.title("Sample Library Search")

        # for testing only
        self._root.geometry("850x775+50+25")
        self._root.config(**self._args['window'])

        self._search_results = Frame(self._root)
        self._search_frame = Frame(self._root)
        self._import_frame = Frame(self._root)

        self.connect()
      
    
    def connect(self):
        '''
        Once the user has created a tunnel, they can now connect to the database to search or upload samples.

        Defaults on startup to searching, user can switch between the two with buttons.
        '''
        for widget in self._root.winfo_children():
            widget.destroy()

        try:
            with Connection() as conn:

                

                button_frame = Frame(self._root, **self._args['button_frame'])
                button_frame.pack(anchor = CENTER, side = TOP)

                # Two buttons to switch between Searching and Importing
                search_mode = Button(button_frame,
                                     text = 'Search Library',
                                     **self._args["mode_button"],
                                     command= lambda : self.search_frame(conn))
                search_mode.grid(row = 0, column = 0, padx= 130, pady= 5)

                import_mode = Button(button_frame,
                                     text = 'Add to Library',
                                     **self._args["mode_button"],
                                     command= lambda : self.import_frame(conn)
                                     )
                import_mode.grid(row = 0, column = 1, padx= 130, pady= 5)
                

                # Default to searching open
                # create search frame on startup
                if self._start :
                    self.search_frame(conn)
                    self._start=False

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
                             **self._args['search_frame'])
        self._search_frame.pack(side = TOP, anchor=CENTER)

        Label(self._search_frame, **self._args['search_title']).pack(fill=X, side = TOP)

        search_area = Frame(self._search_frame, **self._args['window'])
        search_area.pack(side = TOP, anchor=CENTER)

        # Text box
        self._search_box = Entry(search_area, 
                           **self._args['search_text'])
        
        self._search_box.grid(row=1, column=0, padx = 10)

        # Set up dropdown box
        search_column = StringVar(self._root)
        search_column.set(self._args['columns'][0])
        select_menu = OptionMenu(search_area, 
                                 search_column,
                                 *self._args['columns'],
                                 command = lambda x: self.check_status( search_column.get(), search_area)
                                 )
        select_menu.config(**self._args['select_menu'])
        select_menu.grid(row = 1, column= 1, padx=10)

        # Search Button
        search_button = Button(search_area,
                               **self._args['search_button'],
                               command = lambda: self.search(search_column.get(), conn)
                               )
        
        search_button.grid(row=1, column=2, padx=10)

        
       

        return 

    def check_status(self, column : str, search_area : Frame) -> None:
        if column == 'Upload Date' and self._search_box :
            self._search_box.destroy()
            self._search_box = Entry()
        else:
            self._search_box.destroy()
            self._search_box = Entry(search_area, 
                           **self._args['search_text'])
            self._search_box.grid(row=1, column=0, padx = 10)

        

    def search(self, column_name: str, conn: Connection) -> None:
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
        if self._search_box :
            search_term = self._search_box.get()

        else :
            search_term = None

        # wipe old search results before printing new ones
        self._search_results.destroy()

        # create a new frame and place it
        self._search_results = Frame(self._search_frame,
                                     borderwidth=2,
                                     relief='sunken', 
                                     width = 830)
        self._search_results.pack(fill=X, side = TOP)

        column_name = column_name.replace(' ','_').lower()

        # Call the search function provided by conn
        retrieved = conn.search_audio(column_name, search_term)

        curry = 0

        # export and edit buttons

        global export_button
        export_button = PhotoImage(file = os.path.join(os.path.dirname(__file__), os.path.join('icons','export.png'))).subsample(16,16)

        global edit_button
        edit_button = PhotoImage(file = os.path.join(os.path.dirname(__file__), os.path.join('icons','edit.png'))).subsample(30,30)

        # If no results, display "No results for your search term"
        if not retrieved:
            no_results = Label(
                        self._search_results,
                        text='No Search Results.'
            )
            no_results.grid(row=0, column=0, padx=3)

        # Parse through results and display them
        else:
            # add a scrollbar in case results go off screen
            Scrollbar(self._search_results,
                      orient=VERTICAL)
            # Column headers
            for col, settings in enumerate(self._args['table']):
                Label(self._search_results, 
                      **self._args['table_setup'],
                      font = ["times new roman", 8],
                      **settings).grid(column=col, row=curry)

            curry = curry+1

            # organizes results into a grid
            # TODO: Add a scroll bar when results overflow the frame
            for rownum, row in enumerate(retrieved):
                for col, settings in enumerate(self._args['table']):
                    if rownum % 2 == 0 :
                        bgcolor = "#c3d4c8"
                    else:
                        bgcolor = "#b7c9be"

                    if(settings['text'] == 'Export'):
                        # Export button
                        Button(self._search_results,
                               **self._args['table_setup'], 
                               width=48, # Button width is different from label width ffs
                               height=14, 
                               image=export_button, 
                               bg = bgcolor,
                               command=lambda: self.export(row.primary_key, row.file_name, row.file_ext, conn)).grid(column=col, row=curry)
                        
                    elif(settings['text'] == 'Edit'):
                        # Edit button
                        Button(self._search_results,
                               **self._args['table_setup'], 
                               width=36, # Button width is different from label width ffs
                               height=14, 
                               image=edit_button, 
                               bg = bgcolor,
                               command=lambda: self.edit(row, conn)).grid(column=col, row=curry)
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
    
        # get the file from the library
        file = conn.get_audio_file(pk)


        # save to user songs dictionary in the Music Player
        self._mp.user_songs[f'{file_name}{file_ext}'] = file
        self._mp.playlist.insert(END, f'{file_name}{file_ext}')
        self._mp._timeline.commit(**self._mp.user_songs)



        messagebox.showinfo(title = 'Export', message = f"Exported {file_name}{file_ext} to Loaded Samples")


    def edit(self, row: tuple, conn : Connection) :
        '''
        A window pops up that allows the user to edit a stored
        song. This method creates that window, and calls the update
        function with the fields the user inputs
        
        Parameters
        ----------
        pk : int
            the primary key of the song to edit
        title : str
            the title of the song to update
        conn : Connection
            database connection object
        '''

        # Create the window
        edit_window = Toplevel(self._root)
        edit_window.geometry("300x300+900+50")
        edit_window.title("EDIT")
        edit_window.config(**self._args['edit_window'])

        # Title
        Label(edit_window, text = f"Edit {row.title}", **self._args['edit_title']).pack(side = TOP, anchor= CENTER, pady=5)

        # Create a 'grid' of text boxes to change values
        # Is it possible to have them preloaded?
        text_frame = Frame(edit_window, **self._args['edit_window'])
        text_frame.pack(side = TOP, anchor= CENTER)

        text_boxes = []

        for index, label in enumerate(self._args['columns']):
            if label == "Upload Date" :
                pass
            else : 
                # Label for attribute
                Label(text_frame, **self._args["edit_attr_label"], text=label).grid(row=index, column=0, pady= 5)

                # Create text box
                text_boxes.append((Entry(text_frame, **self._args["edit_entry"])))

                if getattr(row, label.replace(' ','_').lower()):
                    text_boxes[index].insert(0, getattr(row, label.replace(' ','_').lower()))
                text_boxes[index].grid(row=index, column=1, pady= 5)

        save_button = Button(edit_window, **self._args["save_button"], command=lambda: self.save_changes(text_boxes, row.primary_key, edit_window, conn))
        save_button.pack(side=TOP, anchor= CENTER, pady= 5)

        

    def save_changes(self, entries : list, pk : int, edit_window : Toplevel, conn: Connection) :
        '''
        Compile changes into kwargs and make an API call to connection

        Parameters
        ----------
        entries: list
            List of entry objects. Need to use get() to get the value in them
        pk : int
            Primary key of the song being modified
        edit_window : TopLevel
            Reference to the edit window so it can be killed when done
        conn : Connection
            Object that allows to connect to the database
        '''

        # compile entry boxes into arguments
        kwargs = {}

        for index, entry in enumerate(entries):
            if entry.get(): 
                kwargs[self._args['columns'][index].replace(' ','_').lower()] = entry.get()

        # Update the db
        conn.update_entry(pk = pk, **kwargs)
        
        # Close the window
        edit_window.destroy()
        
        

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
                                   self._args['import_frame'])
        self._import_frame.pack(side = TOP, anchor=CENTER)

        # Have the user select a file with file explorer
        import_title = Label(self._import_frame,
                             self._args['import_title'])
        import_title.grid(column=0, row=0, columnspan=3)

        select_file_button = Button(self._import_frame,
                                 **self._args['select_file_button'],
                                 command = lambda : self.getfilepath())
        select_file_button.grid(column=0, row=1, padx = 10, pady=20)
        self._file_path = StringVar(self._root)
        self._file_path.set("No file choosen")
        file_choosen = Label(self._import_frame,
                             textvariable=self._file_path,
                             **self._args['file_path'])
        file_choosen.grid(column=1, row=1, padx = 10, pady=20)

        # Pass that file path and other inputed args to the connection function

        import_button = Button(self._import_frame,
                               **self._args['import_button'],
                               command= lambda : self.import_file(conn, self._file_path.get()))
        import_button.grid(column=2, row=1, padx = 10, pady= 20)

        # display success message 

    def getfilepath(self):
        self._file_path.set(filedialog.askopenfilename(title="Select file",
            filetypes=(("Audio Files", ["*.mp3", "*.wav", "*.flac"]), ("mp3 files", "*.mp3"), ("wav files", "*.wav"), ("flac files", "*.flac"))))
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



        




                