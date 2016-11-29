
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.autopilot = tk.Button(self)
        self.autopilot["text"] = "Autopilot"
        self.autopilot["command"] = self.init_autopilot
        self.autopilot.pack(side="top")

        self.training = tk.Button(self)
        self.training["text"] = "Training Mode"
        self.training["command"] = self.init_train
        self.training.pack(side="bottom")


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
app = Application(master=root)


app.mainloop()
