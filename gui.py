# -------------------------------------------------------------------------------------------------------------------- #
# gui.py: includes class GUI                                                                                           #
# -------------------------------------------------------------------------------------------------------------------- #
from tkinter import Tk, Menu, PhotoImage, Frame, Label, Button, IntVar
from tkinter.messagebox import askyesno, showinfo
from pygame import mixer
from my_exceptions import PositionReached
from info_frame_for_gui import InfoFrame
from captured_piece_frame import CapturedPieceFrame


class GUI(Tk):
    """
    Opens a new Tkinter window with the 2D chess board and represents the game from start to end using some basic
    buttons (forwards, backwards etc.)
    The window also includes two frames, one for showing the game info and another one for showing the captured pieces

    ...

    Attributes:
    -----------
        *_image (PhotoImage):
            images for each piece

        game_loader (GameLoader):
            object containing all the info needed for each game

        board (list):
            the 2D chess board

        button_next (Button):
            button for next move

        button_prev (Button):
            button for previous move

        button_restart (Button):
            button for restarting the game

        button_start (Button):
            button for starting the game

        info_frame (Frame):
            frame with game info

        cap_frame (Frame):
            frame with captured pieces

        checkbutton_var (IntVar):
            variable for autoplay checkbutton

        file_menu (Menu):
            drop down file menu

        board_frame (Frame):
            chess board frame

        __next_move_display (Label):
            label with info about next move

        __starting_move (bool):
            boolean value (if true the game is in the first move)

        __ending_move (bool):
            boolean value (if true the game is in the last move)

        __result (str):
            result of the game

    Methods:
    --------
        __update_gui_board(self):
            updates the chess board

        load_next(self):
            continues to next move

        load_previous(self):
            goes back to previous move

        start_game(self):
            starts the game

        restart_game(self):
            restarts the game

        autoplay(self):
            auto-plays the game moves per one second until canceled or game ends

        text_config(self) -> str:
            edits and returns string with next move display info

        show_controls(self):
            shows window with the controls explained

        exit(self):
            shows yes/no window for exit confirmation

        right_key_bind(self, event):
            performs next move using key event <right-arrow>

        left_key_bind(self, event):
            performs previous move using key event <right-arrow>

        down_key_bind(self, event):
            restarts the game using key event <down-arrow>

        up_key_bind(self, event):
            auto-plays next move using key event <up-arrow>
    """

    def __init__(self, game_loader_obj, game_dict: dict):
        """
        Initializes the new window

        ...

        Parameters:
        -----------
            game_loader_obj (game_loader.GameLoader):
                αντικείμενο με τα στιγμιότυπα του αγώνα, καθώς και άλλες πληροφορίες

            game_dict (dict):
                λεξικό με τις πληροφορίες του αγώνα
        """
        # initialization of parent class (Tk)
        super().__init__()
        # initialization of window -------------------------------------------------------------------------------------
        # title and icon
        self.title(f"Chess Match: W: {game_dict['White']} vs B: {game_dict['Black']} - ({game_dict['Result']})")
        self.iconbitmap("icons\\stonk.ico")

        # non-resizable window
        self.resizable(False, False)

        # initialization of GameLoader object --------------------------------------------------------------------------
        self.game_loader = game_loader_obj

        self.__result = game_dict["Result"]

        # menu-bar initialization --------------------------------------------------------------------------------------
        menubar = Menu(self)

        # File sub-menu
        self.file_menu = Menu(menubar, tearoff=0)
        # sub-menu addition to main menu
        menubar.add_cascade(label="  File  ", menu=self.file_menu)
        # options
        self.file_menu.add_checkbutton(label="Autoplay", command=self.autoplay)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)

        # Help sub-menu
        help_menu = Menu(menubar, tearoff=0)
        # sub-menu addition to main menu
        menubar.add_cascade(label="  Help  ", menu=help_menu)
        # options
        help_menu.add_command(label="Help", command=self.show_controls)

        # pygame mixer initialization ----------------------------------------------------------------------------------
        mixer.init()

        # image initialization -----------------------------------------------------------------------------------------
        # blank image for empty squares
        self.blank = PhotoImage(master=self, file="icons\\piece_icons\\BLANK_ICON.png")

        # images for black pieces
        self.rb_image = PhotoImage(master=self, file="icons\\piece_icons\\rb.png")
        self.nb_image = PhotoImage(master=self, file="icons\\piece_icons\\nb.png")
        self.bb_image = PhotoImage(master=self, file="icons\\piece_icons\\bb.png")
        self.qb_image = PhotoImage(master=self, file="icons\\piece_icons\\qb.png")
        self.kb_image = PhotoImage(master=self, file="icons\\piece_icons\\kb.png")
        self.pb_image = PhotoImage(master=self, file="icons\\piece_icons\\pb.png")

        # images for white pieces
        self.rw_image = PhotoImage(master=self, file="icons\\piece_icons\\rw.png")
        self.nw_image = PhotoImage(master=self, file="icons\\piece_icons\\nw.png")
        self.bw_image = PhotoImage(master=self, file="icons\\piece_icons\\bw.png")
        self.qw_image = PhotoImage(master=self, file="icons\\piece_icons\\qw.png")
        self.kw_image = PhotoImage(master=self, file="icons\\piece_icons\\kw.png")
        self.pw_image = PhotoImage(master=self, file="icons\\piece_icons\\pw.png")

        # checked king images
        self.kb_checked = PhotoImage(master=self, file="icons\\piece_icons\\kb_checked.png")
        self.kw_checked = PhotoImage(master=self, file="icons\\piece_icons\\kw_checked.png")

        # chess board initialization -----------------------------------------------------------------------------------
        self.board_frame = Frame(self, bd=10, relief="raised")

        # creation of 2D board with labels
        self.board = []
        for row in range(8):
            temp = []
            for col in range(8):
                # blank image is set to each label until the start of the game
                temp.append(Label(self.board_frame, image=self.blank, bd=7))
            self.board.append(temp)

        # colour setting for background
        for row in range(8):
            for col in range(8):
                self.board[row][col].grid(row=row, column=col)
                if (row + col) % 2 == 0:
                    self.board[row][col].config(bg="#EEEED2")
                else:
                    self.board[row][col].config(bg="#47473C")

        # file and rank indexes for side squares
        letters = self.game_loader.files
        numbers = self.game_loader.ranks
        # pixel index in frame
        position = 0
        for num in range(8):
            if num % 2 == 0:
                # label with rank
                Label(master=self.board_frame,
                      bg="#47473C",
                      fg="#EEEED2",
                      font=("consolas", 10, "bold"),
                      text=numbers[7 - num]).place(relx=0.97, y=position)
                # label with file
                Label(master=self.board_frame,
                      bg="#47473C",
                      fg="#EEEED2",
                      font=("consolas", 10, "bold"),
                      text=letters[num]).place(x=position, rely=0.96)
            else:
                # label with rank
                Label(master=self.board_frame,
                      bg="#EEEED2",
                      fg="#47473C",
                      font=("consolas", 10, "bold"),
                      text=numbers[7 - num]).place(relx=0.97, y=position)
                # label with file
                Label(master=self.board_frame,
                      bg="#EEEED2",
                      fg="#47473C",
                      font=("consolas", 10, "bold"),
                      text=letters[num]).place(x=position, rely=0.96)
            # pixel position index gets added 74 pixels (60 pixels for the image and 7+7 for the padding)
            position += 74

        # auxiliary variables
        self.__starting_move = True
        self.__ending_move = False

        # autoplay options ---------------------------------------------------------------------------------------------
        # initialization of checkbutton variable
        self.checkbutton_var = IntVar(master=self.file_menu)
        self.file_menu.entryconfig(0, variable=self.checkbutton_var, state="disabled")
        # string that stores the self.after() method identifier to cancel if necessary
        self.__identifier_for_after_method = ""

        # initialization of button frame and buttons -------------------------------------------------------------------
        button_frame = Frame(master=self, bg="light blue")

        self.button_next = Button(button_frame,
                                  text="---->",
                                  state="disabled",
                                  font=("consolas", 12, "bold"),
                                  background="light green",
                                  activebackground="green",
                                  width=8,
                                  command=self.load_next)

        self.button_prev = Button(button_frame,
                                  text="<----",
                                  state="disabled",
                                  font=("consolas", 12, "bold"),
                                  background="light green",
                                  activebackground="green",
                                  width=8,
                                  command=self.load_previous)

        self.button_restart = Button(button_frame,
                                     text="||<--",
                                     state="disabled",
                                     font=("consolas", 12, "bold"),
                                     background="light green",
                                     activebackground="green",
                                     width=8,
                                     command=self.restart_game)

        self.button_start = Button(button_frame,
                                   text="start game",
                                   font=("consolas", 12, "bold"),
                                   background="light green",
                                   activebackground="green",
                                   command=self.start_game)

        # next move display label initialization -----------------------------------------------------------------------
        self.__next_move_display = Label(button_frame,
                                         text="'start game' to continue",
                                         background="light blue",
                                         font=("consolas", 12, "bold"),
                                         width=28)

        # widget packing -----------------------------------------------------------------------------------------------
        # packing buttons in button frame
        self.button_next.pack(side="right")
        self.button_prev.pack(side="right")
        self.button_restart.pack(side="right")
        self.button_start.pack(side="left")
        # packing label in button frame
        self.__next_move_display.pack(side="right", fill="both")

        # chess board gets placed on grid
        self.board_frame.grid(row=0, column=0)
        # button frame gets placed on grid
        button_frame.grid(row=1, column=0, sticky="ew")

        # initialization of InfoFrame with the game info and placing on grid
        InfoFrame(master=self, info_dictionary=game_dict).grid(row=0, column=1, sticky="n")

        # initialization of CapturedPieceFrame with captured pieces and placing on grid
        self.cap_frame = CapturedPieceFrame(master=self, blank_image=self.blank,
                                            captured_piece_dictionary=self.game_loader.captured_piece_names,
                                            rw_image=self.rw_image, nw_image=self.nw_image, bw_image=self.bw_image,
                                            qw_image=self.qw_image, pw_image=self.pw_image, pb_image=self.pb_image,
                                            rb_image=self.rb_image, nb_image=self.nb_image, bb_image=self.bb_image,
                                            qb_image=self.qb_image)
        self.cap_frame.grid(row=0, column=1, rowspan=2, sticky="sw")

        # yes/no window for exit confirmation
        self.protocol("WM_DELETE_WINDOW", self.exit)

        # window configuration and mainloop
        self.config(menu=menubar, background="light grey")
        self.mainloop()

    def __update_gui_board(self):
        """
        Updates the chess board after every move
        """
        # the info_dictionaries_per_round list attribute of game_loader contains lists with the positions of each piece
        # for each round
        # each dictionary is looped through and the board gets updated with the new piece positions
        for piece in self.game_loader.info_dictionaries_per_round[self.game_loader.round]:
            if piece["name"] == "  ":
                self.board[piece["row"]][piece["col"]].config(image=self.blank, compound="center")
            elif piece["name"] == "pb":
                self.board[piece["row"]][piece["col"]].config(image=self.pb_image, compound="center")
            elif piece["name"] == "pw":
                self.board[piece["row"]][piece["col"]].config(image=self.pw_image, compound="center")
            elif piece["name"] == "rb":
                self.board[piece["row"]][piece["col"]].config(image=self.rb_image, compound="center")
            elif piece["name"] == "nb":
                self.board[piece["row"]][piece["col"]].config(image=self.nb_image, compound="center")
            elif piece["name"] == "bb":
                self.board[piece["row"]][piece["col"]].config(image=self.bb_image, compound="center")
            elif piece["name"] == "qb":
                self.board[piece["row"]][piece["col"]].config(image=self.qb_image, compound="center")
            elif piece["name"] == "rw":
                self.board[piece["row"]][piece["col"]].config(image=self.rw_image, compound="center")
            elif piece["name"] == "nw":
                self.board[piece["row"]][piece["col"]].config(image=self.nw_image, compound="center")
            elif piece["name"] == "bw":
                self.board[piece["row"]][piece["col"]].config(image=self.bw_image, compound="center")
            elif piece["name"] == "qw":
                self.board[piece["row"]][piece["col"]].config(image=self.qw_image, compound="center")
            elif piece["name"] == "kb":
                if self.game_loader.check_per_round[self.game_loader.round] == "b":
                    self.board[piece["row"]][piece["col"]].config(image=self.kb_checked, compound="center")
                else:
                    self.board[piece["row"]][piece["col"]].config(image=self.kb_image, compound="center")
            elif piece["name"] == "kw":
                if self.game_loader.check_per_round[self.game_loader.round] == "w":
                    self.board[piece["row"]][piece["col"]].config(image=self.kw_checked, compound="center")
                else:
                    self.board[piece["row"]][piece["col"]].config(image=self.kw_image, compound="center")

    def load_next(self):
        """
        Continues to the next move and enables/disables control buttons based on the current round
        """
        # previous move and restart buttons get activated (if previously disabled)
        self.button_prev.config(state="normal")
        self.button_restart.config(state="normal")
        self.__starting_move = False

        try:
            # advance to next move
            self.game_loader.next_move()
        except PositionReached:
            self.game_loader.next_move(force=True)
            # next move button and autoplay checkbutton get disabled
            self.button_next.config(state="disabled")
            self.checkbutton_var.set(0)
            self.file_menu.entryconfig(index=0, state="disabled")
            self.__ending_move = True

        # sound playback
        if self.game_loader.captures_per_round[self.game_loader.round]:
            mixer.music.load('sound_effects\\capture_sound.mp3')
            mixer.music.play(loops=0)
        else:
            mixer.music.load('sound_effects\\move_sound.mp3')
            mixer.music.play(loops=0)

        # board gets updated
        self.__update_gui_board()

        # next move display gets updated
        self.__next_move_display.config(text=self.text_config(),
                                        width=28,
                                        fg="red" if self.__ending_move else "black")

        # cap frame gets updated
        self.cap_frame.next_round()

    def load_previous(self):
        """
        Goes back to previous move and enables/disables control buttons based on the current round
        """
        # next move button and autoplay checkbutton get activated (if previously disabled)
        self.button_next.config(state="normal")
        self.file_menu.entryconfig(index=0, state="normal")
        # autoplay stops if the previous move button is pressed
        self.checkbutton_var.set(0)
        self.__ending_move = False

        try:
            # revert to previous move
            self.game_loader.previous_move()
        except PositionReached:
            self.game_loader.previous_move(force=True)
            # previous move and restart button get disabled
            self.button_prev.config(state="disabled")
            self.button_restart.config(state="disabled")
            self.__starting_move = True

        # sound playback
        mixer.music.load('sound_effects\\previous_move.mp3')
        mixer.music.play(loops=0, fade_ms=200)

        # board gets updated
        self.__update_gui_board()

        # next move display gets updated
        self.__next_move_display.config(text=self.text_config(), width=28, fg="black")

        # cap frame gets updated
        self.cap_frame.previous_round()

    def start_game(self):
        """
        Starts the game and initializes the key-bindings for buttons
        """
        # key-bindings initialization
        self.bind(sequence='<Right>', func=self.right_key_bind)
        self.bind(sequence='<Left>', func=self.left_key_bind)
        self.bind(sequence="<Down>", func=self.down_key_bind)
        self.bind(sequence="<Up>", func=self.up_key_bind)

        # activation of next move button and autoplay checkbutton
        self.button_next.config(state="normal")
        self.button_start.config(state="disabled")
        self.file_menu.entryconfig(index=0, state="normal")

        # board gets updated
        self.__update_gui_board()

        # next move display gets updated
        self.__next_move_display.config(text=self.text_config(), width=28, fg="black")

    def restart_game(self):
        """
        Restarts the game and enables/disables control buttons based on the current round
        """
        # round gets set to zero
        self.game_loader.restart_game()

        # button adjustment
        self.button_next.config(state="normal")
        self.button_prev.config(state="disabled")
        self.button_restart.config(state="disabled")
        self.file_menu.entryconfig(index=0, state="normal")
        self.checkbutton_var.set(0)
        self.__ending_move = False
        self.__starting_move = True

        # sound playback
        mixer.music.load('sound_effects\\restart.mp3')
        mixer.music.play(loops=0)

        # board gets updated
        self.__update_gui_board()

        # next move display gets updated
        self.__next_move_display.config(text=self.text_config(), width=28, fg="black")

        # cap frame gets updated
        self.cap_frame.reset()

    def autoplay(self):
        """
        Performs next move every one second until canceled or a previous move button is pressed
        """
        # if checkbutton is set to 1 (active)...
        if self.checkbutton_var.get() == 1:
            # ... the next move is performed ...
            self.load_next()
            # ... and then again after 1200 milliseconds
            self.__identifier_for_after_method = self.after(1200, self.autoplay)
        # if checkbutton is off and an after() method is active, it gets canceled
        elif self.__identifier_for_after_method:
            self.after_cancel(self.__identifier_for_after_method)

    def text_config(self) -> str:
        """
        Edits and returns string with next move information

        ...

        Returns:
        --------
            (str):
                string with next move information
        """
        if not self.__ending_move:
            cur_round = self.game_loader.round
            to_play = "White to play: " if cur_round % 2 == 0 else "Black to play: "
            self.__ending_move = False
            return to_play + str((cur_round // 2) + 1) + ". " + self.game_loader.moves[cur_round]
        else:
            # if in ending move, the game result gets displayed
            return self.__result

    def show_controls(self):
        """
        Shows information with the controls of the window
        """
        showinfo(master=self,
                 title="Help",
                 message="Press \"start game\" to start the game\n"
                         "Right arrow (---->) button or <Right-Key> for next move\n"
                         "Left arrow (<----) button or <Left-Key> for previous move\n"
                         "Reset arrow (||<--) button or <Down-Key>  to reset the board\n",
                 detail="You can also toggle autoplay (on/off) from the File menu\n"
                        "or by using the <Up-Key>")

    def exit(self):
        """
        Asks confirmation to exit the game display through a yes/no messagebox
        """
        if askyesno(master=self, title="Exit Game?", message="Do you really wish to exit this game?", default="no"):
            if self.__identifier_for_after_method:
                # if after() method is active, it gets canceled
                self.after_cancel(self.__identifier_for_after_method)
            self.destroy()

    def right_key_bind(self, event):
        """
        Performs the next move through key-event <right-arrow>, except if in last move
        """
        if self.__ending_move:
            return
        self.load_next()

    def left_key_bind(self, event):
        """
        Performs the previous move through key-event <left-arrow>, except if in first move
        """
        if self.__starting_move:
            return
        self.load_previous()

    def down_key_bind(self, event):
        """
        Restarts the game through key-event <down-arrow>, except if in first move
        """
        if self.__starting_move:
            return
        self.restart_game()

    def up_key_bind(self, event):
        """
        Activates/Deactivates autoplay function through key-event <up-arrow>, except if in first move
        """
        if self.__ending_move:
            return
        if self.checkbutton_var.get() == 1:
            # εάν το checkbutton_var είναι 1 (δηλαδή ενεργό), διακόπτει την αυτόματη αναπαραγωγή
            self.checkbutton_var.set(0)
            return
        if self.checkbutton_var.get() == 0:
            # εάν το checkbutton_var είναι 0 (δηλαδή ανενεργό), ενεργοποιεί την αυτόματη αναπαραγωγή
            self.checkbutton_var.set(1)
            self.autoplay()
