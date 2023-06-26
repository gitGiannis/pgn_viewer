# -------------------------------------------------------------------------------------------------------------------- #
# captured_piece_frame.py: includes class CapturedPieceFrame                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Frame, Label


class CapturedPieceFrame(Frame):
    """
    Inherits from parent class Frame
    Creates 5X6 grid to show the pieces captured throughout the game

    ...

    Attributes:
    -----------
        blank (PhotoImage):
            blank photo

        photo_dict (dict):
            dictionary with photos

        round (int):
            round counter

        captured_piece_board (list):
            2D list to show the captured pieces

        row_for_white (int):
            row index for white

        col_for_white (int):
            column index for white

        row_for_black (int):
            row index for black

        col_for_black (int):
            column index for black

        dict (dict):
            dictionary of captured pieces

    Methods:
    --------
        __update_frame(self) -> str:
            updates the captured piece frame and returns string with the tag of the captured piece

        next_round(self):
            updates the board of a piece gets captured

        previous_round(self):
            updates the board by removing pieces

        reset(self):
            resets the board
    """
    def __init__(self, master, captured_piece_dictionary: dict, blank_image,
                 rw_image, rb_image, nw_image, nb_image, bw_image, bb_image, qw_image, qb_image, pw_image, pb_image):
        """
        Initializes the frame

        ...

        Parameters:
        ---------
            master (GUI):
                master of the frame

            captured_piece_dictionary (dict):
                dictionary with information about captured pieces

            *_image (PhotoImage):
                piece images
        """
        # initialization of parent class (Frame)
        super().__init__(master=master)
        self.config(bg="light grey")
        # initialization of dictionary with the information about captured pieces
        self.dict = captured_piece_dictionary
        # initialization of round counter
        self.round = 0
        # initialization of images
        self.blank = blank_image
        self.photo_dict = {"rw": rw_image, "rb": rb_image,
                           "nw": nw_image, "nb": nb_image,
                           "bw": bw_image, "bb": bb_image,
                           "qw": qw_image, "qb": qb_image,
                           "pw": pw_image, "pb": pb_image}

        # initialization of 2D board to show the captured pieces
        self.captured_piece_board = []
        for row in range(5):
            temp = []
            for col in range(6):
                # initialized with blank image
                temp.append(Label(self, bg="light grey", image=blank_image))
            self.captured_piece_board.append(temp)

        for row in range(5):
            for col in range(6):
                self.captured_piece_board[row][col].grid(row=row, column=col)

        # initialization of column and row counters
        self.row_for_white = 0
        self.col_for_white = 0
        self.row_for_black = 0
        self.col_for_black = 3

    def __update_frame(self) -> str:
        """
        Updates the captured piece frame and returns string with the tag of the captured piece

        ...

        Returns:
        --------
            (str):
                "w"/"b" based on captured piece, "" if no piece is captured
        """
        try:
            # check if current round exists in dictionary
            captured_piece_name = self.dict[self.round]
        except KeyError:
            # no key found
            return ""

        if captured_piece_name[1] == "w":
            self.captured_piece_board[self.row_for_white][self.col_for_white].config(
                                                                    image=self.photo_dict[captured_piece_name],
                                                                    state="disabled")
            return "w"

        if captured_piece_name[1] == "b":
            self.captured_piece_board[self.row_for_black][self.col_for_black].config(
                                                                    image=self.photo_dict[captured_piece_name],
                                                                    state="disabled")
            return "b"

    def next_round(self):
        """
        Updates the board of a piece gets captured
        """
        self.round += 1
        # temporary storing of the tag
        current_piece_tag = self.__update_frame()
        # formatted placing of the images
        if current_piece_tag == "w":
            self.row_for_white += 1
            if self.row_for_white == 5:
                self.row_for_white = 0
                self.col_for_white += 1
        elif current_piece_tag == "b":
            self.row_for_black += 1
            if self.row_for_black == 5:
                self.row_for_black = 0
                self.col_for_black += 1

    def previous_round(self):
        """
        Updates the board by removing pieces
        """
        # previous round index is stored temporarily
        cur_round = self.round - 1
        # board gets reset
        self.reset()
        # board gets updated till previous round is reached
        for rnd in range(cur_round):
            self.next_round()

    def reset(self):
        """
        Resets the board
        """
        self.round = 0
        self.row_for_white = 0
        self.col_for_white = 0
        self.row_for_black = 0
        self.col_for_black = 3
        for row in range(5):
            for col in range(6):
                self.captured_piece_board[row][col].config(image=self.blank, bg="light grey")
