import numpy as np
from PIL import Image
import pickle
import os.path
import math
import random
import re
import common
import random_points
from tkinter import *
from PIL import Image, ImageTk


imagewidth = 4000
imageheight = 4000



    # load all lidar txt files
    # foreach lidar txt file:
        # translate to bmp
        # pick K points
        # for each point:

            # render bmp
            # first determine general direction for whole bmp
            # render point
            # user clicks 2 points that define the line of direction
            # user clicks on some control that indicates that the labeling is over OR
            # determines another direction in the same way

        # save everything

def on_init():

    lidar_folder = 'E:\workspaces\LIDAR_WORKSPACE\lidar'
    files = [lidar_folder + '\\' + f for f in os.listdir(lidar_folder)]
    pattern = '[0-9]{3}[_]{1}[0-9]{2,3}'
    dataset_names = set([x.group(0) for x in [re.search(pattern, match, flags=0) for match in files] if x != None])

    all_bmps = []
    all_samples = []
    for dataset_name in dataset_names:
        print("Loading " + dataset_name)
        filename = lidar_folder + '\\' + dataset_name + '.txt'
        bmp = common.load_points(filename, imagewidth, imageheight, True)
        #samples = random_points.generate_samples(imagewidth, 30, 200)
        samples = [] #samples[15, :]
        all_bmps.append(bmp)
        all_samples.append(samples)
    return all_bmps, all_samples

class mainWindow():

    def __init__(self):

        self.bmps, self.samples = on_init()
        self.index = -1
        self.init_tkinter()

    def init_tkinter(self):
        self.root = Tk()
        self.frame = Frame(self.root, width=imagewidth, height=imageheight)
        self.frame.pack()

        self.button = Button(self.frame, text="NEXT", fg="red", command=self.on_next_button_click)
        self.button.pack()

        self.canvas = Canvas(self.frame, width=imagewidth, height=imageheight, scrollregion=(0,0, imagewidth, imageheight))
        hbar = Scrollbar(self.frame, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.canvas.xview)
        vbar = Scrollbar(self.frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=imagewidth, height=imageheight)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.canvas.place(x=-2, y=-2)

        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        



        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.root.update()
        self.root.mainloop()

    def render_image_on_canvas(self, data):
        self.im = Image.frombytes('L', (data.shape[1], data.shape[0]), data.astype('b').tostring())
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

    def on_canvas_click(self, event):
        print("clicked at " + str(event.x) + " " + str(event.y))

    def on_next_button_click(self):

        self.index += 1
        if len(self.bmps) >= self.index:
            self.render_image_on_canvas(255 * self.bmps[self.index])
        else:
            print("LABELING FINISHED")

mainWindow()