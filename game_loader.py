# -------------------------------------------------------------------------------------------------------------------- #
# game_loader.py: includes class GameLoader                                                                            #
# -------------------------------------------------------------------------------------------------------------------- #
from move_checking import PieceMoveChecker
from my_exceptions import PositionReached, NoMovesFound, PossibleCorruptFile, FriendlyCapture


class GameLoader(PieceMoveChecker):
    """
    Inherits from parent class PieceMoveChecker
    "Runs" the selected game from start to finish and stores "screenshots" of the chess board for each round
    The screenshots for each round consists of list of dictionaries with the name of each piece,
    as well as it's row and column index
    Due to the fact that going backwards and finding the previous move on the board is extremely difficult or even
    impossible, this class poses a fundamental role in the app's function
    If any mistakes in the game moves are found, an exception is raised

    ...

    Attributes:
    -----------
        round (int):
            counter of current half move (ply)

        info_dictionaries_pre_round (list):
            list that stores the 'screenshots' of each round

        check_per_round (list):
            list that stores whether the current half move has a check or not

        captures_per_round (list):
            list that stores whether the current half move has a captured or not

        captured_piece_names (dict):
            dictionary that stores the round of a capture and the name of the captured piece

    Methods:
    --------
        next_move(self, force: bool=False):
            continues to next move

        previous_move(self, force: bool=False):
            goes back to previous move

        restart_game(self):
            restarts the game

        __update_captured_piece_dict(self, piece_name: str):
            updates dictionary with captured pieces

    Raises:
    -------
        NoMovesFound (Exception):
            the current game has no moves

        PossibleCorruptFile (Exception):
            game could not be processed

        FriendlyCapture (Exception):
            a piece captures a friendly piece (not legal)
    """
    def __init__(self, list_of_moves: list):
        """
        Parameters:
        -----------
            list_of_moves (list):
                λίστα με τις επεξεργασμένες κινήσεις του αγώνα

        Raises:
        -------
            NoMovesFound (Exception):
                the current game has no moves

            PossibleCorruptFile (Exception):
                game could not be processed

            FriendlyCapture (Exception):
                a piece captures a friendly piece (not legal)
        """
        # initialization of parent class PieceMoveChecker
        super().__init__(list_of_moves)

        # initialization of structures for storing information ---------------------------------------------------------
        # list that stores the dictionaries for each round
        self.info_dictionaries_per_round = []

        # dictionary that stores as:
        # key: round a captured happens
        # value: name of the captured piece
        self.captured_piece_names = {}

        # list of booleans for sound playing
        # if False a move sound is played, else a capture sound (first round initialized as False)
        self.captures_per_round = [False]

        # list of booleans king mates
        # if None no mate is active, else "w"/"b" to show which king has mate (first round initialized as None)
        self.check_per_round = [None]

        # current half move counter
        self.round = 0

        # 'screenshot' storing -----------------------------------------------------------------------------------------
        # temporary list variable
        current_round = []
        # information storing for initial position
        for piece in self.pieces:
            current_round.append({
                "name": piece.name[:2],
                "row": piece.row,
                "col": piece.col
            })
        self.info_dictionaries_per_round.append(current_round)

        if self.moves_length == 0:
            raise NoMovesFound

        # loop through each round to create the screenshot of the chess board
        for i in range(self.moves_length):
            # temporary list variable
            current_round = []
            # next move is loaded and the captured piece name is stored temporarily
            captured_piece_name = self.load_next_move()

            # load_next_move() method returned None
            if captured_piece_name is None:
                raise PossibleCorruptFile(f"{self.round_cnt//2 + 1}. {self.moves[self.round_cnt]}")

            # a friendly capture has been made
            if self.friendly_capture:
                raise FriendlyCapture(f"{self.round_cnt//2 + 1}. {self.moves[self.round_cnt]}")

            # captured_piece_names update
            self.__update_captured_piece_dict(captured_piece_name)

            # information storing for current round
            for line in self.board:
                for sqr in line:
                    current_round.append({
                        "name": sqr.name[:2],
                        "row": sqr.row,
                        "col": sqr.col
                        })
            self.info_dictionaries_per_round.append(current_round)

            # captures_per_round list update
            self.captures_per_round.append(self.capture)
            # check_per_round list update
            self.check_per_round.append(self.check)

    def next_move(self, force: bool = False) -> None:
        """
        Continues to the next move
        If in 2nd to final move position, raises PositionReached unless force is set to True

        ...

        Parameters:
        -----------
            force (bool) default=False:
                set to True to access final round

        Raises:
        -------
            PositionReached (Exception):
                if 2nd to final move is reached
        """
        if self.round < self.moves_length - 1:
            self.round += 1
            return
        if force:
            self.round += 1
            return
        raise PositionReached

    def previous_move(self, force: bool = False) -> None:
        """
        Goes back to the previous move
        if in 2nd move, raises PositionReached unless force is set to True

        ...

        Parameters:
        -----------
            force (bool) default=False:
                set to True to access final round

        Raises:
        -------
            PositionReached (Exception):
                if 2nd to final move is reached
        """
        if self.round > 1:
            self.round -= 1
            return
        if force:
            self.round -= 1
            return
        raise PositionReached

    def restart_game(self) -> None:
        """
        Restarts the game
        """
        self.round = 0

    def __update_captured_piece_dict(self, piece_name: str) -> None:
        """
        Updates the dictionary that stores the captured piece's names per round
        This method stores the round (int) in with the piece was captured as key and the piece's name as value
        This only happened if the name is not "   ", which implies an empty square (decoy)

        ...

        Parameters:
        -----------
            piece_name (str):
                name of the captured piece
        """
        if piece_name != "   ":
            self.captured_piece_names[self.round_cnt + 1] = piece_name[:2]
