from PIL import Image, ImageTk
import tkinter as tk
import menu
import json
import os
import threading
import time
from nieobecnosc import *
from plansza import *
from student import Student
from kostki import zaladuj_grafiki_kostek, stworz_labelki_kostek, dodaj_przycisk_rzutu
import question_popup
from pionek import Pionek,pos  # dodane by uniknac NameError

def zakoncz_gre(okno, gracz):
    tk.messagebox.showinfo("Koniec gry", f"Koniec pytań!\nZdobyte ECTS: {gracz.ects}")
    okno.destroy()

def powrot_przycisk(okno):
    okno.destroy()
    menu.main()

def zarejestruj_gracza(login):
    try:
        with open("gra_status.json", "r", encoding="utf-8") as f:
            dane = json.load(f)
    except FileNotFoundError:
        dane = {"status": "oczekiwanie", "gracze": []}

    # 🚫 Blokada dołączenia po starcie gry
    if dane.get("status") == "start":
        tk.messagebox.showerror("Błąd", "Gra już się rozpoczęła. Nie możesz dołączyć.")
        exit()  # albo return None i obsłuż to wyżej

    gracze = dane.get("gracze", [])
    for g in gracze:
        if g["login"] == login:
            return g["kolor"]
    try:
        with open("gra_status.json", "r", encoding="utf-8") as f:
            dane = json.load(f)
    except FileNotFoundError:
        dane = {"status": "oczekiwanie", "gracze": []}

    gracze = dane.get("gracze", [])
    for g in gracze:
        if g["login"] == login:
            return g["kolor"]
    if "tura" not in dane:
        dane["tura"] = 1
    if "ruchy" not in dane:
        dane["ruchy"] = {}
    zajete = {g.get("kolor", 0) for g in gracze}
    wolne = [i for i in range(4) if i not in zajete]
    nowy_kolor = wolne[0] if wolne else 0

    gracze.append({"login": login, "ects": 0, "kolor": nowy_kolor, "pole": 0})
    dane["gracze"] = gracze
    with open("gra_status.json", "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=2)

    return nowy_kolor

def uruchom_okno_student(login):
    okno = tk.Tk()
    
    kolor = zarejestruj_gracza(login)
    gracz = Student(login, kolor)

    try:
        with open("gra_status.json", "r", encoding="utf-8") as f:
            dane = json.load(f)
        for g in dane["gracze"]:
            if g["login"] == login:
                gracz.pionek.numerPola = g.get("pole", 0)
                break
    except:
        pass

    okno.title("Okno Studenta")
    screen_width = okno.winfo_screenwidth()
    screen_height = okno.winfo_screenheight()
    okno.geometry(f"{screen_width}x{screen_height}")
    okno.configure(bg="#e2dbd8")

    powrot_img = Image.open("powrot.png").resize((210, 70))
    powrot_photo = ImageTk.PhotoImage(powrot_img)
    powrot_button = tk.Button(okno, image=powrot_photo, command=lambda: powrot_przycisk(okno), borderwidth=0)
    powrot_button.image = powrot_photo
    powrot_button.place(x=50, y=30)

    ectsy_tlo = tk.Canvas(okno, width=210, height=70, bg="#750006")
    ectsy_tlo.place(x=50, y=120)
    ectsy_tlo.create_text(105, 35, text="ECTSY: ", fill="white", font='Inter 25')

    logo_img = Image.open("logo2.png").resize((800, 700))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(okno, image=logo_photo, bg="#e2dbd8")
    logo_label.image = logo_photo
    logo_label.place(x=300, y=-280)

    ladowanie_tlo = tk.Canvas(okno, width=450, height=330, bg="#f3eee6")
    ladowanie_tlo.place(x=520, y=220)
    ladowanie_tlo.create_text(250, 50, text="Oczekiwanie aż\nprowadzący zacznie grę", fill="black", font='Inter 25')

    ranking_header = tk.Canvas(okno, width=227, height=50, bg="#750006", highlightthickness=0)
    ranking_header.place(x=50, y=200)
    ranking_header.create_text(113, 25, text="RANKING:", fill="white", font=('Inter', 20, 'bold'))

    ranking_canvas = tk.Canvas(okno, width=227, height=450, bg="#750006", highlightthickness=0)
    ranking_canvas.place(x=50, y=250)

    def zapisz_pozycje_gracza():
        with open("gra_status.json", "r", encoding="utf-8") as f:
            dane = json.load(f)
        for g in dane["gracze"]:
            if g["login"] == gracz.login:
                g["pole"] = gracz.pionek.numerPola
                break
        with open("gra_status.json", "w", encoding="utf-8") as f:
            json.dump(dane, f, indent=2)

    def odswiez_ranking():
        try:
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
            gracze = sorted(dane.get("gracze", []), key=lambda x: -x["ects"])
            ranking_canvas.delete("all")
            for idx, g in enumerate(gracze):
                ranking_canvas.create_text(113, 20 + idx * 30, text=f"{g['login']}:  {g['ects']}", fill="white", font=("Arial", 14))
        except:
            pass
        okno.after(1000, odswiez_ranking)
    
    pionki_innych = {}

    def odswiez_pionki():
        try:
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)

            for g in dane["gracze"]:
                if g["login"] == gracz.login:
                    continue

                login = g["login"]
                kolor = g.get("kolor", 0)
                pole = g.get("pole", 0)

                if login not in pionki_innych:
                    pionek_tmp = Pionek(kolor)
                    pionek_tmp.numerPola = pole
                    pionki_innych[login] = pionek_tmp
                else:
                    pionek_tmp = pionki_innych[login]
                    stare_pole = pionek_tmp.numerPola
                    if pionek_tmp.img_id is not None:
                        plansza_do_gry.pola[stare_pole].tlo.delete(pionek_tmp.img_id)
                    pionek_tmp.numerPola = pole

                pionek_tmp.img_id = plansza_do_gry.pola[pole].tlo.create_image(
                    12 + pos[kolor][0],
                    18 + pos[kolor][1],
                    image=plansza_do_gry.pola[pole].pionek[kolor]
                )
        except Exception as e:
            print(f"[Błąd odświeżania pionków]: {e}")

        okno.after(1000, odswiez_pionki)

    plansza_do_gry = Plansza(okno, 11, 8, 100, 400, 70, 50)
    plansza_do_gry.WypelnijDomyslnie()
    plansza_do_gry.Rysuj()
    gracz.pionek.wyswietlPionek(plansza_do_gry, gracz.pionek.kolor)
    def czy_moze_rzucic(gracz):
        try:
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)

            tura = dane.get("tura", 1)
            ruchy = dane.get("ruchy", {})

            return ruchy.get(gracz.login, 0) < tura
        except:
            return False
    grafiki_kostek = zaladuj_grafiki_kostek()
    label1, label2 = stworz_labelki_kostek(okno, grafiki_kostek)

    def po_rzucie(w1, w2):
        if not czy_moze_rzucic(gracz):
            tk.messagebox.showinfo("Tura", "Poczekaj na swoją kolej.")
            return

        suma = w1 + w2
        gracz.pionek.animowany_ruch(plansza_do_gry, gracz.pionek.kolor, suma, sprawdz_pole)

        try:
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)

            # Zapewnij istnienie "tura" i "ruchy"
            if "tura" not in dane:
                dane["tura"] = 1
            if "ruchy" not in dane:
                dane["ruchy"] = {}

            # Zwiększ licznik ruchu tego gracza
            dane["ruchy"][gracz.login] = dane["ruchy"].get(gracz.login, 0) + 1

            # Jeśli wszyscy gracze mają ruchy >= obecnej tury -> nowa tura
            if all(r >= dane["tura"] for r in dane["ruchy"].values()):
                dane["tura"] += 1

            with open("gra_status.json", "w", encoding="utf-8") as f:
                json.dump(dane, f, indent=2)

        except Exception as e:
            print(f"[Błąd aktualizacji tury]: {e}")



    # Zaktualizuj liczbę ruchów
    with open("gra_status.json", "r", encoding="utf-8") as f:
        dane = json.load(f)

    dane.setdefault("ruchy", {})
    dane["ruchy"][gracz.login] = dane["ruchy"].get(gracz.login, 0) + 1

    # Jeśli wszyscy wykonali ruch, zwiększ turę
    if all(r >= dane["tura"] for r in dane["ruchy"].values()):
        dane["tura"] += 1

    with open("gra_status.json", "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=2)

    dodaj_przycisk_rzutu(okno, label1, label2, grafiki_kostek, po_rzucie)

    def sprawdz_pole():
        pole = plansza_do_gry.pola[gracz.pionek.numerPola]
        typ = type(pole).__name__
        if hasattr(pole, "akcja"):
            pole.akcja(gracz)
        if typ == "Stypendium":
            gracz.ects += 2
            zapisz_pozycje_gracza()
            question_popup.aktualizuj_ects(gracz.login,gracz.ects)
            tk.messagebox.showinfo("Stypendium", "+2 ECTS za stypendium!")
        if typ == "SprawdzenieWiedzy" and gracz.pytania_wiedza:
            pytanie = gracz.pytania_wiedza.pop(0)
            question_popup.pokaz_pytanie(okno, pytanie, gracz)
        elif typ == "SesjaEgzaminacyjna" and gracz.pytania_sesja:
            pytanie = gracz.pytania_sesja.pop(0)
            question_popup.pokaz_pytanie(okno, pytanie, gracz)
        zapisz_pozycje_gracza()

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
                gracz.pionek.wyswietlPionek(plansza_do_gry, gracz.pionek.kolor)
                break

    threading.Thread(target=sprawdz_start, daemon=True).start()

    odswiez_ranking()
    odswiez_pionki()

    okno.mainloop()
