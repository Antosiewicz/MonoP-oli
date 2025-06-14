from PIL import Image, ImageTk
import tkinter as tk
import menu
import json
from nieobecnosc import *
from plansza import *
from student import Student
from kostki import zaladuj_grafiki_kostek, stworz_labelki_kostek, dodaj_przycisk_rzutu
import question_popup 
import threading
import time
import os
from tkinter import messagebox
from question_popup import aktualizuj_ects
def zakoncz_gre(okno, gracz):
    tk.messagebox.showinfo("Koniec gry", f"Koniec pytań!\nZdobyte ECTS: {gracz.ects}")
    okno.destroy()  
def powrot_przycisk(okno):
    okno.destroy()
    menu.main()

def uruchom_okno_student(login):
    okno = tk.Tk()
    gracz = Student(login, 0)
    okno.title("Okno Studenta")

    # Dynamiczne ustawienie rozmiaru okna
    screen_width = okno.winfo_screenwidth()
    screen_height = okno.winfo_screenheight()
    okno.geometry(f"{screen_width}x{screen_height}")

    okno.configure(bg="#e2dbd8")
    def zarejestruj_gracza(login):
        try:
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
        except FileNotFoundError:
            dane = {"status": "oczekiwanie", "gracze": []}

        gracze = dane.get("gracze", [])
        if not any(g["login"] == login for g in gracze):
            gracze.append({"login": login, "ects": 0})
            dane["gracze"] = gracze
            with open("gra_status.json", "w", encoding="utf-8") as f:
                json.dump(dane, f, indent=2)

    zarejestruj_gracza(login)
    
    # Przygotowanie grafiki przycisku
    powrot_img = Image.open("powrot.png").resize((210, 70))
    powrot_photo = ImageTk.PhotoImage(powrot_img)
    powrot_button = tk.Button(okno, image=powrot_photo, command=lambda: powrot_przycisk(okno), borderwidth=0)
    powrot_button.image = powrot_photo
    powrot_button.place(x=50, y=30)

    # przygotowanie tla do wyswietlania liczby punktow ECTS
    ectsy_tlo = tk.Canvas(okno, width=210, height=70, bg="#750006")
    ectsy_tlo.place(x=50, y=120)
    ectsy_tlo.create_text(105, 35, text="ECTSY: ", fill="white", font='Inter 25')

    # Wczytanie logo
    logo_img = Image.open("logo2.png").resize((800, 700))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(okno, image=logo_photo, bg="#e2dbd8")
    logo_label.image = logo_photo
    logo_label.place(x=300, y=-280)

    # przygotowanie ekranu ładowania
    ladowanie_tlo = tk.Canvas(okno, width=450, height=330, bg="#f3eee6")
    ladowanie_tlo.place(x=520, y=220)
    ladowanie_tlo.create_text(250, 50, text="Oczekiwanie aż\nprowadzący zacznie grę", fill="black",
                              font='Inter 25')

    # przygotowanie tła do wyświetlania rankingu
    # Nagłówek RANKING
    ranking_header = tk.Canvas(okno, width=227, height=50, bg="#750006", highlightthickness=0)
    ranking_header.place(x=50, y=200)
    ranking_header.create_text(113, 25, text="RANKING:", fill="white", font=('Inter', 20, 'bold'))

    # Lista rankingowa
    ranking_canvas = tk.Canvas(okno, width=227, height=450, bg="#750006", highlightthickness=0)
    ranking_canvas.place(x=50, y=250)

    def odswiez_ranking():
        try:
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
            gracze = sorted(dane.get("gracze", []), key=lambda x: -x["ects"])
            ranking_canvas.delete("all")
            for idx, g in enumerate(gracze):
                ranking_canvas.create_text(
                    113, 20 + idx * 30,
                    text=f"{g['login']}:  {g['ects']}",
                    fill="white",
                    font=("Arial", 14)
                )
        except Exception as e:
            print(f"[Błąd odświeżania rankingu]: {e}")

        okno.after(1000, odswiez_ranking)

    odswiez_ranking()
    # przygotowanie pól
    plansza_do_gry = Plansza(okno, 11, 8, 100, 400, 70, 50)
    plansza_do_gry.WypelnijDomyslnie()
    plansza_do_gry.Rysuj()

    # umieszczenie pionka gracza na polu startowym
    gracz.pionek.wyswietlPionek(plansza_do_gry, 0)

    grafiki_kostek = zaladuj_grafiki_kostek()
    label1, label2 = stworz_labelki_kostek(okno, grafiki_kostek)

    def po_rzucie(wynik1, wynik2):
        suma = wynik1 + wynik2
        gracz.pionek.animowany_ruch(plansza_do_gry, 0, suma, sprawdz_pole)

    dodaj_przycisk_rzutu(okno, label1, label2, grafiki_kostek, po_rzucie)
    # === ŁADOWANIE PYTAŃ ===
    

    # === FUNKCJA: sprawdzenie pola i pytanie ===
    def sprawdz_pole():
        pole = plansza_do_gry.pola[gracz.pionek.numerPola]
        typ = type(pole).__name__

        if typ == "SprawdzenieWiedzy" and gracz.pytania_wiedza:
            if gracz.pytania_wiedza:
                pytanie = gracz.pytania_wiedza.pop(0)
                question_popup.pokaz_pytanie(okno, pytanie, gracz)
            else:
                zakoncz_gre(okno, gracz)
        elif typ == "SesjaEgzaminacyjna" and gracz.pytania_sesja:
            if gracz.pytania_sesja:
                pytanie =  pytanie = gracz.pytania_sesja.pop(0)
                question_popup.pokaz_pytanie(okno, pytanie, gracz)
            else:
                zakoncz_gre(okno, gracz)
            messagebox.showinfo("Stypendium", "Otrzymujesz 2 ECTS za stypendium!")
            gracz.ects += 2
            aktualizuj_ects(gracz.login, gracz.ects)
    def rusz_o_jedno_pole():
        gracz.pionek.numerPola = (gracz.pionek.numerPola + 1) % len(plansza_do_gry.pola)
        gracz.pionek.wyswietlPionek(plansza_do_gry, gracz.pionek.numerPola)
        sprawdz_pole()
    # === TYM PRZYCISK: testuj pytanie ===
    def sprawdz_start():
        while True:
            time.sleep(1)
            if not os.path.exists("gra_status.json"):
                continue
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
            if dane["status"] == "start":
                ladowanie_tlo.destroy()
                plansza_do_gry.Rysuj()
                gracz.pionek.wyswietlPionek(plansza_do_gry, gracz.pionek.numerPola)
                break

    threading.Thread(target=sprawdz_start, daemon=True).start()
    tk.Button(okno, text="Rusz o 1 pole", command=rusz_o_jedno_pole).place(x=900, y=700)
    tk.Button(okno, text="Sprawdź pole (test)", command=sprawdz_pole).place(x=900, y=750)

    okno.mainloop()
