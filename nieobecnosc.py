from PIL import ImageTk,Image
import plansza
from pole import *
from tkinter import messagebox

class Nieobecnosc(Pole):
    def __init__(self, x, y, pole_x, pole_y):
        super().__init__(x, y, pole_x, pole_y)
        self.filename = "nieobecnosc.png"
        obraz = Image.open(self.filename).resize((self.pole_x, self.pole_y))
        self.photo = ImageTk.PhotoImage(
            Image.open(self.filename).resize((self.pole_x, self.pole_y))
    )
    def akcja(self, gracz):
        messagebox.showwarning("Brak obecności", "Nieobecność – brak punktów za to pole.")