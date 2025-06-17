from PIL import Image, ImageTk
import tkinter as tk

PIONEK_X = 25
PIONEK_Y = 40
LICZBA_POL=38
pos=[[12,0],[36,0],[0,16],[24,16]]

class Pionek:
    kolor=0

    def __init__(self, kolor):
        self.kolor = kolor
        self.numerPola=0
        self.img_id = None

    def wybierzKolor(self,kolorPionka):
        self.kolor=kolorPionka

    def ruch(self, liczbaPol):
        poprzednie_pole = self.numerPola
        if self.numerPola + liczbaPol >= LICZBA_POL:
            self.numerPola = self.numerPola + liczbaPol - LICZBA_POL
        else:
            self.numerPola = self.numerPola + liczbaPol
        return poprzednie_pole

    def wyswietlPionek(self, plansza, slot_na_polu=0, pole=None):
        if pole is None:
            pole = self.numerPola

        # Usuń poprzedni obraz pionka
        if self.img_id:
            for p in plansza.pola:
                p.tlo.delete(self.img_id)
            self.img_id = None

        # Bezpieczne rysowanie na właściwej pozycji
        if 0 <= slot_na_polu < len(pos):
            self.img_id = plansza.pola[pole].tlo.create_image(
                12 + pos[slot_na_polu][0],
                18 + pos[slot_na_polu][1],
                image=plansza.pola[pole].pionek[self.kolor]
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
            self.img_id = plansza.pola[self.numerPola].tlo.create_image(
                12 + pos[ktoryPionek][0],
                18 + pos[ktoryPionek][1],
                image=plansza.pola[self.numerPola].pionek[self.kolor]
            )

            plansza.okno.after(300, wykonaj_krok)

        wykonaj_krok()




