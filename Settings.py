import Neue_Textmanager
import Load_settings
import Class_gen

import os
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tktooltip import *
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

def Check_settings(Tkfont = True):
    global see_the_text, Textmanager_Hintergrund, Textmanager_Textfarbe, Button_hervorheben, Vers_kontroll, Text_anzeiger_textgröße, Button_hervorheben_farbe, Button_Textfarbe, Bildschirm_ausrichtung, Textanzeiger_Hintergrund, Textanzeiger_Textfarbe, Textgröße_von_alle_Texte, text_size
    with open(f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", "r", encoding='utf8') as see_the_textinfo:
        see_the_text = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\Button_hervorheben.txt", "r", encoding='utf8') as see_the_textinfo:
        Button_hervorheben = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\Vers_kontroll.txt", "r", encoding='utf8') as see_the_textinfo:
        Vers_kontroll = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\Hintergrund.txt", "r", encoding='utf8') as Neue_Texmanager_Hinregrund:
        Textmanager_Hintergrund = Neue_Texmanager_Hinregrund.read()
    with open(f"Textmanager Daten\\Textmanager Daten\\Textanzeiger_Hintergrund.txt", "r", encoding='utf8') as Neue_Texmanager_Hinregrund:
        Textanzeiger_Hintergrund = Neue_Texmanager_Hinregrund.read()
    with open(f"Textmanager Daten\\Textmanager Daten\\Textanzeiger_Textfarbe.txt", "r", encoding='utf8') as Neue_Texmanager_Hinregrund:
        Textanzeiger_Textfarbe = Neue_Texmanager_Hinregrund.read()
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
    if Tkfont:
        with open(f"Textmanager Daten\\Textmanager Daten\\text_size.txt", "r", encoding='utf8') as text_size1:
            text_size = text_size1.read()
        Textgröße_von_alle_Texte = tkFont.Font(family="Helvetica", size=text_size)




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
    if see_the_text:
        Load_settings.Font1.config(size= var)
        with open(f"Textmanager Daten\\Textmanager Daten\\Text_anzeiger_textgröße.txt", "w", encoding='utf8') as Text_anzeiger_textgröße1:
            Text_anzeiger_textgröße1.write(var)



def Rechts():
    with open(f"Textmanager Daten\\Textmanager Daten\\Bildschirm_ausrichtung.txt", "w", encoding='utf8') as Bildschirm_ausrichtung:
        Bildschirm_ausrichtung.write("Rechts")
    Class_gen.Bildschirm_ausrichtung_button.config(text="Rechts", command=Links)
    if see_the_text:
        Class_gen.Textanzeiger_setting_class.switch_setting_off()
        Class_gen.Textanzeiger_setting_class.switch_setting_on()

def Links():
    with open(f"Textmanager Daten\\Textmanager Daten\\Bildschirm_ausrichtung.txt", "w", encoding='utf8') as Bildschirm_ausrichtung:
        Bildschirm_ausrichtung.write("Links")
    Class_gen.Bildschirm_ausrichtung_button.config(text="Links", command=Rechts)
    if see_the_text:
        Class_gen.Textanzeiger_setting_class.switch_setting_off()
        Class_gen.Textanzeiger_setting_class.switch_setting_on()

def Auto_auflösung_def():
    Bildschirm_opt.Auto_auflösung(Neue_Textmanager.Textmanager)
    try:
        #Settings_test_auflösung = Tk()
        #Settings_test_auflösung.attributes("-fullscreen",1)
        #print(Settings_test_auflösung.winfo_height())
        Class_gen.Bildschirm_opt1.Auto_auflösung(Load_settings.AnzeigeText)
    except: pass
    Load_anzeige()

def Test(event=None):
    print("hi")

def Load_anzeige():
    if see_the_text:
        Class_gen.Textanzeiger_setting_class.switch_setting_off()
        Class_gen.Textanzeiger_setting_class.switch_setting_on()

def make_settings():
    Check_settings()
    global Settings_bildschirm, Setings_Textanzeiger, Settings_Graphig_option
    try: 
        Settings_bildschirm.config(bg=Textmanager_Hintergrund)
    except:
        Settings_bildschirm = Toplevel(Neue_Textmanager.Textmanager)
        Settings_bildschirm.geometry("600x800")
        Settings_bildschirm.config(bg=Textmanager_Hintergrund)
        Settings_Graphig_option = ResponsiveWidget(Button, Settings_bildschirm, font=Textgröße_von_alle_Texte, fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, command=Load_graphig_settings, text= "Einstellung für\nGraphig", bd=0)
        Settings_Graphig_option.place(x=10, y=20+4*int(text_size))
        Setings_Textanzeiger = ResponsiveWidget(Button, Settings_bildschirm, font=Textgröße_von_alle_Texte, fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, text="Einstellungen für\nTextanzeiger", bd=0, command=Class_gen.Settings_Textanzeiger_def)
        Setings_Textanzeiger.place(y=10, x=10)
        ToolTip(Setings_Textanzeiger, msg="Lädt alle Einstellungen für den Textanzeiger", delay=2, follow=True)
        Neue_Textmanager.Load_Setting()


def Load_graphig_settings():
    global Textfarbe_auswahl, Hintergrndfarbe_auswahl, Button_Hintergrndfarbe_auswahl, Button_Textfarbe_Button,Text_größe_anpassen, Button_hervorheben_class, Graphig_bildschirm, Bildschirm_opt
    Graphig_bildschirm = Toplevel(Neue_Textmanager.Textmanager)
    Graphig_bildschirm.geometry("600x800")
    Graphig_bildschirm.config(bg=Textmanager_Hintergrund)
    Hintergrndfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "Hintergrund", 10, 50+18*int(text_size), "Hintergrund Farbe\n auswählen", "Mit dem Button kann die Farbe des Hintergrund geändert werden")
    Textfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "Textfarbe", 30+12*int(text_size), 10+20*int(text_size), "Textfarbe\nauswählen", "Mit dem Button kann die Textfarbe geändert werden")
    Button_Textfarbe_Button = Class_gen.Farben_class(Graphig_bildschirm, "Button_Textfarbe", 10, 10+24*int(text_size), "Button Textfarbe", "Mit dem Button kann die Textfarbe der button geändert werden die angezeigt wird, wenn der Mauszeiger uber einen Button geht")
    Button_Hintergrndfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "Button_Hintergrund", 10+13*int(text_size), 10+24*int(text_size), "Button Hintergrund\nfarbe", "Mit dem Button kann die Hintergrund geändert der Button werden, die angezeigt wird wenn der Mauszeiger uber einen Button geht")
    Text_größe_anpassen = Class_gen.Text_scalierung(command_=Load_settings.Load_text_size, x_pos=10, y_pos=10+4*int(text_size), Anzeige_ort=Graphig_bildschirm, from__=5, to_=45, aktuelle_zahl=int(text_size), font_=Textgröße_von_alle_Texte, size=int(text_size), tickinterval=15)
    Bildschirm_opt = Class_gen.Bild_schirm_größe_class(Graphig_bildschirm, 10, 10+12*int(text_size), Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten\\Textmanager Daten\\Auflösung", "Hauptbildschirm", Skalierung, "Bestätigt die eingegebene Bildschirmgröße und Bildschirm Skalierung von Hauptbildschirm von Windows")
    Auto_auflösung = ResponsiveWidget(Button,Graphig_bildschirm, font=Textgröße_von_alle_Texte, text="Auto Auflösung", command=Auto_auflösung_def, bd=0)
    Button_hervorheben_class = Class_gen.Swich_generator(Graphig_bildschirm, 10, 10, "Button hervorheben", f"Textmanager Daten\\Textmanager Daten\\Button_hervorheben.txt", Button_hervorheben, Neue_Textmanager.Load_Setting, Text_hover="Bringt die Butten in der eingestellte farbe zum Leuchten", zise=text_size)
    Neue_Textmanager.Load_Setting()

def Info():
    global Info_manager
    try:
        Info_manager.config(bg=Textmanager_Hintergrund)
    except:
        Info_manager = Class_gen.Test_info()

