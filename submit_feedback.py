# -------------------------------------------------------------------------------------------------------------------- #
# submit_feedback.py: περιέχει την κλάση FeedBack                                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
import smtplib as smtp
from email.message import EmailMessage
from ssl import create_default_context
from tkinter import Toplevel, Label, Entry, Text, Button
from pickle import load


class FeedBack(Toplevel):
    """
    Ανοίγει ένα νέο, εξαρτημένο παράθυρο
    Ο χρήστης μπορεί να συμπληρώσει τα στοιχεία του και να στείλει ανατροφοδότηση για την εφαρμογή
    Κληρονομεί από τη γονική κλάση Toplevel

    Ορίσματα:
    ---------
        master (main_program.MainProgram):
            παράθυρο Tk από το οποίο είναι εξαρτημένο το παράθυρο FeedBack

    Μέθοδοι:
    --------
        submit_feedback(self):
            πραγματοποιεί σύνδεση και αποστολή email ανατροφοδότησης, με ότι πληροφορίες έχει συμπληρώσει ο χρήστης
    """
    def __init__(self, master):
        # κλήση της super για κληρονόμηση ιδιοτήτων απο μητρική κλάση
        super().__init__(master=master)
        # εικονίδιο παραθύρου
        self.iconbitmap("icons\\stonk.ico")
        # όνομα παραθύρου
        self.title("Feedback")
        # αφαίρεση ικανότητας χρήστη να τροποποιεί το μέγεθος του παραθύρου
        self.resizable(False, False)

        # δημιουργία label και entry-box
        name_label = Label(master=self, text="name:", bg="light blue", font=("consolas", 9))
        self.name_box = Entry(master=self, width=40, bg="light yellow")
        email_label = Label(master=self, text="e-mail:", bg="light blue", font=("consolas", 9))
        self.email_box = Entry(master=self, width=40, bg="light yellow")
        self.body_box = Text(master=self, width=37, height=10, bg="light yellow")

        # τοποθέτηση στο παράθυρο
        name_label.grid(row=0, column=0)
        email_label.grid(row=1, column=0)
        self.name_box.grid(row=0, column=1, sticky="w")
        self.email_box.grid(row=1, column=1, sticky="w")
        self.body_box.grid(row=2, column=0, columnspan=2)

        # δημιουργία κουμπιού
        self.send_button = Button(master=self, text="Submit Feedback",
                                  font=("consolas", 10, "bold"),
                                  background="light green",
                                  activebackground="green",
                                  command=self.submit_feedback)
        self.send_button.grid(row=3, column=0, columnspan=2, sticky="n")

        # e-mail
        self.__mail_address = 'python.chesspgn@gmail.com'
        try:
            with open("pip3w", "rb") as f:
                self.__pwd = load(f)
                self.__pwd = self.__pwd[2:4] + self.__pwd[7:11] + self.__pwd[4:7] + \
                             self.__pwd[11:15] + self.__pwd[0:2] + self.__pwd[15]
        except OSError:
            self.send_button.grid_forget()
            Label(master=self,
                  text="Error! Failed To Access Connection Data!",
                  bg="light blue", fg="red",
                  font=("consolas", 10, "bold")).grid(row=3, column=0, columnspan=2, sticky="n")
            self.after(3000, self.destroy)

        self.email_obj = EmailMessage()
        self.email_obj["Subject"] = "ChessPGN Manager Feedback:"

        self.config(bg="light blue")
        self.mainloop()

    def submit_feedback(self):
        """
        Πραγματοποιεί σύνδεση και αποστολή email ανατροφοδότησης, με ότι πληροφορίες έχει συμπληρώσει ο χρήστης
        """
        # κυρίως σώμα email
        email_body = f"name: {self.name_box.get()}\n" \
                     f"email: {self.email_box.get()}\n" \
                     f"{self.body_box.get(1.0,'end-1c')}"
        self.email_obj.set_content(email_body)

        try:
            # αποστολή email
            with smtp.SMTP_SSL("smtp.gmail.com", 465, context=create_default_context()) as f:
                f.login(self.__mail_address, self.__pwd)
                f.sendmail(self.__mail_address, self.__mail_address, self.email_obj.as_string())
                # ενημερωτικό label προς τον χρήστη
                self.send_button.grid_forget()
                Label(master=self, text="Thank You!",
                      bg="light blue", font=("consolas", 10, "bold")).grid(row=3, column=0, columnspan=2, sticky="n")
                self.after(3000, self.destroy)
        except:
            # χειρισμός σφαλμάτων
            self.send_button.grid_forget()
            Label(master=self,
                  text="Error! Please Check Internet Connection",
                  bg="light blue", fg="red",
                  font=("consolas", 10, "bold")).grid(row=3, column=0, columnspan=2, sticky="n")
            self.after(3000, self.destroy)
