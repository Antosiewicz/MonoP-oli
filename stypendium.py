from PIL import Image, ImageTk
import plansza
from pole import *

class Stypendium(Pole):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.filename = "stypendium.png"
        obraz = Image.open(self.filename).resize((plansza.POLE_X, plansza.POLE_Y))
        self.photo = ImageTk.PhotoImage(obraz)

    
