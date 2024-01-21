import sqlite3 as db

connector = db.connect("C:\\Users\\tobia\\Github\\Neue Textmanager\\Textmanager Daten\\Lieder Datenbank\\Textmanager Datenbank.db")
cursor = connector.cursor()


def Suche_Lieder(Datenbank="Lieder", Versnummer="Vers 1", Buch="Gesangbuch", Liednummer=1):
    cursor.execute("SELECT * FROM {} WHERE Verse LIKE ? AND Liednummer = ? AND Buch = ?".format(Datenbank), ('%{}%'.format(Versnummer), Liednummer, Buch))

Suche_Lieder(Datenbank="Lieder", Versnummer=2, Liednummer=1, Buch="Gesangbuch")
ergebniss = cursor.fetchall()

for ergebnis in ergebniss:
    print(ergebnis[2])