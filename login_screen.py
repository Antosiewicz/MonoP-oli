import tkinter as tk
from login import uruchom_logowanie
from register import uruchom_rejestracje
import menu
from PIL import Image, ImageTk

def uruchom_ekran_logowania():
    root = tk.Tk()
    root.title("Panel logowania studenta")

    # Automatyczne ustawienie rozmiaru okna do rozdzielczości ekranu
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg="#e2dbd8")

    # Tworzenie tła
    tlo = tk.Canvas(root, width=screen_width, height=screen_height)
    tlo.pack(fill="both", expand=True)
    bg_i = Image.open("tlo_politechnika_kontury.png").resize((screen_width, screen_height))
    bg = ImageTk.PhotoImage(bg_i)
    tlo.create_image(0, 0, image=bg, anchor="nw")

    # wczytanie grafik
    zaloguj_sie_img = Image.open("przycisk_zaloguj_sie.png").resize((400, 100))
    zaloguj_sie_photo = ImageTk.PhotoImage(zaloguj_sie_img)
    zaloz_konto_img = Image.open("przycisk_zaloz_konto.png").resize((400, 100))
    zaloz_konto_photo = ImageTk.PhotoImage(zaloz_konto_img)
    powrot_img = Image.open("przycisk_powrot.png").resize((400, 100))
    powrot_photo = ImageTk.PhotoImage(powrot_img)

    #tk.Label(tlo, text="Witaj, Studencie!", font=("Arial", 18), bg="#e2dbd8").pack(pady=20)

    tk.Button(tlo, image=zaloguj_sie_photo, borderwidth=0, command=lambda: uruchom_logowanie(root)).pack(pady=(screen_height/3.3, 10))
    tk.Button(tlo, image=zaloz_konto_photo, borderwidth=0, command=lambda: uruchom_rejestracje(root)).pack(pady=10)
    tk.Button(tlo, image=powrot_photo, borderwidth=0, command=lambda: powrot_do_menu(root)).pack(pady=10)

    root.mainloop()

def powrot_do_menu(root):
    root.destroy()
    menu.main()
