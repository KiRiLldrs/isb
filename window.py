
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox, filedialog, Tk, Label, Frame, \
    Button, Scrollbar, Text, WORD, BOTH, RIGHT, Y


import CONST
import functions

class App:
    def __init__(self):
        self.root = Tk()
        self.setup_ui()

        self.console = None
        self.setup_console()

    def setup_ui(self):
        self.root.title("Searching for card number")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        bg_image = Image.open("background.jpg").resize((900, 650), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = Label(self.root, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_frame = Frame(self.root, bg='', padx=10, pady=10)
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        Frame(self.root, height=50).pack()
        Button(self.root, text="Find a card number", width=30, height=2,
               command=self.on_find_card_number).pack(pady=10)
        Button(self.root, text="Check the report", width=30, height=2).pack(pady=10)
        Button(self.root, text="Change the data", width=30, height=2).pack(pady=10)
        Button(self.root, text="Experiment", width=30, height=2).pack(pady=10)


    def setup_console(self):
        console_frame = Frame(self.root, bg='#202020', bd=1)
        console_frame.place(relx=0.5, rely=0.7, anchor="center", width=800, height=250)

        console_scroll = Scrollbar(console_frame)
        console_scroll.pack(side=RIGHT)

        self.console = Text(console_frame,
                       bg='#202020',
                       fg='white',
                       font=('Courier', 10),
                       yscrollcommand=console_scroll.set,
                       wrap=WORD)
        self.console.pack(expand=True, fill=BOTH)
        console_scroll.config(command=self.console.yview)

    def write_to_console(self, text: str):
        self.console.insert("end", text + "\n")
        self.console.see("end")

    def run_search(self):
        bin = CONST.SBERBANK_VISA_DEBIT_BINS
        last_four = CONST.LAST_FOUR
        hash = CONST.HASH

        card_number = None

        for bin in CONST.SBERBANK_VISA_DEBIT_BINS:
            card_number = functions.find_card_number(bin, CONST.LAST_FOUR, CONST.HASH)
            if card_number:
                self.write_to_console(f"Result was found: {card_number}")
                functions.write_report(functions.get_report(card_number, bin, CONST.HASH, CONST.LAST_FOUR))
                self.write_to_console(f"Result was saved to report")
                break

    def on_find_card_number(self):
        self.write_to_console("The card number is being selected...")

        self.root.after(500, self.run_search)


    def run(self):
        self.root.mainloop()
