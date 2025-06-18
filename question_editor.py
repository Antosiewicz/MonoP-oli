import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
import prowadzacy_window

# Ścieżka do domyślnego pliku bazy danych
SCIEZKA_PLIKU_JSON = "baza_pytan.json"

def set_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')
    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)
def uruchom_edycje():
    edytor = tk.Tk()
    edytor.title("Edycja Bazy Pytań")

    # Automatyczny rozmiar okna
    screen_width = edytor.winfo_screenwidth()
    screen_height = edytor.winfo_screenheight()
    edytor.geometry(f"{screen_width}x{screen_height}")
    edytor.configure(bg="#e2dbd8")

    questions = []  # Lista przechowująca pytania jako słowniki

    # Tabela do wyświetlania pytań
    tree = ttk.Treeview(
        edytor,
        columns=('Treść', 'Typ', 'Odpowiedzi', 'Poprawna'),
        show='headings',
        height=25  # <-- liczba widocznych wierszy w pionie
    )
    tree.heading('Treść', text='Treść pytania')
    tree.heading('Typ', text='Typ')
    tree.heading('Odpowiedzi', text='Odpowiedzi')
    tree.heading('Poprawna', text='Poprawna odpowiedź')

    scrollbar = ttk.Scrollbar(edytor, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # Tylko fill=tk.X! NIE używaj fill=tk.BOTH ani expand=True
    tree.pack(fill=tk.X, pady=10)
    scrollbar.place(in_=tree, relx=1.0, rely=0, relheight=1.0, bordermode="outside")

    # Pola do wprowadzenia danych
    entry_question = tk.Entry(edytor, width=70)
    entry_question.pack(pady=5)
    set_placeholder(entry_question, "Treść pytania")

    combo_type = ttk.Combobox(edytor, values=["Sprawdzenie wiedzy", "Sesja egzaminacyjna"])
    combo_type.pack(pady=5)
    combo_type.current(0)

    entry_question = tk.Entry(edytor, width=70)
    entry_question.pack(pady=5)
    set_placeholder(entry_question, "Odpowiedź na pytanie")

    # Instrukcja pod polami
    label_help = tk.Label(
        edytor,
        text="Dla 'Sprawdzenie wiedzy' wpisz jedną odpowiedź jako poprawną.\nDla 'Sesja egzaminacyjna' otworzy się dodatkowe okno do wpisania 4 opcji i poprawnej litery (A/B/C/D).",
        bg="#e2dbd8",
        fg="gray"
    )
    label_help.pack(pady=2)

    # Okno dla wpisania odpowiedzi zamkniętych A/B/C/D
    def otworz_okno_opcji():
        top = tk.Toplevel(edytor)
        top.title("Opcje odpowiedzi")

        labels = ['A', 'B', 'C', 'D']
        entries = {}

        for i, lit in enumerate(labels):
            tk.Label(top, text=f"{lit})").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(top, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[lit] = entry

        tk.Label(top, text="Poprawna litera (A/B/C/D):").grid(row=4, column=0, columnspan=2, pady=10)
        correct_var = tk.Entry(top, width=5)
        correct_var.grid(row=5, column=0, columnspan=2)

        # Zapisanie pytań po zamknięciu okna
        def save_and_close():
            options_text = ", ".join([f"{lit}) {entries[lit].get().strip()}" for lit in labels])
            correct = correct_var.get().strip().upper()
            if correct not in labels:
                messagebox.showerror("Błąd", "Poprawna odpowiedź musi być A, B, C lub D")
                return
            top.destroy()
            dodaj_pytanie(options_text, correct)

        tk.Button(top, text="Zapisz", command=save_and_close).grid(row=6, column=0, columnspan=2, pady=10)

    # Funkcja dodająca pytanie do listy i tabeli
    def dodaj_pytanie(options, correct):
        text = entry_question.get().strip()
        qtype = combo_type.get().strip()
        if text and qtype and correct:
            tree.insert('', 'end', values=(text, qtype, options, correct))
            questions.append({'text': text, 'type': qtype, 'options': options, 'correct': correct})
            entry_question.delete(0, tk.END)
            entry_correct.delete(0, tk.END)
            combo_type.set('')
        else:
            messagebox.showwarning("Błąd", "Uzupełnij wszystkie pola")

    # Obsługa przycisku "Dodaj pytanie"
    def add_question():
        qtype = combo_type.get().strip()
        if qtype == "Sesja egzaminacyjna":
            otworz_okno_opcji()
        else:
            text = entry_question.get().strip()
            correct = entry_correct.get().strip()
            if text and qtype and correct:
                tree.insert('', 'end', values=(text, qtype, '', correct))
                questions.append({'text': text, 'type': qtype, 'options': '', 'correct': correct})
                entry_question.delete(0, tk.END)
                entry_correct.delete(0, tk.END)
                combo_type.set('')
            else:
                messagebox.showwarning("Błąd", "Uzupełnij wszystkie pola")

    # Zapis danych do jednego, stałego pliku JSON
    def save_to_file():
        with open(SCIEZKA_PLIKU_JSON, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Zapisano", f"Pytania zapisane do pliku: {SCIEZKA_PLIKU_JSON}")

    # Wczytanie danych z tego samego pliku
    def load_from_file():
        if not os.path.exists(SCIEZKA_PLIKU_JSON):
            messagebox.showwarning("Brak pliku", f"Plik {SCIEZKA_PLIKU_JSON} nie istnieje.")
            return
        with open(SCIEZKA_PLIKU_JSON, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        questions.clear()
        questions.extend(loaded)
        tree.delete(*tree.get_children())
        for q in questions:
            tree.insert('', 'end', values=(q['text'], q['type'], q.get('options', ''), q.get('correct', '')))

    # Usuwanie zaznaczonego pytania
    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Zaznacz pytanie do usunięcia")
            return
        for item in selected:
            values = tree.item(item, 'values')
            tree.delete(item)
            questions[:] = [q for q in questions if q['text']]
    # Przyciski funkcyjne
    tk.Button(edytor, text="Dodaj Pytanie", command=add_question, fg="#d9dad9", bg="#750006", font='Georgia', width=20, height=1).pack(pady=5)
    tk.Button(edytor, text="Zapisz do pliku", command=save_to_file, fg="#d9dad9", bg="#750006", font='Georgia', width=20, height=1).pack(pady=5)
    tk.Button(edytor, text="Wczytaj z pliku", command=load_from_file, fg="#d9dad9", bg="#750006", font='Georgia', width=20, height=1).pack(pady=5)
    tk.Button(edytor, text="Usuń zaznaczone pytanie", command=delete_selected, fg="#d9dad9", bg="#750006", font='Georgia', width=20, height=1).pack(pady=5)
    tk.Button(edytor, text="Powrót", command=lambda: [edytor.destroy(), prowadzacy_window.uruchom_okno_prowadzacy()], fg="#d9dad9", bg="#750006", font='Georgia', width=20, height=1).pack(pady=10)

    # Automatyczne wczytanie pytań przy starcie
    load_from_file()

    edytor.mainloop()
