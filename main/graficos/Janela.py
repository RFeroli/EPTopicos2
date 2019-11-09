from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import threading
import time;
import re
from main.graficos import  ColorUtils


ALTURA=500
LARGURA=500

class Grafico:
    def __init__(self,estados,h,w,estimativa,politica):
        this=self
        self.estimativa=estimativa
        self.politica=politica
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
        self.arrows={}
        for estado in estimativa:
            i =int(re.search ('x(.*)y', estado).group(1))-1
            j = int(re.search ('y(.*)', estado).group (1))
            j=(h-j)
            self.grid[estado]=self.canvas.create_rectangle (i*(altura+2), j*(largura+2),(i*(altura+2))+altura ,(j*(largura+2))+largura, fill="blue", outline='black')
            x1=(i*(altura+2)+(i*(altura+2))+altura)/2
            x2=x1;
            y1=j*(largura+2)
            y2=(j*(largura+2))+largura

            self.arrows[estado]=self.canvas.create_line (x1,y1,x2,y2, width=2, tags="tudo",arrow=tk.LAST,fill='blue')
    def atualizar(self):
        for estado in self.estimativa:
            self.canvas.itemconfig (self.grid[estado], fill=ColorUtils.toHex(int(self.estimativa[estado]*5),0,0))
            self.atualiza_seta(estado,self.politica[estado])

    def seta_cima(self,celula,seta):
        cordenadas=self.canvas.coords(celula)
        x1=(cordenadas[0]+cordenadas[2])/2
        x2=x1;
        y1=cordenadas[3]
        y2=cordenadas[1]
        self.canvas.coords(seta,x1,y1,x2,y2)

    def seta_baixo(self,celula,seta):
        cordenadas=self.canvas.coords(celula)
        x1=(cordenadas[0]+cordenadas[2])/2
        x2=x1;
        y1=cordenadas[1]
        y2=cordenadas[3]
        self.canvas.coords(seta,x1,y1,x2,y2)


    def seta_direita(self,celula,seta):
        cordenadas=self.canvas.coords(celula)
        x1=cordenadas[0]
        x2=cordenadas[2]
        y1=(cordenadas[1]+cordenadas[3])/2
        y2=y1
        self.canvas.coords(seta,x1,y1,x2,y2)

    def seta_esquerda(self,celula,seta):
        cordenadas=self.canvas.coords(celula)
        x1=cordenadas[2]
        x2=cordenadas[0]
        y1=(cordenadas[1]+cordenadas[3])/2
        y2=y1
        self.canvas.coords(seta,x1,y1,x2,y2)

    def atualiza_seta(self,estado,acao):
        if(acao=='move-south'):
            self.seta_baixo(self.grid[estado],self.arrows[estado])
        if (acao == 'move-north'):
            self.seta_cima (self.grid[estado], self.arrows[estado])
        if (acao == 'move-west'):
            self.seta_esquerda (self.grid[estado], self.arrows[estado])
        if (acao == 'move-east'):
            self.seta_direita (self.grid[estado], self.arrows[estado])



