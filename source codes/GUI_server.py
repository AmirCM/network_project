from socket import *
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from Receiver_Phase2 import Receiver


class ClientGui:
    def __init__(self):
        self.path = '../imgs/received_image.bmp'
        self.root = Tk()
        self.root.geometry("400x400")  # size of the window
        self.root.title("Server GUI")  # changing the title of our master widget

        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.pack(fill=BOTH, expand=1)  # allowing the widget to take the full space of the root window

        ttk.Button(self.frm, text="Quit", command=self.root.destroy).place(x=300, y=350)
        self.btn = ttk.Button(self.frm, text="Start Server", command=self.start_server)
        self.btn.place(x=10, y=350)
        self.root.mainloop()
        self.server = None

    def start_server(self):
        self.btn.config(state="disable")
        self.server = Receiver(12000, socket(AF_INET, SOCK_DGRAM))  # opens bitmap file
        self.server.start()
        ttk.Label(self.frm, text="Incoming image received!!!").place(x=105, y=10)
        self.btn.config(text="Show Image", command=self.show_image, state="enable")

    def show_image(self):
        self.server.make_file(self.path)
        with Image.open(self.path) as img:
            img = img.resize((img.size[0] // 2, img.size[1] // 2))  # resize the image
            img_tk = ImageTk.PhotoImage(img)  # PhotoImage class is used to add image to widgets, icons etc
            panel = Label(self.root, image=img_tk)
            panel.image = img_tk
            panel.place(x=(400 - img.size[0]) // 2, y=80)


ClientGui()
