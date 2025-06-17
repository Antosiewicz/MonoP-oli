from pionek import Pionek
import json
import random
from pionek import Pionek

class Student:
    def __init__(self, login, kolor, ksztalt):
        self.login = login
        self.ects = 0
        self.kolor = kolor
        self.ksztalt = ksztalt
        self.pionek = Pionek(kolor, ksztalt)
        self.ects = 0
        self.login = login
        self.sesja_counter = 0
        self.pionek = Pionek(kolor, ksztalt)
        # self.pionek.wybierzKolor(awatar)
        with open("baza_pytan.json", "r", encoding="utf-8") as f:
            wszystkie = json.load(f)

        self.pytania_wiedza = [p for p in wszystkie if p["type"] == "Sprawdzenie wiedzy"]
        self.pytania_sesja = [p for p in wszystkie if p["type"] == "Sesja egzaminacyjna"]

        random.shuffle(self.pytania_wiedza)
        random.shuffle(self.pytania_sesja)