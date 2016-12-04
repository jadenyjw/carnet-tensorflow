
import vlc
import sys
import tkinter as Tk
from tkinter import ttk

import string
import random
# import standard libraries
import os
import pathlib
from threading import Thread, Event
import time
import platform
import argparse

parser = argparse.ArgumentParser(description='Wireless controller of CarNet.')
parser.add_argument('camera', type=str, help='The IP address of the remote camera.')
#parser.add_argument('car', type=str, help='The IP address of the car.')
args = parser.parse_args()



class Player(Tk.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, parent, title=None):
        Tk.Frame.__init__(self, parent)

        self.parent = parent

        if title == None:
            title = "Carnet"
        self.parent.title(title)

        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

        # below is a test, now use the File->Open file menu
        media = self.Instance.media_new('rtsp://' + args.camera + ':5554/playlist.m3u')
        self.player.set_media(media)
        self.player.play() # hit the player button
        self.player.video_set_deinterlace(str.encode('yadif'))

        ctrlpanel = ttk.Frame(self.parent)
        autopilot  = ttk.Button(ctrlpanel, text="Autopilot", command=self.init_autopilot)
        training   = ttk.Button(ctrlpanel, text="Training", command=self.init_train)

        autopilot.pack(side=Tk.LEFT)
        training.pack(side=Tk.LEFT)

        ctrlpanel.pack(side=Tk.BOTTOM)

        self.parent.update()
        self.player.set_xwindow(self.GetHandle())

    def GetHandle(self):
        return self.videopanel.winfo_id()

    def init_autopilot(self):
        print("Commencing Autopilot mode.")

    def init_train(self):

        print("Training Mode.")

        def upKey(event):
            print ("Up key pressed")
            self.player.video_take_snapshot(0, "data/up/up_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
 + ".png", 0, 0)


        def leftKey(event):
            print ("Left key pressed")
            self.player.video_take_snapshot(0, "data/left/left_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
 + ".png", 0, 0)

        def rightKey(event):
            print ("Right key pressed")
            self.player.video_take_snapshot(0, "data/right/right_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)) + ".png", 0, 0)


        root.bind('<Up>', upKey)
        root.bind('<Left>', leftKey)
        root.bind('<Right>', rightKey)

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"): #(1)
        Tk_get_root.root= Tk.Tk()  #initialization call is inside the function
    return Tk_get_root.root

def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)

if __name__ == "__main__":
    # Create a Tk.App(), which handles the windowing system event loop
    root = Tk_get_root()
    root.protocol("WM_DELETE_WINDOW", _quit)

    player = Player(root, title="CarNet")

    #buttons = Tk.Frame(root)
    # show the player window centred and run the application
    root.mainloop()
