# -------------------------------------------------------------------------------------------------------------------- #
# piece.py: includes class Piece                                                                                       #
# -------------------------------------------------------------------------------------------------------------------- #


class Piece:
    """
    Initializes every chess piece as an object with basic attributes

    ...

    Attributes:
    -----------
        name (str):
            name of the piece (e.g. rbl= rook black left etc.)

        pos (str):
            position of the piece (e.g. a8= column a, row 8 etc.)

        state (bool):
            state of the piece (True if active, False if captured)

        row (int):
            row (0~7) on the board (used in gui.GUI)

        col (int):
            column (0~7) on the board (used in gui.GUI)

    Methods:
    --------
        got_captured(self) -> None:
            turns a piece into a captured decoy
    """

    def __init__(self, name: str, pos: str, state: bool = True, row=-1, col=-1):
        """
        Initializes the object

        ...

        Parameters:
        -----------
            name (str):
                name of the piece (e.g. rbl= rook black left etc.)

            pos (str):
                position of the piece (e.g. a8= column a, row 8 etc.)

            state (bool):
                state of the piece (True if active, False if captured)

            row (int):
                row (0~7) on the board (used in gui.GUI)

            col (int):
                column (0~7) on the board (used in gui.GUI)
        """
        self.name = name    # name of the piece (e.g. rbl= rook black left etc.)
        self.pos = pos      # position of the piece (e.g. a8= column a, row 8 etc.)
        self.state = state  # state of the piece (True if active, False if captured)

        # coordinates used in the graphical representation of the pieces on the board (see class gui.GUI)
        self.row = row  # row (0~7) on the board (used in gui.GUI)
        self.col = col  # column (0~7) on the board (used in gui.GUI)

    def got_captured(self) -> None:
        """
        Turns a piece into a captured decoy
        """
        self.name = "   "
        self.state = False

    def __repr__(self):
        """
        Return a string with the object info
        """
        return f"{self.name}({self.pos}) [{self.row}][{self.col}]"
