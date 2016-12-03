
import tkinter as tk
from tkinter import ttk
import vlc
import sys


class MainFrame(tk.Frame):
    def __init__(self, parent, title=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.parent = parent

        self.autopilot = tk.Button(self)
        self.autopilot["text"] = "Autopilot"
        self.autopilot["command"] = self.init_autopilot
        self.autopilot.pack(side="top")

        self.training = tk.Button(self)
        self.training["text"] = "Training Mode"
        self.training["command"] = self.init_train
        self.training.pack(side="bottom")

        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)


    def init_autopilot(self):
        print("Commencing Autopilot mode.")


    def init_train(self):
        print("Training Mode.")
        def upKey(event):
            print ("Up key pressed")
        def downKey(event):
            print ("Down key pressed")
        def leftKey(event):
            print ("Left key pressed")
        def rightKey(event):
            print ("Right key pressed")
        root.bind('<Up>', upKey)
        root.bind('<Down>', downKey)
        root.bind('<Left>', leftKey)
        root.bind('<Right>', rightKey)





root = tk.Tk()
app = MainFrame()


app.mainloop()
