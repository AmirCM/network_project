from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog


class SenderGui:
    def __init__(self):
        self.path = ''
        self.root = Tk()
        self.root.geometry("400x400")  # size of the window
        self.root.title("Sender GUI")  # changing the title of our master widget

        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.pack(fill=BOTH, expand=1)  # allowing the widget to take the full space of the root window
        ttk.Label(self.frm, text="Hello World!").place(x=150, y=10)
        ttk.Button(self.frm, text="Quit", command=self.root.destroy).place(x=300, y=350)
        self.btn = ttk.Button(self.frm, text="Show Image", command=self.show_image)
        self.btn.place(x=10, y=350)
        self.root.mainloop()

    def show_image(self):
        self.path = self.openfilename()
        img = Image.open(self.path)  # Select the Image name from a folder
        img = img.resize((img.size[0] // 2, img.size[1] // 2))  # resize the image

        img_tk = ImageTk.PhotoImage(img)  # PhotoImage class is used to add image to widgets, icons etc
        panel = Label(self.root, image=img_tk)
        panel.image = img_tk
        panel.place(x=(400 - img.size[0]) // 2, y=80)
        self.btn.config(text="Send Image", command=self.send_image)
        pass

    def send_image(self):
        return self.path

    def openfilename(self):
        # open file dialog box to select image
        # The dialogue box has a title "Open"
        filename = filedialog.askopenfilename(title='"pen')
        return filename


SenderGui()
