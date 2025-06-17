import tkinter as tk
from tkinter import messagebox
from database import zarejestruj_uzytkownika
import login_screen
from PIL import Image, ImageTk

def uruchom_rejestracje(prev_window):
    prev_window.destroy()
    root = tk.Tk()
    root.title("Rejestracja")

    # Dynamiczne dopasowanie rozmiaru okna
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

    tlo1_height = 350
    tlo1_width = 300
    tlo1 = tk.Canvas(tlo, width=tlo1_width, height=tlo1_height, bg="#750006")

    nowy_login_label = tk.Label(tlo1, text="NOWY LOGIN:", font="Georgia 16 bold", bg="#750006", fg="#d9dad9")
    login_window = tlo1.create_window(tlo1_width / 2, 50, window=nowy_login_label)
    login_entry = tk.Entry(tlo1)
    login_entry_window = tlo1.create_window(tlo1_width / 2, 75, window=login_entry)

    haslo_label = tk.Label(tlo1, text="HASŁO:", font="Georgia 16 bold", bg="#750006", fg="#d9dad9")
    haslo_window = tlo1.create_window(tlo1_width / 2, 125, window=haslo_label)
    haslo_entry = tk.Entry(tlo1, show="*")
    haslo_window = tlo1.create_window(tlo1_width / 2, 150, window=haslo_entry)

    powtorz_haslo_label = tk.Label(tlo1, text="POWTÓRZ HASŁO:", font="Georgia 16 bold", bg="#750006", fg="#d9dad9")
    powtorz_haslo_window = tlo1.create_window(tlo1_width / 2, 200, window=powtorz_haslo_label)
    haslo2_entry = tk.Entry(tlo1, show="*")
    haslo2_window = tlo1.create_window(tlo1_width / 2, 225, window=haslo2_entry)

    def zarejestruj():
        login = login_entry.get()
        haslo = haslo_entry.get()
        haslo2 = haslo2_entry.get()

        if haslo != haslo2:
            messagebox.showerror("Błąd", "Hasła się nie zgadzają")
            return

        if zarejestruj_uzytkownika(login, haslo, rola="student"):
            messagebox.showinfo("Sukces", "Rejestracja zakończona")
            root.destroy()
            login_screen.uruchom_ekran_logowania()
        else:
            messagebox.showerror("Błąd", "Użytkownik już istnieje")

    zarejestruj_button = tk.Button(root, text="ZAREJESTRUJ", command=zarejestruj, font="Georgia 14", bg="#d9dad9", fg="#750006")
    haslo2_window = tlo1.create_window(tlo1_width / 2, 275, window=zarejestruj_button)
    powrot = tk.Button(tlo1, text="POWRÓT", command=lambda: powrot_do_ekranu_wyboru(root), font="Georgia 14", bg="#d9dad9", fg="#750006")
    haslo2_window = tlo1.create_window(tlo1_width / 2, 325, window=powrot)
    tlo1.place(x=screen_width / 2, y=screen_height / 3, anchor="c")
    root.bind('<Return>', lambda event: zarejestruj())

    root.mainloop()

def powrot_do_ekranu_wyboru(current_root):
    current_root.destroy()
    login_screen.uruchom_ekran_logowania()
