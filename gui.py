#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#import chronometer
import chron
import threading
from Tkinter import *



# a subclass of Canvas for dealing with resizing of windows
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
        self._mycanvas = ResizingCanvas(self.parent._mycanvas2,width=850, height=400, highlightthickness=0)
        self._mycanvas.pack(fill=BOTH, expand=YES)
        #Diego-Removing max option form the window
        self.labelText = StringVar()
        self.labelText.set('0:00:00')
        self.stopFlag = threading.Event()
        self.c = chron.Chronometer(self.stopFlag)
        self.c.start()
        self.stopFlag.set()
        self.Draw()
        #Diego-Adding two variables, so Far is a temp container or the sum of elapsed
        self.soFar = 0
        self.grandTotal = 0
        self.startFlag = False

    def Draw(self):
        self.startButton()
        self.chronLabel()
        self.taskText()
        self.deleteButton()

    def startButton(self):
        self.button = Button(self._mycanvas, text = 'Start', command = self.startStop, anchor = W)
        self.button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.button.pack(side = LEFT, padx=20)

    def chronLabel(self):
        self.label = Label(self._mycanvas, textvariable=self.labelText, fg = 'black')
        self.label.pack(side = LEFT)

    def taskText(self):
        self.entry = Entry(self._mycanvas)
        self.entry.pack(side = LEFT)

    def deleteButton(self):
        self.delbutton = Button(self._mycanvas, text = 'Delete', command = self.delete, anchor = W)
        self.delbutton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.delbutton.pack(side = LEFT)

    def addTaskButton(self):
        self.addtaskbutton = Button(self._mycanvas, text = 'Add Task', command = self.addTask, anchor = W)
        self.addtaskbutton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.addtaskbutton.pack(side = LEFT)

    def startStop(self):
        if self.startFlag == False:
            self.stopFlag.clear()
            self.tick()
            self.startFlag = True
            self.button["text"] = 'Stop'
        else:
            self.stopFlag.set()
            self.startFlag = False
            self.button["text"] = 'Start'

    def tick(self):
        m, s = divmod(self.c.time, 60)
        h, m = divmod(m, 60)
        timeLabel = "%d:%02d:%02d" % (h, m, s)
        self.labelText.set(timeLabel)
        self._mycanvas.after(1000, self.tick)

    def delete(self):
        self.button.destroy()
        self.label.destroy()
        self._mycanvas.destroy()
        del self


class ParentCanvas(object):
    def __init__(self, parent):
        self.parent = parent
        self._tasklist = []
        self._mycanvas = ResizingCanvas(self.parent._mycanvas2, width=850, height=400, highlightthickness=0)
        self._mycanvas.pack(fill=BOTH, expand=YES)
        self._mycanvas2 = ResizingCanvas(self.parent._mycanvas2,width=100, height=2, highlightthickness=0)
        self._mycanvas2.pack(fill=BOTH, expand=YES)
        self.labelText = StringVar()
        self.labelText.set('0:00:00')
        self.stopFlag = threading.Event()
        self.c = chron.Chronometer(self.stopFlag)
        self.c.start()
        self.stopFlag.set()
        self.Draw()
        self.tick()
        self.startFlag = False

    def Draw(self):
        self.addTaskButton()
        self.chronLabel()
        self.taskText()
        self.stopAllButton()

    def stopAllButton(self):
        self.button = Button(self._mycanvas, text = 'Pause all', command = self.stopAll, anchor = W)
        self.button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.button.pack(side = LEFT)

    def stopAll(self):
        for i in self._tasklist:
            if i.startFlag:
                i.startStop()
            i.stopFlag.set()

    def chronLabel(self):
        self.label = Label(self._mycanvas, textvariable=self.labelText, fg = 'black')
        self.label.pack(side = LEFT)

    def taskText(self):
        self.entry = Entry(self._mycanvas)
        self.entry.pack(side = LEFT)

    def deleteButton(self):
        self.delbutton = Button(self._mycanvas, text = 'Delete', command = self.delete, anchor = W)
        self.delbutton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.delbutton.pack(side = LEFT)

    def addTaskButton(self):
        self.addtaskbutton = Button(self._mycanvas, text = 'Add Task', command = self.addTask, anchor = W)
        self.addtaskbutton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.addtaskbutton.pack(side = LEFT)

    def addTask(self):
        t = ChildCanvas(self)
        self._tasklist.append(t)
        self._mycanvas.addtag_all("all")

    def tick(self):
        self.total = 0
        for i in self._tasklist:
            self.total += i.c.time
        m, s = divmod(self.total, 60)
        h, m = divmod(m, 60)
        timeLabel = "%d:%02d:%02d" % (h, m, s)
        self.labelText.set(timeLabel)
        self._mycanvas2.after(1000, self.tick)

    def delete(self):
        self.button.destroy()
        self.label.destroy()
        self._mycanvas.destroy()
        del self

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
