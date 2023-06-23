# -------------------------------------------------------------------------------------------------------------------- #
# gui.py: περιέχει την κλάση GUI                                                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Tk, Menu, PhotoImage, Frame, Label, Button, IntVar
from tkinter.messagebox import askyesno, showinfo
from pygame import mixer
from my_exceptions import PositionReached
from info_frame_for_gui import InfoFrame
from captured_piece_frame import CapturedPieceFrame


class GUI(Tk):
    """
    Ανοίγει ένα παράθυρο με το πλαίσιο της σκακιέρας και εκτελεί τις κινήσεις του αγώνα με γραφική 2D αναπαράσταση
    Ο χρήστης, αφού πραγματοποιήσει έναρξη του αγώνα και θέσει τα κομμάτια στις θέσεις τους, μπορεί να επιλέξει να
    κινηθεί εμπρός - πίσω στην αλληλουχία των κινήσεων
    Στο δεξί μέρος του παραθύρου γίνεται προβολή των λεπτομερειών του αγώνα

    Ορίσματα:
    ---------
        game_loader_obj (game_loader.GameLoader):
            αντικείμενο με τα στιγμιότυπα του αγώνα, καθώς και άλλες πληροφορίες

        game_dict (dict):
            λεξικό με τις πληροφορίες του αγώνα

    Μέθοδοι:
    --------
        update_gui_board(self):
            πραγματοποιεί ανανέωση του γραφικού περιβάλλοντος μετά από κάθε κίνηση

        next_move(self):
            μετάβαση στην επόμενη κίνηση του αγώνα

        previous_move(self):
            μετάβαση στην προηγούμενη κίνηση του αγώνα

        start_game(self):
            εκκίνηση του αγώνα

        restart_game(self):
            επανεκκίνηση του αγώνα

        autoplay(self):
            εκτελεί αυτόματη αναπαραγωγή του παιχνιδιού

        text_config(self) -> str:
            διαχειρίζεται και επιστρέφει συμβολοσειρά με πληροφορίες για την επόμενη κίνηση

        show_controls(self):
            εμφανίζει παράθυρο με τις οδηγίες χρήσης του παραθύρου

        exit(self):
            ζητά επιβεβαίωση εξόδου από την αναπαραγωγή του παιχνιδιού

        right_key_bind(self, event):
            εκτελεί την επόμενη κίνηση χρησιμοποιώντας key-event <δεξί-βέλος>
            εάν το παιχνίδι βρίσκεται στην τελευταία κίνηση, δεν εκτελεί κάτι

        left_key_bind(self, event):
            εκτελεί την προηγούμενη κίνηση χρησιμοποιώντας key-event <αριστερό-βέλος>
            εάν το παιχνίδι βρίσκεται στην πρώτη κίνηση, δεν εκτελεί κάτι

        down_key_bind(self, event):
            επιστρέφει το ταμπλό στην αρχική θέση χρησιμοποιώντας key-event <κάτω-βέλος>
            εάν το παιχνίδι βρίσκεται στην πρώτη κίνηση, δεν εκτελεί κάτι

        up_key_bind(self, event):
            ενεργοποιεί την αυτόματη αναπαραγωγή του αγώνα χρησιμοποιώντας key-event <πάνω-βέλος>
            εάν το παιχνίδι βρίσκεται στην τελευταία κίνηση, δεν εκτελεί κάτι
    """
    def __init__(self, game_loader_obj, game_dict: dict):
        # κλήση της super για κληρονόμηση ιδιοτήτων γονικής κλάσης
        super().__init__()
        # αρχικοποίηση παραθύρου γραφικών ------------------------------------------------------------------------------
        # τίτλος και εικονίδιο παραθύρου
        self.title(f"Chess Match: W: {game_dict['White']} vs B: {game_dict['Black']} - ({game_dict['Result']})")
        self.iconbitmap("icons\\stonk.ico")

        # αφαίρεση ικανότητας χρήστη να τροποποιεί το μέγεθος του παραθύρου
        self.resizable(False, False)

        # συλλογή των στιγμιοτύπων του παιχνιδιού ----------------------------------------------------------------------
        self.game_loader = game_loader_obj

        self.__result = game_dict["Result"]

        # δημιουργία μπάρας μενού --------------------------------------------------------------------------------------
        menubar = Menu(self)

        # υπο-μενού File
        self.file_menu = Menu(menubar, tearoff=0)
        # προσθήκη υπο-μενού File στην μπάρα μενού
        menubar.add_cascade(label="  File  ", menu=self.file_menu)
        # προσθήκη επιλογών
        self.file_menu.add_checkbutton(label="Autoplay", command=self.autoplay)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)

        # υπο-μενού Help
        help_menu = Menu(menubar, tearoff=0)
        # προσθήκη υπο-μενού Help στην μπάρα μενού
        menubar.add_cascade(label="  Help  ", menu=help_menu)
        # προσθήκη επιλογών
        help_menu.add_command(label="Help", command=self.show_controls)

        # αρχικοποίηση ήχου --------------------------------------------------------------------------------------------
        mixer.init()

        # αρχικοποίηση εικόνων -----------------------------------------------------------------------------------------
        # αρχικοποίηση εικόνας κενών κελιών
        self.blank = PhotoImage(master=self, file="icons\\piece_icons\\BLANK_ICON.png")

        # αρχικοποίηση εικόνων μαύρων κομματιών
        self.rb_image = PhotoImage(master=self, file="icons\\piece_icons\\rb.png")
        self.nb_image = PhotoImage(master=self, file="icons\\piece_icons\\nb.png")
        self.bb_image = PhotoImage(master=self, file="icons\\piece_icons\\bb.png")
        self.qb_image = PhotoImage(master=self, file="icons\\piece_icons\\qb.png")
        self.kb_image = PhotoImage(master=self, file="icons\\piece_icons\\kb.png")
        self.pb_image = PhotoImage(master=self, file="icons\\piece_icons\\pb.png")

        # αρχικοποίηση εικόνων λευκών κομματιών
        self.rw_image = PhotoImage(master=self, file="icons\\piece_icons\\rw.png")
        self.nw_image = PhotoImage(master=self, file="icons\\piece_icons\\nw.png")
        self.bw_image = PhotoImage(master=self, file="icons\\piece_icons\\bw.png")
        self.qw_image = PhotoImage(master=self, file="icons\\piece_icons\\qw.png")
        self.kw_image = PhotoImage(master=self, file="icons\\piece_icons\\kw.png")
        self.pw_image = PhotoImage(master=self, file="icons\\piece_icons\\pw.png")

        # αρχικοποίηση εικόνων βασιλιάδων με ματ
        self.kb_checked = PhotoImage(master=self, file="icons\\piece_icons\\kb_checked.png")
        self.kw_checked = PhotoImage(master=self, file="icons\\piece_icons\\kw_checked.png")

        # αρχικοποίηση πλαισίου σκακιέρας ------------------------------------------------------------------------------
        self.frame = Frame(self, bd=10, relief="raised")

        # δημιουργία πίνακα με ετικέτες (labels)
        self.board = []
        for row in range(8):
            temp = []
            for col in range(8):
                # γίνεται αρχικοποίηση όλων των ετικετών με την κενή εικόνα, μέχρι να γίνει η έναρξη
                temp.append(Label(self.frame, image=self.blank, bd=7))
            self.board.append(temp)

        for row in range(8):
            for col in range(8):
                self.board[row][col].grid(row=row, column=col)
                if (row + col) % 2 == 0:
                    self.board[row][col].config(bg="#EEEED2")
                else:
                    self.board[row][col].config(bg="#47473C")

        # προσθήκη συντεταγμένων στα εξωτερικά κελιά της σκακιέρας
        letters = self.game_loader.gameplay.files
        numbers = self.game_loader.gameplay.ranks
        # αριθμός pixel πάνω στο frame
        position = 0
        # τοποθέτηση γράμματος/αριθμού στα ακραία κελιά και προσθήκη κατάλληλων background και foreground χρωμάτων
        for num in range(8):
            if num % 2 == 0:
                # ετικέτα με αριθμό
                Label(master=self.frame,
                      bg="#47473C",
                      fg="#EEEED2",
                      font=("consolas", 10, "bold"),
                      text=numbers[7-num]).place(relx=0.97, y=position)
                # ετικέτα με γράμμα
                Label(master=self.frame,
                      bg="#47473C",
                      fg="#EEEED2",
                      font=("consolas", 10, "bold"),
                      text=letters[num]).place(x=position, rely=0.96)
            else:
                # ετικέτα με αριθμό
                Label(master=self.frame,
                      bg="#EEEED2",
                      fg="#47473C",
                      font=("consolas", 10, "bold"),
                      text=numbers[7-num]).place(relx=0.97, y=position)
                # ετικέτα με γράμμα
                Label(master=self.frame,
                      bg="#EEEED2",
                      fg="#47473C",
                      font=("consolas", 10, "bold"),
                      text=letters[num]).place(x=position, rely=0.96)
            # επαύξηση θέσης (pixel) πάνω στο frame κατά 74 pixel
            # 60 pixel η εικόνα του κομματιού και 7+7 το εξωτερικό border που έχω ορίσει στα Labels
            position += 74

        # αρχικοποίηση βοηθητικής μεταβλητής
        self.starting_move = True
        self.ending_move = False

        # διαμόρφωση επιλογής autoplay ---------------------------------------------------------------------------------
        # αρχικοποίηση μεταβλητής τύπου int που θα ελέγχει το checkbutton
        self.checkbutton_var = IntVar(master=self.file_menu)
        # ανάθεση της μεταβλητής στο checkbutton και διαμόρφωση αρχικής του κατάστασης
        self.file_menu.entryconfig(0, variable=self.checkbutton_var, state="disabled")
        # συμβολοσειρά για αποθήκευση identifier της self.after() για ακύρωσή της (η μέθοδος after() επιστρέφει ένα
        # αναγνωριστικό, σε περίπτωση που θέλουμε να την ακυρώσουμε με τη μέθοδο after_cancel() )
        self.__identifier_for_after_method = ""

        # αρχικοποίηση κουμπιών και πλαισίου που θα τα συμπεριλάβει ----------------------------------------------------
        # δημιουργία πλαισίου κομβίων
        button_frame = Frame(master=self, bg="light blue")

        self.button_next = Button(button_frame,
                                  text="---->",
                                  state="disabled",
                                  font=("consolas", 12, "bold"),
                                  background="light green",
                                  activebackground="green",
                                  width=8,
                                  command=self.next_move)

        self.button_prev = Button(button_frame,
                                  text="<----",
                                  state="disabled",
                                  font=("consolas", 12, "bold"),
                                  background="light green",
                                  activebackground="green",
                                  width=8,
                                  command=self.previous_move)

        self.button_restart = Button(button_frame,
                                     text="||<--",
                                     state="disabled",
                                     font=("consolas", 12, "bold"),
                                     background="light green",
                                     activebackground="green",
                                     width=8,
                                     command=self.restart_game)

        self.button_start = Button(button_frame,
                                   text="start game",
                                   font=("consolas", 12, "bold"),
                                   background="light green",
                                   activebackground="green",
                                   command=self.start_game)

        # δημιουργία ετικέτας για προβολή επόμενης κίνησης -------------------------------------------------------------
        self.next_move_display = Label(button_frame,
                                       text="'start game' to continue",
                                       background="light blue",
                                       font=("consolas", 12, "bold"),
                                       width=28)

        # τοποθέτηση στο παράθυρο --------------------------------------------------------------------------------------
        # τοποθέτηση κουμπιών στο button_frame
        self.button_next.pack(side="right")
        self.button_prev.pack(side="right")
        self.button_restart.pack(side="right")
        self.button_start.pack(side="left")
        # τοποθέτηση ετικέτας με την επόμενη κίνηση
        self.next_move_display.pack(side="right", fill="both")

        # τοποθέτηση σκακιέρας στο παράθυρο
        self.frame.grid(row=0, column=0)
        # τοποθέτηση button_frame στο παράθυρο
        button_frame.grid(row=1, column=0, sticky="ew")

        # αρχικοποίηση και τοποθέτηση Frame με τις πληροφορίες του αγώνα στο παράθυρο
        InfoFrame(master=self, info_dictionary=game_dict).grid(row=0, column=1, sticky="n")

        # αρχικοποίηση και τοποθέτηση Frame με τα αιχμαλωτισμένα κομμάτια στο παράθυρο
        self.cap_frame = CapturedPieceFrame(master=self, blank_image=self.blank,
                                            captured_piece_dictionary=self.game_loader.captured_piece_names,
                                            rw_image=self.rw_image, nw_image=self.nw_image, bw_image=self.bw_image,
                                            qw_image=self.qw_image, pw_image=self.pw_image, pb_image=self.pb_image,
                                            rb_image=self.rb_image, nb_image=self.nb_image, bb_image=self.bb_image,
                                            qb_image=self.qb_image)
        self.cap_frame.grid(row=0, column=1, rowspan=2, sticky="sw")

        # ερώτηση για επιβεβαίωση εξόδου από το παράθυρο
        self.protocol("WM_DELETE_WINDOW", self.exit)

        # επεξεργασία παραθύρου για προσθήκη παραμέτρων
        self.config(menu=menubar, background="light grey")

        # εντολή για έναρξη του παραθύρου (πάντα στο τέλος)
        self.mainloop()

    def update_gui_board(self):
        """
        Πραγματοποιεί ανανέωση του γραφικού περιβάλλοντος μετά από κάθε κίνηση
        """
        # η λίστα game_rounds του αντικειμένου game_loader περιέχει τα στιγμιότυπα (λεξικά) του αγώνα με τη θέση των
        # κομματιών σε κάθε γύρο
        # πραγματοποιείται διαπέραση της λίστας για τον εκάστοτε γύρο, και ανανεώνεται αντίστοιχα το γραφικό περιβάλλον
        # της σκακιέρας
        for piece in self.game_loader.info_dictionaries_per_round[self.game_loader.round]:
            if piece["name"] == "  ":
                self.board[piece["row"]][piece["col"]].config(image=self.blank, compound="center")
            elif piece["name"] == "pb":
                self.board[piece["row"]][piece["col"]].config(image=self.pb_image, compound="center")
            elif piece["name"] == "pw":
                self.board[piece["row"]][piece["col"]].config(image=self.pw_image, compound="center")
            elif piece["name"] == "rb":
                self.board[piece["row"]][piece["col"]].config(image=self.rb_image, compound="center")
            elif piece["name"] == "nb":
                self.board[piece["row"]][piece["col"]].config(image=self.nb_image, compound="center")
            elif piece["name"] == "bb":
                self.board[piece["row"]][piece["col"]].config(image=self.bb_image, compound="center")
            elif piece["name"] == "qb":
                self.board[piece["row"]][piece["col"]].config(image=self.qb_image, compound="center")
            elif piece["name"] == "rw":
                self.board[piece["row"]][piece["col"]].config(image=self.rw_image, compound="center")
            elif piece["name"] == "nw":
                self.board[piece["row"]][piece["col"]].config(image=self.nw_image, compound="center")
            elif piece["name"] == "bw":
                self.board[piece["row"]][piece["col"]].config(image=self.bw_image, compound="center")
            elif piece["name"] == "qw":
                self.board[piece["row"]][piece["col"]].config(image=self.qw_image, compound="center")
            elif piece["name"] == "kb":
                if self.game_loader.check_per_round[self.game_loader.round] == "b":
                    self.board[piece["row"]][piece["col"]].config(image=self.kb_checked, compound="center")
                else:
                    self.board[piece["row"]][piece["col"]].config(image=self.kb_image, compound="center")
            elif piece["name"] == "kw":
                if self.game_loader.check_per_round[self.game_loader.round] == "w":
                    self.board[piece["row"]][piece["col"]].config(image=self.kw_checked, compound="center")
                else:
                    self.board[piece["row"]][piece["col"]].config(image=self.kw_image, compound="center")

    def next_move(self):
        """
        Μετάβαση στην επόμενη κίνηση του αγώνα
        Η μέθοδος επίσης απενεργοποιεί/ενεργοποιεί τα αντίστοιχα κουμπιά/checkbuttons για αποφυγή σφαλμάτων
        """
        # ενεργοποίηση του κουμπιού προηγούμενης κίνησης και επαναφοράς στην αρχική θέση
        # (σε περίπτωση που είναι ανενεργό, εάν βρισκόμαστε στην αρχική θέση)
        self.button_prev.config(state="normal")
        self.button_restart.config(state="normal")
        self.starting_move = False

        try:
            # μετάβαση στον επόμενο γύρο
            self.game_loader.next_round()
        except PositionReached:
            self.game_loader.next_round(force=True)
            # απενεργοποίηση του κουμπιού επόμενης κίνησης όταν φτάσουμε στην τελευταία
            self.button_next.config(state="disabled")
            # απο-επιλογή και απενεργοποίηση του checkbutton autoplay
            self.checkbutton_var.set(0)
            self.file_menu.entryconfig(index=0, state="disabled")
            self.ending_move = True

        # αναπαραγωγή ήχων
        if self.game_loader.captures_per_round[self.game_loader.round]:
            mixer.music.load('sound_effects\\capture_sound.mp3')
            mixer.music.play(loops=0)
        else:
            mixer.music.load('sound_effects\\move_sound.mp3')
            mixer.music.play(loops=0)

        # ανανέωση γραφικής αναπαράστασης σκακιέρας
        self.update_gui_board()

        # προβολή επόμενης κίνησης στο ταμπλό
        self.next_move_display.config(text=self.text_config(),
                                      width=28,
                                      fg="red" if self.ending_move else "black")

        # ενημέρωση πλαισίου με αιχμαλωτισμένα κομμάτια
        self.cap_frame.next_round()

    def previous_move(self):
        """
        Μετάβαση στην προηγούμενη κίνηση του αγώνα
        """
        # ενεργοποίηση του κουμπιού επόμενης κίνησης
        # (σε περίπτωση που είναι ανενεργό, εάν βρισκόμαστε στην τελική θέση)
        self.button_next.config(state="normal")
        # ενεργοποίηση του checkbutton autoplay
        self.file_menu.entryconfig(index=0, state="normal")
        # απο-επιλογή για να σταματήσει η αυτόματη αναπαραγωγή άμα ο χρήστης κινηθεί προς τα πίσω
        self.checkbutton_var.set(0)
        self.ending_move = False

        try:
            # μετάβαση στον προηγούμενο γύρο
            self.game_loader.previous_round()
        except PositionReached:
            self.game_loader.previous_round(force=True)
            # απενεργοποίηση του κουμπιού προηγούμενης κίνησης και επαναφοράς στην αρχική θέση όταν φτάσουμε στην πρώτη
            self.button_prev.config(state="disabled")
            self.button_restart.config(state="disabled")
            self.starting_move = True

        # αναπαραγωγή ήχου
        mixer.music.load('sound_effects\\previous_move.mp3')
        mixer.music.play(loops=0, fade_ms=200)

        # ανανέωση γραφικής αναπαράστασης σκακιέρας
        self.update_gui_board()

        # προβολή επόμενης κίνησης στο ταμπλό
        self.next_move_display.config(text=self.text_config(),
                                      width=28,
                                      fg="black")

        # ενημέρωση πλαισίου με αιχμαλωτισμένα κομμάτια
        self.cap_frame.previous_round()

    def start_game(self):
        """
        Εκκίνηση του αγώνα
        Η μέθοδος αρχικοποιεί τα key-bindings για ευκολία κύλισης εμπρός-πίσω στην αλληλουχία των κινήσεων
        """
        # key-bindings με την εκκίνηση του αγώνα
        self.bind(sequence='<Right>', func=self.right_key_bind)
        self.bind(sequence='<Left>', func=self.left_key_bind)
        self.bind(sequence="<Down>", func=self.down_key_bind)
        self.bind(sequence="<Up>", func=self.up_key_bind)

        # ενεργοποίηση πλήκτρων ελέγχου αγώνα
        self.button_next.config(state="normal")
        self.button_start.config(state="disabled")
        self.file_menu.entryconfig(index=0, state="normal")

        # αντιστοίχηση εικονιδίων κομματιών με τα κομμάτια κάθε θέσης
        self.update_gui_board()

        # προβολή επόμενης κίνησης στο ταμπλό
        self.next_move_display.config(text=self.text_config(),
                                      width=28,
                                      fg="black")

    def restart_game(self):
        """
        Επανεκκίνηση του αγώνα
        """
        # θέτω τον γύρο στην αρχική τιμή (0)
        self.game_loader.round = 0

        # ανανέωση γραφικής αναπαράστασης σκακιέρας
        self.update_gui_board()

        # ενεργοποίηση του κουμπιού επόμενου γύρου και απενεργοποίηση του προηγούμενου
        self.button_next.config(state="normal")
        self.button_prev.config(state="disabled")
        self.button_restart.config(state="disabled")
        # ενεργοποίηση του checkbutton autoplay
        self.file_menu.entryconfig(index=0, state="normal")
        # απο-επιλογή για να σταματήσει η αυτόματη αναπαραγωγή άμα ο χρήστης κινηθεί προς τα πίσω
        self.checkbutton_var.set(0)
        self.ending_move = False
        self.starting_move = True

        # αναπαραγωγή ήχου
        mixer.music.load('sound_effects\\restart.mp3')
        mixer.music.play(loops=0)

        # προβολή επόμενης κίνησης στο ταμπλό
        self.next_move_display.config(text=self.text_config(),
                                      width=28,
                                      fg="black")

        # επαναφορά πλαισίου με αιχμαλωτισμένα κομμάτια
        self.cap_frame.reset()

    def autoplay(self):
        """
        Εκτελεί αυτόματη αναπαραγωγή του παιχνιδιού, μέχρι να πιεστεί πλήκτρο επαναφοράς / προηγούμενων κινήσεων ή να
        απενεργοποιηθεί χειροκίνητα
        """
        # εάν το checkbutton είναι ενεργό, η μεταβλητή παρακάτω παίρνει την τιμή 0
        if self.checkbutton_var.get() == 1:
            # εκτέλεση επόμενης κίνησης
            self.next_move()
            # επανάκληση της μεθόδου autoplay μετά από 1200 milliseconds
            self.__identifier_for_after_method = self.after(1200, self.autoplay)
        # εάν το checkbutton είναι ανενεργό, ελέγχω εάν υπάρχει ενεργή after, και αν ναι την ακυρώνω
        elif self.__identifier_for_after_method:
            self.after_cancel(self.__identifier_for_after_method)

    def text_config(self) -> str:
        """
        Διαχειρίζεται και επιστρέφει συμβολοσειρά με πληροφορίες για την επόμενη κίνηση

        Επιστρεφόμενο αντικείμενο:
        --------------------------
            (str):
                συμβολοσειρά με πληροφορίες για την επόμενη κίνηση
        """
        if not self.ending_move:
            cur_round = self.game_loader.round
            to_play = "White to play: " if cur_round % 2 == 0 else "Black to play: "
            self.ending_move = False
            return to_play + str((cur_round//2)+1) + ". " + self.game_loader.gameplay.moves[cur_round]
        else:
            # εάν είμαστε στην τελευταία κίνηση επιστρέφεται το τελικό σκορ του αγώνα
            return self.__result

    def show_controls(self):
        """
        Εμφανίζει παράθυρο με τις οδηγίες χρήσης του παραθύρου
        """
        showinfo(master=self,
                 title="Help",
                 message="Press \"start game\" to start the game\n"
                         "Right arrow (---->) button or <Right-Key> for next move\n"
                         "Left arrow (<----) button or <Left-Key> for previous move\n"
                         "Reset arrow (||<--) button or <Down-Key>  to reset the board\n",
                 detail="You can also toggle autoplay (on/off) from the File menu\n"
                        "or by using the <Up-Key>")

    def exit(self):
        """
        Ζητάει επιβεβαίωση εξόδου από την αναπαραγωγή του παιχνιδιού
        Εμφανίζει messagebox με επιλογή yes/no
        """
        if askyesno(master=self, title="Exit Game?", message="Do you really wish to exit this game?", default="no"):
            if self.__identifier_for_after_method:
                # ακύρωση της μεθόδου self.after() σε περίπτωση είναι ενεργή ενώ τερματίζει το παράθυρο
                self.after_cancel(self.__identifier_for_after_method)
            self.destroy()

    def right_key_bind(self, event):
        """
        Εκτελεί την επόμενη κίνηση χρησιμοποιώντας key-event <δεξί-βέλος>
        Εάν το παιχνίδι βρίσκεται στην τελευταία κίνηση, δεν εκτελεί κάτι
        """
        if self.ending_move:
            return
        self.next_move()

    def left_key_bind(self, event):
        """
        Εκτελεί την προηγούμενη κίνηση χρησιμοποιώντας key-event <αριστερό-βέλος>
        Εάν το παιχνίδι βρίσκεται στην πρώτη κίνηση, δεν εκτελεί κάτι
        """
        if self.starting_move:
            return
        self.previous_move()

    def down_key_bind(self, event):
        """
        Επιστρέφει το ταμπλό στην αρχική θέση χρησιμοποιώντας key-event <κάτω-βέλος>
        Εάν το παιχνίδι βρίσκεται στην πρώτη κίνηση, δεν εκτελεί κάτι
        """
        if self.starting_move:
            return
        self.restart_game()

    def up_key_bind(self, event):
        """
        Ενεργοποιεί την αυτόματη αναπαραγωγή του αγώνα χρησιμοποιώντας key-event <πάνω-βέλος>
        Εάν το παιχνίδι βρίσκεται στην τελευταία κίνηση, δεν εκτελεί κάτι
        """
        if self.ending_move:
            return
        if self.checkbutton_var.get() == 1:
            # εάν το checkbutton_var είναι 1 (δηλαδή ενεργό), διακόπτει την αυτόματη αναπαραγωγή
            self.checkbutton_var.set(0)
            return
        if self.checkbutton_var.get() == 0:
            # εάν το checkbutton_var είναι 0 (δηλαδή ανενεργό), ενεργοποιεί την αυτόματη αναπαραγωγή
            self.checkbutton_var.set(1)
            self.autoplay()
