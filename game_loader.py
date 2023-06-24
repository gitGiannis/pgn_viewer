# -------------------------------------------------------------------------------------------------------------------- #
# game_loader.py: περιέχει την κλάση GameLoader                                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
from move_checking import PieceMoveChecker
from my_exceptions import PositionReached, NoMovesFound, PossibleCorruptFile, FriendlyCapture


class GameLoader:
    """
    "Τρέχει" το παιχνίδι από την αρχή μέχρι το τέλος, ενώ παράλληλα αποθηκεύει σε μία λίστα με λεξικά τις πληροφορίες
    κάθε κομματιού (όνομα, θέση κλπ) για κάθε γύρο, που θα χρησιμεύσουν στη γραφική αναπαράσταση του παιχνιδιού και στην
    προβολή των κινήσεων (μπροστά-πίσω)
    Κάθε λεξικό περιλαμβάνει σαν κλειδί συμβολοσειρά με το όνομα του κομματιού για κάθε κομμάτι και σαν τιμή τη θέση του
    στον πίνακα

    Ορίσματα:
    ---------
        list_of_moves (list):
            λίστα με τις επεξεργασμένες κινήσεις του αγώνα

    Μέθοδοι:
    --------
        next_round(self, force: bool=False):
            μετάβαση στον επόμενο γύρο

        previous_round(self, force: bool=False):
            μετάβαση στον προηγούμενο γύρο

        restart_game(self):
            μετάβαση στον αρχικό γύρο

        update_captured_piece_dict(self, piece_name: str):
            ενημέρωση του λεξικού με τα αιχμαλωτισμένα κομμάτια

    Εξαιρέσεις:
    ----------------
        NoMovesFound: εάν το αρχείο δεν έχει κινήσεις ή το αρχείο δεν μπορεί να εκτελεστεί λογικά στην κλάση Gameplay

        PositionReached: εάν ξεπεραστεί το όριο κινήσεων (0 ~ μήκος λίστας κινήσεων)
    """
    def __init__(self, list_of_moves: list):
        # αρχικοποίηση κλάσης Gameplay για το "τρέξιμο" του παιχνιδιού
        self.gameplay = PieceMoveChecker(list_of_moves)

        # αρχικοποίηση μεταβλητών για συσσώρευση πληροφορίας -----------------------------------------------------------
        # λίστα όπου αποθηκεύονται τα λεξικά με τα στιγμιότυπα κάθε γύρου
        # λεξικό που θα συσσωρεύσει στα στοιχεία του:
        # 1. κλειδί (key) συμβολοσειρά με το όνομα του κομματιού (για κάθε κομμάτι)
        # 2. τιμή (value) τη θέση του στον πίνακα [row][col]
        self.info_dictionaries_per_round = []

        # λεξικό που θα συσσωρεύσει στα στοιχεία του:
        # 1. κλειδί (key) τον γύρο στον οποίο έγινε η κατάληψη ενός κομματιού και
        # 2. τιμή (value) το όνομα και το χρώμα του εκάστοτε κομματιού που αιχμαλωτίστηκε
        # το λεξικό αυτό το χρησιμοποιεί η κλάση captured_piece_frame.CapturedPieceFrame για αναπαράσταση των κομματιών
        # που έχουν αιχμαλωτιστεί σε ζωντανό χρόνο (παράλληλα με την εξέλιξη του παιχνιδιού)
        self.captured_piece_names = {}

        # λίστα τιμών boolean για αναπαραγωγή ήχων ---------------------------------------------------------------------
        # εάν είναι False θα παίξει ο ήχος κίνησης κομματιού, εάν είναι True θα παίξει ο ήχος κατάληψης κομματιού
        self.captures_per_round = []
        # προσθήκη τιμής κατάληψης κομματιού για την αρχική θέση
        self.captures_per_round.append(False)

        # λίστα τιμών για δήλωση ματ σε βασιλιά ------------------------------------------------------------------------
        # εάν είναι None δεν υπάρχει κάποιο μάτ,
        # διαφορετικά οι συμβολοσειρές "w"/"b" υποδηλώνουν μάτ σε λευκό/μαύρο βασιλιά αντιστοίχως
        self.check_per_round = []
        # προσθήκη τιμής ματ σε βασιλιά για την αρχική θέση
        self.check_per_round.append(None)

        # δείκτης τρέχοντος γύρου
        self.round = 0

        # αποθήκευση πληροφοριών ---------------------------------------------------------------------------------------
        # βοηθητική μεταβλητή
        current_round = []
        # αποθήκευση πληροφοριών για την αρχική θέση των κομματιών
        for piece in self.gameplay.pieces:
            current_round.append({
                "name": piece.name[:2],
                "row": piece.row,
                "col": piece.col
            })
        self.info_dictionaries_per_round.append(current_round)

        if self.gameplay.moves_length == 0:
            raise NoMovesFound

        # προσπέλαση όλων των κομματιών του πίνακα σε κάθε γύρο και αποθήκευση τον πληροφοριών -------------------------
        for i in range(self.gameplay.moves_length):
            current_round = []
            # εκτέλεση επόμενης κίνησης και προσωρινή αποθήκευση ονόματος κομματιού που αιχμαλωτίστηκε
            captured_piece_name = self.gameplay.next_move()

            # η μέθοδος next_move() επέστρεψε None
            if captured_piece_name is None:
                raise PossibleCorruptFile(f"{self.gameplay.round_cnt//2 + 1}. "
                                          f"{self.gameplay.moves[self.gameplay.round_cnt]}")

            if self.gameplay.friendly_capture:
                raise FriendlyCapture(f"{self.gameplay.round_cnt//2 + 1}. "
                                      f"{self.gameplay.moves[self.gameplay.round_cnt]}")

            # ενημέρωση λεξικού captured_piece_names
            self.update_captured_piece_dict(captured_piece_name)

            # αποθήκευση πληροφοριών κάθε κομματιού για κάθε γύρο
            for line in self.gameplay.board:
                for sqr in line:
                    current_round.append({
                        "name": sqr.name[:2],
                        "row": sqr.row,
                        "col": sqr.col
                        })
            self.info_dictionaries_per_round.append(current_round)

            # προσθήκη τιμής κατάληψης κομματιού (True/False) στη λίστα
            self.captures_per_round.append(self.gameplay.capture)
            # προσθήκη τιμής ματ σε βασιλιά στη λίστα
            self.check_per_round.append(self.gameplay.check)

    def next_round(self, force: bool = False):
        """
        Μετάβαση στον επόμενο γύρο
        Εκτελεί την επόμενη κίνηση μέχρι να φτάσει στον προτελευταίο γύρο
        force=True για μετάβαση στον τελικό γύρο

        Ορίσματα:
        ---------
            force (bool) default=False:
                True για συνέχεια στον τελικό γύρο

        Εξαίρεση:
        ---------
            PositionReached: εάν έχουμε φτάσει στον προτελευταίο γύρο
        """
        if self.round < self.gameplay.moves_length - 1:
            self.round += 1
        else:
            if force:
                self.round += 1
            else:
                raise PositionReached

    def previous_round(self, force: bool = False):
        """
        Μέθοδος για μετάβαση στον προηγούμενο γύρο
        Εκτελεί την προηγούμενη κίνηση μέχρι να φτάσει στη δεύτερη
        force=True για μετάβαση στην αρχική θέση

        Ορίσματα:
        ---------
            force (bool) default=False:
                True για συνέχεια στον αρχικό γύρο

        Εξαίρεση:
        ---------
            PositionReached: εάν έχουμε φτάσει στον 1ο γύρο
        """
        if self.round > 1:
            self.round -= 1
        else:
            if force:
                self.round -= 1
            else:
                raise PositionReached

    def restart_game(self):
        """
        Μετάβαση στον αρχικό γύρο
        """
        self.round = 0

    def update_captured_piece_dict(self, piece_name: str):
        """
        Ενημέρωση του λεξικού με τα αιχμαλωτισμένα κομμάτια
        Η μέθοδος αυτή αποθηκεύει τον γύρο στον οποίο αιχμαλωτίστηκε κάποιο κομμάτι σαν κλειδί του λεξικού και το όνομα
        του κομματιού σαν τιμή
        Η αποθήκευση γίνεται εφόσον αιχμαλωτίστηκε κάποιο κομμάτι (το όνομα δεν είναι κενή συμβολοσειρά)

        Ορίσματα:
        ---------
            piece_name (str):
                όνομα κομματιού που αιχμαλωτίστηκε
        """
        if piece_name != "   ":
            self.captured_piece_names[self.gameplay.round_cnt + 1] = piece_name[:2]
