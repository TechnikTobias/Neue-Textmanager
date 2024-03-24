import sqlite3 as db

conn = db.connect("C:\\Users\\tobia\\Github\\Neue Textmanager\\Textmanager Daten\\Lieder Datenbank\\Textmanager Datenbank.db")
cursor = conn.cursor()


def Suche_Lieder(Datenbank="Lieder", Versnummer="Vers 1", Buch="Gesangbuch", Liednummer=1):
    cursor.execute("SELECT * FROM {} WHERE Verse LIKE ? AND Liednummer = ? AND Buch = ?".format(Datenbank), ('%{}%'.format(Versnummer), Liednummer, Buch))
    ergebniss = cursor.fetchall()
    verse = []
    for ergebnis in ergebniss:
        verse = verse+[ergebnis[2]]
    return verse

def Eingabe_Lieder(Datenbank, Versnummer, Buch, Liednummer):
    cursor.execute("INSERT INTO {} (Verse, Liednummer, Buch) VALUES (?,?,?)".format(Datenbank), (Versnummer, Liednummer, Buch))
    conn.commit()
    print("fertig")

#print(Suche_Lieder(Liednummer=146, Buch="Chorbuch", Versnummer="")[0])

#Buch = "Gesangbuch"
#Lied = 1
#Vers = 1
#Text = open(f"C:\\Users\\tobia\\Desktop\\Lieder\\Buch\\{Buch}\\{Lied} Vers {Vers}.txt", 'r', encoding='utf8')
#Nummer = 1  # Startnummer

# Die Liste der Versnummern oder Dateinamen, die du verarbeiten möchtest
#versnummern = [1,2,3,4,5,6,7,8,9]  # Füge hier die gewünschten Versnummern hinzu

# Die Liste der Lieder (Liednummer) von 1 bis 430
#liednummern = range(1, 446)

# Die Liste der Verse, die du verarbeiten möchtest
#for Liednummer in liednummern:
    #for Versnummer in versnummern:
        #try:
            #Buch = "Chorbuch"  # Setze das Buch entsprechend deiner Dateistruktur

            #with open(f"C:\\Users\\tobia\\Desktop\\Lieder\\Buch\\{Buch}\\{Liednummer} Vers {Versnummer}.txt", 'r', encoding='utf8') as Text:
                #Vers = Text.read()

            #Eingabe_Lieder(Liednummer=Liednummer, Versnummer=Vers, Buch=Buch, Datenbank="Lieder")
        #except FileNotFoundError:
            #print(f"Datei für Lied {Liednummer}, Vers {Versnummer} nicht gefunden.")

import tkinter as tk
from tkinter import ttk
import sqlite3


# Funktion zum Laden der Lieder aus der Datenbank
def lade_lieder():
    cursor.execute("SELECT * FROM Lieder")
    lieder = cursor.fetchall()
    return lieder

# Funktion zum Speichern der Änderungen
def speichern():
    selected_lied = lieder_listbox.get(lieder_listbox.curselection())  # Ausgewähltes Lied
    neuer_liedname = lied_name_entry.get()  # Neuer Liedname
    neuer_liednummer = lied_nummer_entry.get()  # Neue Liednummer
    neuer_buch = buch_entry.get()  # Neues Buch
    neuer_inhalt = lied_inhalt_entry.get()  # Neuer Liedinhalt

    # Änderungen in der Datenbank speichern
    cursor.execute("UPDATE Lieder SET  Liednummer = ?, Buch = ?, Versnummer = ? WHERE Liednummer = ?",
                   (neuer_liednummer, neuer_buch, neuer_inhalt, selected_lied))
    conn.commit()

    # Aktualisiere die Anzeige
    aktualisiere_anzeige()
    print(f"Lied '{selected_lied}' wurde aktualisiert.")

# Funktion zum Anzeigen des Bearbeitungsfensters
def bearbeiten():
    selected_lied = lieder_listbox.get(lieder_listbox.curselection())  # Ausgewähltes Lied
    print(selected_lied)
    bearbeiten_fenster = tk.Toplevel(root)
    bearbeiten_fenster.title(f"Lied '{selected_lied}' bearbeiten")

    # Eingabefelder für die vier Spalten
    lied_name_label = tk.Label(bearbeiten_fenster, text="Neuer Liedname:")
    lied_name_label.pack()
    lied_name_entry = tk.Entry(bearbeiten_fenster)
    lied_name_entry.pack()

    lied_nummer_label = tk.Label(bearbeiten_fenster, text="Neue Liednummer:")
    lied_nummer_label.pack()
    lied_nummer_entry = tk.Entry(bearbeiten_fenster)
    lied_nummer_entry.pack()

    buch_label = tk.Label(bearbeiten_fenster, text="Neues Buch:")
    buch_label.pack()
    buch_entry = tk.Entry(bearbeiten_fenster)
    buch_entry.pack()

    lied_inhalt_label = tk.Label(bearbeiten_fenster, text="Neuer Liedinhalt:")
    lied_inhalt_label.pack()
    lied_inhalt_entry = tk.Entry(bearbeiten_fenster)
    lied_inhalt_entry.pack()

    # Daten für das ausgewählte Lied aus der Datenbank abrufen
    cursor.execute("SELECT * FROM Lieder WHERE Liednummer = ?", (selected_lied,))
    lied_daten = cursor.fetchone()
    if lied_daten:
        lied_name_entry.insert(0, lied_daten[1])  # Hier steht der Name an zweiter Stelle (Index 1)
        lied_nummer_entry.insert(0, lied_daten[2])  # Index 2 für Liednummer
        buch_entry.insert(0, lied_daten[0])  # Index 3 für Buch

    # Button zum Speichern der Änderungen
    speichern_button = tk.Button(bearbeiten_fenster, text="Änderungen speichern", command=speichern)
    speichern_button.pack()

    # Aktualisiere die Anzeige beim Start
    aktualisiere_anzeige()

# Funktion zum Aktualisieren der Anzeige
def aktualisiere_anzeige():
    lieder_listbox.delete(0, tk.END)
    lieder = lade_lieder()
    for lied in lieder:
        lieder_listbox.insert(tk.END, f"{lied[0]} | {lied[1]} | {lied[2]}")

# Tkinter-App erstellen
root = tk.Tk()
root.title("Lieder bearbeiten")

# Liste der Lieder aus der Datenbank laden
lieder_listbox = tk.Listbox(root)
lieder_listbox.config(width=100)
lieder = lade_lieder()
for lied in lieder:
    lieder_listbox.insert(tk.END, f"{lied[0]} | {lied[1]} | {lied[2]}")
lieder_listbox.pack()

# Button zum Öffnen des Bearbeitungsfensters
bearbeiten_button = tk.Button(root, text="Lied bearbeiten", command=bearbeiten)
bearbeiten_button.pack()

# Aktualisiere die Anzeige beim Start
aktualisiere_anzeige()

root.mainloop()

# Verbindung zur Datenbank schließen
conn.close()