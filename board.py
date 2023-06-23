# -------------------------------------------------------------------------------------------------------------------- #
# board.py: περιέχει την κλάση Board                                                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
from piece import Piece


class Board:
    """
    "Δημιουργεί" το πινάκιο (ταμπλό) της σκακιέρας, όπου τοποθετούνται αντικείμενα piece.Piece (κομμάτια)
    Μέσω μεθόδων τοποθετεί τα κομμάτια στην αρχική τους θέση και εκτελεί τις κινήσεις τους

    Μέθοδοι:
    --------
        __update_squares(self):
            ενημερώνει το λεξικό κενών και κατηλλειμένων κελιών

        update_self(self):
            διατρέχει τα κομμάτια και ενημερώνει το ταμπλό με τις νέες θέσεις

        move_piece(self, src: str, dest: str) -> str:
            μετακινεί το κομμάτι που πρέπει να κινηθεί, επιστρέφει το όνομά του κομματιού που αιχμαλωτίστηκε
    """
    def __init__(self):
        # αρχικοποίηση κομματιών ---------------------------------------------------------------------------------------
        self.pieces = [
            # κομμάτια "λευκού" παίκτη
            Piece("rwl", "a1", row=7, col=0), Piece("nwl", "b1", row=7, col=1), Piece("bwl", "c1", row=7, col=2),
            Piece("qwl", "d1", row=7, col=3), king_w := Piece("kwr", "e1", row=7, col=4),
            Piece("bwr", "f1", row=7, col=5), Piece("nwr", "g1", row=7, col=6), Piece("rwr", "h1", row=7, col=7),
            Piece("pw1", "a2", row=6, col=0), Piece("pw2", "b2", row=6, col=1), Piece("pw3", "c2", row=6, col=2),
            Piece("pw4", "d2", row=6, col=3), Piece("pw5", "e2", row=6, col=4), Piece("pw6", "f2", row=6, col=5),
            Piece("pw7", "g2", row=6, col=6), Piece("pw8", "h2", row=6, col=7),
            # κομμάτια "μαύρου" παίκτη
            Piece("rbl", "a8", row=0, col=0), Piece("nbl", "b8", row=0, col=1), Piece("bbl", "c8", row=0, col=2),
            Piece("qbl", "d8", row=0, col=3), king_b := Piece("kbr", "e8", row=0, col=4),
            Piece("bbr", "f8", row=0, col=5), Piece("nbr", "g8", row=0, col=6), Piece("rbr", "h8", row=0, col=7),
            Piece("pb1", "a7", row=1, col=0), Piece("pb2", "b7", row=1, col=1), Piece("pb3", "c7", row=1, col=2),
            Piece("pb4", "d7", row=1, col=3), Piece("pb5", "e7", row=1, col=4), Piece("pb6", "f7", row=1, col=5),
            Piece("pb7", "g7", row=1, col=6), Piece("pb8", "h7", row=1, col=7)
        ]

        # αρχικοποίηση κενών κελιών
        # θεωρώ ότι κάθε κελί της σκακιέρας περιέχει κάποιο κομμάτι, τα κενά κελιά περιέχουν decoys, τα οποία ο χρήστης
        # δεν αντιλαμβάνεται, αλλά διευκολύνουν στις μετακινήσεις των κομματιών, όπως θα φανεί στη συνέχεια
        r = 5
        for cnt in range(3, 7):
            self.pieces.append(Piece(" " * 3, f"a{cnt}", state=False, row=r, col=0))
            self.pieces.append(Piece(" " * 3, f"b{cnt}", state=False, row=r, col=1))
            self.pieces.append(Piece(" " * 3, f"c{cnt}", state=False, row=r, col=2))
            self.pieces.append(Piece(" " * 3, f"d{cnt}", state=False, row=r, col=3))
            self.pieces.append(Piece(" " * 3, f"e{cnt}", state=False, row=r, col=4))
            self.pieces.append(Piece(" " * 3, f"f{cnt}", state=False, row=r, col=5))
            self.pieces.append(Piece(" " * 3, f"g{cnt}", state=False, row=r, col=6))
            self.pieces.append(Piece(" " * 3, f"h{cnt}", state=False, row=r, col=7))
            r -= 1

        # αρχικοποίηση πινακίου (ταμπλό) σκακιού -----------------------------------------------------------------------
        # σημειώνεται πως η δημιουργία του πινακίου θα μπορούσε να γίνει με πιο κομψό και προγραμματιστικό τρόπο,
        # ωστόσο με αυτόν τον τρόπο ήταν πιο εύκολη η κατανόηση και η εξοικείωση με τις θέσεις
        # και τις διευθύνσεις της σκακιέρας
        self.board = [
            [None, None, None, None, None, None, None, None],  # 8
            [None, None, None, None, None, None, None, None],  # 7
            [None, None, None, None, None, None, None, None],  # 6
            [None, None, None, None, None, None, None, None],  # 5
            [None, None, None, None, None, None, None, None],  # 4
            [None, None, None, None, None, None, None, None],  # 3
            [None, None, None, None, None, None, None, None],  # 2
            [None, None, None, None, None, None, None, None]   # 1
            #  a     b     c     d     e     f     g     h
        ]

        # λεξικό με τις διευθύνσεις των βασιλιάδων για πιο εύκολη εύρεση
        self.kings = {"w": king_w,
                      "b": king_b}

        # λεξικό που θα συσσωρεύσει τα ονόματα των κελιών (θέσεις [pos] της σκακιέρας)
        # και την κατάσταση τους (state [True/False]) (εάν περιέχουν κομμάτι True, εάν περιέχουν decoy False)
        # θα χρησιμεύσει στον έλεγχο της εγκυρότητας των κινήσεων των κομματιών της κλάσης Gameplay
        self.squares = {}

        # τιμή bool για δήλωση ότι ένα κομμάτι κατέλαβε κομμάτι ίδιου tag (χρώματος)
        self.friendly_capture: bool = False

    def __update_squares(self, piece):
        """
        Ενημερώνει το λεξικό κενών και κατηλλειμένων κελιών
        Το λεξικό self.squares (dict) περιέχει τα ονόματα των κελιών και την τιμή καθενός (True/False)
        Εάν το κελί έχει κάποιο ενεργό κομμάτι, χαρακτηρίζεται ως το tag (w/b) του κομματιού
        Εάν αν είναι κενό χαρακτηρίζεται ως False

        Ορίσματα:
        ---------
            piece (Piece): τρέχων κομμάτι κατά τη διαπέραση της λίστας κομματιών
        """
        # εάν το κελί έχει κάποιο ενεργό κομμάτι, χαρακτηρίζεται ως το tag (w/b) του κομματιού,
        # διαφορετικά αν είναι κενό False
        if piece.state:
            self.squares[piece.pos] = piece.name[1]
        else:
            self.squares[piece.pos] = False

    def update_self(self):
        """
        Διατρέχει τα κομμάτια και τα τοποθετεί στο πινάκιο (ταμπλό)
        Σε κάθε γύρο, γίνεται προσπέλαση των κομματιών για να τοποθετηθούν στη νέα τους θέση, σε περίπτωση που αυτή έχει
        αλλάξει
        """
        for piece in self.pieces:
            self.__update_squares(piece)
            # γίνεται ομαδοποίηση ελέγχων ανα στήλη για λιγότερους ελέγχους
            # στήλη A
            if piece.pos[0] == "a":
                if piece.pos == "a8":
                    self.board[0][0] = piece
                elif piece.pos == "a7":
                    self.board[1][0] = piece
                elif piece.pos == "a6":
                    self.board[2][0] = piece
                elif piece.pos == "a5":
                    self.board[3][0] = piece
                elif piece.pos == "a4":
                    self.board[4][0] = piece
                elif piece.pos == "a3":
                    self.board[5][0] = piece
                elif piece.pos == "a2":
                    self.board[6][0] = piece
                elif piece.pos == "a1":
                    self.board[7][0] = piece

            # στήλη B
            elif piece.pos[0] == "b":
                if piece.pos == "b8":
                    self.board[0][1] = piece
                elif piece.pos == "b7":
                    self.board[1][1] = piece
                elif piece.pos == "b6":
                    self.board[2][1] = piece
                elif piece.pos == "b5":
                    self.board[3][1] = piece
                elif piece.pos == "b4":
                    self.board[4][1] = piece
                elif piece.pos == "b3":
                    self.board[5][1] = piece
                elif piece.pos == "b2":
                    self.board[6][1] = piece
                elif piece.pos == "b1":
                    self.board[7][1] = piece

            # στήλη C
            elif piece.pos[0] == "c":
                if piece.pos == "c8":
                    self.board[0][2] = piece
                elif piece.pos == "c7":
                    self.board[1][2] = piece
                elif piece.pos == "c6":
                    self.board[2][2] = piece
                elif piece.pos == "c5":
                    self.board[3][2] = piece
                elif piece.pos == "c4":
                    self.board[4][2] = piece
                elif piece.pos == "c3":
                    self.board[5][2] = piece
                elif piece.pos == "c2":
                    self.board[6][2] = piece
                elif piece.pos == "c1":
                    self.board[7][2] = piece

            # στήλη D
            elif piece.pos[0] == "d":
                if piece.pos == "d8":
                    self.board[0][3] = piece
                elif piece.pos == "d7":
                    self.board[1][3] = piece
                elif piece.pos == "d6":
                    self.board[2][3] = piece
                elif piece.pos == "d5":
                    self.board[3][3] = piece
                elif piece.pos == "d4":
                    self.board[4][3] = piece
                elif piece.pos == "d3":
                    self.board[5][3] = piece
                elif piece.pos == "d2":
                    self.board[6][3] = piece
                elif piece.pos == "d1":
                    self.board[7][3] = piece

            # στήλη E
            elif piece.pos[0] == "e":
                if piece.pos == "e8":
                    self.board[0][4] = piece
                elif piece.pos == "e7":
                    self.board[1][4] = piece
                elif piece.pos == "e6":
                    self.board[2][4] = piece
                elif piece.pos == "e5":
                    self.board[3][4] = piece
                elif piece.pos == "e4":
                    self.board[4][4] = piece
                elif piece.pos == "e3":
                    self.board[5][4] = piece
                elif piece.pos == "e2":
                    self.board[6][4] = piece
                elif piece.pos == "e1":
                    self.board[7][4] = piece

            # στήλη F
            elif piece.pos[0] == "f":
                if piece.pos == "f8":
                    self.board[0][5] = piece
                elif piece.pos == "f7":
                    self.board[1][5] = piece
                elif piece.pos == "f6":
                    self.board[2][5] = piece
                elif piece.pos == "f5":
                    self.board[3][5] = piece
                elif piece.pos == "f4":
                    self.board[4][5] = piece
                elif piece.pos == "f3":
                    self.board[5][5] = piece
                elif piece.pos == "f2":
                    self.board[6][5] = piece
                elif piece.pos == "f1":
                    self.board[7][5] = piece

            # στήλη G
            elif piece.pos[0] == "g":
                if piece.pos == "g8":
                    self.board[0][6] = piece
                elif piece.pos == "g7":
                    self.board[1][6] = piece
                elif piece.pos == "g6":
                    self.board[2][6] = piece
                elif piece.pos == "g5":
                    self.board[3][6] = piece
                elif piece.pos == "g4":
                    self.board[4][6] = piece
                elif piece.pos == "g3":
                    self.board[5][6] = piece
                elif piece.pos == "g2":
                    self.board[6][6] = piece
                elif piece.pos == "g1":
                    self.board[7][6] = piece

            # στήλη H
            elif piece.pos[0] == "h":
                if piece.pos == "h8":
                    self.board[0][7] = piece
                elif piece.pos == "h7":
                    self.board[1][7] = piece
                elif piece.pos == "h6":
                    self.board[2][7] = piece
                elif piece.pos == "h5":
                    self.board[3][7] = piece
                elif piece.pos == "h4":
                    self.board[4][7] = piece
                elif piece.pos == "h3":
                    self.board[5][7] = piece
                elif piece.pos == "h2":
                    self.board[6][7] = piece
                elif piece.pos == "h1":
                    self.board[7][7] = piece

    def move_piece(self, src: str, dest: str) -> str:
        """
        Μετακινεί το κομμάτι που πρέπει να κινηθεί, επιστρέφει το όνομά του κομματιού που αιχμαλωτίστηκε

        Ορίσματα:
        ---------
            src (str): θέση κομματιού που θα εκτελέσει κάποια κίνηση

            dest (str): θέση προορισμού του κομματιού που θα μετακινηθεί

        Επιστρεφόμενο αντικείμενο:
        --------------------------
            piece_dest_name_to_return (str):
                το όνομα κομματιού που αιχμαλωτίστηκε θα επιστραφεί από τη μέθοδο και θα χρησιμοποιηθεί από λεξικό που
                αποθηκεύει πληροφορίες για τα αιχμαλωτισμένα κομμάτια ώστε να προβληθούν στο παράθυρο εξέλιξης του αγώνα
                (gui.GUI)
        """
        # επαναφορά μεταβλητής
        self.friendly_capture = False

        # αρχικοποίηση επιστρεφόμενης τιμής
        piece_dest_name_to_return = ""

        # προσπέλαση κομματιών για εύρεση κομματιού που μετακινείται (στο εξής κομμάτι src)
        for piece_src in self.pieces:
            # εύρεση κομματιού src
            if piece_src.pos == src:
                # προσωρινή αποθήκευση τρεχόντων συντεταγμένων του κομματιού src
                row_src = piece_src.row
                col_src = piece_src.col

                # προσπέλαση κομματιών για εύρεση κομματιού στη θέση προορισμού (στο εξής κομμάτι dest)
                for piece_dest in self.pieces:
                    # εύρεση κομματιού dest
                    if piece_dest.pos == dest:
                        # έλεγχος χρώματος (tag)
                        if piece_src.name[1] == piece_dest.name[1]:
                            self.friendly_capture = True

                        # προσωρινή αποθήκευση τρεχόντων συντεταγμένων του κομματιού dest
                        row_dest = piece_dest.row
                        col_dest = piece_dest.col

                        # ανταλλαγή θέσης με το src
                        piece_dest.pos = src

                        # διατηρώ σε μία μεταβλητή το όνομα του κομματιού που αιχμαλωτίστηκε
                        piece_dest_name_to_return = piece_dest.name
                        # το κομμάτι "αιχμαλωτίστηκε" και γίνεται κενό κελί (decoy)
                        piece_dest.name = "   "
                        piece_dest.state = False
                        # γίνεται ανταλλαγή συντεταγμένων στον πίνακα
                        piece_dest.row = row_src
                        piece_dest.col = col_src
                        piece_src.row = row_dest
                        piece_src.col = col_dest
                        break
                # ανταλλαγή θέσης με το dest
                piece_src.pos = dest
                break
        return piece_dest_name_to_return
