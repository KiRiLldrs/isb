from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox, filedialog, Tk, Label, Frame, Button

from const import (
    ENCRYPTED_SYMMETRIC_KEY,
    PUBLIC_KEY,
    PRIVATE_KEY,
    PLAINTEXT,
    ENCRYPTED_TEXT,
    DECRYPTED_TEXT
)
from Keys import Keys
from FileDecryptor import FileDecryptor
from FileEncryptor import FileEncryptor


class App:
    def __init__(self):
        self.state = {
            "symmetric_key_length": None,
            "symmetric_key": None,
            "private_key": None,
            "public_key": None
        }


    def generate_keys(self):
        try:
            key_length = simpledialog.askinteger("Input the key length", "Input the key length (128,192,256):")
            if not key_length:
                return

            self.state["symmetric_key_length"] = key_length
            self.state["symmetric_key"] = Keys.generate_symmetric_key(key_length)
            self.state["private_key"], self.state["public_key"] = Keys.generate_asymmetric_keys()

            Keys.serialize_private_key(self.state["private_key"], PRIVATE_KEY)
            Keys.serialize_public_key(self.state["public_key"], PUBLIC_KEY)

            encrypted_key = Keys.encrypt_symmetric_key(self.state["symmetric_key"],self.state["public_key"])
            Keys.save_encrypted_key(encrypted_key, ENCRYPTED_SYMMETRIC_KEY)

            messagebox.showinfo("Success", f"Keys were created (symmetric key length: {key_length} bit")
        except Exception as e:
            messagebox.showerror("Error", f"The wrong length: {e}")


    def encrypt_text(self):
        try:
            file_path = filedialog.askopenfilename(title="Select file for encryption")
            if not file_path:
                return

            save_path = filedialog.asksaveasfilename(title="Select where encrypted file will be saved")
            if not save_path:
                return

            private_key = Keys.load_private_key(PRIVATE_KEY)
            encrypted_key = Keys.load_encrypted_key(ENCRYPTED_SYMMETRIC_KEY)
            symmetric_key = Keys.symmetric_key_decryption(encrypted_key, private_key)

            iv = FileEncryptor.generate_iv()
            cipher_text = FileEncryptor.encrypt_data(
                FileEncryptor.add_padding(FileEncryptor.read_file(PLAINTEXT)),
                symmetric_key, iv
            )

            FileEncryptor.write_encrypted_file(ENCRYPTED_TEXT, iv, cipher_text)

            messagebox.showinfo("Success", f"Text were encrypted")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurs while encryption: {e}")


    def decrypt_text(self):
        try:
            file_path = filedialog.askopenfilename(title="Select file for decryption")
            if not file_path:
                return

            save_file = filedialog.asksaveasfilename(title="Select where decrypted file will be saved")
            if not save_file:
                return

            private_key = Keys.load_private_key(PRIVATE_KEY)
            encrypted_key = Keys.load_encrypted_key(ENCRYPTED_SYMMETRIC_KEY)
            symmetric_key = Keys.symmetric_key_decryption(encrypted_key, private_key)

            iv, cipher_text = FileDecryptor.read_encrypted_file(ENCRYPTED_TEXT)
            FileDecryptor.write_decrypted_file(
                DECRYPTED_TEXT,
                FileDecryptor.remove_padding(FileDecryptor.decrypt_data(cipher_text, symmetric_key, iv)))

            messagebox.showinfo("Success", f"Text were decrypted")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurs while decryption: {e}")


    def run(self):
        root = Tk()
        root.title("Encryption and Decryption")
        root.geometry("600x400")
        root.resizable(False, False)

        bg_image = Image.open("background.jpg")
        bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = Label(root, image=bg_photo)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        button_frame = Frame(root, bg='', padx=10, pady=10)
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        Button(root, text="Generate keys", width=30, height=2, command=self.generate_keys).pack(pady=20)
        Button(root, text="Encrypt text", width=30, height=2, command=self.encrypt_text).pack(pady=20)
        Button(root, text="Decrypt text", width=30, height=2, command=self.decrypt_text).pack(pady=20)

        root.mainloop()



if __name__ == "__main__":
    app = App()
    app.run()

