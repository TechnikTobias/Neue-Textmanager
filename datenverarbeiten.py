import sqlite3
import tkinter as tk
from tkinter import *

# Datenbankverbindung
def get_db_connection():
    conn = sqlite3.connect("C:\\Users\\tobia\\Github\\Neue Textmanager\\Textmanager Daten\\Lieder Datenbank\\Lieder Datenbank.db")
    return conn


def add_or_edit_song(song_id=None):
    def save_song():
        nonlocal song_id  # Deklariert, dass song_id aus der umschließenden Funktion verwendet wird
        book_name = book_name_entry.get()
        song_number = song_number_entry.get()

        if book_name and song_number:
            conn = get_db_connection()
            cursor = conn.cursor()
            if song_id:  # Update existing song
                cursor.execute("UPDATE songs SET book_name = ?, song_number = ? WHERE song_id = ?", (book_name, song_number, song_id))
            else:  # Add new song
                cursor.execute("INSERT INTO songs (book_name, song_number) VALUES (?, ?)", (book_name, song_number))
                song_id = cursor.lastrowid  # Erfasst die song_id für neue Lieder

            # Verse speichern oder aktualisieren
            for i, verse_entry in enumerate(verse_widget):
                verse_text = verse_entry.get()
                if verse_text:
                    cursor.execute("REPLACE INTO verses (song_id, verse_number, verse_text) VALUES (?, ?, ?)", (song_id, i + 1, verse_text))

            conn.commit()
            conn.close()
            edit_window.destroy()
            view_songs()


    edit_window = Toplevel(window)
    edit_window.title("Lied Bearbeiten" if song_id else "Lied Hinzufügen")
    edit_window.geometry('600x400')

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

    verse_frame = tk.Frame(edit_window)  # Rahmen für Verse
    verse_frame.pack(expand=True, fill='both')

    verse_widgets = []  # Liste, um die Textfelder zu speichern
    if song_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_name, song_number FROM songs WHERE song_id = ?", (song_id,))
        song = cursor.fetchone()
        book_name_entry.insert(0, song[0])
        song_number_entry.insert(0, song[1])

        cursor.execute("SELECT verse_text FROM verses WHERE song_id = ? ORDER BY verse_number", (song_id,))
        verses = cursor.fetchall()
        for i, verse_text in enumerate(verses):
            verse_widget = tk.Text(verse_frame, font=("Helvetica", 10), height=12, width=44)
            verse_widget.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            verse_widget.insert(tk.END, verse_text[0])
            verse_widgets.append(verse_widget)

        conn.close()

    # Zusätzliche leere Eingabefelder für neue Verse
    for i in range(len(verse_widgets), 9):
        verse_widget = tk.Text(verse_frame, font=("Helvetica", 10), height=12, width=44)
        verse_widget.grid(row=i // 2, column=i % 2, padx=5, pady=5)
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
    cursor.execute("SELECT song_id, book_name, song_number FROM songs")
    songs = cursor.fetchall()
    conn.close()

    song_list.delete(0, tk.END)
    for song in songs:
        song_list.insert(tk.END, (song[0], f"{song[1]} - Lied {song[2]}"))

# Lied auswählen und bearbeiten
def edit_selected_song():
    selected = song_list.curselection()
    if selected:
        song_id = song_list.get(selected[0])[0]
        add_or_edit_song(song_id)

# Haupt UI Setup
def setup_ui():
    global window, song_list
    window = tk.Tk()
    window.title("Lieder Datenbank")

    song_list = tk.Listbox(window)
    song_list.pack()

    tk.Button(window, text="Lied Hinzufügen", command=lambda: add_or_edit_song()).pack()
    tk.Button(window, text="Lied Bearbeiten", command=edit_selected_song).pack()
    tk.Button(window, text="Lieder Anzeigen", command=view_songs).pack()

    window.mainloop()

# Hauptprogramm
if __name__ == "__main__":
    setup_ui()