import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame

pygame.mixer.init()

def odtworz_dzwiek():
    try:
        pygame.mixer.Sound('rolling_dice.mp3').play()
    except Exception as e:
        print(f"Błąd dźwięku: {e}")

def zaladuj_grafiki_kostek():
    return [ImageTk.PhotoImage(Image.open(f"Kostka_{i}.png").resize((100, 100))) for i in range(1, 7)]

def stworz_labelki_kostek(okno, grafiki):
    label1 = tk.Label(okno, image=grafiki[0], bg="#e2dbd8")
    label2 = tk.Label(okno, image=grafiki[0], bg="#e2dbd8")
    screen_width = okno.winfo_screenwidth()
    screen_height = okno.winfo_screenheight()
    label1.place(x=screen_width/2-75-25, y=screen_height/3)
    label2.place(x=screen_width/2+25, y=screen_height/3)
    return label1, label2

def animuj_rzut_kostkami(okno, label1, label2, grafiki, callback_wyniku=None):
    rzut_wynik = {'kostka1': 0, 'kostka2': 0}

    def animuj(klatka=0):
        if klatka < 10:
            idx1 = random.randint(0, 5)
            idx2 = random.randint(0, 5)
            label1.configure(image=grafiki[idx1])
            label2.configure(image=grafiki[idx2])
            okno.after(100, lambda: animuj(klatka + 1))
        else:
            wynik1 = random.randint(1, 6)
            wynik2 = random.randint(1, 6)
            label1.configure(image=grafiki[wynik1 - 1])
            label2.configure(image=grafiki[wynik2 - 1])
            rzut_wynik['kostka1'] = wynik1
            rzut_wynik['kostka2'] = wynik2
            if callback_wyniku:
                callback_wyniku(wynik1, wynik2)
    animuj()

def dodaj_przycisk_rzutu(okno, label1, label2, grafiki, callback_wyniku=None):
    def przycisk_click():
        odtworz_dzwiek()
        animuj_rzut_kostkami(okno, label1, label2, grafiki, callback_wyniku)
    btn = tk.Button(
        okno, text="Rzuć kostkami", font=("Inter", 20), bg="#750006", fg="white",
        command=przycisk_click

    )
    screen_width = okno.winfo_screenwidth()
    screen_height = okno.winfo_screenheight()
    btn.place(x=screen_width/2-85, y=screen_height/3+125)
