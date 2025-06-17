from PIL import ImageTk,Image
import plansza
from pole import *
from tkinter import messagebox

class Nieobecnosc(Pole):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.filename = "nieobecnosc.png"
        obraz = Image.open(self.filename).resize((plansza.POLE_X, plansza.POLE_Y))
        self.photo = ImageTk.PhotoImage(
        Image.open(self.filename).resize((plansza.POLE_X, plansza.POLE_Y))
    )
    def akcja(self, gracz):
        messagebox.showwarning("Brak obecności", "Nieobecność – brak punktów za to pole.")