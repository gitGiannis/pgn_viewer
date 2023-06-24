# -------------------------------------------------------------------------------------------------------------------- #
# move_checking.py: includes class PieceMoveChecker                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
from board import Board


class PieceMoveChecker(Board):
    """
    Inherits from parent class Board
    Combines the information from the moves list (it is provided as parameter) and the attributes and methods of the
    parent Board class
    Using the moves list and performing a series of checks, it manages the chess board by moving the pieces to their
    new positions through the Board.move_piece(*args) method

    Attributes:
    -----------
        moves (list):
            the moves taken in as argument

        moves_length (int):
            the length of the moves list

        files (list[str]):
            list with the columns of the chess board

        ranks (list[str]):
            list with the rows of the chess board

        diags (list[list[str]]):
            list containing all the diagonals of the chess board

        knight_moves (list[tuple[int]]):
            list with all the move ranges of the knight (N)

        round_cnt (int):
            counter for each half move

        check (str | None):
            variable to keep track of the rounds with check/checkmate

        capture (bool):
            variable to keep track of the rounds with captured

    Methods:
    --------
        next_move(self) -> str | None:
            executes next move and returns the name of the piece captured

        __diagonal_move_is_valid(self, src: str, dest: str) -> bool:
            checks whether the diagonal move of a piece is valid

        __horizontal_or_vertical_move_is_valid(self, src: str, dest: str) -> bool:
            checks whether the horizontal/vertical move of a piece is valid

        __knight_move_is_valid(self, src: str, dest: str) -> bool:
            checks whether the knight move of a piece is valid

        __king_move_is_valid(self, src: str, dest: str) -> bool:
            checks whether the king move of a piece is valid

        __piece_is_not_pinned(self, src: str, dest: str, tag: str) -> bool:
            checks whether a piece is pinned to the king
    """
    def __init__(self, list_of_moves: list):
        """
        Initializes the Gameplay object, to check which piece is to move

        ...

        Parameters:
        -----------
            list_of_moves (list):
                list with the moves of the game stripped of extra information (round indexes, comments etc.)
        """
        # initialization of the parent class Board ---------------------------------------------------------------------
        super().__init__()

        # list of moves of the game
        self.moves = list_of_moves

        # length of the moves list
        self.moves_length = len(self.moves)

        # initialization of list with various information --------------------------------------------------------------
        # list of board columns
        self.files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        # list of board rows
        self.ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]
        # # list of board diagonals
        self.diags = [["a1", "b2", "c3", "d4", "e5", "f6", "g7", "h8"],
                      ["a8", "b7", "c6", "d5", "e4", "f3", "g2", "h1"],
                      ["a2", "b3", "c4", "d5", "e6", "f7", "g8"],
                      ["a7", "b6", "c5", "d4", "e3", "f2", "g1"],
                      ["h2", "g3", "f4", "e5", "d6", "c7", "b8"],
                      ["h7", "g6", "f5", "e4", "d3", "c2", "b1"],
                      ["a3", "b4", "c5", "d6", "e7", "f8"],
                      ["a6", "b5", "c4", "d3", "e2", "f1"],
                      ["h3", "g4", "f5", "e6", "d7", "c8"],
                      ["h6", "g5", "f4", "e3", "d2", "c1"],
                      ["a4", "b5", "c6", "d7", "e8"],
                      ["a5", "b4", "c3", "d2", "e1"],
                      ["h4", "g5", "f6", "e7", "d8"],
                      ["h5", "g4", "f3", "e2", "d1"],
                      ["a5", "b6", "c7", "d8"],
                      ["a4", "b3", "c2", "d1"],
                      ["h5", "g6", "f7", "e8"],
                      ["h4", "g3", "f2", "e1"],
                      ["a6", "b7", "c8"],
                      ["a3", "b2", "c1"],
                      ["h6", "g7", "f8"],
                      ["h3", "g2", "f1"],
                      ["a7", "b8"],
                      ["a2", "b1"],
                      ["h7", "g8"],
                      ["h2", "g1"]
                      ]
        # list with all possible ranges for the knight (N) to move, assuming the latter is in the (0, 0) position
        self.knight_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]

        # initialization of counter var
        self.round_cnt = -1

        # initialization of auxiliary variables ------------------------------------------------------------------------
        self.check = None
        self.capture = False

    def next_move(self) -> str | None:
        """
        Executes the next move based on the current move from the moves list

        ...

        Returns:
        --------
            (str | None):
                (str) the name (piece.name) of the captured piece
                (None) no move could be executed (used to raise an exception later on)
        """
        # return the auxiliary variables to the original values
        self.check = None
        self.capture = False

        # increase of the counter value
        self.round_cnt += 1
        # update the board with the new piece positions
        self.update_board()
        # switching between colour tag of the current player to play ('w' for white, 'b' for black)
        if self.round_cnt % 2 == 0:
            tag = "w"
        else:  # self.round % 2 == 1
            tag = "b"

        # temporary assignment of current move
        move: str = self.moves[self.round_cnt]

        if "x" in move:
            # if the move contains the 'x' character, it means an enemy piece is to be captured
            self.capture = True

        # special moves ------------------------------------------------------------------------------------------------
        # brilliant move, blunder etc.
        if "!" in move or "?" in move:
            move = move[:len(move) - 1]
            if "!" in move or "?" in move:
                move = move[:len(move) - 1]

        # check / checkmate
        if "+" in move or "#" in move:
            # self.check is assigned the tag of the king being checked
            self.check = "b" if tag == "w" else "w"
            move = move[:len(move) - 1]

        # castling
        if move == "O-O" or move == "O-O-O":
            #  O-O -> king-side castling, 0-0-0 queen-side castling
            for piece in self.pieces:
                if piece.name[0] == "k" and piece.name[1] == tag:
                    if tag == "w":
                        # white king castles
                        if move == "O-O":
                            self.move_piece(piece.pos, "g1")
                            self.move_piece("h1", "f1")
                            return "   "
                        if move == "O-O-O":
                            self.move_piece(piece.pos, "c1")
                            self.move_piece("a1", "d1")
                            return "   "

                    elif tag == "b":
                        # black king castles
                        if move == "O-O":
                            self.move_piece(piece.pos, "g8")
                            self.move_piece("h8", "f8")
                            return "   "
                        if move == "O-O-O":
                            self.move_piece(piece.pos, "c8")
                            self.move_piece("a8", "d8")
                            return "   "

        # pawn promotion
        # variable to store whether a pawn gets promoted (True) or not (False)
        pawn_promotion = False
        # variable to store the pawn promotion type ("q"=promotes to queen, "r"=promotes to rook etc.)
        promotion = ""
        # temporary variable to store the name of the captured piece if en-passant is performed
        en_passant = ""

        if "=" in move:
            # if the move contains the '=' character, it means a pawn is to be promoted (e.g. e8=Q or fxe8=R etc.)
            pawn_promotion = True
            # 'promotion' variable is assigned the type of piece it is promoted to
            # the moves gets stripped of the promotion part (e.g. e8=Q -> promotion == q and move == e8)
            promotion = move[-1].lower()
            move = move[:len(move) - 2]

        # pawn gets moved ----------------------------------------------------------------------------------------------
        if len(move) == 2 or (len(move) == 4 and move[0].islower() and move[1] == "x"):
            # simple forward move (e.g. e4)
            if len(move) == 2:
                # loop through the pieces list to find the pawn to move
                for piece in self.pieces:
                    # check whether it's a suitable colour and position pawn (same file)
                    if piece.name[0] == "p" and piece.name[1] == tag and piece.pos[0] == move[0]:
                        if self.squares[move]:
                            # a pawn cannot perform a simple move if the destination square is active
                            continue

                        # white pawns increase their rank when moved, so the difference in rank is positive
                        # black pawns decrease their rank when moved, so the difference in rank is negative
                        diff_in_rank_after_moving = int(move[1]) - int(piece.pos[1])

                        # a pawn cannot move more than two squares or stay stationary
                        if diff_in_rank_after_moving < -2 or diff_in_rank_after_moving > 2 or piece.pos[0] != move[0]:
                            continue

                        # a white pawn can only increase its rank, the opposite applies for black pawns
                        if (diff_in_rank_after_moving > 0 and piece.name[1] == "b") or \
                           (diff_in_rank_after_moving < 0 and piece.name[1] == "w"):
                            continue

                        # for a pawn to move two squares, it has ot be on the starting position
                        if (diff_in_rank_after_moving == 2 and piece.pos[1] != "2") or \
                           (diff_in_rank_after_moving == -2 and piece.pos[1] != "7"):
                            continue

                        # if all the above statements are false, the pawn is free to move
                        # promotion check
                        if pawn_promotion:
                            # the pawn promotes and gets assigned a new name
                            piece.name = promotion + tag + "+"
                        return self.move_piece(piece.pos, move)

            # pawn captures (e.g. dxe4)
            elif len(move) == 4 and move[0].islower() and move[1] == "x":
                # loop through the pieces list to find the pawn to move
                for piece in self.pieces:
                    # # check whether it's a suitable colour and position pawn
                    if piece.name[0] == "p" and piece.name[1] == tag and piece.pos[0] == move[0]:
                        # temporary assignment of the piece rank difference
                        diff_in_rank_after_moving = int(move[3]) - int(piece.pos[1])

                        # check whether the pawn can perform the capture
                        if (tag == "w" and diff_in_rank_after_moving != 1) or \
                           (tag == "b" and diff_in_rank_after_moving != -1):
                            # the piece rank difference must be equal to 1 for white pawns and -1 for black pawns
                            continue

                        # check if the captured square is empty (en-passant performed)
                        if not self.squares[move[2:]]:
                            # the pawn will secretly move to each side to capture the enemy pawn and then move to its
                            # final destination
                            if tag == "w":
                                # a white pawn performed "en passant"
                                # temporary new rank
                                temporary_rank = int(move[3]) - 1
                                # temporary move
                                temporary_move = move[2] + str(temporary_rank)
                                # secret move to capture the enemy pawn
                                en_passant = self.move_piece(piece.pos, temporary_move)

                            elif tag == "b":
                                # a black pawn performed "en passant"
                                # temporary new rank
                                temporary_rank = int(move[3]) + 1
                                # temporary move
                                temporary_move = move[2] + str(temporary_rank)
                                # secret move to capture the enemy pawn
                                en_passant = self.move_piece(piece.pos, temporary_move)

                        # promotion check
                        if pawn_promotion:
                            # the pawn promotes and gets assigned a new name
                            piece.name = promotion + tag + "+"

                        # pawn moves to its new position
                        captured_piece_name = self.move_piece(piece.pos, move[2:])
                        # there was a capture in this move, so a captured piece name must be returned
                        if captured_piece_name != "   ":
                            return captured_piece_name
                        if en_passant:
                            # if en_passant != "", a piece was captured by en-passant
                            return en_passant

        # king gets moved (king K) -------------------------------------------------------------------------------------
        elif move[0] == "K":
            # a piece has been captured
            if "x" in move:
                x = move.find("x")
                move = move[:x] + move[x + 1:]

            # loop through the pieces list to find the king
            for piece in self.pieces:
                # check if suitable colour king
                if piece.name[0] == "k" and piece.name[1] == tag:
                    # check if the move is valid
                    if self.__king_move_is_valid(piece.pos, move[1:]):
                        # king gets moved
                        return self.move_piece(piece.pos, move[1:])

        # queen gets moved (Queen Q) ----------------------------------------------------------------------------------
        elif move[0] == "Q":
            # a piece has been captured
            if "x" in move:
                x = move.find("x")
                move = move[:x] + move[x + 1:]

            # case Q__: (e.g. Qf3)
            if len(move) == 3:
                # loop through the pieces list to find the queen to move
                for piece in self.pieces:
                    # check if suitable colour queen
                    if piece.name[0] == "q" and piece.name[1] == tag:
                        # check if the move is valid
                        if self.__diagonal_move_is_valid(src=piece.pos, dest=move[1:]) or \
                           self.__horizontal_or_vertical_move_is_valid(src=piece.pos, dest=move[1:]):
                            # check if the queen is not pinned to the king
                            if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                # queen gets moved
                                return self.move_piece(piece.pos, move[1:])

            # case Q___: (e.g. Qcb4 or Q3b4)
            if len(move) == 4:
                # loop through the pieces list to find the queen to move
                for piece in self.pieces:
                    # check if suitable colour queen
                    if piece.name[0] == "q" and piece.name[1] == tag:
                        # check if suitable position queen
                        if piece.pos[0] == move[1] or piece.pos[1] == move[1]:
                            # check if the move is valid
                            if self.__diagonal_move_is_valid(piece.pos, move[2:]) or \
                               self.__horizontal_or_vertical_move_is_valid(piece.pos, move[2:]):
                                # check if the queen is not pinned to the king
                                if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                    # queen gets moved
                                    return self.move_piece(piece.pos, move[2:])

            # case Q____: (e.g. Qb1b4)
            elif len(move) == 5:
                # loop through the pieces list to find the queen to move
                for piece in self.pieces:
                    # check if suitable colour and position queen
                    if piece.name[0] == "q" and piece.name[1] == tag and piece.pos == move[1:3]:
                        # check if the move is valid
                        if self.__diagonal_move_is_valid(piece.pos, move[3:]) or \
                           self.__horizontal_or_vertical_move_is_valid(piece.pos, move[3:]):
                            # check if the queen is not pinned to the king
                            if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                # queen gets moved
                                return self.move_piece(piece.pos, move[3:])

        # knight gets moved (knight N) ---------------------------------------------------------------------------------
        elif move[0] == "N":
            # a piece has been captured
            if "x" in move:
                x = move.find("x")
                move = move[:x] + move[x + 1:]

            # case N__: (e.g. Nf3)
            if len(move) == 3:
                # loop through the pieces list to find the knight to move
                for piece in self.pieces:
                    # check if suitable colour knight
                    if piece.name[0] == "n" and piece.name[1] == tag:
                        # check if the move is valid
                        if self.__knight_move_is_valid(src=piece.pos, dest=move[-2:]):
                            # check if the knight is not pinned to the king
                            if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                # knight gets moved
                                return self.move_piece(piece.pos, move[1:])

            # case N___: (e.g. Nfb4 or N1b4)
            elif len(move) == 4:
                # loop through the pieces list to find the knight to move
                for piece in self.pieces:
                    # check if suitable colour knight
                    if piece.name[0] == "n" and piece.name[1] == tag:
                        # check if suitable position knight
                        if piece.pos[0] == move[1] or piece.pos[1] == move[1]:
                            # check if the move is valid
                            if self.__knight_move_is_valid(src=piece.pos, dest=move[-2:]):
                                # check if the knight is not pinned to the king
                                if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                    # knight gets moved
                                    return self.move_piece(piece.pos, move[2:])

            # case N____: (e.g. Nd3b5)
            elif len(move) == 5:
                # loop through the pieces list to find the knight to move
                for piece in self.pieces:
                    # check if suitable colour and position knight
                    if piece.name[0] == "n" and piece.name[1] == tag and piece.pos == move[1:3]:
                        # check if the move is valid
                        if self.__knight_move_is_valid(src=piece.pos, dest=move[-2:]):
                            # check if the knight is not pinned to the king
                            if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                # knight gets moved
                                return self.move_piece(piece.pos, move[3:])

        # bishop gets moved (bishop B) ---------------------------------------------------------------------------------
        elif move[0] == "B":
            # a piece has been captured
            if "x" in move:
                x = move.find("x")
                move = move[:x] + move[x + 1:]

            # case B__: (e.g. Bf3)
            if len(move) == 3:
                # loop through the pieces list to find the bishop to move
                for piece in self.pieces:
                    # check if suitable colour bishop
                    if piece.name[0] == "b" and piece.name[1] == tag:
                        # check if the move is valid
                        if self.__diagonal_move_is_valid(src=piece.pos, dest=move[1:]):
                            # check if the bishop is not pinned to the king
                            if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                # bishop gets moved
                                return self.move_piece(piece.pos, move[1:])

            # case B___: (e.g. Bcb4 or B3b4)
            elif len(move) == 4:
                # loop through the pieces list to find the bishop to move
                for piece in self.pieces:
                    # check if suitable colour bishop
                    if piece.name[0] == "b" and piece.name[1] == tag:
                        # check if suitable position bishop
                        if piece.pos[0] == move[1] or piece.pos[1] == move[1]:
                            # check if the move is valid
                            if self.__diagonal_move_is_valid(src=piece.pos, dest=move[2:]):
                                # check if the bishop is not pinned to the king
                                if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                    # bishop gets moved
                                    return self.move_piece(piece.pos, move[2:])

            # case B____: (e.g. Bb1e4)
            elif len(move) == 5:
                # loop through the pieces list to find the bishop to move
                for piece in self.pieces:
                    # check if suitable colour and position bishop
                    if piece.name[0] == "b" and piece.name[1] == tag and piece.pos == move[1:3]:
                        # check if the move is valid
                        if self.__diagonal_move_is_valid(src=piece.pos, dest=move[3:]):
                            # check if the bishop is not pinned to the king
                            if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                # bishop gets moved
                                return self.move_piece(piece.pos, move[3:])

        # rook gets moved (rook R) -------------------------------------------------------------------------------------
        elif move[0] == "R":
            # a piece has been captured
            if "x" in move:
                x = move.find("x")
                move = move[:x] + move[x + 1:]

            # case R__: (e.g. Rf3)
            if len(move) == 3:
                # loop through the pieces list to find the rook to move
                for piece in self.pieces:
                    # check if suitable colour rook
                    if piece.name[0] == "r" and piece.name[1] == tag:
                        # check if the move is valid
                        if self.__horizontal_or_vertical_move_is_valid(src=piece.pos, dest=move[1:]):
                            # check if the rook is not pinned to the king
                            if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                # rook gets moved
                                return self.move_piece(piece.pos, move[1:])

            # case R___: (e.g. Rbb4 or R4b4)
            elif len(move) == 4:
                # loop through the pieces list to find the rook to move
                for piece in self.pieces:
                    # check if suitable colour rook
                    if piece.name[0] == "r" and piece.name[1] == tag:
                        # έλεγχος εάν είναι στην κατάλληλη θέση
                        if piece.pos[0] == move[1] or piece.pos[1] == move[1]:
                            # check if the move is valid
                            if self.__horizontal_or_vertical_move_is_valid(src=piece.pos, dest=move[2:]):
                                # check if the rook is not pinned to the king
                                if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                    # rook gets moved
                                    return self.move_piece(piece.pos, move[2:])

            # case R____: (e.g. Rb1b4)
            elif len(move) == 5:
                # loop through the pieces list to find the rook to move
                for piece in self.pieces:
                    # check if suitable colour and position rook
                    if piece.name[0] == "r" and piece.name[1] == tag and piece.pos == move[1:3]:
                        # check if the move is valid
                        if self.__horizontal_or_vertical_move_is_valid(src=piece.pos, dest=move[1:3]):
                            # check if the rook is not pinned to the king
                            if self.__piece_is_not_pinned(src=piece.pos, dest=move[-2:], tag=tag):
                                # rook gets moved
                                return self.move_piece(piece.pos, move[1:3])

        # no move could be performed (the file might not be correct)
        return None

    def __diagonal_move_is_valid(self, src: str, dest: str) -> bool:
        """
        Returns True if the diagonal move of a piece (queen, bishop) is valid by checking if the path from src to dest
        position is clear
        Returns False if the path is blocked

        ...

        Parameters:
        -----------
            src (str): starting position (e.g. e4)

            dest (str): destination position (e.g. g6)

        Returns:
        --------
            (bool):
                True: the move is valid
                False: the move is not valid
        """
        if src == dest:
            # piece cannot stay on the same square
            return False

        # initialization of auxiliary var
        # gets set to True if checking between src and dest
        in_range_flag = False
        # loop through the diagonals to find the one containing both the src and dest positions
        for diag in self.diags:
            if src in diag and dest in diag:
                # both squares are in the same diagonal
                # all squares in between must be empty for the move to be performed
                for square in diag:
                    # loop through the current diagonal until one is found
                    if square != src and square != dest and in_range_flag is False:
                        # continues to the next loop while out of range
                        continue

                    if square == src or square == dest:
                        # the first time this statement is passes means the loop is in range and the flag is set to True
                        # the second time it is set to False as the loop gets out of the move range
                        in_range_flag = not in_range_flag
                        continue
                    # the squares are checked while the flag is True
                    if in_range_flag:
                        # if a square is active, the path is blocked and the False value is returned
                        if self.squares[square]:
                            return False

                # the for loop ends without breaks, the path is not blocked and the move is valid
                else:
                    return True

        # no diagonal contains both src and dest
        return False

    def __horizontal_or_vertical_move_is_valid(self, src: str, dest: str) -> bool:
        """
        Returns True if the horizontal/vertical move of a piece (queen, rook) is valid by checking if the path from src
        to dest position is clear
        Returns False if the path is blocked

        ...

        Parameters:
        -----------
            src (str): starting position (e.g. e4)

            dest (str): destination position (e.g. e6)

        Returns:
        --------
            (bool):
                True: the move is valid
                False: the move is not valid
        """
        if src == dest:
            # piece cannot stay on the same square
            return False

        # rook on same file
        if src[0] == dest[0]:
            # 1. rook rank < move rank
            if src[1] < dest[1]:
                for num in self.ranks:
                    # loop continues while out of move range
                    if num <= src[1] or num >= dest[1]:
                        continue
                    if self.squares[src[0] + num]:
                        # if a square is active, the path is blocked and the False value is returned
                        return False
                # the for loop ends without breaks, the path is not blocked and the move is valid
                return True

            # 2. rook rank > move rank
            if src[1] > dest[1]:
                for num in self.ranks:
                    # loop continues while out of move range
                    if num <= dest[1] or num >= src[1]:
                        continue
                    if self.squares[src[0] + num]:
                        # if a square is active, the path is blocked and the False value is returned
                        return False
                # the for loop ends without breaks, the path is not blocked and the move is valid
                return True

        # rook on same rank
        elif src[1] == dest[1]:
            # 1. rook file > move file
            if src[0] > dest[0]:
                for letter in self.files:
                    # loop continues while out of move range
                    if letter <= dest[0] or letter >= src[0]:
                        continue
                    if self.squares[letter + src[1]]:
                        # if a square is active, the path is blocked and the False value is returned
                        return False
                # the for loop ends without breaks, the path is not blocked and the move is valid
                return True

            # 2. rook file < move file
            if src[0] < dest[0]:
                for letter in self.files:
                    # loop continues while out of move range
                    if letter >= dest[0] or letter <= src[0]:
                        continue
                    if self.squares[letter + str(src[1])]:
                        # if a square is active, the path is blocked and the False value is returned
                        return False
                # the for loop ends without breaks, the path is not blocked and the move is valid
                return True

    def __knight_move_is_valid(self, src: str, dest: str) -> bool:
        """
        Returns True if the knight move is valid by checking if the latter is within the correct range
        Returns False if the knight is out of range

        ...

        Parameters:
        -----------
            src (str): staring position (e.g. b1)

            dest (str): destination position (e.g. c3)

        Returns:
        --------
            (bool):
                True: the move is valid
                False: the move is not valid
        """
        # storing the difference in dile and rank
        # the difference is converted to integer by finding their positions on the list (file, rank)
        distance_by_file = self.files.index(src[0]) - self.files.index(dest[0])
        distance_by_rank = self.ranks.index(src[1]) - self.ranks.index(dest[1])
        # if the tuple is contained in the knight_moves list, the move is valid
        if (distance_by_file, distance_by_rank) in self.knight_moves:
            return True
        # else the move is not valid and False is returned
        return False

    def __king_move_is_valid(self, src: str, dest: str) -> bool:
        """
        Returns True if the move of the king is valid
        Else returns False

        ...

        Parameters:
        -----------
            src (str): staring position (e.g. e4)

            dest (str): destination position (e.g. e5)

        Επιστρεφόμενο αντικείμενο:
        --------------------------
            (bool):
                True: η κίνηση είναι έγκυρη
                False: η κίνηση δεν είναι έγκυρη
        """
        if src == dest:
            # έλεγχος εάν έχουμε ίδια θέση εκκίνησης - προορισμού (δεν επιτρέπεται)
            return False

        # ορισμός μεταβλητών για πιο εύκολη πρόσβαση
        king_file = src[0]
        king_rank = int(src[1])
        dest_file = dest[0]
        dest_rank = int(dest[1])

        # --- οριζόντια κίνηση ---
        if king_file == dest_file:
            # έλεγχος εάν το rank (γραμμή) του βασιλιά έχει διαφορά μία μονάδα
            if king_rank - 1 == dest_rank or king_rank + 1 == dest_rank:
                return True

        # --- κάθετη κίνηση ---
        if king_rank == dest_rank:
            # εύρεση του index του γράμματος μέσα στο self.files, ώστε να "μετατραπούν" σε αριθμητικές τιμές και να
            # γίνει σύγκριση
            king_file_index = self.files.index(king_file)
            dest_file_index = self.files.index(dest_file)
            # έλεγχος εάν το file (στήλη) του βασιλιά έχει διαφορά ένα γράμμα
            if king_file_index - 1 == dest_file_index or king_file_index + 1 == dest_file_index:
                return True

        # --- διαγώνια κίνηση ---
        # αρχικοποίηση βοηθητικής μεταβλητής
        # όταν ενεργοποιηθεί, σημαίνει πως πρέπει να ελεγχθεί το επόμενο κελί
        check_next_flag = False
        for diag in self.diags:
            # έλεγχος εάν και οι δύο θέσεις βρίσκονται στην ίδια διαγώνιο
            if src in diag and dest in diag:
                # βασιλιάς και θέση επίθεσης βρίσκονται στην ίδια διαγώνιο
                # για να μπορεί να εκτελεστεί η κίνηση από αυτό τον βασιλιά, θα πρέπει να είναι το αμέσως επόμενο κελί
                for square in diag:
                    # διατρέχουμε τα κελιά μέχρι να βρούμε το ένα απο τα δύο (κομμάτι ή θέση επίθεσης)
                    if square != src and square != dest and check_next_flag is False:
                        # συνεχίζουμε στην επόμενη επανάληψη όσο είμαστε εκτός εύρους κίνησης
                        continue
                    # όταν βρεθεί το ένα, ενεργοποιείται το flag, ώστε να ελεγχθεί το επόμενο κελί
                    if (square == src or square == dest) and check_next_flag is False:
                        check_next_flag = True
                        continue
                    # όταν το flag ενεργοποιηθεί, ελέγχεται το επόμενο κελί
                    if check_next_flag:
                        # εάν κάποιο από τα κελιά είναι ενεργό, διακόπτεται η αναζήτηση
                        if square == dest or square == src:
                            return True

        # απέτυχαν όλοι οι έλεγχοι, η κίνηση δεν είναι εφικτή
        return False

    def __piece_is_not_pinned(self, src: str, dest: str, tag: str) -> bool:
        """
        Checked whether a piece is pinned to the king
        If a piece is blocking its king from being checked, it is said that the first is pinned to the king and cannot
        move in any position that would expose the king

        ...

        Parameters:
        -----------
            src (str): staring position (e.g. e4)

            dest (str): destination position (e.g. e6)

            tag (str): "w"/"b" based on the player that plays the move

        Returns:
        --------
            (bool):
                True: piece is not pinned
                False: piece is pinned
        """
        # αποθήκευση θέσης βασιλιά με τη χρήση του λεξικού kings της κλάσης board.Board
        king_pos = self.kings[tag].pos

        # έλεγχος γραμμής ----------------------------------------------------------------------------------------------
        # δημιουργία λίστας με κελιά γραμμής που ανήκει ο βασιλιάς
        king_row: list = []
        for letter in self.files:
            king_row.append(letter + king_pos[1])

        # έλεγχος εάν το κομμάτι που θα κινηθεί βρίσκεται στην ίδια γραμμή με τον βασιλιά
        if src in king_row:
            # το κομμάτι που θα κινηθεί βρίσκεται στην ίδια γραμμή με τον βασιλιά
            # θέσεις του βασιλιά και κομματιού που θα κινηθεί (src) στη λίστα
            king_index = king_row.index(king_pos)
            src_index = king_row.index(src)

            # εάν η θέση src είναι μικρότερη, ξεκινάμε από την επόμενή της και προς τα "αριστερά"
            if src_index < king_index:
                # έλεγχος εάν τα ενδιάμεσα κελιά είναι κενά
                for i in range(king_index - 1, src_index, -1):
                    if self.squares[king_row[i]]:
                        # βρέθηκε κάποιο κομμάτι ενδιάμεσα, οπότε δεν είναι "καρφωμένο"
                        return True

                for i in range(src_index - 1, -1, -1):
                    # king_row[i] == θέση της λίστας
                    if self.squares[king_row[i]]:
                        # βρέθηκε το πρώτο κατειλημμένο κελί
                        for piece in self.pieces:
                            # εύρεση κομματιού που βρίσκεται σε αυτήν τη θέση
                            if piece.pos == king_row[i]:
                                if piece.name[1] == tag:
                                    # εάν βρεθεί κομμάτι ίδιου χρώματος, δεν απειλείται ο βασιλιάς
                                    # άρα δεν είναι καρφωμένο
                                    return True
                                else:
                                    if piece.name[0] != "q" and piece.name[0] != "r":
                                        # εάν βρεθεί αντίπαλο κομμάτι, αλλά δεν μπορεί να απειλήσει,
                                        # δεν είναι καρφωμένο
                                        return True

                                    if piece.name[0] == "q" or piece.name[0] == "r":
                                        if dest in king_row:
                                            # εάν η κίνηση που θα εκτελεστεί, διατηρεί το "κάρφωμα" στο κομμάτι
                                            # η κίνηση είναι νόμιμη
                                            return True
                                        # εάν είναι βασίλισσα ή πύργος στην ίδια γραμμή, το κομμάτι είναι "καρφωμένο"
                                        return False

            # εάν η θέση src είναι μεγαλύτερη, ξεκινάμε από την επόμενή της και προς τα "δεξιά"
            if src_index > king_index:
                for i in range(king_index + 1, src_index):
                    if self.squares[king_row[i]]:
                        # βρέθηκε κάποιο κομμάτι ενδιάμεσα, οπότε δεν είναι "καρφωμένο"
                        return True

                for i in range(src_index + 1, 8):
                    # king_row[i] == θέση της λίστας
                    if self.squares[king_row[i]]:
                        # βρέθηκε το πρώτο κατειλημμένο κελί
                        for piece in self.pieces:
                            # εύρεση κομματιού που βρίσκεται σε αυτήν τη θέση
                            if piece.pos == king_row[i]:
                                # εάν είναι κομμάτι ίδιου χρώματος, δεν είναι καρφωμένο
                                if piece.name[1] == tag:
                                    # εάν βρεθεί κομμάτι ίδιου χρώματος, δεν απειλείται ο βασιλιάς
                                    # άρα δεν είναι καρφωμένο
                                    return True
                                else:
                                    if piece.name[0] != "q" and piece.name[0] != "r":
                                        # εάν βρεθεί αντίπαλο κομμάτι, αλλά δεν μπορεί να απειλήσει,
                                        # δεν είναι καρφωμένο
                                        return True
                                    # εάν είναι βασίλισσα ή πύργος στην ίδια γραμμή, το κομμάτι είναι "καρφωμένο"
                                    if piece.name[0] == "q" or piece.name[0] == "r":
                                        if dest in king_row:
                                            # εάν η κίνηση που θα εκτελεστεί, διατηρεί το "κάρφωμα" στο κομμάτι
                                            # η κίνηση είναι νόμιμη
                                            return True
                                        # εάν είναι βασίλισσα ή πύργος στην ίδια γραμμή, το κομμάτι είναι "καρφωμένο"
                                        return False

            # το κομμάτι είναι στην ίδια ευθεία, αλλά δε βρέθηκε κάποιο αντίπαλο κομμάτι που να το "καρφώνει",
            # άρα μπορεί να μετακινηθεί
            return True

        # έλεγχος στήλης -----------------------------------------------------------------------------------------------
        # δημιουργία λίστας με κελιά στήλης που ανήκει ο βασιλιάς
        king_col: list = []
        for number in self.ranks:
            king_col.append(king_pos[0] + number)

        # έλεγχος εάν το κομμάτι που θα κινηθεί βρίσκεται στην ίδια στήλη με τον βασιλιά
        if src in king_col:
            # το κομμάτι που θα κινηθεί βρίσκεται στην ίδια στήλη με τον βασιλιά
            # θέσεις του βασιλιά και κομματιού που θα κινηθεί (src) στη λίστα
            king_index = king_col.index(king_pos)
            src_index = king_col.index(src)
            # εάν η θέση src είναι μικρότερη, ξεκινάμε από την επόμενή της και προς τα "κάτω"
            if src_index < king_index:
                for i in range(king_index - 1, src_index, -1):
                    if self.squares[king_col[i]]:
                        # βρέθηκε κάποιο κομμάτι ενδιάμεσα, οπότε δεν είναι "καρφωμένο"
                        return True

                for i in range(src_index - 1, -1, -1):
                    # king_row[i] == θέση της λίστας
                    if self.squares[king_col[i]]:
                        # βρέθηκε το πρώτο κατειλημμένο κελί
                        for piece in self.pieces:
                            # εύρεση κομματιού που βρίσκεται σε αυτήν τη θέση
                            if piece.pos == king_col[i]:
                                if piece.name[1] == tag:
                                    # εάν βρεθεί κομμάτι ίδιου χρώματος, δεν απειλείται ο βασιλιάς
                                    # άρα δεν είναι καρφωμένο
                                    return True
                                else:
                                    if piece.name[0] != "q" and piece.name[0] != "r":
                                        # εάν βρεθεί αντίπαλο κομμάτι, αλλά δεν μπορεί να απειλήσει,
                                        # δεν είναι καρφωμένο
                                        return True

                                    if piece.name[0] == "q" or piece.name[0] == "r":
                                        if dest in king_col:
                                            # εάν η κίνηση που θα εκτελεστεί, διατηρεί το "κάρφωμα" στο κομμάτι
                                            # η κίνηση είναι νόμιμη
                                            return True
                                        # εάν είναι βασίλισσα ή πύργος στην ίδια στήλη, το κομμάτι είναι "καρφωμένο"
                                        return False

            # εάν η θέση src είναι μεγαλύτερη, ξεκινάμε από την επόμενή της και προς τα "πάνω"
            if src_index > king_index:
                for i in range(king_index + 1, src_index):
                    if self.squares[king_col[i]]:
                        # βρέθηκε κάποιο κομμάτι ενδιάμεσα, οπότε δεν είναι "καρφωμένο"
                        return True

                for i in range(src_index + 1, 8):
                    # king_row[i] == θέση της λίστας
                    if self.squares[king_col[i]]:
                        # βρέθηκε το πρώτο κατειλημμένο κελί
                        for piece in self.pieces:
                            # εύρεση κομματιού που βρίσκεται σε αυτήν τη θέση
                            if piece.pos == king_col[i]:
                                if piece.name[1] == tag:
                                    # εάν βρεθεί κομμάτι ίδιου χρώματος, δεν απειλείται ο βασιλιάς
                                    # άρα δεν είναι καρφωμένο
                                    return True
                                else:
                                    if piece.name[0] != "q" and piece.name[0] != "r":
                                        # εάν βρεθεί αντίπαλο κομμάτι, αλλά δεν μπορεί να απειλήσει,
                                        # δεν είναι καρφωμένο
                                        return True

                                    if piece.name[0] == "q" or piece.name[0] == "r":
                                        if dest in king_col:
                                            # εάν η κίνηση που θα εκτελεστεί, διατηρεί το "κάρφωμα" στο κομμάτι
                                            # η κίνηση είναι νόμιμη
                                            return True
                                        # εάν είναι βασίλισσα ή πύργος στην ίδια γραμμή, το κομμάτι είναι "καρφωμένο"
                                        return False

            # το κομμάτι είναι στην ίδια στήλη, αλλά δε βρέθηκε κάποιο αντίπαλο κομμάτι που να το "καρφώνει",
            # άρα μπορεί να μετακινηθεί
            return True

        # έλεγχος διαγωνίων --------------------------------------------------------------------------------------------
        # δημιουργία λίστας με λίστες με τα κελιά διαγωνίων που ανήκει ο βασιλιάς
        king_diags: list = []
        for diag in self.diags:
            # γίνεται προσθήκη των διαγωνίων που ανήκει ο βασιλιάς, εκτός από τις μικρές (με δύο κελιά)
            # επίσης άμα ο βασιλιάς βρίσκεται σε κάποια γωνία, ανήκει μόνο σε μία διαγώνιο
            if king_pos in diag and len(diag) > 2:
                king_diags.append(diag)

        # διαπέραση διαγωνίων (μπορεί να είναι μία ή δύο)
        for diag in king_diags:
            # έλεγχος εάν το κομμάτι που θα κινηθεί βρίσκεται στην ίδια διαγώνιο με τον βασιλιά
            if src in diag:
                # το κομμάτι που θα κινηθεί βρίσκεται στην ίδια διαγώνιο με τον βασιλιά
                # θέσεις του βασιλιά και κομματιού που θα κινηθεί (src) στη λίστα
                king_index = diag.index(king_pos)
                src_index = diag.index(src)

                # εάν η θέση src είναι μικρότερη, ξεκινάμε από την επόμενή της και προς την αντίθετη μεριά του βασιλιά
                if src_index < king_index:
                    for i in range(king_index - 1, src_index, -1):
                        if self.squares[diag[i]]:
                            # βρέθηκε κάποιο κομμάτι ενδιάμεσα, οπότε δεν είναι "καρφωμένο"
                            return True

                    for i in range(src_index - 1, -1, -1):
                        # king_row[i] == θέση της λίστας
                        if self.squares[diag[i]]:
                            # βρέθηκε το πρώτο κατειλημμένο κελί
                            for piece in self.pieces:
                                # εύρεση κομματιού που βρίσκεται σε αυτήν τη θέση
                                if piece.pos == diag[i]:
                                    if piece.name[1] == tag:
                                        # εάν βρεθεί κομμάτι ίδιου χρώματος, δεν απειλείται ο βασιλιάς
                                        # άρα δεν είναι καρφωμένο
                                        return True
                                    else:
                                        if piece.name[0] != "q" and piece.name[0] != "b":
                                            # εάν βρεθεί αντίπαλο κομμάτι, αλλά δεν μπορεί να απειλήσει,
                                            # δεν είναι καρφωμένο
                                            return True
                                        # εάν είναι βασίλισσα ή αξ/κός στην ίδια διαγώνιο, το κομμάτι είναι "καρφωμένο"
                                        if piece.name[0] == "q" or piece.name[0] == "b":
                                            if dest in diag:
                                                # εάν η κίνηση που θα εκτελεστεί, διατηρεί το "κάρφωμα" στο κομμάτι
                                                # η κίνηση είναι νόμιμη
                                                return True
                                            # εάν είναι βασίλισσα ή αξιωματικός στην ίδια διαγώνιο,
                                            # το κομμάτι είναι "καρφωμένο"
                                            return False

                # εάν η θέση src είναι μεγαλύτερη, ξεκινάμε από την επόμενή της και προς την αντίθετη μεριά του βασιλιά
                if src_index > king_index:
                    for i in range(king_index + 1, src_index):
                        if self.squares[diag[i]]:
                            # βρέθηκε κάποιο κομμάτι ενδιάμεσα, οπότε δεν είναι "καρφωμένο"
                            return True

                    for i in range(src_index + 1, len(diag)):
                        # king_row[i] == θέση της λίστας
                        if self.squares[diag[i]]:
                            # βρέθηκε το πρώτο κατειλημμένο κελί
                            for piece in self.pieces:
                                # εύρεση κομματιού που βρίσκεται σε αυτήν τη θέση
                                if piece.pos == diag[i]:
                                    if piece.name[1] == tag:
                                        # εάν βρεθεί κομμάτι ίδιου χρώματος, δεν απειλείται ο βασιλιάς
                                        # άρα δεν είναι καρφωμένο
                                        return True
                                    else:
                                        if piece.name[0] != "q" and piece.name[0] != "b":
                                            # εάν βρεθεί αντίπαλο κομμάτι, αλλά δεν μπορεί να απειλήσει,
                                            # δεν είναι καρφωμένο
                                            return True

                                        if piece.name[0] == "q" or piece.name[0] == "b":
                                            if dest in diag:
                                                # εάν η κίνηση που θα εκτελεστεί, διατηρεί το "κάρφωμα" στο κομμάτι
                                                # η κίνηση είναι νόμιμη
                                                return True
                                            # εάν είναι βασίλισσα ή αξιωματικός στην ίδια διαγώνιο,
                                            # το κομμάτι είναι "καρφωμένο"
                                            return False

                # το κομμάτι είναι στην ίδια διαγώνιο, αλλά δε βρέθηκε κάποιο αντίπαλο κομμάτι που να το "καρφώνει",
                # άρα μπορεί να μετακινηθεί
                return True

        # τελείωσαν όλοι οι βασικοί έλεγχοι και δε βρέθηκε αντίπαλο κομμάτι που να "καρφώνει" το κομμάτι,
        # άρα μπορεί να κινηθεί νόμιμα
        return True
