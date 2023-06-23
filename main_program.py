# -------------------------------------------------------------------------------------------------------------------- #
# main_program.py: περιέχει την κλάση MainProgram για έναρξη κυρίως παραθύρου                                          #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Tk, Menu, Button, Label, Frame, PhotoImage
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from os import listdir, mkdir
from os.path import abspath
from manual_game_selector import ManualGameSelector
from listbox_game_display import ListboxGameDisplay
from functions import show_help, show_info, show_credits, about
from submit_feedback import FeedBack


class MainProgram(Tk):
    """
    Δημιουργεί το κύριο παράθυρο γραφικής αλληλεπίδρασης με τον χρήστη
    Από εδώ ο χρήστης μπορεί να επιλέξει τον τρόπο που θα αναζητήσει τα αρχεία pgn και το αρχείο που θέλει να προβάλει
    Κληρονομεί τις ιδιότητές του από το tkinter.Tk

    Μέθοδοι:
    --------
        select_file(self):
            ανοίγει παράθυρο εξερεύνησης των windows για χειροκίνητη επιλογή αρχείου pgn

        open_file(self):
            φορτώνει τα αρχεία pgn που βρέθηκαν σε έναν προκαθορισμένο φάκελο

        submit_fb(self):
            λήψη ανατροφοδότησης από τον χρήστη

        copy_path(self):
            αντιγραφή απόλυτης διεύθυνσης προκαθορισμένου φακέλου με αρχεία pgn

        exit(self):
            καταστρέφει το παράθυρο και τερματίζει το πρόγραμμα
    """

    def __init__(self):
        """
        Μέθοδος για αρχικοποίηση αντικειμένου της κλάσης και άνοιγμα του παραθύρου διεπαφής
        """
        # αρχικοποίηση παραθύρου γραφικών ------------------------------------------------------------------------------
        # κλήση της super για κληρονόμηση ιδιοτήτων γονικής κλάσης
        super().__init__()
        # αφαίρεση ικανότητας χρήστη να τροποποιεί το μέγεθος του παραθύρου
        self.resizable(False, False)
        # εικονίδιο εφαρμογής
        self.iconbitmap("icons\\stonk.ico")
        # όνομα εφαρμογής
        self.title("Chess PGN manager v1.0")

        # δημιουργία μπάρας μενού --------------------------------------------------------------------------------------
        self.menubar = Menu(self)
        # μενού File
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="  File  ", menu=self.file_menu)
        # μενού Help
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="  Help  ", menu=self.help_menu)

        # υπο-μενού File
        self.file_menu.add_command(label="Show Files", command=self.show_files)
        self.file_menu.add_command(label="Select File", command=self.select_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Copy Path", command=self.copy_path)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Back", state="disabled")
        self.file_menu.add_command(label="Exit", command=self.exit)

        # υπο-μενού Help
        self.help_menu.add_command(label="Help", command=show_help)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About PGN", command=show_info)
        self.help_menu.add_command(label="App Info", command=about)
        self.help_menu.add_command(label="Show Credits", command=show_credits)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Submit Feedback", command=self.submit_fb)

        # δημιουργία frame μέσα στο οποίο θα τοποθετηθούν τα κουμπιά κλπ -----------------------------------------------
        self.main_frame = Frame(master=self, bg="light blue")
        # δημιουργία ετικέτας με εικόνα για το παρασκήνιο
        chess_image = PhotoImage(master=self.main_frame, file="icons\\chess.png")
        Label(master=self.main_frame,
              image=chess_image,
              width=550,
              background="light yellow").pack()

        # δημιουργία και τοποθέτηση κουμπιών ---------------------------------------------------------------------------
        Button(self.main_frame,
               text="Select File",
               font=("consolas", 12, "bold"),
               background="light green",
               activebackground="green",
               width="15",
               command=self.select_file).pack(side="right")
        Button(self.main_frame,
               text="Show Files",
               font=("consolas", 12, "bold"),
               background="light green",
               activebackground="green",
               width="15",
               command=self.show_files).pack(side="left")

        # Label για προβολή μηνυμάτων προς χρήστη ----------------------------------------------------------------------
        self.warning_label = Label(self.main_frame,
                                   bg="light blue",
                                   fg="red",
                                   font=("consolas", 12, "bold"),
                                   pady=5)

        # τοποθέτηση μπάρας μενού και καθορισμός χρώματος φόντου
        self.config(menu=self.menubar, background="light blue")
        # τοποθέτηση του frame στο παράθυρο
        self.main_frame.pack(fill="x")

        # επιβεβαίωση εξόδου από το πρόγραμμα
        self.protocol("WM_DELETE_WINDOW", self.exit)
        # έναρξη λειτουργίας παραθύρου ---------------------------------------------------------------------------------
        self.mainloop()

    def select_file(self):
        """
        Ανοίγει παράθυρο εξερεύνησης των windows για χειροκίνητη επιλογή αρχείου
        """
        # άνοιγμα παραθύρου εξερεύνησης των windows
        file_path = askopenfilename(initialdir="pgn_files",
                                    title="Choose PGN file",
                                    filetypes=(("PGN files", "*.pgn"), ("All files", "*.*")))
        if file_path:
            # έλεγχος για ορθότητα τύπου αρχείου
            if file_path[-4:] == ".pgn":
                # απόκρυψη κύριου πλαισίου
                self.main_frame.forget()
                self.file_menu.entryconfig(0, state="disabled")
                self.file_menu.entryconfig(1, state="disabled")
                self.file_menu.entryconfig(3, state="disabled")

                try:
                    # τοποθέτηση frame με τους αγώνες για επιλογή παιχνιδιού
                    ManualGameSelector(root=self, pgn_filepath=file_path)
                except OSError:
                    # εμφάνιση μηνύματος σφάλματος σε περίπτωση αποτυχία διαβάσματος αρχείου
                    self.warning_label.config(text="Could not open file")
                    self.warning_label.pack(fill="both")
                    self.warning_label.after(2000, self.warning_label.pack_forget)
            else:
                # το αρχείο είναι λάθος τύπου
                self.warning_label.config(text="Invalid File Type!")
                self.warning_label.pack(fill="both")
                self.warning_label.after(2000, self.warning_label.pack_forget)

    def show_files(self):
        """
        Φορτώνει τα αρχεία pgn που βρέθηκαν σε έναν προκαθορισμένο φάκελο και τα προβάλει στο παράθυρο διεπαφής
        """
        try:
            # λίστα με τα περιεχόμενα του φακέλου
            list_dir = listdir("pgn_files")
        except FileNotFoundError:
            # εάν ο φάκελος δεν υπάρχει ή έχει διαγραφεί, δημιουργείται εξ αρχής άδειος,
            # ώστε να προσθέσει ο χρήστης αρχεία pgn
            mkdir("pgn_files")
            list_dir = []

        # έλεγχος για ορθότητα τύπου αρχείου
        for pgn_file_path in list_dir:
            if pgn_file_path[-4:] != ".pgn":
                # αφαίρεση αρχείων που δεν πληρούν τα κριτήρια (κατάληξη .pgn)
                list_dir.remove(pgn_file_path)

        if list_dir:
            # απόκρυψη κύριου πλαισίου
            self.main_frame.forget()
            self.file_menu.entryconfig(0, state="disabled")
            self.file_menu.entryconfig(1, state="disabled")
            self.file_menu.entryconfig(3, state="disabled")

            # άνοιγμα παραθύρου με τα αρχεία pgn για επιλογή αρχείου
            ListboxGameDisplay(root=self, pgn_list=list_dir)
        else:
            # δε βρέθηκε αρχείο ή τα αρχεία που βρέθηκαν δεν πληρούν τα κριτήρια
            self.warning_label.config(text="No Files Found!")
            self.warning_label.pack(fill="both")
            self.warning_label.after(2000, self.warning_label.pack_forget)

    def submit_fb(self):
        """
        Λήψη ανατροφοδότησης από τον χρήστη
        """
        FeedBack(master=self)

    def copy_path(self):
        """
        Αντιγραφή απόλυτης διεύθυνσης προκαθορισμένου φακέλου με αρχεία pgn
        """
        self.clipboard_clear()
        self.clipboard_append(abspath("pgn_files"))
        self.warning_label.config(text="Copied 'pgn_files' dir path")
        self.warning_label.pack(fill="both")
        self.warning_label.after(2000, self.warning_label.pack_forget)

    def exit(self):
        """
        Καταστρέφει το παράθυρο και τερματίζει το πρόγραμμα
        Εμφανίζει messagebox με επιλογή yes/no
        """
        if askyesno(master=self,
                    title="Quit?",
                    message="Do you really wish to quit?",
                    default="no"):
            self.destroy()
