# -------------------------------------------------------------------------------------------------------------------- #
# captured_pieces.py: includes class CapturedPieces                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Frame, Label, PhotoImage


class CapturedPieces:
    """


    ...

    Attributes:
    -----------


    Methods:
    --------

    """

    def __init__(self, master, captured_list: dict):
        """
        Initializes the frame

        ...

        Parameters:
        -----------

        """
        self.master = master
        # initialization of images dictionary
        self.images = self.image_dictionary_init()
        # initialization of dictionary with the information about captured pieces
        self.captured_list = captured_list
        # initialization of round counter
        self.round = 0

        self.white_value: int = 39
        self.black_value: int = 39

        self.white_index: int = 0
        self.black_index: int = 0

        self.call_signs = ('q', 'r', 'b', 'n', 'p')

        self.white_pawns_frame = Frame(master=master, bg="orange", bd=3, relief="raised")
        self.black_pawns_frame = Frame(master=master, bg="orange", bd=3, relief="raised")
        self.white_array = [Label(master=self.white_pawns_frame, bg="orange",
                                  image=self.images["blank"]) for _ in range(15)]

        self.black_array = [Label(master=self.black_pawns_frame, bg="orange",
                                  image=self.images["blank"]) for _ in range(15)]
        self.__pack()

    def forward_captured_piece_frames(self) -> None:
        self.round += 1
        self.reset()
        for call_sign in self.call_signs:
            self.update_item(call_sign, self.captured_list[self.round][call_sign])
        """for call_sign, diff in self.captured_list[self.round].items():
            self.update_item(call_sign, diff)"""

    def backwards_captured_piece_frames(self):
        self.round -= 2
        self.forward_captured_piece_frames()

    def restart_captured_piece_frames(self):
        self.round = -1
        self.forward_captured_piece_frames()

    def reset(self):
        self.white_index = 0
        self.black_index = 0
        for i in range(15):
            self.white_array[i].config(image=self.images["blank"])
            self.black_array[i].config(image=self.images["blank"])

    def update_item(self, call_sign: str, diff: int) -> None:
        """

        ...

        Returns:
        --------
        """
        # white player captured a piece
        if diff > 0:
            diff += self.white_index
            for i in range(self.white_index, diff):
                self.white_array[i].config(image=self.images[call_sign])
            self.white_index = diff

        # black player captured a piece
        elif diff < 0:
            diff *= -1
            diff += self.black_index
            for i in range(self.black_index, diff):
                self.black_array[i].config(image=self.images[call_sign])
            self.black_index = diff

    def __pack(self):
        for _ in range(15):
            self.white_array[_].grid(row=0, column=_)
            self.black_array[_].grid(row=0, column=_)

    def image_dictionary_init(self):
        return {"p": PhotoImage(master=self.master, file="icons\\piece_icons\\basic\\pawn.png"),
                "n": PhotoImage(master=self.master, file="icons\\piece_icons\\basic\\knight.png"),
                "b": PhotoImage(master=self.master, file="icons\\piece_icons\\basic\\bishop.png"),
                "r": PhotoImage(master=self.master, file="icons\\piece_icons\\basic\\rook.png"),
                "q": PhotoImage(master=self.master, file="icons\\piece_icons\\basic\\queen.png"),
                "blank": PhotoImage(master=self.master, file="icons\\piece_icons\\basic\\blank.png")}
