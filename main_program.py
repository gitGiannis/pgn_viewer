# -------------------------------------------------------------------------------------------------------------------- #
# main_program.py: includes class MainProgram                                                                          #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Tk, Menu, Button, Label, Frame, PhotoImage
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from os import listdir, mkdir
from os.path import abspath
from manual_game_selector import ManualGameSelector
from listbox_game_display import ListboxGameDisplay
from functions import show_help, show_info, show_credits, about
from my_exceptions import PossibleCorruptFile
from submit_feedback import FeedBack


class MainProgram(Tk):
    """
    Inherits from the parent class (Tk) and creates the main window of the app
    Provides two main ways for the user to load pgn files

    ...

    Attributes:
    -----------
        menubar (Menu):
            top side menu-bar

        file_menu (Menu):
            dropdown sub-menu

        help_menu (Menu):
            dropdown sub-menu

        main_frame (Frame):
            main frame of the window

        warning_label (Label):
            label to show messages to user

    Methods:
    --------
        select_file(self):
            opens Windows explorer window for manual pgn file loading

        open_file(self):
            loads al the pgn files found in the pre-selected folder inside the app files

        submenus_config(self):
            configures the options of file and help sub-menus

        submit_fb(self):
            reception of user feedback

        copy_path(self):
            copies (to clipboard) the absolute path to pre-selected folder with pgn files

        exit(self):
            destroys the main window and exits the app
    """

    def __init__(self):
        """
        Initialization of the main window object
        """
        # initialization of parent class (Tk)
        super().__init__()
        # window title and icon
        self.iconbitmap("icons\\stonk.ico")
        self.title("Chess PGN manager v1.0")
        # non-resizable window
        self.resizable(False, False)

        # menu-bar initialization --------------------------------------------------------------------------------------
        self.menubar = Menu(self)
        # file sub-menu
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="  File  ", menu=self.file_menu)
        # help sub-menu
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="  Help  ", menu=self.help_menu)

        # configuring of the sub-menus options
        self.submenus_config()

        # main frame to include the widgets ----------------------------------------------------------------------------
        self.main_frame = Frame(master=self, bg="light blue")
        # main label with image for background
        chess_image = PhotoImage(master=self.main_frame, file="icons\\chess.png")
        Label(master=self.main_frame, image=chess_image, anchor="s", width=550, height=320, background="light yellow"
              ).pack()

        # initialization and placing of buttons ------------------------------------------------------------------------
        Button(self.main_frame,
               text="Select File",
               font=("consolas", 12, "bold"),
               background="light green",
               activebackground="green",
               width="15",
               command=self.select_file).pack(side="right")

        Button(self.main_frame,
               text="Show Files",
               font=("consolas", 12, "bold"),
               background="light green",
               activebackground="green",
               width="15",
               command=self.show_files).pack(side="left")

        # Label for showing messages to user ---------------------------------------------------------------------------
        self.warning_label = Label(self.main_frame, bg="light blue", fg="red", font=("consolas", 12, "bold"), pady=5)

        # main window configuration and main frame packing -------------------------------------------------------------
        self.config(menu=self.menubar, background="light blue")
        self.main_frame.pack(fill="x")

        # window mainloop ----------------------------------------------------------------------------------------------
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.mainloop()

    def select_file(self):
        """
        Opens new Windows explorer window for manual pgn file selection
        """
        # explorer window
        file_path = askopenfilename(initialdir="pgn_files",
                                    title="Choose PGN file",
                                    filetypes=(("PGN files", "*.pgn"), ("All files", "*.*")))
        if file_path:
            # check file type
            if file_path[-4:] == ".pgn":
                # main frame gets withdrawn
                self.main_frame.forget()
                self.file_menu.entryconfig(0, state="disabled")
                self.file_menu.entryconfig(1, state="disabled")
                self.file_menu.entryconfig(3, state="disabled")

                try:
                    # ManualGameSelector frame gets packed
                    ManualGameSelector(root=self, pgn_filepath=file_path)
                except OSError:
                    # a relevant message is shown in case of failure to open the file
                    self.warning_label.config(text="Could not open file")
                    self.warning_label.pack(fill="both")
                    self.warning_label.after(2000, self.warning_label.pack_forget)
                except PossibleCorruptFile as v:
                    # in case of corrupt file, a relevant message is shown
                    self.warning_label.config(text=str(v))
                    self.warning_label.pack(fill="both")
                    self.warning_label.after(2000, self.warning_label.pack_forget)
            else:
                # wrong file type
                self.warning_label.config(text="Invalid File Type!")
                self.warning_label.pack(fill="both")
                self.warning_label.after(2000, self.warning_label.pack_forget)

    def show_files(self):
        """
        Loads all pgn file found in pre-selected folder
        """
        try:
            # list with directory items
            list_dir = listdir("pgn_files")
        except FileNotFoundError:
            # pre-selected directory was not found or deleted, and is created again
            mkdir("pgn_files")
            list_dir = []

        # check file type
        for pgn_file_path in list_dir:
            if pgn_file_path[-4:] != ".pgn":
                # removal of wrong file types
                list_dir.remove(pgn_file_path)

        if list_dir:
            # main frame gets withdrawn
            self.main_frame.forget()
            self.file_menu.entryconfig(0, state="disabled")
            self.file_menu.entryconfig(1, state="disabled")
            self.file_menu.entryconfig(3, state="disabled")

            # ListboxGameDisplay frame gets packed
            ListboxGameDisplay(root=self, pgn_list=list_dir)
        else:
            # no files (of correct type) were found in the pre-selected directory
            self.warning_label.config(text="No Files Found!")
            self.warning_label.pack(fill="both")
            self.warning_label.after(2000, self.warning_label.pack_forget)

    def submenus_config(self):
        """
        Configures the options of file and help sub-menus
        """
        # file sub-menu options
        self.file_menu.add_command(label="Show Files", command=self.show_files)
        self.file_menu.add_command(label="Select File", command=self.select_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Copy Path", command=self.copy_path)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Back", state="disabled")
        self.file_menu.add_command(label="Exit", command=self.exit)

        # help sub-menu options
        self.help_menu.add_command(label="Help", command=show_help)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About PGN", command=show_info)
        self.help_menu.add_command(label="App Info", command=about)
        self.help_menu.add_command(label="Show Credits", command=show_credits)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Submit Feedback", command=self.submit_fb)

    def submit_fb(self):
        """
        User feedback
        """
        FeedBack(master=self)

    def copy_path(self):
        """
        Copies absolute path to pre-selected pgn directory
        """
        self.clipboard_clear()
        self.clipboard_append(abspath("pgn_files"))
        self.warning_label.config(text="Copied 'pgn_files' dir path")
        self.warning_label.pack(fill="both")
        self.warning_label.after(2000, self.warning_label.pack_forget)

    def exit(self):
        """
        Ask confirmation to terminate the app
        """
        if askyesno(master=self, title="Quit?", message="Do you really wish to quit?", default="no"):
            self.destroy()
