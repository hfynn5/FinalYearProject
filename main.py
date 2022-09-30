# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from graphics import *
import tkinter

win = GraphWin('test',200,400)

def helloCallBack():
   tkinter.messageBox.showinfo( "Hello Python", "Hello World")

B = tkinter.Button(win, text ="Hello", command = helloCallBack)

B.place(x = 20, y = 20)

win.getMouse()
win.close()