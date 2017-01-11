
import vlc
import sys
import tkinter as Tk
from tkinter import ttk

import numpy as np

import tflearn
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
from tflearn.layers.normalization import local_response_normalization
import h5py
from tflearn.data_utils import build_hdf5_image_dataset

import scipy
import socket

import string
import random
# import standard libraries
import os
import pathlib
from threading import Thread, Event
import time
import platform
import argparse

# Make sure the data is normalized
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()

network = input_data(shape=[None, 144, 144, 3],
                     data_preprocessing=img_prep)
network = fully_connected(network, 64, activation='relu')
network = fully_connected(network, 3, activation='softmax')
# Tell tflearn how we want to train the network
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

# Wrap the network in a model object
model = tflearn.DNN(network, tensorboard_verbose=3, checkpoint_path='carnet.tfl.ckpt')
model.load("carnet.tfl")
parser = argparse.ArgumentParser(description='Wireless controller of CarNet.')
parser.add_argument('camera', type=str, help='The IP address of the remote camera.')
parser.add_argument('car', type=str, help='The IP address of the car.')
args = parser.parse_args()

UDP_IP = args.car
UDP_PORT = 42069

def go_left():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(str.encode("left"), (UDP_IP, UDP_PORT))
def go_right():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(str.encode("right"), (UDP_IP, UDP_PORT))
def go_forward():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(str.encode("forward"), (UDP_IP, UDP_PORT))


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
        while 1:
            self.player.video_take_snapshot(0, "picture.png", 0, 0)
            img = scipy.misc.imread('picture.png')
            img = scipy.misc.imresize(img, [144,144])
            img = np.reshape(img, [-1, 144, 144, 3])
            prediction = model.predict(img.astype('float32'))


            max = 0.
            for i in range(len(prediction[0])):
                if prediction[0][i] > max:
                    max = prediction[0][i]
                    maxIndex = i
            print(maxIndex)
            if maxIndex == 0:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(str.encode("forward"), (UDP_IP, UDP_PORT))
            elif maxIndex == 1:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(str.encode("left"), (UDP_IP, UDP_PORT))
            elif maxIndex == 2:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(str.encode("right"), (UDP_IP, UDP_PORT))


    def init_train(self):

        print("Training Mode.")

        def upKey(event):
            print ("Up key pressed")
            self.player.video_take_snapshot(0, "data/forward/forward_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
 + ".png", 0, 0)
            go_forward()


        def leftKey(event):
            print ("Left key pressed")
            self.player.video_take_snapshot(0, "data/left/left_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
 + ".png", 0, 0)
            go_left()

        def rightKey(event):
            print ("Right key pressed")
            self.player.video_take_snapshot(0, "data/right/right_" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)) + ".png", 0, 0)
            go_right()

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
