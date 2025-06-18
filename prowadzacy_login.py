import tkinter as tk
from tkinter import messagebox
import menu
import login_screen
from database import zaloguj_uzytkownika
import prowadzacy_window
from PIL import Image, ImageTk

def uruchom_logowanie_prowadzacy(prev_window):
    root = tk.Tk()
    root.title("Logowanie Prowadzącego")

    # Dynamiczne ustawienie rozmiaru okna na pełny ekran
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

    tlo1_height = 300
    tlo1_width = 300
    tlo1 = tk.Canvas(tlo, width=tlo1_width, height=tlo1_height, bg="#750006")

    login_label = tk.Label(tlo1, text="LOGIN:", font="Georgia 16 bold", bg="#750006", fg="#d9dad9")
    login_window = tlo1.create_window(tlo1_width / 2, 50, window=login_label)
    login_entry = tk.Entry(tlo1)
    login_entry_window = tlo1.create_window(tlo1_width / 2, 75, window=login_entry)

    haslo_label = tk.Label(tlo1, text="HASŁO:", font="Georgia 16 bold", bg="#750006", fg="#d9dad9")
    haslo_window = tlo1.create_window(tlo1_width / 2, 100, window=haslo_label)
    haslo_entry = tk.Entry(tlo1, show="*")
    haslo_window = tlo1.create_window(tlo1_width / 2, 125, window=haslo_entry)

    def zaloguj():
        login = login_entry.get()
        haslo = haslo_entry.get()
        if zaloguj_uzytkownika(login, haslo, rola="prowadzacy"):
            messagebox.showinfo("Sukces", "Zalogowano jako prowadzący!")
            root.destroy()
            prowadzacy_window.uruchom_okno_prowadzacy()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")

    zaloguj_button = tk.Button(tlo1, text="ZALOGUJ", command=zaloguj, font="Georgia 14", bg="#d9dad9", fg="#750006")
    zaloguj_window = tlo1.create_window(tlo1_width / 2, 200, window=zaloguj_button)
    powrot = tk.Button(root, text="POWRÓT", command=lambda: powrot_do_menu(root), font="Georgia 14", bg="#d9dad9", fg="#750006")
    powrot_window = tlo1.create_window(tlo1_width / 2, 250, window=powrot)
    tlo1.place(x=screen_width / 2, y=screen_height / 2.5, anchor="c")

    root.bind('<Return>', lambda event: zaloguj())

    root.mainloop()

def powrot_do_menu(root):
    root.destroy()
    menu.main()
