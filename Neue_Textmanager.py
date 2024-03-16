from tkinter import *
import os
import sqlite3

import Settings
import Kamera
import Lied_Kontrolle
import Load_settings

Speicherort = os.path.dirname(os.path.abspath(__file__))
factor = 1.2

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
    Textmanager.bind("<Configure>", on_resize)
    Menu_generator()
    Load_Setting()

    for pos,i in enumerate (input_lieder):
        alle_inhalt.append(gegerator_lieder(i, pos, factor))



def on_resize(event):
    with_size= Textmanager.winfo_width()
    hight_size = Textmanager.winfo_height()
    posistion(with_size, hight_size,factor)


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



def gegerator_lieder(input, pos, factor):
    ja = input.split(",")
    name_lied = ja[0].split(":")
    aktion = ja[1].split(":")
    inhalt = []
    inhalt.append(aktion[1])
    Lied_start = Label(Textmanager, text=name_lied[1])
    inhalt.append(Lied_start)
    if aktion[1] == " Textwort":
        Button_Textwrt = Button(Textmanager, text="Textwort")
        #Button_Textwrt.place(relx=0,rely=0.05,relwidth=0.02, relheight=0.01)
        inhalt.append(Button_Textwrt)
    elif aktion[1] == " Lied":
        Lable_Kamer = Button(Textmanager, text="Kamera", border=0)
        inhalt.append(Lable_Kamer)
        befehle = ["Kamera", "Textwort", "Lied"]
        clicked = StringVar()
        clicked.set(befehle[0])
        opt = OptionMenu(Textmanager, clicked, *befehle)
        opt.config(font=('Helvetica', 15), fg="black", bg="white")
        inhalt.append(opt)
        eingabe_Lied = Entry(Textmanager)
        eingabe_Lied.bind("<KeyRelease>", eingabe_änderung)
        inhalt.append(eingabe_Lied)
        eingabe_Vers = Entry(Textmanager)
        inhalt.append(eingabe_Vers)
        befehle_buch = ["Kamera", "Textwort", "Lied"]
        clicked_buch = StringVar()
        clicked_buch.set(befehle[0])
        opt_buch = OptionMenu(Textmanager, clicked_buch, *befehle_buch)
        opt_buch.config(font=('Helvetica', 15), fg="black", bg="white", )
        inhalt.append(opt_buch)
        Tex_lied_lable = Label(Textmanager)
        inhalt.append(Tex_lied_lable)
    elif aktion[1] == " Kamera":
        lied_weiter = Button(Textmanager, text= "servus", border=0)
        inhalt.append(lied_weiter)
    return inhalt


def eingabe_änderung(event):
    print(True)


def posistion(fenster_width, fenster_height, factor):
    for pos, i in enumerate (alle_inhalt):
        text_size = min( int(i[1].winfo_height()/3*factor), int(i[1].winfo_width()/10*factor))
        i[1].config(font=('Helvetica', text_size))
        if pos == 0:
            i[1].place(x= 0, y= 0,relwidth=0.15*factor, relheight=0.05*factor)
            i[1].config(font=('Helvetica', text_size))
        else:
            i[1].place(x= 0, y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[1].config(font=('Helvetica', text_size))
        if i[0] == " Textwort":
            pass
        elif i[0] == " Lied":
            i[2].place(x= 0, y= pos*(i[1].winfo_height()+1)*2+i[1].winfo_height()+1,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].config(font=('Helvetica', text_size))
            i[3].place(x= (i[1].winfo_width()+1), y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[3].config(font=('Helvetica', text_size))
            i[4].place(x= (i[1].winfo_width()+2+i[2].winfo_width()), y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[4].config(font=('Helvetica', text_size))
            i[5].place(x= (i[1].winfo_width()+2+i[2].winfo_width()), y= pos*(i[1].winfo_height()+1)*2+i[1].winfo_height()+1,relwidth=0.15*factor, relheight=0.05*factor)
            i[5].config(font=('Helvetica', text_size))
            i[6].place(x= i[1].winfo_width()+2+i[3].winfo_width()+2+i[4].winfo_width(), y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[7].place(x= i[1].winfo_width()+2+i[3].winfo_width()+2+i[4].winfo_width()+2+i[6].winfo_width(), y= pos*(i[1].winfo_height()+1)*2,relwidth=0.15*factor, relheight=0.05*factor)
        elif i[0] == " Kamera":
            i[2].place(x= 0, y= pos*(i[1].winfo_height()+1)*2+i[1].winfo_height()+1,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].config(font=('Helvetica', text_size))

