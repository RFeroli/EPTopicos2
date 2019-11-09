from tkinter import *
from tkinter.ttk import *
import threading
import time;
import re
from main.graficos import  ColorUtils


ALTURA=500
LARGURA=500

class Grafico:
    def __init__(self,estados,h,w,estimativa):
        this=self
        self.estimativa=estimativa
        def initialization():
            this.raiz = Tk ()
            this.raiz.geometry (str(ALTURA)+"x"+str(LARGURA))
           # this.raiz.minsize(self.raiz.winfo_screenwidth (), self.raiz.winfo_screenheight ())
            this.canvas = Canvas (self.raiz, bg=ColorUtils.toHex(255,255,255))
            this.canvas.initAresta=False
            this.canvas.pack(fill=BOTH,expand=1)


           # this.raiz.withdraw()
            this.raiz.mainloop()

        threading.Thread (target=initialization).start()
        time.sleep(0.1)

        altura=(ALTURA/h)-2
        largura=(LARGURA/w)-2
        self.grid={}
        for estado in estimativa:
            i =int(re.search ('x(.*)y', estado).group(1))-1
            j = int(re.search ('y(.*)', estado).group (1))-1
            self.grid[estado]=self.canvas.create_rectangle (i*(altura+2), j*(largura+2),(i*(altura+2))+altura ,(j*(largura+2))+largura, fill="blue", outline='black')

    def atualizar(self):
        for estado in self.estimativa:
            self.canvas.itemconfig (self.grid[estado], fill=ColorUtils.toHex(int(self.estimativa[estado]*5),0,0))
