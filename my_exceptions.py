# -------------------------------------------------------------------------------------------------------------------- #
# my_exceptions.py: includes custom exception for error handling                                                       #
# -------------------------------------------------------------------------------------------------------------------- #


class PositionReached(Exception):
    """
    Declares that the GameLoader.next_move or GameLoader.previous_move method has reached the second/second to last
    round
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "PositionReached (Exception): 'arrived one move before limit (1 ~ len-1)'"


class NoMovesFound(Exception):
    """
    Declares that the GameLoader class couldn't load any moves for a game
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "no moves for this game"

    def __repr__(self):
        return "NoMovesFound (Exception): 'could not retrieve any moves for this game'"


class FalseGame(Exception):
    """
    Declares that the GameLoader class could not process the moves list and create screenshots of the game

    ...

    Parameters:
    -----------
        bug (str):
            move that raised the exception
    """
    def __init__(self, bug: str = ""):
        super().__init__()
        self.bug = bug

    def __str__(self):
        return f"Failed processing {self.bug}"

    def __repr__(self):
        return f"FalseGame (Exception): 'failed processing {self.bug}"


class PossibleCorruptFile(Exception):
    """
    Declares that the FilePGN class could not load the file properly and the list of data created is not ok

    ...

    Parameters:
    -----------
        bug (str):
            description
    """
    def __init__(self, bug: str = ""):
        super().__init__()
        self.bug = bug

    def __str__(self):
        return "Error! Please check pgn file"

    def __repr__(self):
        return f"PossibleCorruptFile (Exception): {self.bug}"


class FriendlyCapture(Exception):
    """
    Declares that the GameLoader class could not create screenshot of the game, because a friendly capture occurred

    Parameters:
    -----------
        bug (str):
            move that raised the exception
    """
    def __init__(self, bug: str = ""):
        super().__init__()
        self.bug = bug

    def __str__(self):
        return f"Friendly Capture at {self.bug}"

    def __repr__(self):
        return f"FriendlyCapture (Exception): 'failed processing {self.bug}"
