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

        rooks (dict):
            dictionary containing the rooks

        squares (dict):
            dictionary to accumulate every cell of the board and the state of the piece inside

        friendly_capture (bool):
            boolean value to show same colour capture (not allowed)

    Methods:
    --------
        update_squares(self):
            updates the "squares" dictionary

        update_board(self):
            loops on the pieces and updates the board with the new positions

        move_piece_by_position(self, src: str, dest: str) -> str:
            moves a piece from src square to dest square and returns the name of the captured piece

        move_piece(self, src: str, dest: str) -> str:
            moves the piece to dest and returns the captured piece name
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
        for rank, row in enumerate(range(5, 1, -1), start=3):
            self.pieces.append(Piece(" " * 3, f"a{rank}", state=False, row=row, col=0))
            self.pieces.append(Piece(" " * 3, f"b{rank}", state=False, row=row, col=1))
            self.pieces.append(Piece(" " * 3, f"c{rank}", state=False, row=row, col=2))
            self.pieces.append(Piece(" " * 3, f"d{rank}", state=False, row=row, col=3))
            self.pieces.append(Piece(" " * 3, f"e{rank}", state=False, row=row, col=4))
            self.pieces.append(Piece(" " * 3, f"f{rank}", state=False, row=row, col=5))
            self.pieces.append(Piece(" " * 3, f"g{rank}", state=False, row=row, col=6))
            self.pieces.append(Piece(" " * 3, f"h{rank}", state=False, row=row, col=7))

        # initialization of the chess board ----------------------------------------------------------------------------
        # 2D board 8x8 (only used for printing the board in the console)
        # self.board = [[None for _ in range(8)] for __ in range(8)]
        # pieces are set on the board
        # self.update_board()

        # dictionary containing the kings for easier access
        self.kings = {"w": king_w, "b": king_b}

        # dictionary to accumulate every cell of the board and the state of the piece inside
        # key: square name (e.g. "a8")
        # value: True if the square contains an active piece, False if it contains a decoy
        self.squares = {}
        self.update_squares()

        # boolean value to show same colour capture (not allowed)
        self.friendly_capture: bool = False

    def update_squares(self):
        """
        Loops over the piece list and updates the squares dictionary
        If a square contains an active piece, it is set as True
        Else it is set as False
        """
        for piece in self.pieces:
            self.squares[piece.pos] = piece.state

    def update_board(self):
        """
        Loops over the piece list and updates the board with the new positions
        """
        for piece in self.pieces:
            # self.board[piece.row][piece.col] = piece
            pass

    def move_piece_by_position(self, src: str, dest: str) -> str:
        """
        Moves the piece from src to dest and returns the captured piece name

        ...

        Parameters:
        -----------
            src (str):
                position of the piece to move

            dest (str):
                position to be moved to

        Returns:
        --------
            captured_piece_name_to_return (str):
                the name of the captured piece
        """
        # initialization of variable
        self.friendly_capture = False

        # loop through pieces list to find the piece to move (piece_src)
        for piece_src in self.pieces:
            if piece_src.pos == src:
                # src piece has been found
                # loop through pieces list to find the piece at destination (piece_dest)
                for piece_dest in self.pieces:
                    if piece_dest.pos == dest:
                        # dest piece has been found

                        # colour check (if True, game_loader.GameLoader raises exception)
                        if piece_src.name[1] == piece_dest.name[1]:
                            self.friendly_capture = True

                        # coordinates swap
                        piece_src.row, piece_dest.row = piece_dest.row, piece_src.row
                        piece_src.col, piece_dest.col = piece_dest.col, piece_src.col

                        # position swap between src and dest
                        piece_src.pos, piece_dest.pos = piece_dest.pos, piece_src.pos

                        # temporary assignment of the captured piece name
                        captured_piece_name_to_return = piece_dest.name
                        # captured piece becomes empty (decoy)
                        piece_dest.got_captured()

                        # update the squares dictionary after move is performed
                        self.update_squares()
                        # updates the board with new piece positions (only used for console printing)
                        # self.update_board()

                        return captured_piece_name_to_return

    def move_piece(self, piece_src: Piece, dest: str) -> str:
        """
        Moves the piece to dest and returns the captured piece name

        ...

        Parameters:
        -----------
            piece_src (Piece):
                piece to move

            dest (str):
                position to be moved to

        Returns:
        --------
            captured_piece_name_to_return (str):
                the name of the captured piece
        """
        # initialization of variable
        self.friendly_capture = False

        # loop through pieces list to find the piece at destination (piece_dest)
        for piece_dest in self.pieces:
            if piece_dest.pos == dest:
                # dest piece has been found

                # colour check (if True, game_loader.GameLoader raises exception)
                if piece_src.name[1] == piece_dest.name[1]:
                    self.friendly_capture = True

                # coordinates swap
                piece_src.row, piece_dest.row = piece_dest.row, piece_src.row
                piece_src.col, piece_dest.col = piece_dest.col, piece_src.col

                # position swap between src and dest
                piece_dest.pos = piece_src.pos
                piece_src.pos = dest

                # temporary assignment of the captured piece name
                captured_piece_name_to_return = piece_dest.name
                # captured piece becomes empty (decoy)
                piece_dest.got_captured()

                # update the squares dictionary after move is performed
                self.update_squares()
                # updates the board with new piece positions (only used for console printing)
                # self.update_board()

                return captured_piece_name_to_return
