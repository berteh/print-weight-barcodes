#!/usr/bin/python3

"""
credit: 
- software : berteh, for co-labor, CC-BY-SA, https://github.com/berteh/print-weight-barcodes
- vegetables photo by <a href="https://unsplash.com/es/@nate_dumlao?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Nathan Dumlao</a> on <a href="https://unsplash.com/photos/bRdRUUtbxO0?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
- nuts photo by <a href="https://unsplash.com/@marcospradobr?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Marcos Paulo Prado</a> on <a href="https://unsplash.com/photos/GQTfzrGWzWU?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
"""

import os, tkinter as tk
import tkinter.font as tkFont
import PrintWeightLabels as pwl
from PIL import ImageTk, Image, ImageChops
from functools import partial

FULLSCREEN = True
DEBUG = False
BGCOLOR = "#010101"
HCOLOR = "#85a01f"
LOGO = 'logo.png'
LEFT = 'left2.jpg'
RIGHT = 'right2.jpg'
PRINT = 'Zebra.png'  #'ZD410_tsp.png'
PICSDIR = os.path.realpath(os.path.dirname(__file__))+"/pics/"


TXTS = {
    'FR' : {
        'print': "Imprimer mon\nétiquette",
        'instructions': """1. Placez votre récipient vide avec son couvercle sur la balance
2. Imprimez une étiquette qui contient son poids à vide
3. Collez cette étiquette sur le récipient à un endroit accessible
4. Remplissez votre récipient avec 1 type de produit en vrac, 
son poids sera déduit en caisse grâce au code-barre de l'étiquette""",
        'status': "statut : "        
    }, 
    'EN' : { 
        'print': "Print my label",
        'instructions': """1. Place your empty container with its lid on the scale
2. Print a label with its empty weight
3. Stick this label on the container in an accessible place
4. Fill your container with 1 type of bulk product, 
its weight will be deducted at the checkout thanks to the barcode on the label""",
        'status': ""
    },
    'DE' : {
        'print': "Mein Etikett drucken",
        'instructions': """1. Stellen Sie Ihren leeren Behälter mit Deckel auf die Waage.
2. Drucken Sie ein Etikett aus, das sein Leergewicht enthält.
3. Kleben Sie dieses Etikett an einer zugänglichen Stelle auf den Behälter.
4. Füllen Sie Ihren Behälter mit 1 Sorte Schüttgut, 
sein Gewicht wird an der Kasse anhand des Strichcodes auf dem Etikett abgezogen""",
        'status': ""
    },
    'LU' : {
        'print': "Imprimer",
        'instructions': "",
        'status': ""
    },
    'PT' : {
        'print': "Imprimir a\nminha etiqueta",
        'instructions': """1. Coloque o seu recipiente vazio com a sua tampa na balança
2. Imprimir uma etiqueta com o seu peso vazio
3. Colar este rótulo no recipiente num local acessível
4. Encha o seu recipiente com 1 tipo de produto a granel, 
o seu peso será deduzido no checkout graças ao código de barras no rótulo""",
        'status': ""
    }
}


def resize_image(image, maxsize) :
        # from https://stackoverflow.com/a/46885084
        #if DEBUG : print(f"resing picture to max sizes {maxsize}")
        r1 = image.size[0]/maxsize[0] # width ratio
        r2 = image.size[1]/maxsize[1] # height ratio
        ratio = max(r1, r2)
        newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio))
        image = image.resize(newsize, Image.ANTIALIAS)
        return image

def set_lang(lang) :
        if DEBUG : print(f"setting language to {lang}")
        _btn.set(TXTS[lang]['print'])
        _msg.set(TXTS[lang]['instructions'])
        _statut.set(TXTS[lang]['status'])


class App:

    def __init__(self, root) :
        
        #setting title
        root.title("kiosque pour les Tares")
        root['bg']=BGCOLOR
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight() 
        if DEBUG :  print(f"screen size: {width}x{height}")       
        root.geometry('%dx%d+%d+%d' % (width, height, 0 ,0))
        root.resizable(width=True, height=True)
        if FULLSCREEN : root.attributes('-fullscreen',True)  #not resizeable fullscreen, option for kiosk
                
        
        #decor
        self.leftI = ImageTk.PhotoImage(Image.open(PICSDIR+LEFT))
        leftP = tk.Label(root, image = self.leftI, bg=BGCOLOR)
        leftP.place(anchor="e", relx=0.25, rely=0.5, relheight=1.0)
        
        self.rightI = ImageTk.PhotoImage(Image.open(PICSDIR+RIGHT))
        rightP = tk.Label(root, image = self.rightI, bg=BGCOLOR)
        rightP.place(anchor="w", relx=0.75, rely=0.5, relheight=1.0)
  
        self.bottomI = ImageTk.PhotoImage(Image.open(PICSDIR+LOGO)) # ImageTk needs link from self to prevent early garbage collection
        bottomP = tk.Label(root, image = self.bottomI, bg=BGCOLOR)
        bottomP.place(anchor="s", relx=0.60, rely=0.98)
      
        
        #instructions
        ftL = tkFont.Font(family='Noto sans, sans-serif', size=17)
        ftS = tkFont.Font(family='Noto sans, sans-serif', size=11)

        msgM=tk.Message(root, textvariable=_msg, font=ftS, justify=tk.LEFT,
            fg="lightgrey", bg=BGCOLOR, aspect=400)
        msgM.place(anchor="n", relx=0.5, rely=0.05, width=width*0.5)
        

        #flags
        luO = Image.open(PICSDIR+"LU.png")
        luR = resize_image(luO, [width*0.05, height*0.05])
        self.luI = ImageTk.PhotoImage(luR)
        luB = tk.Button(root, text='LU', font = ftS, justify="center",
            image=self.luI,
            bg=BGCOLOR, activebackground=BGCOLOR,
            fg=HCOLOR, activeforeground=HCOLOR,
            borderwidth=0, relief=tk.FLAT, pady=3)
        luB["command"] = partial(set_lang, 'LU')
        luB.place(anchor="s", relx=0.20, rely=0.95, width=width*0.04)

        frO = Image.open(PICSDIR+"FR.png")
        frR = resize_image(frO, [width*0.05, height*0.05])
        self.frI = ImageTk.PhotoImage(frR)
        frB = tk.Button(root, text='FR', font = ftS, justify="center",
            image=self.frI,
            bg=BGCOLOR, activebackground=BGCOLOR,
            fg=HCOLOR, activeforeground=HCOLOR,
            borderwidth=0, relief=tk.FLAT, pady=3)
        frB["command"] = partial(set_lang, 'FR')
        frB.place(anchor="s", relx=0.25, rely=0.95, width=width*0.04)
            
        deO = Image.open(PICSDIR+"DE.png")
        deR = resize_image(deO, [width*0.05, height*0.05])
        self.deI = ImageTk.PhotoImage(deR)
        deB = tk.Button(root, text='DE', font = ftS, justify="center",
            image=self.deI,
            bg=BGCOLOR, activebackground=BGCOLOR,
            fg=HCOLOR, activeforeground=HCOLOR,
            borderwidth=0, relief=tk.FLAT, pady=3)
        deB["command"] = partial(set_lang, 'DE')
        deB.place(anchor="s", relx=0.30, rely=0.95, width=width*0.04)
     
        ptO = Image.open(PICSDIR+"PT.png")
        ptR = resize_image(ptO, [width*0.05, height*0.05])
        self.ptI = ImageTk.PhotoImage(ptR)
        ptB = tk.Button(root, text='PT', font = ftS, justify="center",
            image=self.ptI,
            bg=BGCOLOR, activebackground=BGCOLOR,
            fg=HCOLOR, activeforeground=HCOLOR,
            borderwidth=0, relief=tk.FLAT, pady=3)
        ptB["command"] = partial(set_lang, 'PT')
        ptB.place(anchor="s", relx=0.35, rely=0.95, width=width*0.04)

        enO = Image.open(PICSDIR+"EN.png")
        enR = resize_image(enO, [width*0.05, height*0.05])
        self.enI = ImageTk.PhotoImage(enR)
        enB = tk.Button(root, text='EN', font = ftS, justify="center",
            image=self.enI,
            bg=BGCOLOR, activebackground=BGCOLOR,
            fg=HCOLOR, activeforeground=HCOLOR,
            borderwidth=0, relief=tk.FLAT, pady=3)
        enB["command"] = partial(set_lang, 'EN')
        enB.place(anchor="s", relx=0.40, rely=0.95, width=width*0.04)


        #print button        
        printO = Image.open(PICSDIR+PRINT)
        printO = resize_image(printO, [width*0.3*0.7, height*0.4*0.7])
        self.printI = ImageTk.PhotoImage(printO)        
        printB=tk.Button(root, textvariable=_btn, font = ftL, justify="center",
            image=self.printI, compound=tk.BOTTOM,
            bg=BGCOLOR, activebackground=BGCOLOR,
            fg=HCOLOR, activeforeground=HCOLOR,
            borderwidth=7, relief=tk.RAISED, pady=10)
        printB.place(anchor="center", relx=0.5, rely=0.55, width=width*0.3)
        printB["command"] = self.printB_command



    def printB_command(self):
        print("printing")
        pwl.weight_and_print()




if __name__ == "__main__":

    #i18n
    root = tk.Tk()

    _btn = tk.StringVar()
    _msg = tk.StringVar()
    _statut = tk.StringVar()
    
    app = App(root)
    set_lang('FR')

    root.mainloop()
