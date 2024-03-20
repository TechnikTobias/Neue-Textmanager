from tkinter import *
import os
import sqlite3

import Settings
import Kamera
import datenverarbeiten
import Load_settings

Speicherort = os.path.dirname(os.path.abspath(__file__))
factor = 1

def Einstellung_laden(Einstellugen_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT supjekt FROM Einstellungen WHERE name = ?", (Einstellugen_name,))
    verses = cursor.fetchall()
    input_lieder = (str(verses[0]).split("!"))
    zeichen_zum_entfernen = "'()"
    input_lieder = [element.translate({ord(zeichen): None for zeichen in zeichen_zum_entfernen}) for element in input_lieder]
    return input_lieder

def get_db_connection():
    conn = sqlite3.connect(f"{Speicherort}\\Textmanager Daten\\Lieder Datenbank\\Lieder Datenbank.db")
    return conn

def Start():
    global Textmanager, alle_inhalt
    alle_inhalt = []
    Settings.Check_settings(Tkfont=False)
    Textmanager = Tk()
    Textmanager.title("Textmanager")
    Textmanager.config(bg=Settings.Textmanager_Hintergrund)
    Textmanager.geometry("1040x800")
    Textmanager.iconbitmap(f"{Speicherort}\\Bild.ico")
    Textmanager.bind("<F11>", Settings.Test)
    Textmanager.bind("<Configure>", on_resize)
    Menu_generator()
    Load_Setting()

    for pos,i in enumerate (Einstellung_laden("Ablauf")):
        alle_inhalt.append(gegerator_lieder(i, pos, factor))
    eingabe_änderung("hallo")
    alle_inhalt.append(button_generator())



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
    Menu_LiedKontrolle.add_command(label="Einstellungen", )
    Menu_LiedKontrolle.add_command(label="Lied Kontrolieren", command=datenverarbeiten.setup_ui)
    Menu_Help.add_command(label="Hilfe")
    Textmanager.config(menu=Menu_Settings)

def Load_Setting():
    Settings.Check_settings()
    Load_settings.Load_Text_anzeiger()
    Load_settings.Load_all_collor()


def button_generator():
    rückgabe = []
    rückgabe.append("Button")
    Bestätigen = Button(Textmanager, text="Bestätigen")
    rückgabe.append(Bestätigen)
    Wiederherstellen = Button(Textmanager, text="Wiederherstellen")
    rückgabe.append(Wiederherstellen)
    Löschen = Button(Textmanager, text="Löschen", command=delete)
    rückgabe.append(Löschen)
    Präsentation = Button(Textmanager, text="Präsentation")
    rückgabe.append(Präsentation)
    return rückgabe


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
        inhalt.append(Button_Textwrt)
    elif aktion[1] == " Lied":
        Lable_Kamera = Button(Textmanager, text="Kamera", border=0)
        inhalt.append(Lable_Kamera)
        befehle = ["Kamera", "Textwort", "Lied"]
        clicked = StringVar()
        clicked.set(befehle[0])
        opt = OptionMenu(Textmanager, clicked, *befehle)
        opt.config(font=('Helvetica', 15), fg="black", bg="white")
        inhalt.append(clicked)
        inhalt.append(opt)
        eingabe_Lied = Entry(Textmanager)
        eingabe_Lied.bind("<KeyRelease>", eingabe_änderung)
        inhalt.append(eingabe_Lied)
        eingabe_Vers = Entry(Textmanager)
        eingabe_Vers.bind("<KeyRelease>", eingabe_änderung)
        inhalt.append(eingabe_Vers)
        befehle_buch = ["Gesangbuch", "Chorbuch", "Jugendliederbuch"]
        clicked_buch = StringVar()
        clicked_buch.set(befehle_buch[0])
        opt_buch = OptionMenu(Textmanager, clicked_buch, *befehle_buch, command=eingabe_änderung)
        opt_buch.config(font=('Helvetica', 15), fg="black", bg="white", )
        inhalt.append(clicked_buch)
        inhalt.append(opt_buch)
        Tex_lied_lable = Label(Textmanager)
        inhalt.append(Tex_lied_lable)
    elif aktion[1] == " Kamera":
        lied_weiter = Button(Textmanager, text= "servus", border=0)
        inhalt.append(lied_weiter)
        befehle = ["Kamera", "Textwort", "Lied"]
        clicked = StringVar()
        clicked.set(befehle[0])
        opt = OptionMenu(Textmanager, clicked, *befehle)
        opt.config(font=('Helvetica', 15), fg="black", bg="white")
        inhalt.append(clicked)
    return inhalt

def delete():
    for i in alle_inhalt:
        if i[0] == " Textwort":
            pass
        elif i[0] == " Lied":
            i[5].delete(0, "end")
            i[6].delete(0, "end")
    eingabe_änderung("")


def eingabe_änderung(event):
    for pos, i in enumerate(alle_inhalt):
        if i[0] == " Textwort":
            pass
        elif i[0] == " Lied":
            i[3].get()
            i[5].get()
            i[6].get()
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT song_name FROM songs WHERE song_number = ? AND book_name = ?", (i[5].get(),i[7].get()))
            song = cursor.fetchone()
            Vers_info = i[6].get()
            if not Vers_info:
                text_einfügen = ""
            elif len(Vers_info) == 1:
                text_einfügen = f"Vers {Vers_info}"
            elif len(Vers_info) > 1:
                text_einfügen = f"Verse {Vers_info}"
            if song:
                Text_speicher = f"{i[7].get()} {i[5].get()} {text_einfügen}\n{song[0]}"
                i[9].config(text= Text_speicher)
            else:
                i[9].config(text = "Bitte geben sie eine Nummer ein")
        elif i[0] == " Kamera":
            pass
            #cursor.execute("SELECT verse_text FROM verses WHERE song_id = ? ORDER BY verse_number", (song_id,))
            #verses = cursor.fetchall()
            #for i, verse_text in enumerate(verses):
                #verse_widget = tk.Text(verse_frame, font=("Helvetica", 10), height=12, width=44)
                #verse_widget.grid(row=i // 3, column=i % 3, padx=5, pady=5)
                #verse_widget.insert(tk.END, verse_text[0])
                #verse_widgets.append(verse_widget)



def posistion(fenster_width, fenster_height, factor):
    for pos, i in enumerate (alle_inhalt):
        text_size = min( int(i[1].winfo_height()/3*factor), int(i[1].winfo_width()/10*factor))
        i[1].config(font=('Helvetica', text_size))
        if i[0] == " Textwort":
            i[1].place(x= 0, y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].place(x= (i[1].winfo_width()+1), y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.3*factor, relheight=0.1*factor)
            i[2].config(font=('Helvetica', text_size))
        elif i[0] == " Lied":
            i[1].place(x= 0, y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].place(x= 0, y= pos*(i[1].winfo_height()+1)*2+i[1].winfo_height()+1,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].config(font=('Helvetica', text_size))
            i[4].place(x= (i[1].winfo_width()+1), y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.1*factor, relheight=0.05*factor)
            i[4].config(font=('Helvetica', text_size))
            i[5].place(x= (i[1].winfo_width()+2+i[4].winfo_width()), y= pos*i[1].winfo_height()*2+pos*2-1,relwidth=0.1*factor, relheight=0.05*factor)
            i[5].config(font=('Helvetica', text_size))
            i[6].place(x= (i[1].winfo_width()+2+i[4].winfo_width()), y= pos*(i[1].winfo_height()+1)*2+i[1].winfo_height(),relwidth=0.1*factor, relheight=0.05*factor)
            i[6].config(font=('Helvetica', text_size))
            i[8].place(x= i[1].winfo_width()+2+i[4].winfo_width()+2+i[5].winfo_width(), y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[8].config(font=('Helvetica', text_size))
            i[9].place(x= i[1].winfo_width()+2+i[4].winfo_width()+2+i[5].winfo_width()+2+i[8].winfo_width(), y= pos*(i[1].winfo_height()+1)*2,relwidth=0.3*factor, relheight=0.1*factor)
            i[9].config(font=('Helvetica', text_size))
        elif i[0] == " Kamera":
            i[1].place(x= 0, y= pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].place(x= 0, y= pos*(i[1].winfo_height()+1)*2+i[1].winfo_height()+1,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].config(font=('Helvetica', text_size))
        elif i[0] == "Button":
            i[1].place(x=fenster_width-i[1].winfo_width()-15, y=10, relwidth=0.12*factor, relheight=0.07*factor)
            i[2].place(x=fenster_width-i[2].winfo_width()-15, y=i[1].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)
            i[2].config(font=('Helvetica', text_size))
            i[3].place(x=fenster_width-i[1].winfo_width()-15, y=i[1].winfo_height()+i[2].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)
            i[3].config(font=('Helvetica', text_size))
            i[4].place(x=fenster_width-i[1].winfo_width()-15, y=i[1].winfo_height()+i[2].winfo_height()+i[3].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)
            i[4].config(font=('Helvetica', text_size))
