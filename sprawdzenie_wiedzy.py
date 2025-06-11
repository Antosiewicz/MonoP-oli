from PIL import ImageTk
from pole import *


class SprawdzenieWiedzy(Pole):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.filename = "sprawdzenie_wiedzy.png"
        obraz = Image.open(self.filename).resize((plansza.POLE_X, plansza.POLE_Y))
        self.photo = ImageTk.PhotoImage(obraz)
        self.pytanie = None