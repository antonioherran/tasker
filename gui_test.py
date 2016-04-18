#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import chron
import threading
from Tkinter import *

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)


class ChildCanvas(object):
    def __init__(self, parent):
        self.parent = parent
        self._mycanvas = ResizingCanvas(self.parent._mycanvas2,width=850, height=400, highlightthickness=0, bg="green")
        self._mycanvas.pack(fill=BOTH, expand=YES)
        #Diego-Removing max option form the window
        self.taskText()
        self.addTaskButton()

    def taskText(self):
        self.entry = Entry(self._mycanvas)
        self.entry.pack(side = LEFT, padx=15)

    def addTaskButton(self):
        self.addtaskbutton = Button(self._mycanvas, text = 'Add Task', command = self.addTask, anchor = W)
        self.addtaskbutton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.addtaskbutton.pack(side = LEFT)

    def addTask(self):
        t = ChildTask(self)
        self._mycanvas.addtag_all("all")

class ParentCanvas(object):
    def __init__(self, parent):
        self.parent = parent
        self._mycanvas = ResizingCanvas(self.parent._mycanvas2, width=850, height=400, highlightthickness=0, bg="blue")
        self._mycanvas.pack(fill=BOTH, expand=YES)
        self._mycanvas2 = ResizingCanvas(self.parent._mycanvas2,width=100, height=2, highlightthickness=0)
        self._mycanvas2.pack(fill=BOTH, expand=YES)
        #Diego-Removing max option form the window
        self.taskText()
        self.addTaskButton()

    def taskText(self):
        self.entry = Entry(self._mycanvas)
        self.entry.pack(side = LEFT)

    def addTaskButton(self):
        self.addtaskbutton = Button(self._mycanvas, text = 'Add Task', command = self.addTask, anchor = W)
        self.addtaskbutton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.addtaskbutton.pack(side = LEFT)

    def addTask(self):
        t = ChildCanvas(self)
        self._mycanvas.addtag_all("all")


class NewGui(object):
    def __init__(self, parent):
        self._root = Tk()
        self._root.title('Tasker')
        self._myframe = Frame(self._root)
        self._myframe.pack(fill=BOTH, expand=YES)
        self._mycanvas = ResizingCanvas(self._myframe,width=850, height=400, highlightthickness=0)
        self._mycanvas.pack(fill=BOTH, expand=YES)
        self._mycanvas2 = ResizingCanvas(self._myframe,width=100, height=20, highlightthickness=0)
        self._mycanvas2.pack(fill=BOTH, expand=YES)
        #Diego-Removing max option form the window
        self._root.resizable(0,0)
        button = Button(self._mycanvas, text = 'New task', command = self.createTask , anchor = W)
        button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        button.pack(side = LEFT)
        button = Button(self._mycanvas, text = 'Quit', command = self._myframe.quit, anchor = W)
        button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        button.pack(side = RIGHT)

    def createTask(self):
        t = ParentCanvas(self)
        self._mycanvas.addtag_all("all")

def main():
    g = NewGui(None)
    g._root.mainloop()

if __name__ == "__main__":
        main()
