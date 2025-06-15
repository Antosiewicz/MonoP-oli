from PIL import Image, ImageTk
import tkinter as tk
import json
import os
import threading
import time
import menu
from plansza import Plansza
from student import Student
from kostki import zaladuj_grafiki_kostek, stworz_labelki_kostek, dodaj_przycisk_rzutu
import question_popup

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

    powrot_img = Image.open("powrot.png").resize((210, 70))
    powrot_photo = ImageTk.PhotoImage(powrot_img)
    powrot_button = tk.Button(okno, image=powrot_photo, command=lambda: powrot_przycisk(okno), borderwidth=0)
    powrot_button.image = powrot_photo
    powrot_button.place(x=50, y=30)

    ectsy_tlo = tk.Canvas(okno, width=210, height=70, bg="#750006")
    ectsy_tlo.place(x=50, y=120)
    ectsy_tlo.create_text(105, 35, text="ECTSY: ", fill="white", font='Inter 25')

    ranking_header = tk.Canvas(okno, width=227, height=50, bg="#750006", highlightthickness=0)
    ranking_header.place(x=50, y=200)
    ranking_header.create_text(113, 25, text="RANKING:", fill="white", font=('Inter', 20, 'bold'))

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

    # POWIĘKSZONA PLANSZA z lekko wyższymi polami
    length = 11
    width = 8

    max_plansza_w = int(screen_width * 0.75)
    max_plansza_h = int(screen_height * 0.75)

    bazowy_pole_h = max_plansza_h // length
    bazowy_pole_w = int(bazowy_pole_h * 1.5)

    factor = 1.2
    pole_h = int(bazowy_pole_h * factor * 0.85)  # zamiast 0.8 -> 0.85, wyższe pola
    pole_w = int(bazowy_pole_w * factor)

    import plansza as pl_mod
    pl_mod.POLE_Y = pole_h
    pl_mod.POLE_X = pole_w

    plansza_w = (width + 2) * pole_w
    plansza_h = length * pole_h

    margin_left = (screen_width - plansza_w) // 2
    margin_top = (screen_height - plansza_h) // 2 + 10  # przesunięcie o 10 pikseli niżej

    plansza_do_gry = Plansza(okno, length, width, margin_top, margin_left, pole_w, pole_h)
    plansza_do_gry.WypelnijDomyslnie()
    plansza_do_gry.Rysuj()

    gracz.pionek.wyswietlPionek(plansza_do_gry, 0)

    grafiki_kostek = zaladuj_grafiki_kostek()
    label1, label2 = stworz_labelki_kostek(okno, grafiki_kostek)

    def po_rzucie(wynik1, wynik2):
        suma = wynik1 + wynik2
        gracz.pionek.animowany_ruch(plansza_do_gry, 0, suma, sprawdz_pole)

    dodaj_przycisk_rzutu(okno, label1, label2, grafiki_kostek, po_rzucie)

    def sprawdz_pole():
        pole = plansza_do_gry.pola[gracz.pionek.numerPola]
        typ = type(pole).__name__

        if typ == "SprawdzenieWiedzy" and gracz.pytania_wiedza:
            pytanie = gracz.pytania_wiedza.pop(0)
            question_popup.pokaz_pytanie(okno, pytanie, gracz)
        elif typ == "SesjaEgzaminacyjna" and gracz.pytania_sesja:
            pytanie = gracz.pytania_sesja.pop(0)
            question_popup.pokaz_pytanie(okno, pytanie, gracz)
        else:
            if not gracz.pytania_wiedza and not gracz.pytania_sesja:
                zakoncz_gre(okno, gracz)

    def rusz_o_jedno_pole():
        gracz.pionek.numerPola = (gracz.pionek.numerPola + 1) % len(plansza_do_gry.pola)
        gracz.pionek.wyswietlPionek(plansza_do_gry, gracz.pionek.numerPola)
        sprawdz_pole()

    def sprawdz_start():
        while True:
            time.sleep(1)
            if not os.path.exists("gra_status.json"):
                continue
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
            if dane["status"] == "start":
                plansza_do_gry.Rysuj()
                gracz.pionek.wyswietlPionek(plansza_do_gry, gracz.pionek.numerPola)
                break

    threading.Thread(target=sprawdz_start, daemon=True).start()

    tk.Button(okno, text="Rusz o 1 pole", command=rusz_o_jedno_pole).place(x=900, y=700)
    tk.Button(okno, text="Sprawdź pole (test)", command=sprawdz_pole).place(x=900, y=750)

    okno.mainloop()
