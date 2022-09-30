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
        self.root.title("Server GUI")  # changing the title of the window

        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.pack(fill=BOTH, expand=1)  # allowing the widget to take the full space of the root window

        ttk.Button(self.frm, text="Quit", command=self.root.destroy).place(x=300, y=350)    # Quit Button
        self.btn = ttk.Button(self.frm, text="Start Server", command=self.start_server)     # Custom Button
        self.btn.place(x=10, y=350)
        self.root.mainloop()
        self.server = None

    def start_server(self):
        self.btn.config(state="disable")
        self.server = Receiver(12000, socket(AF_INET, SOCK_DGRAM))  # create instance of Receiver class
        self.server.start()                                         # Start server & listening for incoming data
        ttk.Label(self.frm, text="Incoming image received!!!").place(x=105, y=10)
        self.btn.config(text="Show Image", command=self.show_image, state="enable")

    def show_image(self):
        self.server.make_file(self.path)            # rebuild & save the image

        # Display saved image
        with Image.open(self.path) as img:
            img = img.resize((img.size[0] // 2, img.size[1] // 2))
            img_tk = ImageTk.PhotoImage(img)
            panel = Label(self.root, image=img_tk)
            panel.image = img_tk
            panel.place(x=(400 - img.size[0]) // 2, y=80)


ClientGui()
