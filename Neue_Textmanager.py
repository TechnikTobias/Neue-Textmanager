from tkinter import *
import os
import sqlite3

import Settings
import Kamera
import Lied_Kontrolle
import Load_settings

Speicherort = os.path.dirname(os.path.abspath(__file__))


conn = sqlite3.connect(f"{Speicherort}\\Textmanager Daten\\Lieder Datenbank\\Lieder Datenbank.db")
cursor = conn.cursor()
cursor.execute("SELECT supjekt FROM Einstellungen WHERE name = ?", ("Ablauf",))
verses = cursor.fetchall()
input_lieder = (str(verses[0]).split("!"))
zeichen_zum_entfernen = "'()"

# Entferne die Zeichen aus dem String
input_lieder = [element.translate({ord(zeichen): None for zeichen in zeichen_zum_entfernen}) for element in input_lieder]
All_entitie_save = []

Programm_ort = os.path.dirname(os.path.abspath(__file__))


def Start():
    global Textmanager, alle_inhalt
    alle_inhalt = []
    Settings.Check_settings(Tkfont=False)
    Textmanager = Tk()
    Textmanager.title("Textmanager")
    Textmanager.config(bg=Settings.Textmanager_Hintergrund)
    Textmanager.geometry("1040x800")
    Textmanager.iconbitmap(f"{Programm_ort}\\Bild.ico")
    Textmanager.bind("<F11>", Settings.Test)
    Menu_generator()
    Load_Setting()

    for pos,i in enumerate (input_lieder):
        alle_inhalt.append(gegerator_lieder(i))
    posistion()

def Menu_generator():
    global Menu_Settings, Menu_Info, Menu_Kamera, Menu_LiedKontrolle, Menu_Help
    Menu_Settings = Menu(Textmanager, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0, borderwidth=0, tearoff=False)
    Menu_Info = Menu(Menu_Settings, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0, borderwidth=0, tearoff=False)
    Menu_Kamera = Menu(Menu_Settings, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0, borderwidth=0, tearoff=False)
    Menu_LiedKontrolle = Menu(Menu_Settings, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0, borderwidth=0, tearoff=False)
    Menu_Help = Menu(Menu_Settings, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0, borderwidth=0, tearoff=False)
    Menu_Settings.add_cascade(label="Info", menu=Menu_Info)
    Menu_Settings.add_cascade(label="Kamera", menu=Menu_Kamera)
    Menu_Settings.add_cascade(label="Lied Kontrolle", menu=Menu_LiedKontrolle)
    Menu_Settings.add_cascade(label="Hilfe", menu=Menu_Help)
    Menu_Info.add_command(label="Einstellungen", command=Settings.make_settings)
    Menu_Info.add_command(label= "Info", command=Settings.Info)
    Menu_Kamera.add_command(label="Einstellungen", command=Kamera.Settings)
    Menu_Kamera.add_command(label="Position", command=Kamera.Position)
    Menu_LiedKontrolle.add_command(label="Einstellungen", command=Lied_Kontrolle.Settings)
    Menu_LiedKontrolle.add_command(label="Lied Kontrolieren", command=Lied_Kontrolle.controll)
    Menu_Help.add_command(label="Hilfe")
    Textmanager.config(menu=Menu_Settings)

def Load_Setting():
    Settings.Check_settings()
    Load_settings.Load_Text_anzeiger()
    Load_settings.Load_all_collor()



def gegerator_lieder(input):
    ja = input.split(",")
    name_lied = ja[0].split(":")
    aktion = ja[1].split(":")
    inhalt = []
    main = Label(Textmanager, width=500, height=30, font=("Helvetica", 1))
    Lied_start = Button(main, text=name_lied[1])
    Lied_start.place(relx=0,rely=0)
    if aktion[1] == " Textwort":
        Button_Textwrt = Button(main, text="Textwort")
        Button_Textwrt.place(relx=0,rely=0.45)
    elif aktion[1] == " Kamera":
        Lable_Kamer = Label(main, text="Kamera")
        Lable_Kamer.place(relx=0,rely=0.45)
    elif aktion[1] == " Lied":
        lied_weiter = Button(main, text= "servus")
        lied_weiter.place(relx=0,rely=0.45)
    inhalt.append(main)
    return inhalt


def posistion():
    for pos, i in enumerate (alle_inhalt):
        for o in i:
            o.place(y=pos*80)


