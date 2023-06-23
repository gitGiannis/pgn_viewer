# -------------------------------------------------------------------------------------------------------------------- #
# info_frame_for_gui.py: περιέχει την κλάση InfoFrame για προβολή πληροφορίας αγώνα                                    #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Scrollbar, Text, Frame


class InfoFrame(Frame):
    """
    Κληρονομεί τις ιδιότητες της γονικής κλάσης Frame, τοποθετεί μέσα στον χώρο της ένα αντικείμενο τύπου Text που
    περιλαμβάνει τις πληροφορίες του αγώνα
    Τις πληροφορίες αυτές της αντλεί από το λεξικό που χρησιμοποιεί σαν όρισμα
    Χρησιμοποιείται από την κλάση gui.GUI

    Ορίσματα:
        master (gui.GUI):
            ο master στον οποίο ανήκει το Frame που θα δημιουργηθεί

        info_dictionary (dict):
            λεξικό με τις πληροφορίες του αγώνα
    """
    def __init__(self, master, info_dictionary: dict):
        # κλήση της super() για κληρονόμηση ιδιοτήτων
        super().__init__(master=master)
        self.config(bg="light grey")

        # αποθήκευση λίστας κινήσεων (περιλαμβάνει συμβολοσειρές με τις κινήσεις του αγώνα)
        moves = info_dictionary['moves']
        # αρχικοποίηση μετρητή (θα χρησιμεύσει στην αναπαράσταση των γύρων)
        cnt = 1
        # αρχικοποίηση λίστας όπου θα αποθηκευτούν οι αριθμοί γύρων και οι κινήσεις
        moves_numbered = []
        # επανάληψη πάνω στα στοιχεία της λίστας με τις κινήσεις
        for i in range(len(moves)):
            if cnt % 1 == 0:
                # προσθήκη δείκτη γύρου ανα δύο κινήσεις
                moves_numbered.append(str(int(cnt)) + ".")
            # προσθήκη κίνησης στη λίστα
            moves_numbered.append(moves[i])
            cnt += 0.5

        # αρχικοποίηση συμβολοσειράς που θα προβληθεί
        moves_str = ""
        # μεταβλητή που καθορίζει πόσοι γύροι θα προβληθούν ανα σειρά
        # κάθε γύρος περιλαμβάνει 3 συμβολοσειρές (δείκτη γύρου, κίνηση λευκού και κίνηση μαύρου παίκτη), οπότε
        # χρησιμοποιείται ακέραιος αριθμός πολλαπλάσιος του 3, για λόγους καλαισθησίας
        number_of_items_per_line = 3
        # αρχική και τελική θέση κατά τη διαπέραση της λίστας moves_numbered
        start = 0
        end = number_of_items_per_line
        # ατέρμον βρόγχος που διακόπτεται μόλις έχουμε εξαίρεση για IndexError
        while True:
            try:
                for i in range(start, end):
                    # η λίστα moves_numbered περιλαμβάνει δείκτη γύρου, κίνηση λευκού και κίνηση μαύρου παίκτη σε όλες
                    # τις θέσεις διαδοχικά
                    moves_str += moves_numbered[i]
                    moves_str += "  "
                # ανά τους γύρους που έχουν οριστεί από τη number_of_rounds_per_line, προστίθεται ο χαρακτήρας αλλαγής
                # γραμμής και η επανάληψη διατρέχει τα επόμενα στοιχεία της λίστας μέχρι το τελευταίο
                moves_str += "\n"
                start += number_of_items_per_line
                end += number_of_items_per_line
            except IndexError:
                break

        # δημιουργία συμβολοσειράς που θα προβληθεί στο Message
        text_to_show = f"Event: {info_dictionary['Event']}\n" \
                       f"Site: {info_dictionary['Site']}\n" \
                       f"Date: {info_dictionary['Date']}\n" \
                       f"Round: {info_dictionary['Round']}\n" \
                       f"White: {info_dictionary['White']}\n" \
                       f"Black: {info_dictionary['Black']}\n" \
                       f"Result: {info_dictionary['Result']}\n" \
                       f"Rounds Played: {info_dictionary['RoundsPlayed']}\n" \
                       f"\n{moves_str + ' ' + info_dictionary['Result']}"

        # τοποθέτηση του αντικειμένου Text και Scrollbar μέσα στο Frame
        text = Text(self, background="light grey",
                    relief="flat",
                    width=45,
                    height=20)
        text.insert(index=0.0, chars=text_to_show)
        scrollbar = Scrollbar(master=self, command=text.yview)
        text.config(state="disabled", yscrollcommand=scrollbar.set)
        text.pack(fill="both", side="left")
        scrollbar.pack(fill="both", side="right")
