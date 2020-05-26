from PIL import Image
from PIL import ImageTk
import tkinter as Tkinter
from tkinter import filedialog
from tkinter import tkMessageBox
import cv2
import os
import pickle

with open(filedialog.askopenfilename(initialdir = os.path.join(os.getcwd(), 'sessions'),title = "Select sessions file"), "rb") as fp: # Unpickling and appending to Known Lists
    sessionData = pickle.load(fp)

fheight, fwidth = sessionData[0]["frame"].shape[:2]


current = 0

def move(delta):
    global sessionData, current, img
    if not (0 <= current + delta < len(sessionData)):
        tkMessageBox.showinfo('End', 'No more image.')
        return
    current += delta
    image = Image.fromarray(cv2.cvtColor(sessionData[current]["frame"], cv2.COLOR_BGR2RGB))
    img = ImageTk.PhotoImage(image)
    label['text'] = sessionData[current]["datetime"]
    # label['image'] = img
    # label.photo = img


root = Tkinter.Tk()

label = Tkinter.Label(root, compound=Tkinter.TOP)
label.pack()

frame = Tkinter.Frame(root)
frame.pack()




canvas = Tkinter.Canvas(root, width = fwidth, height = fheight)      
canvas.pack() 




img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(sessionData[current]["frame"], cv2.COLOR_BGR2RGB))) 




Tkinter.Button(frame, text='Previous picture', command=lambda: move(-1)).pack(side=Tkinter.LEFT)
Tkinter.Button(frame, text='Next picture', command=lambda: move(+1)).pack(side=Tkinter.LEFT)
Tkinter.Button(frame, text='Quit', command=root.quit).pack(side=Tkinter.LEFT)

move(0)



canvas.create_image(20, 20, anchor="nw", image=img) 



root.mainloop()