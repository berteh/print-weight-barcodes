#!/usr/bin/python3

"""
credit: 
- vegetables photo by <a href="https://unsplash.com/es/@nate_dumlao?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Nathan Dumlao</a> on <a href="https://unsplash.com/photos/bRdRUUtbxO0?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
- nuts photo by <a href="https://unsplash.com/@marcospradobr?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Marcos Paulo Prado</a> on <a href="https://unsplash.com/photos/GQTfzrGWzWU?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

"""

import os, tkinter as tk
import tkinter.font as tkFont
import PrintWeightLabels as pwl
from PIL import ImageTk, Image

DEBUG = True
HEADER = 'fruits.jpg'
LOGO = 'logo.png'
LEFT = 'left.jpg'
RIGHT = 'right.jpg'
PICSDIR = os.path.realpath(os.path.dirname(__file__))+"/pics/"


class App:

    # Function to resize the images
    def resize_image(e):
       global image, resized, image2
       # open image to resize it
       image = Image.open("tutorialspoint.png")
       # resize the image with width and height of root
       resized = image.resize((e.width, e.height), Image.ANTIALIAS)

       image2 = ImageTk.PhotoImage(resized)
       canvas.create_image(0, 0, image=image2, anchor='nw')


    def __init__(self, root):
        
        #setting title
        root.title("kiosque de tares")
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()        
        root.geometry('%dx%d+%d+%d' % (width, height, 0 ,0))
        root.resizable(width=True, height=True)
        #root.attributes('-fullscreen',True)  #not resizeable fullscreen, option for kiosk ?
        root.columnconfigure(0, weight=3)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=2)
        root.columnconfigure(1, weight=3)
        root.rowconfigure(0, weight=2)
        root.rowconfigure(1, weight=2)
        root.rowconfigure(2, weight=2)
        root.rowconfigure(3, weight=2)
        root.rowconfigure(4, weight=2)
        root.rowconfigure(5, weight=2)
        root.rowconfigure(6, weight=1)
        root.rowconfigure(7, weight=2)
                
        self.bottomI = ImageTk.PhotoImage(Image.open(PICSDIR+LOGO)) # needs link from self to prevent early garbage collection
        bottomP = tk.Label(root, image = self.bottomI)
        bottomP.grid(row=7, column=2, columnspan=2)
        
        leftO = Image.open(PICSDIR+LEFT)
        leftR = leftO.resize((int(width/3), height), Image.ANTIALIAS)
        self.leftI = ImageTk.PhotoImage(leftR) # needs link from self to prevent early garbage collection
        leftP = tk.Label(root, image = self.leftI)
        leftP.grid(row=1, column=1, rowspan=7,
            sticky=tk.N+tk.S+tk.E+tk.W)
        
        rightO = Image.open(PICSDIR+RIGHT)
        rightR = rightO.resize((int(width/3), height), Image.ANTIALIAS)        
        self.rightI = ImageTk.PhotoImage(rightR) # needs link from self to prevent early garbage collection
        rightP = tk.Label(root, image = self.rightI)
        rightP.grid(row=1, column=4, rowspan=7,
            sticky=tk.N+tk.S+tk.E+tk.W)
        
        ft = tkFont.Font(family='Times',size=10)
        GButton_736=tk.Button(root, text="Tare",
            bg = "#e9e9ed", fg="#000000", justify="center", font = ft)
        GButton_736.grid(row=4, column=2, rowspan=2, columnspan=2,
            sticky=tk.N+tk.S+tk.E+tk.W)
        GButton_736["command"] = self.GButton_736_command

        
        GMessage_84=tk.Message(root, text = "Message FR",
            font=ft, fg="#333333", justify="center")        
        GMessage_84.grid(row=1, column=2, columnspan=2)
        """
        GMessage_631=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_631["font"] = ft
        GMessage_631["fg"] = "#333333"
        GMessage_631["justify"] = "center"
        GMessage_631["text"] = "Message DE"
        GMessage_631.place(x=240,y=30,width=133,height=82)

        GMessage_631=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_631["font"] = ft
        GMessage_631["fg"] = "#333333"
        GMessage_631["justify"] = "center"
        GMessage_631["text"] = "Message DE"
        GMessage_631.place(x=240,y=30,width=133,height=82)

        GLabel_516=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_516["font"] = ft
        GLabel_516["fg"] = "#333333"
        GLabel_516["justify"] = "center"
        GLabel_516["text"] = "label"
        GLabel_516.place(x=430,y=60,width=138,height=77)
        """

    

    def GButton_736_command(self):
        print("printing")
        pwl.weight_and_print()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
