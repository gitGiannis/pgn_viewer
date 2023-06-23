# -------------------------------------------------------------------------------------------------------------------- #
# captured_piece_frame.py: περιέχει την κλάση CapturedPieceFrame                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Frame, Label


class CapturedPieceFrame(Frame):
    """
    Κληρονομεί τις ιδιότητες της γονικής κλάσης Frame
    Περιλαμβάνει grid 5Χ6 όπου απεικονίζονται όσα κομμάτια έχουν καταληφθεί κατά την εξέλιξη του αγώνα
    Χρησιμοποιείται από την κλάση gui.GUI

    Ορίσματα:
    ---------
        master (tkinter object):
            ο master στον οποίο ανήκει το Frame που θα δημιουργηθεί

        captured_piece_dictionary (dict):
            λεξικό με τις πληροφορίες αιχμαλωτισμένων κομματιών

        *_image (tkinter.PhotoImage):
            εικόνες κομματιών σκακιού

    Μέθοδοι:
    --------
        __update_frame(self) -> str:
            ενημερώνει το ταμπλό αιχμαλωτισμένων κομματιών, επιστρέφει συμβολοσειρά με το tag του κομματιού

        next_round(self):
            ενημερώνει το ταμπλό εάν καταληφθεί κάποιο κομμάτι

        previous_round(self):
            ενημερώνει το ταμπλό αφαιρώντας κομμάτια από το πλαίσιο

        reset(self):
            επαναφέρει το ταμπλό στην αρχική κατάσταση
    """
    def __init__(self, master, captured_piece_dictionary: dict, blank_image,
                 rw_image, rb_image, nw_image, nb_image, bw_image, bb_image, qw_image, qb_image, pw_image, pb_image):
        # κλήση της super() για κληρονόμηση ιδιοτήτων
        super().__init__(master=master)
        self.config(bg="light grey")
        # αρχικοποίηση λεξικού με τις πληροφορίες των αιχμαλωτισμένων κομματιών ανά γύρο
        self.dict = captured_piece_dictionary
        # αρχικοποίηση μετρητή γύρων
        self.round = 0
        # αρχικοποίηση εικόνων
        self.blank = blank_image
        self.photo_dict = {"rw": rw_image, "rb": rb_image,
                           "nw": nw_image, "nb": nb_image,
                           "bw": bw_image, "bb": bb_image,
                           "qw": qw_image, "qb": qb_image,
                           "pw": pw_image, "pb": pb_image}

        # αρχικοποίηση πίνακα με labels που θα χρησιμοποιήσει το grid για να προβάλει τις εικόνες των αιχμαλωτισμένων
        # κομματιών
        self.captured_piece_board = []
        for row in range(5):
            temp = []
            for col in range(6):
                # γίνεται αρχικοποίηση όλων των ετικετών με την κενή εικόνα, μέχρι να γίνει η έναρξη
                temp.append(Label(self, bg="light grey", image=blank_image))
            self.captured_piece_board.append(temp)

        for row in range(5):
            for col in range(6):
                self.captured_piece_board[row][col].grid(row=row, column=col)

        # αρχικοποίηση μετρητών γραμμών και στηλών για σωστή τοποθέτηση των κομματιών στο grid
        self.row_for_white = 0
        self.col_for_white = 0
        self.row_for_black = 0
        self.col_for_black = 3

    def __update_frame(self) -> str:
        """
        Ενημερώνει το ταμπλό αιχμαλωτισμένων κομματιών
        Επιστρέφει συμβολοσειρά με την πληροφορία των αιχμαλωτισμένων κομματιών σε κάθε γύρο

        Επιστρεφόμενο αντικείμενο:
        --------------------------
            (str): "w"/"b" αναλόγως το χρώμα του κομματιού, "" εάν δεν υπάρχει κάποιο κομμάτι στον συγκεκριμένο γύρο
        """
        try:
            # έλεγχος εάν υπάρχει ο τρέχων γύρος στο λεξικό
            captured_piece_name = self.dict[self.round]
        except KeyError:
            # εάν δεν υπάρχει το συγκεκριμένο κλειδί, έχουμε εξαίρεση
            return ""

        if captured_piece_name[1] == "w":
            self.captured_piece_board[self.row_for_white][self.col_for_white].config(
                                                                    image=self.photo_dict[captured_piece_name],
                                                                    state="disabled")
            return "w"

        if captured_piece_name[1] == "b":
            self.captured_piece_board[self.row_for_black][self.col_for_black].config(
                                                                    image=self.photo_dict[captured_piece_name],
                                                                    state="disabled")
            return "b"

    def next_round(self):
        """
        Ενημερώνει το ταμπλό εάν καταληφθεί κάποιο κομμάτι
        """
        self.round += 1
        # προσωρινή αποθήκευση του tag
        current_piece_tag = self.__update_frame()
        # έλεγχος θέση που θα μπει η νέα εικόνα
        # τα λευκά κομμάτια τοποθετούνται στις τρεις πρώτες στήλες (0, 1, 2), τα μαύρα στις τρεις τελευταίες (3, 4, 5)
        # ξεκινώντας από την πρώτη στήλη για το καθένα και μόλις γεμίσει συνεχίζει στην επόμενη
        if current_piece_tag == "w":
            self.row_for_white += 1
            if self.row_for_white == 5:
                self.row_for_white = 0
                self.col_for_white += 1
        elif current_piece_tag == "b":
            self.row_for_black += 1
            if self.row_for_black == 5:
                self.row_for_black = 0
                self.col_for_black += 1

    def previous_round(self):
        """
        Ενημερώνει το ταμπλό αφαιρώντας κομμάτια από το πλαίσιο
        """
        # κρατάω τον προηγούμενο γύρο
        cur_round = self.round - 1
        # καλώ τη reset() για άδειασμα του ταμπλό
        self.reset()
        # ενημερώνω κατάλληλα το ταμπλό μέχρι τον εκάστοτε γύρο
        for rnd in range(cur_round):
            self.next_round()

    def reset(self):
        """
        Επαναφέρει το ταμπλό στην αρχική κατάσταση
        """
        self.round = 0
        self.row_for_white = 0
        self.col_for_white = 0
        self.row_for_black = 0
        self.col_for_black = 3
        for row in range(5):
            for col in range(6):
                self.captured_piece_board[row][col].config(image=self.blank, bg="light grey")
