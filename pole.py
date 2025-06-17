import tkinter as tk
from PIL import Image, ImageTk
import plansza
from plansza import *
from pionek import PIONEK_X,PIONEK_Y


class Pole:
    def __init__(self, x, y, pole_x, pole_y):
        self.x = x
        self.y = y
        self.pole_x=pole_x
        self.pole_y=pole_y
        self.filename = "logo.png"
        self.wlasciwosc = None
        obraz = Image.open(self.filename).resize((self.pole_x, self.pole_y))
        self.photo = ImageTk.PhotoImage(obraz)
        self.tlo = None
        self.pionek=[]
        obraz= Image.open("pionek_zolty.png").resize((PIONEK_X, PIONEK_Y))
        self.pionek.append(ImageTk.PhotoImage(obraz))
        obraz = Image.open("pionek_zielony.png").resize((PIONEK_X, PIONEK_Y))
        self.pionek.append(ImageTk.PhotoImage(obraz))
        obraz = Image.open("pionek_czerwony.png").resize((PIONEK_X, PIONEK_Y))
        self.pionek.append(ImageTk.PhotoImage(obraz))
        obraz = Image.open("pionek_niebieski.png").resize((PIONEK_X, PIONEK_Y))
        self.pionek.append(ImageTk.PhotoImage(obraz))
