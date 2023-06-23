# -------------------------------------------------------------------------------------------------------------------- #
# board.py: includes class Board                                                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
from piece import Piece


class Board:
    """
    Creates the chess board
    Places the piece objects and performs their moves through methods

    ...

    Attributes:
    -----------
        pieces (list):
            list containing the piece objects

        board (list):
            2D array representing the chess board

        kings (dict):
            dictionary containing the kings

        rooks(dict):
            dictionary containing the rooks

        squares (dict):
            dictionary to accumulate every cell of the board and the state of the piece inside

        friendly_capture (bool):
            boolean value to show same colour capture (not allowed)

    Methods:
    --------
        __update_squares(self):
            updates the "squares" dictionary

        update_self(self):
            loops on the pieces and updates the board with the new positions

        move_piece(self, src: str, dest: str) -> str:
            moves a piece from src square to dest square and returns the name of the captured piece
    """
    def __init__(self):
        """
        Initializes the board and other useful attributes
        """
        # initialization of the pieces ---------------------------------------------------------------------------------
        # list containing the pieces
        self.pieces = [
            # "white" pieces
            king_w := Piece("kwr", "e1", row=7, col=4), Piece("qwl", "d1", row=7, col=3),
            Piece("rwl", "a1", row=7, col=0), Piece("rwr", "h1", row=7, col=7),
            Piece("nwl", "b1", row=7, col=1), Piece("nwr", "g1", row=7, col=6),
            Piece("bwl", "c1", row=7, col=2), Piece("bwr", "f1", row=7, col=5),
            Piece("pw1", "a2", row=6, col=0), Piece("pw2", "b2", row=6, col=1),
            Piece("pw3", "c2", row=6, col=2), Piece("pw4", "d2", row=6, col=3),
            Piece("pw5", "e2", row=6, col=4), Piece("pw6", "f2", row=6, col=5),
            Piece("pw7", "g2", row=6, col=6), Piece("pw8", "h2", row=6, col=7),
            # "black" pieces
            king_b := Piece("kbr", "e8", row=0, col=4), Piece("qbl", "d8", row=0, col=3),
            Piece("rbl", "a8", row=0, col=0), Piece("rbr", "h8", row=0, col=7),
            Piece("nbl", "b8", row=0, col=1), Piece("nbr", "g8", row=0, col=6),
            Piece("bbl", "c8", row=0, col=2), Piece("bbr", "f8", row=0, col=5),
            Piece("pb1", "a7", row=1, col=0), Piece("pb2", "b7", row=1, col=1),
            Piece("pb3", "c7", row=1, col=2), Piece("pb4", "d7", row=1, col=3),
            Piece("pb5", "e7", row=1, col=4), Piece("pb6", "f7", row=1, col=5),
            Piece("pb7", "g7", row=1, col=6), Piece("pb8", "h7", row=1, col=7)
        ]

        # initialization of empty squares
        # assuming every board square contains a piece, empty squares contain invisible decoys
        # these are used to simplify the position transitions of the pieces
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

        # initialization of the chess board ----------------------------------------------------------------------------
        # 2D board 8x8
        self.board = [[None for _ in range(8)] for __ in range(8)]

        # dictionary containing the kings for easier access
        self.kings = {"w": king_w, "b": king_b}

        # dictionary to accumulate every cell of the board and the state of the piece inside
        # key: square name (e.g. "a8")
        # value: True if the square contains an active piece, False if it contains a decoy
        self.squares = {}

        # boolean value to show same colour capture (not allowed)
        self.friendly_capture: bool = False

    def __update_squares(self, piece):
        """
        Updates the squares dictionary

        ...

        Parameters:
        -----------
            piece (Piece):
                current piece from the loop in update_self method
        """
        # εάν το κελί έχει κάποιο ενεργό κομμάτι, χαρακτηρίζεται ως το tag (w/b) του κομματιού,
        # διαφορετικά αν είναι κενό False
        if piece.state:
            self.squares[piece.pos] = piece.name[1]
        else:
            self.squares[piece.pos] = False

    def update_self(self):
        """
        Loops over the piece list and updates the board with the new positions
        """
        for piece in self.pieces:
            self.__update_squares(piece)
            # column a
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

            # column b
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

            # column c
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

            # column d
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

            # column e
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

            # column f
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

            # column g
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

            # column h
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
        Moves the piece from src to dest and returns the captures piece name

        Parameters:
        -----------
            src (str): piece to move

            dest (str): position to be moved to

        Returns:
        --------
            captured_piece_name_to_return (str):
                the name of the captured piece (used in captured_piece_frame.CapturedPieceFrame to show captured pieces)
        """
        # initialization of variable
        self.friendly_capture = False

        # loop through pieces list to find the piece to move (piece_src)
        for piece_src in self.pieces:
            if piece_src.pos == src:
                # src piece has been found
                # temporary assignment of current coordinates of src
                row_src = piece_src.row
                col_src = piece_src.col

                # loop through pieces list to find the piece at destination (piece_dest)
                for piece_dest in self.pieces:
                    if piece_dest.pos == dest:
                        # src piece has been found

                        # colour check
                        if piece_src.name[1] == piece_dest.name[1]:
                            self.friendly_capture = True

                        # temporary assignment of current coordinates of dest
                        row_dest = piece_dest.row
                        col_dest = piece_dest.col

                        # position swap between src and dest
                        piece_dest.pos = src
                        piece_src.pos = dest

                        # temporary assignment of the captured piece name
                        captured_piece_name_to_return = piece_dest.name
                        # captured piece becomes empty (decoy)
                        piece_dest.name = "   "
                        piece_dest.state = False

                        # coordinates swap
                        piece_dest.row = row_src
                        piece_dest.col = col_src
                        piece_src.row = row_dest
                        piece_src.col = col_dest

                        return captured_piece_name_to_return
