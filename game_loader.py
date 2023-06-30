# -------------------------------------------------------------------------------------------------------------------- #
# game_loader.py: includes class GameLoader                                                                            #
# -------------------------------------------------------------------------------------------------------------------- #
from move_checking import PieceMoveChecker
from my_exceptions import PositionReached, NoMovesFound, FriendlyCapture, FalseGame


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

        info_dictionaries_per_round (list):
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

        FalseGame (Exception):
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

        # list with the captured pieces difference per round
        self.captured_diff_per_round = [{"p": 0, "n": 0, "b": 0, "r": 0, "q": 0, "advantage": 0}]
        # value of each piece
        values = {'qw': 9, 'qb': -9, 'rw': 5, 'rb': -5, 'bw': 3, 'bb': -3, 'nw': 3, 'nb': -3, 'pw': 1, 'pb': -1}
        # variable for temporary storing of the current advantage
        adv: int = 0

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
            current_round.append({"name": piece.name[:2], "row": piece.row, "col": piece.col})
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
                raise FalseGame(f"{self.round_cnt//2 + 1}. {self.moves[self.round_cnt]}")

            # a friendly capture has been made
            if self.friendly_capture:
                raise FriendlyCapture(f"{self.round_cnt//2 + 1}. {self.moves[self.round_cnt]}")

            # information storing for current round
            for piece in self.pieces:
                current_round.append({"name": piece.name[:2], "row": piece.row, "col": piece.col})
                try:
                    # current board advantage gets stored
                    adv += values[piece.name[:2]]
                except KeyError:
                    pass
            self.info_dictionaries_per_round.append(current_round)

            # captured_piece_names update
            self.__update_captured_piece_dict(captured_piece_name, adv)
            adv = 0

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

    def __update_captured_piece_dict(self, piece_name: str, advantage: int) -> None:
        """
        Updates the dictionary that stores the captured piece difference for each piece type per round
        Also updates the overall advantage of the current half move

        ...

        Parameters:
        -----------
            piece_name (str):
                name of the captured piece

            advantage (int):
                numeric difference in piece value
        """
        self.captured_diff_per_round.append(self.captured_diff_per_round[-1].copy())
        self.captured_diff_per_round[-1]['advantage'] = advantage
        if piece_name[1] == "w":
            self.captured_diff_per_round[-1][piece_name[0]] += 1
            return

        if piece_name[1] == "b":
            self.captured_diff_per_round[-1][piece_name[0]] -= 1
            return
