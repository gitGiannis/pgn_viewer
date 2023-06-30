# -------------------------------------------------------------------------------------------------------------------- #
# captured_pieces.py: includes class CapturedPieces                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Frame, Label, PhotoImage


class CapturedPieces:
    """
    Initializes and processes the top and bottom frames for the GUI window
    These frames contain the difference in pieces between the two players

    ...

    Attributes:
    -----------
        *_array (list):
            array for each white/black captured pieces

        *_index (int):
            index for arrays

        captured_*_piece_value (int):
            value of captured pieces for each colour

        *_pawns_frame (Frame):
            frames for each array

        call_signs (tuple):
            tuple of prioritizes call signs

        captured_list (list[dict]):
            list with dictionaries of captured differences for each round

        images (dict):
            dictionary of images

        round (int):
            current round index

    Methods:
    --------
        forward_captured_piece_frames(self) -> None:
            continues to next move

        backwards_captured_piece_frames(self) -> None:
            goes one move back

        restart_captured_piece_frames(self) -> None:
            restarts the frames to first round

        reset(self) -> None:
            resets the two lists before each next/previous move

        update_item(self, call_sign: str, diff: int) -> None:
            updates the 'call_sign' piece on the boards based on their difference

        arrays_init(self) -> None:
            processes and fills the arrays with labels

        @staticmethod
        image_dictionary_init(master) -> dict:
            returns the images dictionary
    """

    def __init__(self, master, captured_list: dict):
        """
        Initializes the class attributes

        ...

        Parameters:
        -----------
            master (Tk):
                window containing the two frames created here

            captured_list (list):
                list with dictionaries with piece difference for each round
        """
        # initialization of images dictionary
        self.images = self.image_dictionary_init(master=master)
        # initialization of dictionaries list with the information about captured pieces
        self.captured_list = captured_list

        # initialization of variables ----------------------------------------------------------------------------------
        # round counter
        self.round = 0

        # call signs list for each piece (placed by priority)
        self.call_signs = ('q', 'r', 'b', 'n', 'p')

        # value of pieces for each player
        self.captured_white_piece_value: int = 0
        self.captured_black_piece_value: int = 0

        # indexes for lists
        self.w_index: int = 1
        self.b_index: int = 1

        # frame initialization -----------------------------------------------------------------------------------------
        self.white_pawns_frame = Frame(master=master, bg="orange", bd=3, relief="raised")
        self.black_pawns_frame = Frame(master=master, bg="orange", bd=3, relief="raised")

        # array initialization and placement inside frames -------------------------------------------------------------
        self.white_array = []
        self.black_array = []
        self.arrays_init()

    def forward_captured_piece_frames(self) -> None:
        """
        Continues to next move
        """
        self.round += 1
        self.reset()
        for call_sign in self.call_signs:
            # pieces get updated by priority
            self.update_item(call_sign, self.captured_list[self.round][call_sign])

        adv = self.captured_list[self.round]['advantage']
        # values label update
        if adv > 0:
            self.white_array[0].config(text=f"-{adv:<3}")
            self.black_array[0].config(text=f"+{adv:<3}")
            return
        if adv < 0:
            self.white_array[0].config(text=f"+{adv * (-1):<3}")
            self.black_array[0].config(text=f"{adv:<3}")
            return

    def backwards_captured_piece_frames(self) -> None:
        """
        Goes one move back
        """
        self.round -= 2
        self.forward_captured_piece_frames()

    def restart_captured_piece_frames(self) -> None:
        """
        Restarts the frames to first round
        """
        self.round = -1
        self.forward_captured_piece_frames()

    def reset(self) -> None:
        """
        Resets the two lists before each next/previous move
        """
        # indexes reset
        self.w_index = 1
        self.b_index = 1
        # values reset
        self.captured_white_piece_value = 0
        self.captured_black_piece_value = 0
        self.white_array[0].config(text="")
        self.black_array[0].config(text="")
        # lists reset
        for i in range(1, 16):
            self.white_array[i].config(image=self.images["blank"])
            self.black_array[i].config(image=self.images["blank"])

    def update_item(self, call_sign: str, diff: int) -> None:
        """
        Updates the 'call_sign' piece on the boards based on their difference
        (call signs are initialized in the self.call_signs tuple)

        ...

        Parameters:
        ----------
            call_sign (str):
                the first letter of each piece ('q', 'b' etc.)

            diff (int):
                the difference in pieces (positive number if more captured white pieces, negative for black)
        """
        # white piece got captured
        if diff > 0:
            # adding the current list index
            diff += self.w_index
            # adding the right amount of pieces captured
            for i in range(self.w_index, diff):
                self.white_array[i].config(image=self.images[call_sign])
            # index gets updated for following pieces
            self.w_index = diff
            return

        # black piece got captured
        if diff < 0:
            # multiplied by (-1) to become a positive entity
            diff *= -1
            # adding the current list index
            diff += self.b_index
            # adding the right amount of pieces captured
            for i in range(self.b_index, diff):
                self.black_array[i].config(image=self.images[call_sign])
            # index gets updated for following pieces
            self.b_index = diff
            return

    def arrays_init(self) -> None:
        """
        Method that processes and fills the arrays with labels
        """
        # appending one label for showing difference in piece (arithmetic value)
        self.white_array.append(Label(master=self.white_pawns_frame, bg="orange", font="consolas"))
        self.black_array.append(Label(master=self.black_pawns_frame, bg="orange", font="consolas"))
        self.white_array[0].grid(row=0, column=0)
        self.black_array[0].grid(row=0, column=0)
        for _ in range(1, 16):
            self.white_array.append(Label(master=self.white_pawns_frame, bg="orange", image=self.images["blank"]))
            self.black_array.append(Label(master=self.black_pawns_frame, bg="orange", image=self.images["blank"]))
            self.white_array[_].grid(row=0, column=_)
            self.black_array[_].grid(row=0, column=_)

    @staticmethod
    def image_dictionary_init(master) -> dict:
        """
        Static method that returns the images dictionary

        ...

        Parameters:
        -----------
            master (Tk):
                master of the PhotoImages

        Returns:
        --------
            (dict):
                dictionary with the PhotoImages of pieces
        """
        return {"p": PhotoImage(master=master, file="icons\\basic\\pawn.png"),
                "n": PhotoImage(master=master, file="icons\\basic\\knight.png"),
                "b": PhotoImage(master=master, file="icons\\basic\\bishop.png"),
                "r": PhotoImage(master=master, file="icons\\basic\\rook.png"),
                "q": PhotoImage(master=master, file="icons\\basic\\queen.png"),
                "blank": PhotoImage(master=master, file="icons\\basic\\blank.png")}
