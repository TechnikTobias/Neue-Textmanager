import Neue_Textmanager
import Load_settings
import Class_gen

import os
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor
Programm_ort = os.getlogin()

Bildschirm_auflösung_hoch = [
    600,
    768,
    634,
    720,
    768,
    900,
    990,
    1024,
    1050,
    1080
]

Bildschirm_auflösung_quere = [
    800,
    1024,
    1128,
    1280,
    1366,
    1600,
    1680,
    1760,
    1920
]

def ResponsiveWidget(widget, *args, **kwargs):
    bindings = {'<Enter>': {'state': 'active'},
                '<Leave>': {'state': 'normal'}}

    w = widget(*args, **kwargs)

    for (k, v) in bindings.items():
        w.bind(k, lambda e, kwarg=v: e.widget.config(**kwarg))
    return w

def Check_settings():
    global see_the_text, Textmanager_Hintergrund, Textmanager_Textfarbe, Button_hervorheben, Vers_kontroll, Text_anzeiger_textgröße, Button_hervorheben_farbe, Button_Textfarbe
    with open(f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", "r", encoding='utf8') as see_the_textinfo:
        see_the_text = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\Button_hervorheben.txt", "r", encoding='utf8') as see_the_textinfo:
        Button_hervorheben = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\Vers_kontroll.txt", "r", encoding='utf8') as see_the_textinfo:
        Vers_kontroll = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\Hintergrund.txt", "r", encoding='utf8') as Neue_Texmanager_Hinregrund:
        Textmanager_Hintergrund = Neue_Texmanager_Hinregrund.read()
    with open(f"Textmanager Daten\\Textmanager Daten\\Textfarbe.txt", "r", encoding='utf8') as Neue_Texmanager_Textfarbe:
        Textmanager_Textfarbe = Neue_Texmanager_Textfarbe.read()
    with open(f"Textmanager Daten\\Textmanager Daten\\Text_anzeiger_textgröße.txt", "r", encoding='utf8') as Text_anzeiger_textgröße1:
        Text_anzeiger_textgröße = Text_anzeiger_textgröße1.read()
    with open(f"Textmanager Daten\\Textmanager Daten\\Button_Hintergrund.txt", "r", encoding='utf8') as Text_anzeiger_textgröße1:
            Button_hervorheben_farbe = Text_anzeiger_textgröße1.read()
    with open(f"Textmanager Daten\\Textmanager Daten\\Button_Textfarbe.txt", "r", encoding='utf8') as Text_anzeiger_textgröße1:
            Button_Textfarbe = Text_anzeiger_textgröße1.read()


def Textfarbe_farbe_def():
    color = askcolor()  
    if not (color[1]) == None:
        with open(f"Textmanager Daten\\Textmanager Daten\\Textfarbe.txt", "w", encoding='utf8') as Neue_Texmanager_Textfarbe:
            Neue_Texmanager_Textfarbe.write(color[1])
    Load_settings.Load_all_collor()

def Hintergrundfarbe_farbe_def():
    color = askcolor()  
    if not (color[1]) == None:
        with open(f"Textmanager Daten\\Textmanager Daten\\Hintergrund.txt", "w", encoding='utf8') as Neue_Texmanager_Textfarbe:
            Neue_Texmanager_Textfarbe.write(color[1])
    Load_settings.Load_all_collor()


def Button_hervorheben_farben_def():
    color = askcolor()  
    if not (color[1]) == None:
        with open(f"Textmanager Daten\\Textmanager Daten\\Button_Hintergrund.txt", "w", encoding='utf8') as Neue_Texmanager_Textfarbe:
            Neue_Texmanager_Textfarbe.write(color[1])
    Load_settings.Button_hervorhen_frabe()


def Button_texthervorheben_farben_def():
    color = askcolor()  
    if not (color[1]) == None:
        with open(f"Textmanager Daten\\Textmanager Daten\\Button_Textfarbe.txt", "w", encoding='utf8') as Neue_Texmanager_Textfarbe:
            Neue_Texmanager_Textfarbe.write(color[1])
    Load_settings.Button_hervorhen_frabe()


def Text_size_def(var):
    Load_settings.Font1.config(size= var)
    with open(f"Textmanager Daten\\Textmanager Daten\\Text_anzeiger_textgröße.txt", "w", encoding='utf8') as Text_anzeiger_textgröße1:
        Text_anzeiger_textgröße1.write(var)







def make_settings():
    Check_settings()
    global Textanzeiger_setting_class, Button_hervorheben_class, Vers_kontroll_class, Settings_bildschirm, Bildschirm_opt, Bildschirm_opt1, Textfarbe_auswahl, Text_größe_Textanzeiger, Hintergrndfarbe_auswahl, Button_Textfarbe_auswahl, Button_Hintergrndfarbe_auswahl
    try: Settings_bildschirm.config(bg=Textmanager_Hintergrund)
    except:
        Settings_bildschirm = Toplevel(Neue_Textmanager.Textmanager)
        Settings_bildschirm.geometry("600x800")
        Settings_bildschirm.config(bg=Textmanager_Hintergrund)
        Textanzeiger_setting_class = Class_gen.Swich_generator(Settings_bildschirm, 10, 10, "Liedtextanzeige", 70, f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", see_the_text, Neue_Textmanager.Load_Setting, Neue_Textmanager.Load_Setting)
        if see_the_text:
            Text_größe_Textanzeiger = Scale(Settings_bildschirm, from_=0, to=100, orient= HORIZONTAL, background=Textmanager_Hintergrund, foreground=Textmanager_Textfarbe, font=24, length=300, width=25, command=Text_size_def, tickinterval=25, activebackground=Button_hervorheben_farbe)
            Text_größe_Textanzeiger.set(Text_anzeiger_textgröße)
            Text_größe_Textanzeiger.place(y=10, x=250)


        Button_hervorheben_class = Class_gen.Swich_generator(Settings_bildschirm, 10, 70, "Button hervorheben", 70, f"Textmanager Daten\\Textmanager Daten\\Button_hervorheben.txt", Button_hervorheben, Neue_Textmanager.Load_Setting, Neue_Textmanager.Load_Setting)
        Bildschirm_opt = Class_gen.Bild_schirm_größe_class(Settings_bildschirm, 10, 250, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten\\Textmanager Daten\\Auflösung", "Hauptbildschirm")
        Bildschirm_opt1 = Class_gen.Bild_schirm_größe_class(Settings_bildschirm, 240, 250, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten\\Textmanager Daten\\Auflösung2", "Textbildschirm")
        Textfarbe_auswahl = ResponsiveWidget(Button, Settings_bildschirm, font=("Helvetica", 20), fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, text="Textfarbe\nauswählen", command=Textfarbe_farbe_def, border=0, activebackground="black", activeforeground="white",highlightbackground="black", highlightthickness="4",highlightcolor="green")
        Textfarbe_auswahl.place(x=10, y=370)
        Hintergrndfarbe_auswahl = ResponsiveWidget(Button, Settings_bildschirm, font=("Helvetica", 20), fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, text="Hintergrund Farbe\nauswählen", command=Hintergrundfarbe_farbe_def, border=0)
        Hintergrndfarbe_auswahl.place(x=220, y=370)
        Button_Hintergrndfarbe_auswahl = ResponsiveWidget(Button, Settings_bildschirm, font=("Helvetica", 20), fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, text="Hintergrund Farbe\nauswählen", command=Button_hervorheben_farben_def, border=0)
        Button_Hintergrndfarbe_auswahl.place(x=220, y=420)
        Button_Textfarbe_auswahl = ResponsiveWidget(Button, Settings_bildschirm, font=("Helvetica", 20), fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, text="Hintergrund Farbe\nauswählen", command=Button_texthervorheben_farben_def, border=0)
        Button_Textfarbe_auswahl.place(x=10, y=420)
        Neue_Textmanager.Load_Setting()





def Info():
    global Info_manager
    try:
        Info_manager.config(bg=Textmanager_Hintergrund)
    except:
        Info_manager = Class_gen.Test_info()

