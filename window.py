import json
import time
from threading import Thread

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

        self.root.title("01001000 011䷄䷅䷆䷇0001 0101䷁01011 ䷀䷂1䷃0䷈䷉䷊䷋ █▒▒0011 01▒▒▒▒▒▒▒ 10%")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        img = Image.open("icon.jpg").resize((32,32))
        icon = ImageTk.PhotoImage(img)
        self.root.iconphoto(True, icon)


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
        Button(self.root, text="Check the report", width=30, height=2,
               command=self.on_check_the_report).pack(pady=10)
        Button(self.root, text="Change the data", width=30, height=2,
               command=self.on_change_the_data).pack(pady=10)
        Button(self.root, text="Experiment", width=30, height=2).pack(pady=10)

        Button(self.root, text="Clear", width=10, height=1,
               command=self.on_clear).place(x=770,y=590)


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

    def write_to_console(self, text: str, color = "white"):
        def typewriter_effect():
            delay = 0.05

            self.console.tag_config("green", foreground="green")
            self.console.tag_config("red", foreground="red")
            self.console.tag_config("yellow", foreground="yellow")
            self.console.tag_config("white", foreground="white")

            tag_colors = {
                "success": "green",
                "fail": "red",

                "status": "yellow",
                "card_number": "yellow",
                "bin": "yellow",
                "hash": "yellow",
                "last_four_numbers": "yellow",
                "processes_used": "yellow"
            }

            words = text.split()
            for word in words:
                clean_word = word.strip(":").lower()
                new_color = tag_colors.get(clean_word)

                if len(word) >=50:
                    delay = 0.01

                for char in word:
                    if new_color:
                        self.console.insert("end", char, new_color)
                    else:
                        self.console.insert("end", char, color)

                    self.console.see("end")
                    time.sleep(delay)
                    self.console.update()

                self.console.insert("end", " ")
                delay = 0.025

            self.console.insert("end","\n")

            self.console.see("end")

        Thread(target=typewriter_effect(), daemon=True).start()

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

    def on_check_the_report(self):
        with open('card_search_result.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        for key, value in data.items():
            self.write_to_console(f"{key}: {value}")

    def on_clear(self):
        self.console.delete("1.0", "end")

    def on_change_the_data(self):
        self.write_to_console("Input the new hash: ", color="red")

    def run(self):
        self.root.mainloop()
