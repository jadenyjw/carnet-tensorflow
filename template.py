#! /usr/bin/python
# -*- coding: utf-8 -*-

#
# tkinter example for VLC Python bindings
# Copyright (C) 2015 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#
"""A simple example for VLC python bindings using tkinter. Uses python 3.4

Author: Patrick Fay
Date: 23-09-2015
"""

# import external libraries
import vlc
import sys
import tkinter as Tk
from tkinter import ttk


# import standard libraries
import os
import pathlib
from threading import Thread, Event
import time
import platform

class ttkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters

class Player(Tk.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, parent, title=None):
        Tk.Frame.__init__(self, parent)

        self.parent = parent

        if title == None:
            title = "tk_vlc"
        self.parent.title(title)

        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

        # below is a test, now use the File->Open file menu
        media = self.Instance.media_new('rtsp://192.168.0.199:5554/playlist.m3u')
        self.player.set_media(media)
        self.player.play() # hit the player button
        #self.player.video_set_deinterlace(str.encode('yadif'))


        self.parent.update()
        self.player.set_xwindow(self.GetHandle())
        while 1:
            time.sleep(1)
            print (self.player.video_take_snapshot(0, "hello.jpg", 0, 0))
            print("Screenshotted")

        #self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this
    def GetHandle(self):
        return self.videopanel.winfo_id()




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

    player = Player(root, title="tkinter vlc")
    # show the player window centred and run the application
    root.mainloop()
