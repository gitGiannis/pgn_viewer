# -------------------------------------------------------------------------------------------------------------------- #
# manual_game_selector.py: περιέχει την κλάση ManualGameSelector                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Frame, Button, Listbox, Scrollbar, Label
from game_loader import GameLoader
from gui import GUI
from pgn import FilePGN
from my_exceptions import PossibleCorruptFile, NoMovesFound, FriendlyCapture, FalseGame


class ManualGameSelector(Frame):
    """
    Inherits from parent class Frame and opens a Windows explorer window
    Through this window, the user can manually select the pgn file he/she wants to load
    If a valid file type is selected, a new frame is created that stores all the games of the selected pgn file inside
    a listbox

    ...

    Attributes:
    -----------
        button_back (Button):
            button to go back to main frame

        button_run (Button):
            button to run the selected game

        game_dict_collection (list[dict]):
            list of dictionaries for each game

        listbox (Listbox):
            listbox to store the games of the selected file

        root (Tk):
            master window

        scrollbar (Scrollbar):
            scrollbar for the listbox

        warning_label (Label):
            label to show messages to the user

    Methods:
    --------
        display_game():
            displays the selected game

        __fill_listbox():
            adds games in listbox

        __pack_widgets():
            places widgets

        retrieve_master():
            retrieves master frame
    """
    def __init__(self, root, pgn_filepath: str):
        """
        Initializes the frame for manual selection

        ...

        Parameters:
        -----------
            root (main_program.MainProgram):
                κύριο παράθυρο της εφαρμογής

            pgn_filepath (str):
                διεύθυνση αρχείου pgn που επιλέχθηκε
        """
        # initialization of parent class (Frame)
        super().__init__()
        self.config(bg="light blue")
        # master of the frame
        self.root = root
        # selected filepath
        self.__filepath = pgn_filepath
        # initialization of list to store the dictionaries for each game
        self.game_dict_collection = []
        # back option enabled (in file sub-menu)
        self.root.file_menu.entryconfig(5, state="normal", command=self.retrieve_master)

        # initialization of listbox and label --------------------------------------------------------------------------
        self.warning_label = Label(self, bg="light blue", fg="red", font=("consolas", 10, "bold"), pady=5)
        self.listbox = Listbox(self, bg="#f7ffde", width=80, height=20, font=("consolas", 10))

        # scrollbar added to listbox
        self.scrollbar = Scrollbar(master=self, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # initialization of buttons ------------------------------------------------------------------------------------
        self.button_run = Button(self,
                                 text="Run",
                                 font=("consolas", 12, "bold"),
                                 background="light green",
                                 activebackground="green",
                                 width=12,
                                 command=self.display_game)

        self.button_back = Button(self,
                                  text="Back",
                                  font=("consolas", 12, "bold"),
                                  background="light green",
                                  activebackground="green",
                                  width=12,
                                  command=self.retrieve_master)

        # packing widgets ----------------------------------------------------------------------------------------------
        self.__pack_widgets()

        # add games in listbox -----------------------------------------------------------------------------------------
        self.__fill_listbox()

    def display_game(self):
        """
        Displays the selected game
        """
        # storing the user's selection
        index = self.listbox.curselection()
        # if something is selected...
        if index:
            # ... the first part of the returned tuple is kept
            index_for_collection: int = index[0]
            current_game_dictionary = self.game_dict_collection[index_for_collection]

            try:
                # collecting screenshot of game through the GameLoader object
                game_loader = GameLoader(current_game_dictionary["moves"])
                # running GUI for selected game
                GUI(game_loader, current_game_dictionary)
            except (FalseGame, PossibleCorruptFile, NoMovesFound, FriendlyCapture) as v:
                self.warning_label.config(text=str(v))
                self.warning_label.grid(row=1, column=0, columnspan=2, sticky="n")
                self.warning_label.after(3000, self.warning_label.grid_forget)
        else:
            # no selection was made
            self.warning_label.config(text="Select a game to continue")
            self.warning_label.grid(row=1, column=0, columnspan=2, sticky="n")
            self.warning_label.after(3000, self.warning_label.grid_forget)

    def __fill_listbox(self):
        """
        Fills the listbox with the games loaded from the pgn file
        """
        try:
            # FilePGN object is used to extract information
            file = FilePGN(self.__filepath)
        except OSError:
            self.retrieve_master()
            raise OSError
        except PossibleCorruptFile:
            self.retrieve_master()
            raise PossibleCorruptFile
        else:
            # games loaded are added to the listbox
            for i, num in enumerate(file.index_of_games):
                # dictionary creation through the get_info method
                game_dictionary = file.get_info(num)
                # dictionary gets added to the collection
                self.game_dict_collection.append(game_dictionary)
                self.listbox.insert(i, f'{str(i + 1) + ".":4}{game_dictionary["White"]} vs '
                                       f'{game_dictionary["Black"]} '
                                       f'({game_dictionary["Result"]})')
                # showing results by 100, if many games were loaded
                if i % 100 == 0:
                    self.update()

    def __pack_widgets(self):
        """
        Places the widgets in the frame
        """
        # τοποθέτηση στο πλαίσιο
        self.listbox.grid(row=0, column=0, sticky="ne")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.button_back.grid(row=1, column=0, sticky="w")
        self.button_run.grid(row=1, column=0, columnspan=2, sticky="e")

        # frame gets packed
        self.pack()

    def retrieve_master(self):
        """
        Main frame retrieval
        """
        # main frame retrieval
        self.root.main_frame.pack()
        # menu retrieval
        self.root.file_menu.entryconfig(0, state="normal")
        self.root.file_menu.entryconfig(1, state="normal")
        self.root.file_menu.entryconfig(3, state="normal")
        self.root.file_menu.entryconfig(5, state="disabled")
        # current frame gets destroyed
        self.destroy()
