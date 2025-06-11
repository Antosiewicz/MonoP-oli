from PIL import ImageTk
from pole import *


class SesjaEgzaminacyjna(Pole):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.filename = "sesja_egzaminacyjna.png"
        obraz = Image.open(self.filename).resize((plansza.POLE_X, plansza.POLE_Y))
        self.photo = ImageTk.PhotoImage(obraz)
        self.pytanie = None