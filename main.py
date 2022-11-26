# import tkinter
import tkinter.messagebox
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk
from Crypto.Cipher import DES3
from hashlib import md5

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.hawkeye_logo_small = None
        self.button7 = None
        self.button5 = None
        self.button6 = None
        self.e1 = None
        self.button4 = None
        self.filename = None
        self.img = None
        self.title("Image Encryption using Triple DES")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        self.lb = customtkinter.CTkLabel(master=self, text="IMAGE ENCR/DECR USING TRIPLE DES",
                                         text_font=("Roboto Medium", -30))
        self.lb.grid()
        self.encbt = customtkinter.CTkButton(master=self, text='Encryption',
                                             text_font=("Roboto Medium", -20), command=self.upload_file)
        self.encbt.grid(pady=5)
        self.decbt = customtkinter.CTkButton(master=self, text='Decryption',
                                             text_font=("Roboto Medium", -20), command=self.upload_file1)
        self.decbt.grid(pady=5)
        self.grid_columnconfigure(0, weight=1)

    def retimage(self, filepath):
        try:
            temp = Image.open(filepath)
            temp = temp.resize((250, 300), resample=3)
            img = ImageTk.PhotoImage(temp)
            return img
        except:
            return 0

    def upload_file(self):
        self.reset()
        f_types = [('Jpg Files', '*.jpg')]
        self.filename = filedialog.askopenfilename(filetypes=f_types)
        self.x = self.retimage(self.filename)
        if self.x:
            self.hawkeye_logo_small = customtkinter.CTkLabel(master=self, image=self.x, bg="black")
            self.hawkeye_logo_small.grid()
            self.button4 = customtkinter.CTkButton(master=self, text="Enter TDES Secret Key",
                                                   text_font=("Roboto Medium", -16),
                                                   command=self.tdeskey1)
            self.button4.grid(pady=20)
            self.button5 = customtkinter.CTkButton(master=self, text="Encrypt image", command=self.submit1)

        else:
            tkinter.messagebox.showerror("Encrypted Image", 'Decrypt It')
            self.upload_file1()

    def upload_file1(self):
        self.reset()
        f_types = [('Jpg Files', '*.jpg')]
        self.filename = filedialog.askopenfilename(filetypes=f_types)
        x = self.retimage(self.filename)
        if x:
            tkinter.messagebox.showerror("Decrypted Image", 'Encrypt It')
            self.upload_file()
        else:
            self.img = self.retimage('img_1.png')
            self.hawkeye_logo_small = customtkinter.CTkLabel(master=self, image=self.img, bg="black")
            self.hawkeye_logo_small.grid()
            self.hawkeye_logo_small.configure(image=self.img)
            self.button4 = customtkinter.CTkButton(master=self, text="Enter TDES Secret Key",
                                                   text_font=("Roboto Medium", -16),
                                                   command=self.tdeskey1)
            self.button4.grid(pady=20)
            self.button5 = customtkinter.CTkButton(master=self, text="Decrypt image", command=self.submit)

    def tdeskey1(self):
        if self.e1 is None:
            self.e1 = customtkinter.CTkEntry(master=self)
            self.e1.grid()
            self.button5.grid(pady=10)
            self.button7 = customtkinter.CTkButton(master=self, text="RESET", command=self.reset)
            self.button7.grid(pady=10)

    def submit1(self):
        name = self.e1.get()
        self.encryption(name, self.filename)
        self.e1.configure(text='')

    def submit(self):
        name = self.e1.get()
        self.decryption(name, self.filename)
        self.e1.configure(text='')

    def button_event(self):
        print("Button pressed")

    def reset(self):
        self.e1 = None
        x = 0
        for i in self.winfo_children():
            if x > 2:
                i.destroy()
            x += 1

    @staticmethod
    def change_appearance_mode(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def encryption(self, key, file_path):

        # Encode given key to 16 byte ascii key with md5 operation
        key_hash = md5(key.encode('ascii')).digest()

        # Adjust key parity of generated Hash Key for Final Triple DES Key
        tdes_key = DES3.adjust_key_parity(key_hash)

        cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

        with open(file_path, 'rb') as input_file:
            file_bytes = input_file.read()
            new_file_bytes = cipher.encrypt(file_bytes)

        with open(file_path, 'wb') as output_file:
            output_file.write(new_file_bytes)
            # self.hawkeye_logo_small.destroy()
            # self.hawkeye_logo_small = customtkinter.CTkLabel()
            self.img = self.retimage('img_1.png')
            self.hawkeye_logo_small.configure(image=self.img)
            tkinter.messagebox.showinfo("success", 'Encryption success')

    def decryption(self, key, file_path):
        key_hash = md5(key.encode('ascii')).digest()
        tdes_key = DES3.adjust_key_parity(key_hash)
        cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')
        with open(file_path, 'rb') as input_file:
            file_bytes = input_file.read()
            new_file_bytes = cipher.encrypt(file_bytes)
            with open(file_path, 'wb') as output_file:
                output_file.write(new_file_bytes)
                self.img = self.retimage(file_path)
                self.hawkeye_logo_small.configure(image=self.img)
                tkinter.messagebox.showinfo("success", 'Decryption success')


if __name__ == "__main__":
    app = App()
    app.mainloop()
