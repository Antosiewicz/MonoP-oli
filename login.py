import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import zaloguj_uzytkownika
import student_window
import login_screen

def uruchom_logowanie(prev_window):
    prev_window.destroy()
    root = tk.Tk()
    root.title("Logowanie")

    # Automatyczny rozmiar okna do rozdzielczości ekranu
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

    tlo1_height=300
    tlo1_width=300
    tlo1 = tk.Canvas(tlo, width=tlo1_width, height=tlo1_height, bg="#750006")

    login_label=tk.Label(tlo1, text="LOGIN:", font="Georgia 16 bold", bg="#750006", fg="#d9dad9")
    login_window = tlo1.create_window(tlo1_width/2, 50, window=login_label)
    login_entry = tk.Entry(tlo1)
    login_entry_window = tlo1.create_window(tlo1_width / 2, 75, window=login_entry)

    haslo_label = tk.Label(tlo1, text="HASŁO:", font="Georgia 16 bold", bg="#750006", fg="#d9dad9")
    haslo_window = tlo1.create_window(tlo1_width / 2, 100, window=haslo_label)
    haslo_entry = tk.Entry(tlo1, show="*")
    haslo_window = tlo1.create_window(tlo1_width / 2, 125, window=haslo_entry)

    def zaloguj():
        login = login_entry.get()
        haslo = haslo_entry.get()
        if zaloguj_uzytkownika(login, haslo, rola="student"):
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
            root.destroy()
            student_window.uruchom_okno_student(login)
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")

    zaloguj = tk.Button(tlo1, text="ZALOGUJ", command=zaloguj, font="Georgia 14", bg="#d9dad9", fg="#750006")#.pack(pady=10)
    zaloguj_window = tlo1.create_window(tlo1_width/2, 200, window=zaloguj)
    powrot = tk.Button(tlo1, text="POWRÓT", command=lambda: powrot_do_ekranu_wyboru(root), font="Georgia 14", bg="#d9dad9", fg="#750006")#.pack(pady=10)
    powrot_window = tlo1.create_window(tlo1_width / 2, 250, window=powrot)
    tlo1.place(x=screen_width / 2, y=screen_height /3, anchor="c")
    root.bind('<Return>', lambda event: zaloguj())

    root.mainloop()

def powrot_do_ekranu_wyboru(current_root):
    current_root.destroy()
    login_screen.uruchom_ekran_logowania()
