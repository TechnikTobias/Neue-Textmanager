import Neue_Textmanager
import Load_settings
import Class_gen

import os
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor
Programm_ort = os.getlogin()

Skalierung = [
    "100",
    "125",
    "150",
    "175",
    "200"
]

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
    global see_the_text, Textmanager_Hintergrund, Textmanager_Textfarbe, Button_hervorheben, Vers_kontroll, Text_anzeiger_textgröße, Button_hervorheben_farbe, Button_Textfarbe, Bildschirm_ausrichtung
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
    with open(f"Textmanager Daten\\Textmanager Daten\\Bildschirm_ausrichtung.txt", "r", encoding='utf8') as Text_anzeiger_textgröße1:
        Bildschirm_ausrichtung = Text_anzeiger_textgröße1.read() == "Rechts"



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





def Text_size_def(var):
    Load_settings.Font1.config(size= var)
    with open(f"Textmanager Daten\\Textmanager Daten\\Text_anzeiger_textgröße.txt", "w", encoding='utf8') as Text_anzeiger_textgröße1:
        Text_anzeiger_textgröße1.write(var)



def Rechts():
    with open(f"Textmanager Daten\\Textmanager Daten\\Bildschirm_ausrichtung.txt", "w", encoding='utf8') as Bildschirm_ausrichtung:
        Bildschirm_ausrichtung.write("Rechts")
    Bildschirm_ausrichtung_button.config(text="Rechts", command=Links)
    if see_the_text:
        Textanzeiger_setting_class.switch_setting_off()
        Textanzeiger_setting_class.switch_setting_on()

def Links():
    with open(f"Textmanager Daten\\Textmanager Daten\\Bildschirm_ausrichtung.txt", "w", encoding='utf8') as Bildschirm_ausrichtung:
        Bildschirm_ausrichtung.write("Links")
    Bildschirm_ausrichtung_button.config(text="Links", command=Rechts)
    if see_the_text:
        Textanzeiger_setting_class.switch_setting_off()
        Textanzeiger_setting_class.switch_setting_on()

def Auto_auflösung_def():
    Bildschirm_opt.Auto_auflösung(Neue_Textmanager.Textmanager)
    try:
        #Settings_test_auflösung = Tk()
        #Settings_test_auflösung.attributes("-fullscreen",1)
        #print(Settings_test_auflösung.winfo_height())
        Bildschirm_opt1.Auto_auflösung(Load_settings.AnzeigeText)
    except: pass
    if see_the_text:
        Textanzeiger_setting_class.switch_setting_off()
        Textanzeiger_setting_class.switch_setting_on()

def Test(event=None):
    print("hi")

def Load_anzeige():
    if see_the_text:
        Textanzeiger_setting_class.switch_setting_off()
        Textanzeiger_setting_class.switch_setting_on()

def make_settings():
    Check_settings()
    global Textanzeiger_setting_class, Button_hervorheben_class, Settings_bildschirm, Bildschirm_opt, Bildschirm_opt1, Textfarbe_auswahl, Setings_Textanzeiger, Hintergrndfarbe_auswahl, Button_Hintergrndfarbe_auswahl, Bildschirm_ausrichtung_button, Auto_auflösung, Button_Textfarbe_Button
    try: Settings_bildschirm.config(bg=Textmanager_Hintergrund)
    except:
        Settings_bildschirm = Toplevel(Neue_Textmanager.Textmanager)
        Settings_bildschirm.geometry("600x800")
        Settings_bildschirm.config(bg=Textmanager_Hintergrund)
        Textanzeiger_setting_class = Class_gen.Swich_generator(Settings_bildschirm, 10, 10, "Liedtextanzeige", 70, f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", see_the_text, Neue_Textmanager.Load_Setting)
        if see_the_text:
            Setings_Textanzeiger = ResponsiveWidget(Button, Settings_bildschirm, font=("Helvetica", 20), fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, text="Einstellungen für\nTextanzeiger", bd=0, command=Class_gen.Settings_Textanzeiger_def)
            Setings_Textanzeiger.place(y=10, x=250)

        Button_hervorheben_class = Class_gen.Swich_generator(Settings_bildschirm, 10, 70, "Button hervorheben", 70, f"Textmanager Daten\\Textmanager Daten\\Button_hervorheben.txt", Button_hervorheben, Neue_Textmanager.Load_Setting)
        Bildschirm_opt = Class_gen.Bild_schirm_größe_class(Settings_bildschirm, 10, 200, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten\\Textmanager Daten\\Auflösung", "Hauptbildschirm", Skalierung)
        Bildschirm_opt1 = Class_gen.Bild_schirm_größe_class(Settings_bildschirm, 240, 200, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten\\Textmanager Daten\\Auflösung2", "Textbildschirm", Skalierung)
        Auto_auflösung = ResponsiveWidget(Button,Settings_bildschirm, font=("Helvetica", 20), text="Auto Auflösung", command=Auto_auflösung_def, bd=0)
        Auto_auflösung.place(x=420, y=200)
        if Bildschirm_ausrichtung:
            Bildschirm_ausrichtung_button = ResponsiveWidget(Button,Settings_bildschirm, font=("Helvetica", 20), text="Rechts", command=Links, bd=0)
        else:
            Bildschirm_ausrichtung_button = ResponsiveWidget(Button, Settings_bildschirm, font=("Helvetica", 20), text="Links", command=Rechts, bd=0)
        Bildschirm_ausrichtung_button.place(x=420,y=300)

        Hintergrndfarbe_auswahl = Class_gen.Farben_class(Settings_bildschirm, "Hintergrund", 10, 370, "Hintergrund Farbe\n auswählen")
        Textfarbe_auswahl = Class_gen.Farben_class(Settings_bildschirm, "Textfarbe", 220, 370, "Textfarbe\nauswählen")
        Button_Textfarbe_Button = Class_gen.Farben_class(Settings_bildschirm, "Button_Textfarbe", 10, 480, "Button Textfarbe")
        Button_Hintergrndfarbe_auswahl = Class_gen.Farben_class(Settings_bildschirm, "Button_Hintergrund", 220, 480, "Button Hintergrund\nfarbe")
        Neue_Textmanager.Load_Setting()





def Info():
    global Info_manager
    try:
        Info_manager.config(bg=Textmanager_Hintergrund)
    except:
        Info_manager = Class_gen.Test_info()

