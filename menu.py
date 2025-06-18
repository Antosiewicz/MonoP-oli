import tkinter as tk
from PIL import Image, ImageTk
import login_screen
import prowadzacy_window
import prowadzacy_login

def student_przycisk(root):
    root.destroy()
    login_screen.uruchom_ekran_logowania()

def prowadzacy_przycisk(root):
    root.destroy()
    prowadzacy_login.uruchom_logowanie_prowadzacy(root)

def main():
    root = tk.Tk()
    root.title("Menu Gry")

    # Automatyczny rozmiar okna do wielkości ekranu
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg="#e2dbd8")

    #wczytanie grafik
    logo_img = Image.open("logo.png")
    logo_photo = ImageTk.PhotoImage(logo_img)

    student_img = Image.open("student.png").resize((400,100))
    student_photo = ImageTk.PhotoImage(student_img)

    prowadzacy_img = Image.open("prowadzacy.png").resize((400,100))
    prowadzacy_photo = ImageTk.PhotoImage(prowadzacy_img)

    # Tworzenie tła
    tlo = tk.Canvas(root, width=screen_width, height=screen_height)
    tlo.pack(fill="both", expand=True)
    bg_i=Image.open("tlo_politechnika_kontury.png").resize((screen_width,screen_height))
    bg = ImageTk.PhotoImage(bg_i)
    tlo.create_image(0, 0, image=bg, anchor="nw")

    #logo
    tlo.create_image(screen_width/2.02, 300, image=logo_photo)


    # Przycisk STUDENT
    student_button = tk.Button(tlo, image=student_photo, command=lambda: student_przycisk(root), borderwidth=0)
    student_button.image = student_photo
    student_button_window = tlo.create_window(screen_width/2, 500, window=student_button)

    # Przycisk PROWADZĄCY
    prowadzacy_button = tk.Button(tlo, image=prowadzacy_photo, command=lambda: prowadzacy_przycisk(root), borderwidth=0)
    prowadzacy_button.image = prowadzacy_photo
    prowadzacy_button_window = tlo.create_window(screen_width/2, 630, window=prowadzacy_button)

    root.mainloop()

if __name__ == "__main__":
    main()
