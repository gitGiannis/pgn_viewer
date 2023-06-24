# -------------------------------------------------------------------------------------------------------------------- #
# listbox_game_display.py: περιέχει την κλάση ListboxGameDisplay                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Frame, Button, Listbox, Label, Scrollbar
from pgn import FilePGN
from game_loader import GameLoader
from gui import GUI
from my_exceptions import PossibleCorruptFile, NoMovesFound, FriendlyCapture


class ListboxGameDisplay(Frame):
    """
    Κατασκευάζει ένα νέο frame και τοποθετεί σε αυτό listbox με τα αρχεία pgn ενός προκαθορισμένου φακέλου (pgn_files)
    Από αυτά τα αρχεία ο χρήστης μπορεί να φορτώνει τα παιχνίδια και να επιλέγει το παιχνίδι που θέλει να τρέξει
    Κληρονομεί από την κλάση tkinter.Frame

    Ορίσματα:
    ---------
        root (main_program.MainProgram):
            κύριο παράθυρο της εφαρμογής

        pgn_list (list):
            λίστα με τα αρχεία pgn ενός φακέλου

    Μέθοδοι:
    --------
        run_game(self):
            προβάλει το παιχνίδι που επιλέχθηκε

        load_file(self, event):
            φορτώνει τα παιχνίδια ενός αρχείου

        __pack_widgets():
            τοποθέτηση widgets

        retrieve_master():
            επαναφέρει το κύριο πλαίσιο
    """
    def __init__(self, root, pgn_list: list):
        # κλήση της super() για αρχικοποίηση γονικής κλάσης
        super().__init__()
        self.config(bg="light blue")
        # ορισμός master του frame
        self.root = root
        # δημιουργία πίνακα για συλλογή των game_dictionaries κάθε παιχνιδιού
        self.game_dict_collection = []
        # ενεργοποίηση επιλογής "back" στο μενού μπάρας
        self.root.file_menu.entryconfig(5, state="normal", command=self.retrieve_master)

        # αρχικοποίηση λίστας με τα αρχεία pgn που βρέθηκαν ------------------------------------------------------------
        self.pgn_list = []
        for item in pgn_list:
            if ".pgn" in item:
                # εξαιρούνται όσα αρχεία δεν είναι *.pgn
                self.pgn_list.append(item)

        # αρχικοποίηση πλαισίου που θα περιέχει τα παιχνίδια που διαβάστηκαν από το αρχείο pgn -------------------------
        # δημιουργία listbox
        self.pgn_listbox = Listbox(self, bg="#f7ffde", width=30, height=20, font=("consolas", 10))
        self.game_listbox = Listbox(self, bg="#f7ffde", width=60, height=20, font=("consolas", 10))

        # δημιουργία scrollbars για τα listbox
        self.scrollbar1 = Scrollbar(master=self, command=self.pgn_listbox.yview)
        self.scrollbar2 = Scrollbar(master=self, command=self.game_listbox.yview)

        # σύνδεση Listbox με Scrollbar
        self.pgn_listbox.config(yscrollcommand=self.scrollbar1.set)
        self.game_listbox.config(yscrollcommand=self.scrollbar2.set)

        # προσθήκη αρχείων pgn στο pgn_listbox
        for item in self.pgn_list:
            self.pgn_listbox.insert("end", item)

        # ετικέτα με σφάλμα μη επιλογής --------------------------------------------------------------------------------
        self.warning_label = Label(self,
                                   bg="light blue",
                                   fg="red",
                                   font=("consolas", 10, "bold"),
                                   pady=5)

        # αρχικοποίηση κουμπιών ----------------------------------------------------------------------------------------
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

        # χειρισμός event όταν επιλέγει κάτι από το Listbox ------------------------------------------------------------
        self.pgn_listbox.bind(sequence="<<ListboxSelect>>", func=self.load_file)

        # τοποθέτηση στο παράθυρο --------------------------------------------------------------------------------------
        self.__pack_widgets()

    def run_game(self):
        """
        Προβάλει το παιχνίδι που επιλέχθηκε
        """
        # αποθηκεύουμε τις πληροφορίες της επιλογής του χρήστη από το listbox
        index = self.game_listbox.curselection()
        # εάν επιλέξει κάτι...
        if index:
            # κρατάμε το πρώτο κομμάτι του επιστρεφόμενου tuple (ακέραιος δείκτης αγώνα)
            index_for_collection: int = index[0]
            current_game_dictionary = self.game_dict_collection[index_for_collection]

            try:
                # συλλογή των στιγμιοτύπων του παιχνιδιού μέσω της κλάσης GameLoader
                game_loader = GameLoader(list_of_moves=current_game_dictionary["moves"])
                # τρέχουμε το GUI (γραφική αναπαράσταση παιχνιδιού) με το συγκεκριμένο παιχνίδι
                GUI(game_loader, current_game_dictionary)
            except (PossibleCorruptFile, NoMovesFound, FriendlyCapture) as v:
                self.warning_label.config(text=str(v))
                self.warning_label.grid(row=1, column=1, columnspan=2, sticky="nw")
                self.warning_label.after(3000, self.warning_label.grid_forget)
        else:
            # εμφάνιση μηνύματος σφάλματος σε περίπτωση που δεν έχει γίνει επιλογή
            self.warning_label.config(text="Select a game to continue")
            self.warning_label.grid(row=1, column=1, columnspan=2, sticky="nw")
            self.warning_label.after(3000, self.warning_label.grid_forget)

    def load_file(self, event):
        """
        Φορτώνει τα παιχνίδια ενός αρχείου

        Ορίσματα:
            event (<<ListboxSelect>>):
                όταν επιλέγεται ένα αρχείο του listbox εκτελείται η μέθοδος
        """
        if self.pgn_listbox.curselection():
            # καθαρισμός λεξικού και listbox από προηγούμενη φόρτωση παιχνιδιών
            self.game_dict_collection.clear()
            self.game_listbox.delete(0, "end")

            try:
                # δημιουργία αντικειμένου για εξαγωγή πληροφοριών
                file = FilePGN("pgn_files\\" + self.pgn_listbox.get(self.pgn_listbox.curselection()))
            except OSError:
                # εμφάνιση μηνύματος σφάλματος σε περίπτωση αποτυχία διαβάσματος αρχείου
                self.warning_label.config(text="Could not open file")
                self.warning_label.grid(row=1, column=1, columnspan=2, sticky="nw")
                self.warning_label.after(3000, self.warning_label.grid_forget)
            else:
                # προσθήκη παιχνιδιών που διαβάστηκαν, στο listbox
                for i, num in enumerate(file.index_of_games):
                    # δημιουργία του λεξικού με τη μέθοδο get_info της κλάσης FilePGN
                    game_dictionary = file.get_info(num)
                    # προσθήκη του λεξικού στη συλλογή με τα λεξικά του συγκεκριμένου αρχείου pgn
                    self.game_dict_collection.append(game_dictionary)
                    self.game_listbox.insert(i, f'{str(i + 1) + ".":4}{game_dictionary["White"]} vs '
                                                f'{game_dictionary["Black"]} '
                                                f'({game_dictionary["Result"]})')
                    # εμφάνιση αποτελεσμάτων ανα εκατό, για ανανέωση του παραθύρου εάν έχουμε πολλά αρχεία
                    if i % 100 == 0:
                        self.update()

    def __pack_widgets(self):
        """
        Τοποθετεί τα widgets στο πλαίσιο και το πλαίσιο στο κυρίως παράθυρο
        """
        # τοποθέτηση στο πλαίσιο
        self.pgn_listbox.grid(row=0, column=0, sticky="nw")
        self.game_listbox.grid(row=0, column=2, sticky="ne")
        self.scrollbar1.grid(row=0, column=1, sticky="ns")
        self.scrollbar2.grid(row=0, column=3, sticky="ns")
        self.button_back.grid(row=1, column=0, sticky="sw")
        self.button_run.grid(row=1, column=2, columnspan=2, sticky="se")

        # προσθήκη πλαισίου στο κυρίως παράθυρο
        self.pack()

    def retrieve_master(self):
        """
        Επαναφέρει το κύριο πλαίσιο
        """
        # επαναφορά κύριου πλαισίου
        self.root.main_frame.pack()
        # επαναφορά μενού
        self.root.file_menu.entryconfig(0, state="normal")
        self.root.file_menu.entryconfig(1, state="normal")
        self.root.file_menu.entryconfig(3, state="normal")
        self.root.file_menu.entryconfig(5, state="disabled")
        # τερματισμός τρέχοντος frame
        self.destroy()
