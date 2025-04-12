from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import filedialog

from const import (
    ENCRYPTED_SYMMETRIC_KEY,
    PUBLIC_KEY,
    PRIVATE_KEY
)
import decryption
import encryption
import generation


state = {
    "symmetric_key_length": None,
    "symmetric_key": None,
    "private_key": None,
    "public_key": None
}


def generate_keys():
    try:
        key_length = simpledialog.askinteger("Input the key length", "Input the key length (128,192,256):")
        if not key_length:
            return

        state["symmetric_key_length"] = key_length
        state["symmetric_key"] = generation.generate_symmetric_key(key_length)
        state["private_key"], state["public_key"] = generation.generate_asymmetric_keys()

        generation.serialize(state["private_key"], state["public_key"], PRIVATE_KEY, PUBLIC_KEY)
        generation.encrypt_symmetric_key(state["symmetric_key"],state["public_key"], ENCRYPTED_SYMMETRIC_KEY)

        messagebox.showinfo("Success", f"Keys were created (symmetric key length: {key_length} bit")
    except Exception as e:
        messagebox.showerror("Error", f"The wrong length: {e}")


def encrypt_text():
    try:
        file_path = filedialog.askopenfilename(title="Select file for encryption")
        if not file_path:
            return

        save_path = filedialog.asksaveasfilename(title="Select where decrypted file will be saved")
        if not save_path:
            return

        encryption.encrypt_file(
            encryption.symmetric_key_decryption(ENCRYPTED_SYMMETRIC_KEY, PRIVATE_KEY),
            file_path, save_path
        )
        messagebox.showinfo("Success", f"Text were encrypted")
    except Exception as e:
        messagebox.showerror("Error", f"Error occurs while encryption: {e}")


def decrypt_text():
    try:
        file_path = filedialog.askopenfilename(title="Select file for decryption")
        if not file_path:
            return

        save_file = filedialog.asksaveasfilename(title="Select where decrypted file will be saved")
        if not save_file:
            return

        decryption.file_decryption(file_path,
                                    encryption.symmetric_key_decryption(ENCRYPTED_SYMMETRIC_KEY, PRIVATE_KEY),
                                    save_file
                                    )
        messagebox.showinfo("Success", f"Text were decrypted")
    except Exception as e:
        messagebox.showerror("Error", f"Error occurs while decryption: {e}")


def main():
    root = tk.Tk()
    root.title("Encryption and Decryption")
    root.geometry("600x400")
    root.resizable(False, False)

    bg_image = Image.open("background.jpg")
    bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    button_frame = tk.Frame(root, bg='', padx=10, pady=10)
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(root, text="Generate keys", width=30, height=2, command=generate_keys).pack(pady=20)
    tk.Button(root, text="Encrypt text", width=30, height=2, command=encrypt_text).pack(pady=20)
    tk.Button(root, text="Decrypt text", width=30, height=2, command=decrypt_text).pack(pady=20)

    root.mainloop()



if __name__ == "__main__":
    main()

