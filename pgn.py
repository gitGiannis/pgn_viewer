# -------------------------------------------------------------------------------------------------------------------- #
# pgn.py: includes class FilePGN                                                                                       #
# -------------------------------------------------------------------------------------------------------------------- #
from my_exceptions import PossibleCorruptFile


class FilePGN:
    """
    Using the filepath provided as parameter, splits the different games in a pgn file, processes the information it
    stores and organizes them into structures

    ...

    Attributes:
    ----------
        file_path (str):
            address of a pgn file

        game_data (list):
            list of information read from the pgn file (prior to being processed)

        index_of_games (list[int]):
            list of integers posing as game indexes in game_data list

    Methods:
    --------
        get_info(self, game_no: int) -> dict:
            returns dict with the information of a game

        __split_files(self) -> list[str]:
            returns list with the information and moves of the games stored inside the pgn file

        __get_index_of_games(self) -> list:
            returns list with indexes of games in game_data list

        @staticmethod
        __get_moves_as_list(game_moves: str) -> list[str]:
            returns list with the processed game moves

        @staticmethod
        __get_total_rounds(processed_game_moves: list) -> str:
            returns string with the number of rounds of the game
    """

    def __init__(self, file_path: str):
        """
        Initialization of class object

        ...

        Parameters:
        -----------
            file_path (str):
                address of a pgn file
        """
        self.file_path = file_path

        # __split_files() gets called for this pgn file
        # game_data list now contains
        # a) in positions n the information of a game and
        # b) in positions n+1 the moves of each game
        # n is even non-negative number (0, 2, 4 etc.)
        self.game_data: list = self.__split_files()

        # list with indexes of games
        self.index_of_games: list = self.__get_index_of_games()

    def get_info(self, game_no: int) -> dict[str, str | list]:
        """
        Returns dictionary with information of a game from the pgn file
        The game is selected by the index 'game_no'
        Dictionary key-words: Event, Site, Date, White, Black, Result, Rounds, moves

        ...

        Parameters:
        -----------
            game_no (int):
                even non-negative number (0, 2, 4 etc.) from index_of_games attribute

        Returns:
        --------
            game_dict (dict):
                dictionary with game information
        """
        # list containing key-words
        info_list = ["Event ", "Site ", "Date ", "Round ", "White ", "Black ", "Result "]
        # initialization of dictionary to be returned
        game_dict = {}

        # storing the game info for easier access
        game_info = self.game_data[game_no].split("\n")

        # extraction of game info
        for key_word in info_list:
            for string in game_info:
                # e.g. key_word: Event , string: [Event "Sparkassen Chess Meeting"]
                if string[1: 1 + len(key_word)] == key_word:
                    # index of staring and ending of the desired information
                    start = string.find("\"") + 1
                    end = string.rfind("\"")
                    # addition to the dictionary
                    game_dict[key_word.strip()] = string[start:end]
                    break
            # no information based on the key-word could be retrieved
            else:
                game_dict[key_word.strip()] = "[no info]"

        try:
            # string with the game moves
            game_moves = self.game_data[game_no + 1]
        except IndexError:
            game_moves = ""

        # moves get added to the dict
        game_dict["moves"] = self.__get_moves_as_list(game_moves)

        # total rounds get added to the dict
        game_dict["RoundsPlayed"] = self.__get_total_rounds(game_dict["moves"])

        # dictionary gets returned
        return game_dict

    def __split_files(self) -> list[str]:
        """
        returns list with the information and moves of the games stored inside the pgn file
        # returned list contains
        # a) in positions n the information of a game and
        # b) in positions n+1 the moves of each game
        # n is even non-negative number (0, 2, 4 etc.)

        ...

        Returns:
        --------
            game_data_list (list[str]):
                list with information extracted

        Raises:
        -------
            PossibleCorruptFile (Exception):
                if the length of the list to return is not even number
        """

        # pgn file gets opened
        with open(self.file_path, "r") as pgn:
            # initialization of list to store information
            game_data_list = []
            # initialization of temporary string variable to store information
            game_data = ''
            # loop through the file contents by line
            for line in pgn:
                # concatenation of line to the game_data string
                game_data += line
                # every time a line with the "\n" is read, the reading of either the game information or game moves has
                # been finished
                if line == "\n":
                    # in case more than one empty lines exist between them, they get ignored
                    if game_data == "\n":
                        game_data = ''
                        continue
                    # all the information stored till now is added to the list
                    game_data_list.append(game_data)
                    # the temporary variable gets reset
                    game_data = ''

            # if the file doesn't end on an empty line, the final information is added to the list
            if game_data:
                game_data_list.append(game_data)

            pgn.close()

            if len(game_data_list) % 2 != 0:
                # some error occurred while reading the file
                raise PossibleCorruptFile('Length of list should be even number, not ' + str(len(game_data_list)))

            return game_data_list

    def __get_index_of_games(self) -> list:
        """
        Returns the index of games for the game_data list

        ...

        Returns:
        --------
            index_of_games (list):
                list of indexes
        """
        index_of_games = []

        # appending the indexes of the games
        for num in range(0, len(self.game_data), 2):
            index_of_games.append(num)

        return index_of_games

    @staticmethod
    def __get_moves_as_list(game_moves: str) -> list[str]:
        """
        Extracts a list with the processed moves from the game_moves string it takes as parameter and returns it
        The list created includes all the moves as strings without any round indexes, comments etc.

        ...

        Parameters:
        -----------
            game_moves (str):
                string with moves of current game before being processed

        Returns:
        --------
            (list):
                list with moves as strings (without the last element which is the result)
        """
        if not game_moves:
            return []
        # searching for comment within the moves string (they will be removed)
        while True:
            # searching for opening bracket of the comment
            comment_start = game_moves.find("{")
            # if no comment is found or all comments were found, the loop is stopped
            if comment_start == -1:
                break
            # the loop was not stopped so an opening comment bracket was found
            # searching for closing comment bracket
            comment_end = game_moves.find("}") + 1
            # comment is removed from the moves string
            game_moves = game_moves[:comment_start] + game_moves[comment_end:]
            # the loop continues to find the next comment

        # the moves string is split based on spaces and '\n' characters
        moves_list = game_moves.split()
        # loop on the moves list created
        for item in moves_list:
            # if the dot character is within the move, it is a round index and must be removed
            if "." in item:
                # check if the current element end with the dot character
                if item[-1] == ".":
                    # if the dot is the last character, then it is a round index and gets removed
                    # e.g. "1."
                    moves_list.remove(item)
                else:
                    # the current element includes the dot character but not at the last position (as before),
                    # it means there is a round index next to a move (e.g. 1.e4 instead of 1. e4)
                    # storing the position of the current element inside the list so that the new element is inserted
                    # at the right spot
                    index = moves_list.index(item)

                    # the string is split based on the dot character (e.g. 1.e4 is now ["1", "e4"])
                    split_move = item.split(".")
                    # the right side of the list is kept (split_move[1] == "e4") and is inserted at the right spot, so
                    # that the order is not spoiled
                    # the old string "1.e4" is replaced by "e4")
                    moves_list[index] = split_move[1]

        # no moves performed (only the score is shown)
        if len(moves_list) == 1:
            return [" "]
        # the list is returned without the last element (the result of the game)
        return moves_list[:len(moves_list) - 1]

    @staticmethod
    def __get_total_rounds(processed_game_moves: list) -> str:
        """
        Takes as argument the processed moves of the game and returns a string with the number of rounds played

        ...

        Parameters:
        -----------
            processed_game_moves (list):
                processed game moves of the current game

        Returns:
        --------
            (str):
                string with the number of rounds played
        """

        # length of the game moves list
        length = len(processed_game_moves)
        # returns string with the number of rounds (number of moves divided by two)
        return str(length // 2 if length % 2 == 0 else (length // 2) + 1)
