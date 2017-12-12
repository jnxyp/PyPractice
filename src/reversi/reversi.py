import tkinter as tk
from tkinter import colorchooser
frame = tk.Tk()
frame.title('My First Frame')
frame.geometry('200x200')

text = tk.StringVar()
label = tk.Label(frame, textvariable = text, bg = colorchooser.askcolor()[1], width=15, height=2)
label.pack()


clicked = True

def on_hit():
    global clicked
    if clicked:
        clicked = False
        text.set('Hello, world!')
    else:
        clicked = True
        text.set('')


button = tk.Button(frame,text = 'click me!', command = on_hit)


button.pack()
frame.mainloop()