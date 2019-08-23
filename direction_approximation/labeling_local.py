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
from collections import defaultdict

imagewidth = 4000
imageheight = 4000

def load_augmentation_samples(file, width, height, minx, miny):
    samples = open(file, 'r').readlines()
    if len(samples) == 0:
        return
    samples = [l.split(' ')[1] for l in samples]
    samples = [l.split(',') for l in samples]
    samples = [(float(l[0]) - minx, float(l[1]) - miny) for l in samples]
    samples = [(x[0] * width / 1000.0, x[1] * height / 1000.0) for x in samples]
    return samples

def on_init():

    lidar_folder = 'E:\\workspaces\\LIDAR_WORKSPACE\\lidar'
    augmentations_folder = 'E:\\workspaces\\LIDAR_WORKSPACE\\augmentation'
    files = [lidar_folder + '\\' + f for f in os.listdir(lidar_folder)]
    pattern = '[0-9]{3}[_]{1}[0-9]{2,3}'
    dataset_names = list(set([x.group(0) for x in [re.search(pattern, match, flags=0) for match in files] if x != None]))

    all_bmps = []
    all_samples = []
    for dataset_name in dataset_names:
        print("Loading " + dataset_name)
        filename = lidar_folder + '\\' + dataset_name + '.txt'
        bmp, minx, miny = common.load_points(filename, imagewidth, imageheight, True)
        samples = load_augmentation_samples(augmentations_folder + '\\' + dataset_name + 'augmentation_result.txt', imagewidth, imageheight, minx, miny)
        all_bmps.append(bmp)
        all_samples.append(samples)
    return dataset_names, all_bmps, all_samples

class mainWindow():

    def __init__(self):

        self.dataset_names, self.bmps, self.samples = on_init()
        self.index = -1
        self.current_chosen_points = []
        self.labelings = defaultdict(dict)
        self.currsampleidx = -1
        self.currsamples = []
        self.current_chosen_points = []
        self.selected_points = {}
        self.selected_points_by_dataset = {}
        self.init_tkinter()


    def init_tkinter(self):
        self.root = Tk()
        self.frame = Frame(self.root, width=imagewidth, height=imageheight)
        self.frame.pack()

        # next button
        self.button = Button(self.frame, text="NEXT", fg="red", command=self.on_next_button_click)
        self.button.pack()

        # next sample button
        self.next_sample_button = Button(self.frame, text="NEXT SAMPLE", fg="red", command=self.on_next_sample_button_click)
        self.next_sample_button.pack()

        # cancel button
        self.cancel_button = Button(self.frame, text="CANCEL", fg="red", command=self.on_cancel_button_click)
        self.cancel_button.pack()

        # save button
        self.save_button = Button(self.frame, text="SAVE", fg="red", command=self.on_save_button_click)
        self.save_button.pack()

        # CANVAS
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

    ####### callbacks #######
    def on_canvas_click(self, event):
        # append the next point, if the new pair is completed, draw a new line!
        print("clicked at " + str(event.x) + " " + str(event.y))
        self.current_chosen_points.append((event.x, event.y))
        if len(self.current_chosen_points) % 2 == 0:
            self.canvas.create_line(self.current_chosen_points[-1][0], self.current_chosen_points[-1][1], self.current_chosen_points[-2][0], self.current_chosen_points[-2][1], fill='blue')

    def on_next_button_click(self):

        print(self.selected_points)
        if self.index < len(self.dataset_names):

            self.selected_points_by_dataset[self.dataset_names[self.index]] = self.selected_points.copy()
            self.selected_points = {}

            self.index += 1

            if self.index < len(self.dataset_names):
                self.canvas.delete("all")
                self.render_image_on_canvas_by_index_and_set_new_samples(self.index)
        else:
            print("LABELING FINISHED")

    def on_next_sample_button_click(self):

        if (self.currsampleidx > -1):
            self.selected_points[self.currsampleidx] = self.current_chosen_points.copy()
            self.current_chosen_points = []

        self.currsampleidx += 1

        if (self.currsampleidx < len(self.currsamples)):

            self.currsample = self.currsamples[self.currsampleidx]
            print('Currently working on sample: ', self.currsample)

            self.render_current_sample_and_image()


        else:
            print("Reached the final sample before!")

    def on_cancel_button_click(self):
        self.current_chosen_points = []
        self.render_current_sample_and_image()

    def on_save_button_click(self):
        pass

    ###### auxiliary #####
    def render_image_on_canvas_by_index_and_set_new_samples(self, index):
        self.render_image_on_canvas(255 * self.bmps[self.index])
        self.currsamples = self.samples[self.index]
        print('Current augmentables: ', self.currsamples)
        self.currsampleidx = -1

    def reset_image_to_apriori_state(self, isbottom=False):
        self.canvas.delete("all")
        self.render_image_on_canvas(255 * self.bmps[self.index], isbottom)

    def render_current_sample_and_image(self):
        if (self.currsample[1] > imageheight / 2):
            self.reset_image_to_apriori_state(isbottom=True)
            try:
                xleft = max(0, self.currsample[0] - 100)
                yleft = max(0, self.currsample[1] - imageheight / 2 - 100)
                xright = self.currsample[0] + 100
                yright = self.currsample[1] - imageheight / 2 + 100
                print('Its transformation is: ', xleft, yleft, xright, yright)
                self.canvas.create_oval(xleft, yleft, xright, yright, fill='green')
            except:
                print("Out of bounds!")

        else:
            self.reset_image_to_apriori_state(isbottom=False)
            try:
                xleft = max(0, self.currsample[0] - 100)
                yleft = max(0, self.currsample[1] - 100)
                xright = self.currsample[0] + 100
                yright = self.currsample[1] + 100
                print('Its transformation is: ', xleft, yleft, xright, yright)
                self.canvas.create_oval(self.currsample[0] - 100, self.currsample[1] - 100,
                                        self.currsample[0] + 100,
                                        self.currsample[1] + 100, fill='green')
            except:
                print("Out of bounds!")

    def render_image_on_canvas(self, data, isbottom=False):
        if isbottom:
            data = data[:int(data.shape[0] / 2),:]
        else:
            data = data[int(data.shape[0] / 2):, :]
        self.im = Image.frombytes('L', (data.shape[1], data.shape[0]), data.astype('b').tostring())
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.currimage = data


mainWindow()