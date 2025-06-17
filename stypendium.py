from PIL import Image, ImageTk
import plansza
from pole import *

class Stypendium(Pole):
    def __init__(self, x, y, pole_x, pole_y):
        super().__init__(x, y, pole_x, pole_y)
        self.filename = "stypendium.png"
        obraz = Image.open(self.filename).resize((self.pole_x, self.pole_y))
        self.photo = ImageTk.PhotoImage(obraz)

    
