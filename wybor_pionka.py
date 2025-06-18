import tkinter as tk
from PIL import Image, ImageTk
import os
import student_window

KOLORY_NAZWY = ['zolty', 'zielony', 'czerwony', 'niebieski']
KSZTALTY_NAZWY = ['pionek', 'klodka', 'wifi', 'zebatka', 'monitor']

def wybierz_pionek_window(login, kolor):
    okno = tk.Tk()
    okno.title("Wybierz swój pionek")
    okno.configure(bg="#e2dbd8")

    images = []
    for i in range(5):
        nazwa = KSZTALTY_NAZWY[i]
        kolor_nazwa = KOLORY_NAZWY[kolor]
        sciezka = f"{nazwa}_{kolor_nazwa}.png"
        if os.path.exists(sciezka):
            img = Image.open(sciezka).resize((100,100))
        else:
            img = Image.new('RGBA', (100,100), (255,0,0,80))
        images.append(ImageTk.PhotoImage(img))

    wybrany = tk.IntVar(value=0)

    def wybierz(i):
        wybrany.set(i)
        for btn in btns:
            btn.config(relief="raised")
        btns[i].config(relief="sunken")

    btns = []
    for i, img in enumerate(images):
        b = tk.Button(okno, image=img, command=lambda i=i: wybierz(i), bg="#e2dbd8", relief="raised", borderwidth=3)
        b.image = img  # ważne dla Tkintera!
        b.grid(row=0, column=i, padx=15, pady=30)
        btns.append(b)
    btns[0].config(relief="sunken")

    def zatwierdz():
        ksztalt = wybrany.get()
        import json
        with open("gra_status.json", "r", encoding="utf-8") as f:
            dane = json.load(f)
        for g in dane["gracze"]:
            if g["login"] == login:
                g["ksztalt"] = ksztalt
        with open("gra_status.json", "w", encoding="utf-8") as f:
            json.dump(dane, f, indent=2)
        okno.destroy()
        student_window.uruchom_okno_student(login)

    liczba_pionkow = len(KSZTALTY_NAZWY)

    zatwierdz_btn = tk.Button(
        okno, text="Wybierz ten pionek", font="Georgia 20", command=zatwierdz,
        bg="#750006", fg="#d9dad9"
    )
    zatwierdz_btn.grid(
        row=1, column=0, columnspan=liczba_pionkow, pady=20, sticky="ew"
    )
    okno.mainloop()
