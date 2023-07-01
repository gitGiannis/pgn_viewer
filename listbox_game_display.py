# -------------------------------------------------------------------------------------------------------------------- #
# listbox_game_display.py: includes class ListboxGameDisplay                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Frame, Button, Listbox, Label, Scrollbar
from pgn import FilePGN
from game_loader import GameLoader
from gui import GUI
from my_exceptions import PossibleCorruptFile, NoMovesFound, FriendlyCapture, FalseGame


class ListboxGameDisplay(Frame):
    """
    Inherits from parent class Frame and adds in a listbox all the pgn files found inside the pre-selected directory
    User can then select any of those and load the games they contain

    ...

    Attributes:
    -----------
        button_back (Button):
            button to go back to main frame

        button_run (Button):
            button to run the selected game

        game_dict_collection (list[dict]):
            list of dictionaries for each game

        pgn_listbox (Listbox):
            listbox to store the pgn files found

        game_listbox (Listbox):
            listbox to store the games of the selected file

        pgn_list (list):
            list with pgn files found

        root (Tk):
            master window

        scrollbar1,2 (Scrollbar):
            scrollbars for list-boxes

        warning_label (Label):
            label to show messages to the user

    Methods:
    --------
        run_game(self):
            displays the selected game

        load_file(self, event):
            loads the games of a file

        __pack_widgets():
            places widgets

        retrieve_master():
            retrieves master frame
    """
    def __init__(self, root, pgn_list: list):
        """
        Initializes the frame for listbox file selection

        ...

        Parameters:
        -----------
            root (Tk):
                main window

            pgn_list (list):
                list with pgn files found
        """
        # initialization of parent class (Frame)
        super().__init__()
        self.config(bg="light blue")
        # # master of the frame
        self.root = root
        # initialization of list to store the dictionaries for each game
        self.game_dict_collection = []
        # back option enabled (in file sub-menu)
        self.root.file_menu.entryconfig(5, state="normal", command=self.retrieve_master)

        # initialization of list with pgn files found ------------------------------------------------------------------
        self.pgn_list = []
        for item in pgn_list:
            if ".pgn" in item:
                # all files that are not the correct type get excluded
                self.pgn_list.append(item)

        # initialization of list-boxes ---------------------------------------------------------------------------------
        self.pgn_listbox = Listbox(self, bg="#f7ffde", width=30, height=20, font=("consolas", 10))
        self.game_listbox = Listbox(self, bg="#f7ffde", width=60, height=20, font=("consolas", 10))

        # initialization of scrollbars for list-boxes
        self.scrollbar1 = Scrollbar(master=self, command=self.pgn_listbox.yview)
        self.scrollbar2 = Scrollbar(master=self, command=self.game_listbox.yview)

        # scrollbars added to list-boxes
        self.pgn_listbox.config(yscrollcommand=self.scrollbar1.set)
        self.game_listbox.config(yscrollcommand=self.scrollbar2.set)

        # adding pgn files in listbox
        for item in self.pgn_list:
            self.pgn_listbox.insert("end", item)

        # initialization of label to show messages to user -------------------------------------------------------------
        self.warning_label = Label(self, bg="light blue", fg="red", font=("consolas", 10, "bold"), pady=5)

        # initialization of buttons ------------------------------------------------------------------------------------
        self.button_run = Button(self,
                                 text="Run",
                                 font=("consolas", 12, "bold"),
                                 background="light green",
                                 activebackground="green",
                                 width=12,
                                 command=self.run_game)

        self.button_back = Button(self,
                                  text="Back",
                                  font=("consolas", 12, "bold"),
                                  background="light green",
                                  activebackground="green",
                                  width=12,
                                  command=self.retrieve_master)

        # event binding for listbox selection --------------------------------------------------------------------------
        self.pgn_listbox.bind(sequence="<<ListboxSelect>>", func=self.load_file)

        # widget placing -----------------------------------------------------------------------------------------------
        self.__pack_widgets()

    def run_game(self):
        """
        Displays the selected game
        """
        # storing the user's selection
        index = self.game_listbox.curselection()
        # if something is selected...
        if index:
            # ... the first part of the returned tuple is kept
            index_for_collection: int = index[0]
            current_game_dictionary = self.game_dict_collection[index_for_collection]

            try:
                # collecting screenshot of game through the GameLoader object
                game_loader = GameLoader(list_of_moves=current_game_dictionary["moves"])
                # running GUI for selected game
                GUI(game_loader, current_game_dictionary)
            except (FalseGame, PossibleCorruptFile, NoMovesFound, FriendlyCapture) as v:
                self.warning_label.config(text=str(v))
                self.warning_label.grid(row=1, column=1, columnspan=2, sticky="nw")
                self.warning_label.after(3000, self.warning_label.grid_forget)
        else:
            # no selection was made
            self.warning_label.config(text="Select a game to continue")
            self.warning_label.grid(row=1, column=1, columnspan=2, sticky="nw")
            self.warning_label.after(3000, self.warning_label.grid_forget)

    def load_file(self, event):
        """
        Loads the selected file

        ...

        Parameters:
        -----------
            event (<<ListboxSelect>>):
                method gets called when a listbox item is selected
        """
        if self.pgn_listbox.curselection():
            # clearing listbox and dictionary from previous selection
            self.game_dict_collection.clear()
            self.game_listbox.delete(0, "end")

            try:
                # FilePGN object is used to extract information
                file = FilePGN("pgn_files\\" + self.pgn_listbox.get(self.pgn_listbox.curselection()))
            except OSError:
                self.warning_label.config(text="Could not open file")
                self.warning_label.grid(row=1, column=1, columnspan=2, sticky="nw")
                self.warning_label.after(3000, self.warning_label.grid_forget)
            except PossibleCorruptFile as v:
                self.warning_label.config(text=str(v))
                self.warning_label.grid(row=1, column=1, columnspan=2, sticky="nw")
                self.warning_label.after(3000, self.warning_label.grid_forget)
            else:
                # games get added to the listbox
                for i, num in enumerate(file.index_of_games):
                    # dictionary creation through the get_info method
                    game_dictionary = file.get_info(num)
                    # dictionary gets added to the collection
                    self.game_dict_collection.append(game_dictionary)
                    self.game_listbox.insert(i, f'{str(i + 1) + ".":4}{game_dictionary["White"]} vs '
                                                f'{game_dictionary["Black"]} '
                                                f'({game_dictionary["Result"]})')
                    # showing results by 100, if many games were loaded
                    if i % 100 == 0:
                        self.game_listbox.update()

    def __pack_widgets(self):
        """
        Places the widgets in the frame
        """
        # τοποθέτηση στο πλαίσιο
        self.pgn_listbox.grid(row=0, column=0, sticky="nw")
        self.game_listbox.grid(row=0, column=2, sticky="ne")
        self.scrollbar1.grid(row=0, column=1, sticky="ns")
        self.scrollbar2.grid(row=0, column=3, sticky="ns")
        self.button_back.grid(row=1, column=0, sticky="sw")
        self.button_run.grid(row=1, column=2, columnspan=2, sticky="se")

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
