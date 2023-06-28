# -------------------------------------------------------------------------------------------------------------------- #
# info_frame_for_gui.py: includes class InfoFrame                                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Scrollbar, Text, Frame


class InfoFrame(Frame):
    """
    Inherits from parent class Frame and places a Text object inside with the game information
    The information is obtained from the dictionary taken as parameter
    """
    def __init__(self, master, info_dictionary: dict):
        """
        Initializes the frame

        ...

        Parameters:
        -----------
            master (GUI):
                master of the frame

            info_dictionary (dict):
                dictionary with game information
        """
        # initialization of parent class (Frame)
        super().__init__(master=master)
        self.config(bg="light grey")

        # storing the moves in variable 'moves' for easier access
        moves = info_dictionary['moves']
        # initialization of counter
        cnt = 1
        # initialization of list to store moves and round indexes
        moves_numbered = []
        # loop through the moves list items
        for i in range(len(moves)):
            if cnt % 1 == 0:
                # round index added every two moves
                moves_numbered.append(str(int(cnt)) + ".")
            # move gets added to list
            moves_numbered.append(moves[i])
            cnt += 0.5

        # initialization of string to show
        moves_str = ""
        number_of_items_per_line = 3
        start = 0
        end = number_of_items_per_line
        # non-ending loop to access all items in list
        while True:
            try:
                for i in range(start, end):
                    # adding round index and moves in each line
                    moves_str += moves_numbered[i]
                    moves_str += "  "
                moves_str += "\n"
                start += number_of_items_per_line
                end += number_of_items_per_line
            except IndexError:
                break

        # string with game info to show
        text_to_show = f"Event: {info_dictionary['Event']}\n" \
                       f"Site: {info_dictionary['Site']}\n" \
                       f"Date: {info_dictionary['Date']}\n" \
                       f"Round: {info_dictionary['Round']}\n" \
                       f"White: {info_dictionary['White']}\n" \
                       f"Black: {info_dictionary['Black']}\n" \
                       f"Result: {info_dictionary['Result']}\n" \
                       f"Rounds Played: {info_dictionary['RoundsPlayed']}\n" \
                       f"\n{moves_str + ' ' + info_dictionary['Result']}"

        # placing in the frame
        text = Text(self, background="light grey", relief="flat", width=39, height=38)
        text.insert(index=0.0, chars=text_to_show)
        scrollbar = Scrollbar(master=self, command=text.yview)
        text.config(state="disabled", yscrollcommand=scrollbar.set)
        text.pack(fill="both", side="left")
        scrollbar.pack(fill="both", side="right")
