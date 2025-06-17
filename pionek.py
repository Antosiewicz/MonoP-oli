from PIL import Image, ImageTk
import tkinter as tk
import pygame
import os

pygame.mixer.init()

def dzwiek_ruch():
    try:
        pygame.mixer.Sound('first_move.mp3').play()
    except Exception as e:
        print(f"Błąd dźwięku (first_move.mp3): {e}")

def dzwiek_koniec():
    try:
        pygame.mixer.Sound('last_move.mp3').play()
    except Exception as e:
        print(f"Błąd dźwięku (last_move.mp3): {e}")

PIONEK_X = 25
PIONEK_Y = 40
LICZBA_POL = 38
pos = [[12, 0], [36, 0], [0, 16], [24, 16]]

# Mapowanie numeru na nazwę koloru
KOLORY_NAZWY = ['zolty', 'zielony', 'czerwony', 'niebieski']
KSZTALTY_NAZWY = ['pionek', 'klodka', 'wifi', 'zebatka', 'monitor']

class Pionek:
    def __init__(self, kolor, ksztalt):
        self.kolor = kolor
        self.ksztalt = ksztalt
        self.numerPola = 0
        self.img_id = None
        self._img_cache = {}

    def wybierzKolor(self, kolorPionka):
        self.kolor = kolorPionka

    def wybierzKsztalt(self, ksztalt):
        self.ksztalt = ksztalt

    def ruch(self, liczbaPol):
        poprzednie_pole = self.numerPola
        if self.numerPola + liczbaPol >= LICZBA_POL:
            self.numerPola = self.numerPola + liczbaPol - LICZBA_POL
        else:
            self.numerPola = self.numerPola + liczbaPol
        return poprzednie_pole

    def get_image(self, canvas=None):
        key = (self.kolor, self.ksztalt)
        if key in self._img_cache:
            return self._img_cache[key]
        nazwa = KSZTALTY_NAZWY[self.ksztalt]          # np. 'klodka'
        kolor_nazwa = KOLORY_NAZWY[self.kolor]        # np. 'czerwony'
        path = f"{nazwa}_{kolor_nazwa}.png"           # np. 'klodka_czerwony.png'
        if not os.path.exists(path):
            img = Image.new('RGBA', (40, 40), (255, 0, 0, 0))
        else:
            img = Image.open(path).resize((40, 40))
        img_tk = ImageTk.PhotoImage(img)
        if canvas:
            canvas.image = img_tk
        self._img_cache[key] = img_tk
        return img_tk

    def wyswietlPionek(self, plansza, slot_na_polu=0, pole=None):
        if pole is None:
            pole = self.numerPola

        if self.img_id:
            for p in plansza.pola:
                p.tlo.delete(self.img_id)
            self.img_id = None

        if 0 <= slot_na_polu < len(pos):
            img = self.get_image(plansza.pola[pole].tlo)
            self.img_id = plansza.pola[pole].tlo.create_image(
                12 + pos[slot_na_polu][0],
                18 + pos[slot_na_polu][1],
                image=img
            )
        else:
            print(f"[Błąd] Nieprawidłowy slot_na_polu={slot_na_polu} — dostępne: 0–{len(pos)-1}")

    def animowany_ruch(self, plansza, ktoryPionek, liczbaPol, callback=None):
        kroki = []
        aktualne_pole = self.numerPola

        for i in range(1, liczbaPol + 1):
            pole = (aktualne_pole + i) % LICZBA_POL
            kroki.append(pole)

        def wykonaj_krok():
            if not kroki:
                if callback:
                    callback()
                return

            nastepne_pole = kroki.pop(0)

            if self.img_id:
                plansza.pola[self.numerPola].tlo.delete(self.img_id)

            self.numerPola = nastepne_pole
            img = self.get_image(plansza.pola[self.numerPola].tlo)
            self.img_id = plansza.pola[self.numerPola].tlo.create_image(
                12 + pos[ktoryPionek][0],
                18 + pos[ktoryPionek][1],
                image=img
            )

            if not kroki:
                dzwiek_koniec()
            else:
                dzwiek_ruch()

            plansza.okno.after(300, wykonaj_krok)

        wykonaj_krok()
