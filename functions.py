# -------------------------------------------------------------------------------------------------------------------- #
# functions.py: includes various functions used in the app                                                             #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter.messagebox import showinfo


# main_program.py ------------------------------------------------------------------------------------------------------
def show_help():
    """
    Shows window with options of main menu
    """
    showinfo(title="Help",
             message="Show Files:\n"
                     "Display all pgn files from pgn_file directory\n"
                     "You can find this directory inside the app folder\n"
                     "or copy the filepath through File/Copy Path",
             detail="Select File:\nManually select a pgn file")


def about():
    """
    Shows technical info about the app
    """
    showinfo(title="About",
             message="Chess PGN Manager v1.0\n"
                     "Release date: 14 June 2023")


def show_credits():
    """
    Shows credits
    """
    showinfo(title="Credits",
             message="Developers:\n"
                     ">> Moiris Ioannis\n",
             detail="Special Thanks To:\n"
                     ">> Gkogkos Christos, for the help provided")


def show_info():
    """
    Shows information on pgn files
    """
    showinfo(title="Info about PGN files",
             message="PGN [Portable Game Notation] is a standard plain text format\n"
                     "for recording chess games (both the moves and related data).\n"
                     "Devised around 1993 by Steven J. Edwards, pgn became\n"
                     "popular because it can be easily read by humans and is also\n"
                     "supported by most chess software\n"
                     "This application reads the information stored in a pgn file\n"
                     "and displays the basic info, as well as the development of\n"
                     "the game in a 2D environment.\n",
             detail="To do so, click the \"Show Files\" / \"Select File\" button and\n"
                     "select a pgn file to load.")
