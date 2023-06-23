# -------------------------------------------------------------------------------------------------------------------- #
# my_exceptions.py: περιέχει προσαρμοσμένες εξαιρέσεις για χειρισμό λαθών                                              #
# -------------------------------------------------------------------------------------------------------------------- #


class PositionReached(Exception):
    """
    Δηλώνει ότι η μέθοδος game_loader.Gameloader.next_round()/game_loader.Gameloader.previous_round() έχει φτάσει στον
    πρώτο/προτελευταίο γύρο
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "PositionReached (Exception): 'arrived one move before limit (1 ~ len-1)'"


class NoMovesFound(Exception):
    """
    Δηλώνει ότι η κλάση game_loader.Gameloader δεν κατάφερε να φορτώσει κινήσεις για τον αγώνα, διότι η συνάρτηση
    functions.get_moves_list() επέστρεψε κενή λίστα
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "no moves for this game"

    def __repr__(self):
        return "NoMovesFound (Exception): 'could not retrieve any moves for this game'"


class PossibleCorruptFile(Exception):
    """
    Δηλώνει ότι η κλάση game_loader.Gameloader δεν κατάφερε να δημιουργήσει στιγμιότυπα του αγώνα, διότι η μέθοδος
    gameplay.Gameplay.next_move() επέστρεψε None

    Ορίσματα:
    ---------
        bug (str): θέση όπου προέκυψε το σφάλμα
    """
    def __init__(self, bug: str = ""):
        super().__init__()
        self.bug = bug

    def __str__(self):
        return f"Failed processing {self.bug}"

    def __repr__(self):
        return f"PossibleCorruptFile (Exception): 'failed processing {self.bug}"


class FriendlyCapture(Exception):
    """
    Δηλώνει ότι η κλάση game_loader.Gameloader δεν κατάφερε να δημιουργήσει στιγμιότυπα του αγώνα, διότι η μεταβλητή
    gameplay.brd.friendly_capture είναι True

    Ορίσματα:
    ---------
        bug (str): θέση όπου προέκυψε το σφάλμα
    """
    def __init__(self, bug: str = ""):
        super().__init__()
        self.bug = bug

    def __str__(self):
        return f"Friendly Capture at {self.bug}"

    def __repr__(self):
        return f"FriendlyCapture (Exception): 'failed processing {self.bug}"
