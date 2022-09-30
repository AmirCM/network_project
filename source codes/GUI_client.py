from socket import *
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from Sender_Phase2 import Sender


class ClientGui:
    def __init__(self):
        self.path = ''
        self.root = Tk()
        self.root.geometry("400x400")  # size of the window
        self.root.title("Client GUI")  # changing the title of the window

        self.frm = ttk.Frame(self.root, padding=10)  # create a Frame
        self.frm.pack(fill=BOTH, expand=1)  # allowing the Frame to take the full space of the root window

        ttk.Button(self.frm, text="Quit", command=self.root.destroy).place(x=300, y=350)  # Quit Button
        self.btn = ttk.Button(self.frm, text="Select Image", command=self.show_image)  # Custom Button
        self.btn.place(x=10, y=350)
        self.root.mainloop()

    def show_image(self):
        self.path = filedialog.askopenfilename(title='Choose "./imgs/select me.bmp"')   # Dialog box to select image
        img = Image.open(self.path)                                                     # Open using PIL Image
        img = img.resize((img.size[0] // 2, img.size[1] // 2))                          # resize the image to fit
        img_tk = ImageTk.PhotoImage(img)            # PhotoImage class is used to add image to widgets

        panel = Label(self.root, image=img_tk)
        panel.image = img_tk
        panel.place(x=(400 - img.size[0]) // 2, y=80)
        self.btn.config(text="Send Image", command=self.send_image)
        pass

    def send_image(self):
        with socket(AF_INET, SOCK_DGRAM) as client_socket:
            s = Sender(12000, gethostname(), client_socket, [])     # create instance of Sender class
            s.make_packet()                                         # call function to parse bmp file into packets
            for packet in s.packets:  # loop through packet array and individually send to receiver
                s.sockets.sendto(packet, (s.destination, s.port))   # send each packet
        ttk.Label(self.frm, text="Image sent!!!").place(x=150, y=10)


ClientGui()
