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

    tk.Label(tlo, text="Login:").pack(pady=5)
    login_entry = tk.Entry(tlo)
    login_entry.pack()

    tk.Label(tlo, text="Hasło:").pack(pady=5)
    haslo_entry = tk.Entry(tlo, show="*")
    haslo_entry.pack()

    def zaloguj():
        login = login_entry.get()
        haslo = haslo_entry.get()
        if zaloguj_uzytkownika(login, haslo, rola="student"):
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
            root.destroy()
            student_window.uruchom_okno_student(login)
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")

    tk.Button(tlo, text="Zaloguj", command=zaloguj).pack(pady=10)
    tk.Button(tlo, text="Powrót", command=lambda: powrot_do_ekranu_wyboru(root)).pack(pady=10)

    root.bind('<Return>', lambda event: zaloguj())

    root.mainloop()

def powrot_do_ekranu_wyboru(current_root):
    current_root.destroy()
    login_screen.uruchom_ekran_logowania()
