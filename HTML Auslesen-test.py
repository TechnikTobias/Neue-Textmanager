"""
import os
import sqlite3
from bs4 import BeautifulSoup
# Funktion zum Parsen einer HTML-Datei
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Entfernen des ersten <div>-Tags mit der ID "navbar"
    navbar_div = soup.find('div', id='navbar')
    if navbar_div:
        navbar_div.decompose()

    # Extrahieren des Buchnamens aus dem <title>-Tag
    title_tag = soup.find('title')
    if title_tag:
        full_title = title_tag.text.strip()
        # Der Buchname ist der zweite Teil, getrennt durch " – "
        book_name = full_title.split(' – ')[1].strip()
    else:
        raise ValueError("Kein <title>-Tag gefunden.")

    # Extrahieren der Kapitelnummer aus dem <h1>-Tag
    h1_tag = soup.find('h1')
    if h1_tag and h1_tag.text:
        h1_text = h1_tag.text.strip()
        parts = h1_text.split()
        if len(parts) > 1 and parts[-1].isdigit():
            chapter = int(parts[-1])
            cut_book = str(parts[0])
        else:
            raise ValueError(f"Kapitelnummer konnte nicht aus '{h1_text}' extrahiert werden.")
    else:
        raise ValueError("Kein <h1>-Tag oder kein Text im <h1>-Tag gefunden.")

    # Liste zur Speicherung der Verse
    verses = []

    # Durchsuchen aller <div>-Tags mit der Klasse "v"
    for verse in soup.find_all('div', class_='v'):
        # Überspringen von <h2> und <h4>-Tags (Überschriften)
        for header in verse.find_all(['h2', 'h4', 'h1', 'h3', 'h5', 'h6', 'h7']):
            header.decompose()
        verse_number_tag = verse.find('span', class_='vn')
        if verse_number_tag:
            verse_number = int(verse_number_tag.text.strip())
            verse_text = verse.get_text(separator=' ', strip=True).split(' ', 1)[1]
            verses.append((book_name, cut_book, chapter, verse_number, verse_text))
        else:
            raise ValueError("Kein <span>-Tag mit der Klasse 'vn' im Vers gefunden.")
    
    return verses

# Funktion zum Erstellen der SQLite-Datenbank
def create_database(db_name='bible.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bible (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book TEXT NOT NULL,
            cut_book TEXT NOT NULL,
            chapter INTEGER NOT NULL,
            verse INTEGER NOT NULL,
            text TEXT NOT NULL,
            UNIQUE(book, chapter, verse)
        )
    ''')
    
    conn.commit()
    conn.close()

# Funktion zum Einfügen der Verse in die Datenbank
def insert_verses(verses, db_name='bible.db'):
    create_database()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.executemany('''
        INSERT OR IGNORE INTO bible (book, cut_book, chapter, verse, text)
        VALUES (?, ?, ?, ?, ?)
    ''', verses)
    
    conn.commit()
    conn.close()

# Funktion zum Verarbeiten aller HTML-Dateien in einem Ordner
def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            try:
                verses = parse_html(file_path)
                insert_verses(verses)
                # Einmalige Ausgabe: Buch, Kapitel, erster Vers und seine Versnummer

            except ValueError as e:
                print(f'Fehler in Datei {filename}: {e}')

# Pfad zum Ordner mit den HTML-Dateien
folder_path = '/home/tobias/Github/Neue-Textmanager/NeUe-RoundtripHTML/ot'
process_folder(folder_path)

# Suchfunktion zum Finden von Versen in der Datenbank
def search_verse(book, chapter, verse, db_name='bible.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT text
        FROM bible
        WHERE book = ? AND chapter = ? AND verse = ?
    ''', (book, chapter, verse))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return "Vers nicht gefunden."

# Beispielaufruf der Suchfunktion
book = 'Chronik (I)'
chapter = 7
verse = 1
import sqlite3

# Funktion zur Aktualisierung der Abkürzungen in der Datenbank
def update_abbreviations(db_name='bible.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Aktualisieren der Abkürzungen in der Datenbank
    cursor.execute('UPDATE bible SET cut_book = "Joh" WHERE cut_book = "Jo"')
    cursor.execute('UPDATE bible SET cut_book = "1Joh" WHERE cut_book = "1Jo"')
    
    conn.commit()
    conn.close()

# Aktualisieren der Abkürzungen in der Datenbank
update_abbreviations()

"""
import sqlite3
import tkinter as tk
from tkinter import ttk

def search_verse():
    selected_book = book_combobox.get()
    selected_chapter = chapter_entry.get()
    selected_verse = verse_entry.get()
    result = search_verse_in_database(selected_book, selected_chapter, selected_verse)
    if result:
        verse_text.set(result)
    else:
        verse_text.set("Vers nicht gefunden.")

def search_verse_in_database(book, chapter, verse):
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT text
        FROM bible
        WHERE book = ? AND chapter = ? AND verse = ?
    ''', (book, chapter, verse))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

# GUI erstellen
root = tk.Tk()
root.title("Bible Search")

# Label und Dropdown-Menü für die Auswahl des Buches
book_label = ttk.Label(root, text="Buch:")
book_label.grid(row=0, column=0, padx=5, pady=5)

# Bücher aus der Datenbank auslesen
conn = sqlite3.connect('bible.db')
cursor = conn.cursor()
cursor.execute('SELECT DISTINCT book FROM bible')
books_from_db = [book[0] for book in cursor.fetchall()]
conn.close()

book_combobox = ttk.Combobox(root, values=books_from_db)
book_combobox.grid(row=0, column=1, padx=5, pady=5)
book_combobox.current(0)

# Eingabefelder für Kapitel und Vers
chapter_label = ttk.Label(root, text="Kapitel:")
chapter_label.grid(row=1, column=0, padx=5, pady=5)
chapter_entry = ttk.Entry(root)
chapter_entry.grid(row=1, column=1, padx=5, pady=5)

verse_label = ttk.Label(root, text="Vers:")
verse_label.grid(row=2, column=0, padx=5, pady=5)
verse_entry = ttk.Entry(root)
verse_entry.grid(row=2, column=1, padx=5, pady=5)

# Suchen-Button
search_button = ttk.Button(root, text="Suchen", command=search_verse)
search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Anzeige des Verses
verse_text = tk.StringVar()
verse_label = ttk.Label(root, textvariable=verse_text, wraplength=400)
verse_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()

