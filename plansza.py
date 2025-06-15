import tkinter as tk
from PIL import Image, ImageTk

import nieobecnosc
import pole
import stypendium
import sprawdzenie_wiedzy
import sesja_egzaminacyjna

# Wartości domyślne, mogą być nadpisane z zewnątrz
POLE_X = 77   # szerokość pola (zmienione na 110% wysokości pola)
POLE_Y = 70   # wysokość pola

class Plansza:

    def __init__(self, okno, length, width, margin_top, margin_left, pole_x, pole_y):
        self.length = length
        self.width = width
        self.margin_top = margin_top
        self.margin_left = margin_left
        self.pole_x = pole_x
        self.pole_y = pole_y

        # Tworzenie list pól dookoła planszy (dół, lewo, góra, prawo)
        pola_gora = [pole.Pole(pole_x * (i + 1) + margin_left, margin_top) for i in range(0, width)]
        pola_dol = [pole.Pole(pole_x * (i + 1) + margin_left, (length-1)*pole_y+margin_top) for i in range(0, width)]
        pola_dol.reverse()
        pola_lewo = [pole.Pole(margin_left, pole_y * i + margin_top) for i in range(0, length)]
        pola_lewo.reverse()
        pola_prawo = [pole.Pole(pole_x * (width+1) + margin_left, pole_y * i + margin_top) for i in range(0, length)]

        self.pola = pola_dol + pola_lewo + pola_gora + pola_prawo
        self.pola.insert(0,self.pola[len(self.pola)-1])
        self.pola.pop()
        self.okno = okno

    def Rysuj(self):
        for p in self.pola:
            p.tlo = tk.Canvas(self.okno, width=self.pole_x, height=self.pole_y, bg="#e2dbd8", highlightthickness=0, bd=0)
            p.tlo.place(x=p.x, y=p.y)
            p.tlo.create_image(self.pole_x/2+2, self.pole_y/2+1, image=p.photo)

    def WypelnijDomyslnie(self):
        for i in range(0, len(self.pola)):
            self.pola[i] = sprawdzenie_wiedzy.SprawdzenieWiedzy(self.pola[i].x, self.pola[i].y)
        for i in [self.width, self.length+self.width-1, self.length*2 + self.width - 3, len(self.pola)-1]:
            self.pola[i] = stypendium.Stypendium(self.pola[i].x, self.pola[i].y)
        for i in [2, 6, 10, 16, 20, 24, 29, 35]:
            self.pola[i] = nieobecnosc.Nieobecnosc(self.pola[i].x, self.pola[i].y)
        for i in [4, 13, 22, 32]:
            self.pola[i] = sesja_egzaminacyjna.SesjaEgzaminacyjna(self.pola[i].x, self.pola[i].y)
