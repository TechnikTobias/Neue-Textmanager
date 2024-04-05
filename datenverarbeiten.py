import os
import sqlite3
import tkinter as tk
from tkinter import *

import Neue_Textmanager

Speicherort = os.path.dirname(os.path.abspath(__file__))


# Datenbankverbindung
def get_db_connection():
    conn = sqlite3.connect(f"{Speicherort}/Textmanager Daten/Lieder Datenbank/Lieder Datenbank.db")
    return conn


def add_or_edit_song(song_id=None):
    def save_song():
        nonlocal song_id
        book_name = book_name_entry.get()
        song_number = song_number_entry.get()
        Uhrheberecht = Uhrheberecht_strinVar.get()
        min_vers = min_vers_entry.get()
        song_name = song_name_entry.get()
        conn = get_db_connection()
        cursor = conn.cursor()
        if not book_name or not song_number or not Uhrheberecht or not min_vers or not song_name:
            return


        if song_id:
            cursor.execute("UPDATE songs SET  Uhrheberecht = ?, min_vers = ?, song_name = ? WHERE song_number = ? AND book_name = ?", (Uhrheberecht, min_vers, song_name, song_number, book_name))
        else:
    

            cursor.execute("SELECT song_id FROM songs WHERE book_name = ? AND song_number = ?", (book_name, song_number))
            lied = cursor.fetchall()
            if not lied:



                    cursor.execute("INSERT INTO songs (book_name, song_number, Uhrheberecht, min_vers, song_name) VALUES (?, ?, ?, ?, ?)", (book_name, song_number, Uhrheberecht, min_vers, song_name))
            else:
                error_window = Toplevel(window)
                error_window.title("Errormeldung")
                error_window.geometry('400x200')
                error = Label(error_window, text="Das Lied exesistiert schon bitte anders lied eingeben oder nicht speichern")
                error.pack()
                return
        # Verse speichern oder aktualisieren
        for i, verse_widget in enumerate(verse_widgets):
            verse_text = verse_widget.get("1.0", "end-1c").strip()
            if verse_text:
                cursor.execute("SELECT verse_id FROM verses WHERE song_number = ? AND verse_number = ? AND book_name = ?", (song_number, i + 1, book_name))
                verse = cursor.fetchone()
                if verse:  # Update existing verse
                    cursor.execute("UPDATE verses SET verse_text = ? WHERE verse_id = ?" , (verse_text, verse[0]))
                else:  # Insert new verse
                    cursor.execute("INSERT INTO verses (song_number, verse_number, verse_text, book_name) VALUES (?, ?, ?, ?)", (song_number, i + 1, verse_text, book_name))

        conn.commit()
        conn.close()
        edit_window.destroy()
        view_songs()



    edit_window = Toplevel(window)
    edit_window.title("Lied Bearbeiten" if song_id else "Lied Hinzufügen")
    edit_window.geometry('1000x400')

    top_frame = tk.Frame(edit_window)
    top_frame.pack()


    book_name_label = tk.Label(top_frame, text="Buchname:")
    book_name_label.pack(side=tk.LEFT)
    book_name_entry = tk.Entry(top_frame)
    book_name_entry.pack(side=tk.LEFT)

    song_number_label = tk.Label(top_frame, text="Liednummer:")
    song_number_label.pack(side=tk.LEFT)
    song_number_entry = tk.Entry(top_frame)
    song_number_entry.pack(side=tk.LEFT)

    Uhrheberecht_wahl = ["Geschüschtz", "Nicht geschütz"]
    Uhrheberecht_strinVar = StringVar()
    Uhrheberecht_strinVar.set(Uhrheberecht_wahl[1])
    Uhrheberecht_optionMenü = OptionMenu(top_frame, Uhrheberecht_strinVar, *Uhrheberecht_wahl)
    Uhrheberecht_optionMenü.pack(side=tk.LEFT)


    min_vers_lable = Label(top_frame, text="Mindest Versanzahl")
    min_vers_lable.pack(side=tk.LEFT)
    min_vers_entry = tk.Entry(top_frame)
    min_vers_entry.pack(side=tk.LEFT)

    song_name_lable = Label(top_frame, text="Liedname")
    song_name_lable.pack(side=tk.LEFT)
    song_name_entry = tk.Entry(top_frame, width=30)
    song_name_entry.pack(side=tk.LEFT)

    canvas = tk.Canvas(edit_window)
    scrollbar = tk.Scrollbar(edit_window, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)

    verse_frame = tk.Frame(canvas)  # Rahmen für Verse
    canvas.create_window((0, 0), window=verse_frame, anchor="nw")
    verse_widgets = []  # Liste, um die Textfelder zu speichern
    if song_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_name, song_number, Uhrheberecht, min_vers, song_name FROM songs WHERE song_number = ? AND book_name = ?", (song_id[1], song_id[0]))
        song = cursor.fetchone()
        book_name_entry.insert(0, song[0])
        song_number_entry.insert(0, song[1])
        if song[2]:
            Uhrheberecht_strinVar.set(song[2])
        if song[3]:
            min_vers_entry.insert(0, song[3])
        if song[4]:
            song_name_entry.insert(0, song[4])

        cursor.execute("SELECT verse_text FROM verses WHERE song_number = ? AND book_name = ?", (song_id[1], song_id[0]))
        verses = cursor.fetchall()
        for i, verse_text in enumerate(verses):
            verse_widget = tk.Text(verse_frame, font=("Helvetica", 10), height=12, width=44)
            verse_widget.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            verse_widget.insert(tk.END, verse_text[0])
            verse_widgets.append(verse_widget)

        conn.close()

    verse_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Zusätzliche leere Eingabefelder für neue Verse
    for i in range(len(verse_widgets), 9):
        verse_widget = tk.Text(verse_frame, font=("Helvetica", 10), height=12, width=44)
        verse_widget.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        verse_widgets.append(verse_widget)

    save_button = tk.Button(edit_window, text="Speichern", command=save_song)
    save_button.pack()


# Verse hinzufügen oder bearbeiten
def add_or_edit_verses(song_id):
    def save_verses():
        for i, verse_entry in enumerate(verse_entries):
            verse_text = verse_entry.get()
            if verse_text:
                if verse_ids[i]:
                    cursor.execute("UPDATE verses SET verse_text = ? WHERE verse_id = ?", (verse_text, verse_ids[i]))
                else:
                    cursor.execute("INSERT INTO verses (song_id, verse_number, verse_text) VALUES (?, ?, ?)", (song_id, i + 1, verse_text))
        conn.commit()
        verses_window.destroy()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT verse_id, verse_text FROM verses WHERE song_id = ? ORDER BY verse_number", (song_id,))
    verses = cursor.fetchall()

    verses_window = Toplevel(window)
    verses_window.title("Verse Bearbeiten")

    verse_entries = []
    verse_ids = []
    for verse_id, verse_text in verses:
        verse_entry = tk.Entry(verses_window)
        verse_entry.insert(0, verse_text)
        verse_entry.pack()
        verse_entries.append(verse_entry)
        verse_ids.append(verse_id)

    # Add empty entries for new verses
    for _ in range(len(verse_entries), 9):
        verse_entry = tk.Entry(verses_window)
        verse_entry.pack()
        verse_entries.append(verse_entry)
        verse_ids.append(None)

    save_button = tk.Button(verses_window, text="Speichern", command=save_verses)
    save_button.pack()

# Lieder anzeigen
def view_songs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_name, song_number, song_name FROM songs")
    songs = cursor.fetchall()
    conn.close()

    song_list.delete(0, tk.END)
    for song in songs:
        song_list.insert(tk.END, (song[0],song[1] ,song[2]))

# Lied auswählen und bearbeiten
def edit_selected_song():
    selected = song_list.curselection()
    if selected:
        song_id = song_list.get(selected)
        add_or_edit_song(song_id)


def display_verses():
    selected = song_list.curselection()  # Abrufen der ausgewählten Song-ID direkt aus der Listbox
    if selected:
        selected_song_id = song_list.get(selected[0])  # Extrahieren der ausgewählten Song-ID
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT verse_text FROM verses WHERE song_id = ? AND book_name = ?", (selected_song_id[2],selected_song_id[1]))
        #cursor.execute("SELECT verse_text FROM verses WHERE song_id = ? AND verse_number = ? AND book_name", (selected_song_id,))
        verses = cursor.fetchall()
        conn.close()

        verses_window = Toplevel(window)
        verses_window.title("Verse Anzeigen")

        verse_text_display = tk.Text(verses_window, font=("Helvetica", 12), wrap=tk.WORD, height=20, width=50)
        verse_text_display.pack()

        for verse in verses:
            verse_text_display.insert(tk.END, verse[0] + "\n\n")
        

        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect("deine_datenbank.db")
        cursor = conn.cursor()

        # SQL-Abfrage, um alle einzigartigen Bücher zu ermitteln
        unique_books_query = "SELECT DISTINCT buch FROM deine_tabelle"
        cursor.execute(unique_books_query)
        unique_books = cursor.fetchall()

        # Schleife über jedes einzigartige Buch
        for book in unique_books:
            # Buchname extrahieren (nehmen Sie an, dass der Buchname im ersten Element der Tupel ist)
            book_name = book[0]
            
            # SQL-Abfrage zum Löschen aller vorhandenen Daten für dieses Buch
            delete_query = f"DELETE FROM deine_tabelle WHERE buch = ?"
            cursor.execute(delete_query, (book_name,))
            
            # SQL-Abfrage zum Einfügen der sortierten Daten für dieses Buch
            insert_query = f"INSERT INTO deine_tabelle SELECT * FROM deine_tabelle WHERE buch = ? ORDER BY buch"
            cursor.execute(insert_query, (book_name,))
            
        # Bestätige die Änderungen und schließe die Verbindung zur Datenbank
        conn.commit()
        conn.close()



# Haupt UI Setup
def setup_ui():
    global window, song_list
    window = tk.Toplevel(Neue_Textmanager.Textmanager)
    window.title("Lieder Datenbank")

    song_list = tk.Listbox(window, width=50, height=10)
    song_list.pack()

    tk.Button(window, text="Lied Hinzufügen", command=lambda: add_or_edit_song()).pack()
    tk.Button(window, text="Lied Bearbeiten", command=edit_selected_song).pack()
    
    view_songs()
    
# Hauptprogramm
if __name__ == "__main__":
    setup_ui()