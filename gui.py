#!/usr/bin/python3

import tkinter as tk
import tkinter.font as tkFont
import PrintWeightLabels as pwl

class App:
    def __init__(self, root):
        #setting title
        root.title("kiosque de tares")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)
        #root.attributes('-fullscreen',True)  #not resizeable fullscreen, option for kiosk ?

        GButton_736=tk.Button(root)
        GButton_736["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_736["font"] = ft
        GButton_736["fg"] = "#000000"
        GButton_736["justify"] = "center"
        GButton_736["text"] = "Button"
        GButton_736.place(x=150,y=180,width=300,height=300)
        GButton_736["command"] = self.GButton_736_command

        GMessage_84=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_84["font"] = ft
        GMessage_84["fg"] = "#333333"
        GMessage_84["justify"] = "center"
        GMessage_84["text"] = "Message"
        GMessage_84.place(x=40,y=40,width=130,height=68)

        GMessage_631=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_631["font"] = ft
        GMessage_631["fg"] = "#333333"
        GMessage_631["justify"] = "center"
        GMessage_631["text"] = "Message"
        GMessage_631.place(x=240,y=30,width=133,height=82)

        GLabel_516=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_516["font"] = ft
        GLabel_516["fg"] = "#333333"
        GLabel_516["justify"] = "center"
        GLabel_516["text"] = "label"
        GLabel_516.place(x=430,y=60,width=138,height=77)

    def GButton_736_command(self):
        print("printing")
        pwl.weight_and_print()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
