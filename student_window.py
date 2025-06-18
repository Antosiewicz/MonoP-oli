from PIL import Image, ImageTk, ImageSequence
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
from pionek import Pionek, pos

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

    #  Blokada dołączenia po starcie gry
    if dane.get("status") == "start":
        tk.messagebox.showerror("Błąd", "Gra już się rozpoczęła. Nie możesz dołączyć.")
        exit()

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

    # Pobierz kolor i KSZTALT gracza
    try:
        with open("gra_status.json", "r", encoding="utf-8") as f:
            dane = json.load(f)
        for g in dane["gracze"]:
            if g["login"] == login:
                kolor = g["kolor"]
                ksztalt = g.get("ksztalt", 0)  # domyślnie 0
                pole_start = g.get("pole", 0)
                break
        else:
            # fallback
            kolor = zarejestruj_gracza(login)
            ksztalt = 0
            pole_start = 0
    except:
        kolor = zarejestruj_gracza(login)
        ksztalt = 0
        pole_start = 0

    gracz = Student(login, kolor, ksztalt)
    gracz.pionek.numerPola = pole_start

    okno.title("Okno Studenta")
    screen_width = okno.winfo_screenwidth()
    screen_height = okno.winfo_screenheight()
    okno.geometry(f"{screen_width}x{screen_height}")
    okno.configure(bg="#e2dbd8")

    powrot_button = tk.Button(okno, text="POWRÓT", command=lambda: powrot_przycisk(okno), font="Georgia 25", fg="#d9dad9", bg="#750006")
    powrot_button.place(x=50, y=30)

    ectsy_tlo = tk.Canvas(okno, width=210, height=70, bg="#750006")
    ectsy_tlo.place(x=50, y=120)
    ectsy_tlo.create_text(105, 35, text="ECTSY: ", fill="#d9dad9", font='Georgia 25')

    logo_img = Image.open("logo2.png").resize((800, 700))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(okno, image=logo_photo, bg="#e2dbd8")
    logo_label.image = logo_photo
    logo_label.place(x=300, y=-280)
    gif = Image.open("loading.gif")
    gif_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
    gif_index = 0

    ladowanie_tlo = tk.Canvas(okno, width=450, height=330, bg="#f3eee6")
    ladowanie_tlo.place(x=screen_width/2-225, y=220)
    ladowanie_tlo.create_text(250, 50, text="Oczekiwanie aż\nprowadzący zacznie grę", fill="black", font='Inter 25')
    gif_img_id = ladowanie_tlo.create_image(225, 165, image=gif_frames[0])

    def animuj_gif():
        nonlocal gif_index
        gif_index = (gif_index + 1) % len(gif_frames)
        ladowanie_tlo.itemconfig(gif_img_id, image=gif_frames[gif_index])
        okno.after(25, animuj_gif)

    animuj_gif()
    def pokaz_okno_pomocy():
        opis = (
            "📘 Zasady gry:\n"
            "- Każdy gracz rzuca kostką i porusza się o sumę oczek.\n"
            "- Po ruchu wywoływana jest akcja pola:\n"
            "  🧪 Sprawdzenie Wiedzy – quiz z bonusem.\n"
            "  🎓 Sesja Egzaminacyjna – trudniejsze pytanie, więcej punktów.\n"
            "  🟡 Stypendium – +2 ECTS bez pytania.\n"
            "  🚫 Nieobecność – tura przepada.\n\n"
            "📌 Nowa tura rozpoczyna się dopiero, gdy KAŻDY gracz zakończy swoją."
        )
        tk.messagebox.showinfo("Pomoc – Zasady Gry", opis)

    pomoc_button = tk.Button(
        okno,
        text="POMOC",
        command=pokaz_okno_pomocy,
        font="Georgia 25",
        fg="#d9dad9",
        bg="#750006"
    )
    pomoc_button.place(x=screen_width - 250, y=30)  #  Umieszczenie po prawej
    ranking_header = tk.Canvas(okno, width=227, height=50, bg="#750006", highlightthickness=0)
    ranking_header.place(x=50, y=200)
    ranking_header.create_text(113, 25, text="RANKING:", fill="#d9dad9", font=('Georgia', 20, 'bold'))

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
                    continue  # nie rysuj swojego drugi raz

                login = g["login"]
                kolor = g.get("kolor", 0)
                pole = g.get("pole", 0)
                ksztalt = g.get("ksztalt", 0)  # <<< TO JEST KLUCZOWE

                if login not in pionki_innych:
                    pionek_tmp = Pionek(kolor, ksztalt)
                    pionek_tmp.numerPola = pole
                    pionki_innych[login] = pionek_tmp
                else:
                    pionek_tmp = pionki_innych[login]
                    stare_pole = pionek_tmp.numerPola
                    if pionek_tmp.img_id is not None:
                        plansza_do_gry.pola[stare_pole].tlo.delete(pionek_tmp.img_id)
                    pionek_tmp.numerPola = pole
                    # >>> Zaktualizuj kształt i kolor!
                    pionek_tmp.kolor = kolor
                    pionek_tmp.ksztalt = ksztalt

                # RYSUJ POPRAWNĄ GRAFIKĘ:
                img = pionek_tmp.get_image(plansza_do_gry.pola[pole].tlo)
                pionek_tmp.img_id = plansza_do_gry.pola[pole].tlo.create_image(
                    12 + pos[kolor][0],
                    18 + pos[kolor][1],
                    image=img
                )
        except Exception as e:
            print(f"[Błąd odświeżania pionków]: {e}")

        okno.after(1000, odswiez_pionki)

    pole_x = int(screen_width / 15)
    pole_y = int(screen_height / 14)
    dl_planszy = 11
    szer_planszy = 8
    margin_left = screen_width / 2 - (szer_planszy / 2 + 1) * pole_x
    margin_top = screen_height / 2 - (dl_planszy / 2 ) * pole_y

    plansza_do_gry = Plansza(okno, dl_planszy, szer_planszy, margin_top, margin_left, pole_x, pole_y)
    plansza_do_gry.WypelnijDomyslnie()
    plansza_do_gry.Rysuj()

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
                grafiki_kostek = zaladuj_grafiki_kostek()
                label1, label2 = stworz_labelki_kostek(okno, grafiki_kostek)
                dodaj_przycisk_rzutu(okno, label1, label2, grafiki_kostek, po_rzucie)
                break

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

    def po_rzucie(w1, w2):
        if not czy_moze_rzucic(gracz):
            tk.messagebox.showinfo("Tura", "Poczekaj na swoją kolej.")
            return

        suma = w1 + w2
        gracz.pionek.animowany_ruch(plansza_do_gry, gracz.pionek.kolor, suma, sprawdz_pole)

        try:
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
            if "tura" not in dane:
                dane["tura"] = 1
            if "ruchy" not in dane:
                dane["ruchy"] = {}
            dane["ruchy"][gracz.login] = dane["ruchy"].get(gracz.login, 0) + 1
            if all(r >= dane["tura"] for r in dane["ruchy"].values()):
                dane["tura"] += 1
            with open("gra_status.json", "w", encoding="utf-8") as f:
                json.dump(dane, f, indent=2)
        except Exception as e:
            print(f"[Błąd aktualizacji tury]: {e}")

    with open("gra_status.json", "r", encoding="utf-8") as f:
        dane = json.load(f)
    dane.setdefault("ruchy", {})
    dane["ruchy"][gracz.login] = dane["ruchy"].get(gracz.login, 0) + 1
    if all(r >= dane["tura"] for r in dane["ruchy"].values()):
        dane["tura"] += 1
    with open("gra_status.json", "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=2)

    def sprawdz_reset():
        gra_rozpoczeta = False
        while True:
            time.sleep(1)
            if not os.path.exists("gra_status.json"):
                continue
            with open("gra_status.json", "r", encoding="utf-8") as f:
                dane = json.load(f)
            status = dane.get("status", "")
            if status == "start":
                gra_rozpoczeta = True
            if gra_rozpoczeta and status == "oczekiwanie":
                tk.messagebox.showinfo("Reset gry", f"Gra zakoniczyła sie.\nZdobyte ECTS: {gracz.ects}")
                okno.destroy()
                break

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

    threading.Thread(target=sprawdz_start, daemon=True).start()
    threading.Thread(target=sprawdz_reset, daemon=True).start()
    odswiez_ranking()
    odswiez_pionki()
    okno.mainloop()
