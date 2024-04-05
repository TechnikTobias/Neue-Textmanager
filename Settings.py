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
    global see_the_text, Button_hervorheben, Vers_kontroll, Text_anzeiger_textgröße, Button_hervorheben_farbe, Button_Textfarbe, Bildschirm_ausrichtung, Textanzeiger_Hintergrund, Textanzeiger_Textfarbe, Textgröße_von_alle_Texte, text_size, Liedvorschau,Smarte_unterstüzung, Kronologische_Verse, Smarte_Vorschläge
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",)) == "True"
    Button_hervorheben = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("button_hervorheben",)) == "True"
    Vers_kontroll = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("vers_kontroll",)) == "True"   
    Textanzeiger_Textfarbe= Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("textanzeiger_textfarbe",))
    Textanzeiger_Hintergrund = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("textanzeiger_Hintergrund",))
    Text_anzeiger_textgröße = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_anzeiger_textgröße",))
    Button_hervorheben_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("button_hintergrund",))
    Button_Textfarbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("button_textfarbe",))
    Bildschirm_ausrichtung = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("bildschirm_ausrichtung",)) == "Rechts"
    Liedvorschau = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("liedvorschau",)) == "True"
    Smarte_unterstüzung = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("smarte_verse",)) == "True"
    Kronologische_Verse = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("kronologische_verse",)) == "True"
    Smarte_Vorschläge = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("smarte_vorschläge",)) == "True"
    text_size1 = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_size",))

    if Tkfont:
        text_size1 = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_size",))
        text_size = int(text_size1[0])*16
        Textgröße_von_alle_Texte = tkFont.Font(family="Helvetica", size=text_size)




def Textfarbe_farbe_def():
    color = askcolor()  
    if not (color[1]) == None:
        with open(f"Textmanager Daten/Textmanager Daten/text_farbe.txt", "w", encoding='utf8') as Neue_Texmanager_Textfarbe:
            Neue_Texmanager_Textfarbe.write(color[1])
    Load_settings.Load_all_collor()

def Hintergrundfarbe_farbe_def():
    color = askcolor()  
    if not (color[1]) == None:
        with open(f"Textmanager Daten/Textmanager Daten/Hintergrund.txt", "w", encoding='utf8') as Neue_Texmanager_Textfarbe:
            Neue_Texmanager_Textfarbe.write(color[1])
    Load_settings.Load_all_collor()





def Text_size_def(var):
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",), True)
    if see_the_text[0] == "True":
        Load_settings.Font1.config(size= var)
        with open(f"Textmanager Daten/Textmanager Daten/Text_anzeiger_textgröße.txt", "w", encoding='utf8') as Text_anzeiger_textgröße1:
            Text_anzeiger_textgröße1.write(var)



def Rechts():
    with open(f"Textmanager Daten/Textmanager Daten/Bildschirm_ausrichtung.txt", "w", encoding='utf8') as Bildschirm_ausrichtung:
        Bildschirm_ausrichtung.write("Rechts")
    Bildschirm_ausrichtung_button.config(text="Rechts", command=Links)
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",), True)
    if see_the_text[0] == "True":
        Textanzeiger_setting_class.switch_setting_off()
        Textanzeiger_setting_class.switch_setting_on()

def Links():
    with open(f"Textmanager Daten/Textmanager Daten/Bildschirm_ausrichtung.txt", "w", encoding='utf8') as Bildschirm_ausrichtung:
        Bildschirm_ausrichtung.write("Links")
    Bildschirm_ausrichtung_button.config(text="Links", command=Rechts)
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",), True)
    if see_the_text[0] == "True":
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
    Load_anzeige()

def Test(event=None):
    print("hi")

def Load_anzeige():
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",))
    if see_the_text[0] == "True":
        Textanzeiger_setting_class.switch_setting_off()
        Textanzeiger_setting_class.switch_setting_on()

def make_settings():
    Check_settings()
    global Settings_bildschirm, Setings_Textanzeiger, Settings_Graphig_option, Smarte_unterstüzung_button
    hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
    text_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
    try: 
        Settings_bildschirm.config(bg=hintergrund_farbe)
    except:
        Settings_bildschirm = Toplevel(Neue_Textmanager.Textmanager)
        Settings_bildschirm.geometry("600x800")
        Settings_bildschirm.config(bg=hintergrund_farbe)
        Settings_Graphig_option = ResponsiveWidget(Button, Settings_bildschirm, font=Textgröße_von_alle_Texte, fg=text_farbe, bg=hintergrund_farbe, command=Load_graphig_settings, text= "Einstellung für\nGraphig", bd=0)
        Setings_Textanzeiger = ResponsiveWidget(Button, Settings_bildschirm, font=Textgröße_von_alle_Texte, fg=text_farbe, bg=hintergrund_farbe, text="Einstellungen für\nTextanzeiger", bd=0, command=Settings_Textanzeiger_def)
        Smarte_unterstüzung_button = ResponsiveWidget(Button, Settings_bildschirm, font= Textgröße_von_alle_Texte, fg= text_farbe, bg= hintergrund_farbe, command= Load_SmarteSettings, bd= 0, text= "Intelligente Unterstützung")
        ToolTip(Setings_Textanzeiger, msg="Lädt alle Einstellungen für den Textanzeiger", delay=2, follow=True)
        Neue_Textmanager.Load_Setting()
        Load_settings.Load_text_size(text_size)


def Load_graphig_settings():
    global Textfarbe_auswahl, Hintergrndfarbe_auswahl, Button_Hintergrndfarbe_auswahl, Button_Textfarbe_Button,Text_größe_anpassen, Button_hervorheben_class, Graphig_bildschirm, Bildschirm_opt
    hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
    Graphig_bildschirm = Toplevel(Neue_Textmanager.Textmanager)
    Graphig_bildschirm.geometry("600x800")
    Graphig_bildschirm.config(bg=hintergrund_farbe)
    Hintergrndfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "Hintergrund", "Hintergrund Farbe\n auswählen", "Mit dem Button kann die Farbe des Hintergrund geändert werden")
    Textfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "text_farbe", "text_farbe\nauswählen", "Mit dem Button kann die text_farbe geändert werden")
    Button_Textfarbe_Button = Class_gen.Farben_class(Graphig_bildschirm, "Button_Textfarbe", "Button text_farbe", "Mit dem Button kann die text_farbe der button geändert werden die angezeigt wird, wenn der Mauszeiger uber einen Button geht")
    Button_Hintergrndfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "Button_Hintergrund", "Button Hintergrund\nfarbe", "Mit dem Button kann die Hintergrund geändert der Button werden, die angezeigt wird wenn der Mauszeiger uber einen Button geht")
    Text_größe_anpassen = Class_gen.Text_scalierung(command_=Load_settings.Load_text_size, Anzeige_ort=Graphig_bildschirm, from__=5, to_=45, aktuelle_zahl=int(text_size), font_=Textgröße_von_alle_Texte, size=int(text_size), tickinterval=15)
    Bildschirm_opt = Class_gen.Bild_schirm_größe_class(Graphig_bildschirm, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten/Textmanager Daten/Auflösung", "Hauptbildschirm", Skalierung, "Bestätigt die eingegebene Bildschirmgröße und Bildschirm Skalierung von Hauptbildschirm von Windows")
    Auto_auflösung = ResponsiveWidget(Button,Graphig_bildschirm, font=Textgröße_von_alle_Texte, text="Auto Auflösung", command=Auto_auflösung_def, bd=0)
    Button_hervorheben_class = Class_gen.Swich_generator(Graphig_bildschirm, "Button hervorheben", f"Button_hervorheben", Button_hervorheben, Neue_Textmanager.Load_Setting, Text_hover="Bringt die Butten in der eingestellte farbe zum Leuchten", zise=text_size)
    Neue_Textmanager.Load_Setting()
    Load_settings.Load_text_size(text_size)


def Settings_Textanzeiger_def():
    global Settings_Textanzeiger_Top, Textanzeiger_Textfarbe_button, Textanzeiger_Hintergrund_Button, Bildschirm_opt1, Bildschirm_ausrichtung_button, Text_größe_ändern, Textanzeiger_setting_class, Liedvorschau_Button
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",), True)
    Settings_Textanzeiger_Top = Toplevel()
    Settings_Textanzeiger_Top.geometry("500x800")
    Settings_Textanzeiger_Top.title("Einstellungen für Textanzeiger")
    hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
    text_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
    Settings_Textanzeiger_Top.config(bg=hintergrund_farbe)
    Textanzeiger_setting_class = Class_gen.Swich_generator(Settings_Textanzeiger_Top, "Liedtextanzeige", f"see_the_text", see_the_text[0] == "True", Neue_Textmanager.Load_Setting, "Lädt die Textanzeige womit der Text an einem anderm Bildschirm", zise=text_size)
    Textanzeiger_Textfarbe_button = Class_gen.Farben_class(Settings_Textanzeiger_Top, "Textanzeiger_Textfarbe", "text_farbe")
    Textanzeiger_Hintergrund_Button = Class_gen.Farben_class(Settings_Textanzeiger_Top, "Textanzeiger_Hintergrund", "Hintergrund")
    Bildschirm_opt1 = Class_gen.Bild_schirm_größe_class(Settings_Textanzeiger_Top, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten/Textmanager Daten/Auflösung2", "Textbildschirm", Skalierung)
    if Bildschirm_ausrichtung:
        Bildschirm_ausrichtung_button = ResponsiveWidget(Button,Settings_Textanzeiger_Top, font=Textgröße_von_alle_Texte, text="Rechts", command=Links, bd=0)
    else:
        Bildschirm_ausrichtung_button = ResponsiveWidget(Button, Settings_Textanzeiger_Top, font=Textgröße_von_alle_Texte, text="Links", command=Rechts, bd=0)
    Text_größe_ändern = Class_gen.Text_scalierung(Settings_Textanzeiger_Top, Text_size_def, from__=0, to_=100, orient_=HORIZONTAL, backgrund=hintergrund_farbe, foregrund=text_farbe, aktuelle_zahl=int(Text_anzeiger_textgröße), font_=Textgröße_von_alle_Texte, size=int(text_size))
    Liedvorschau_Button = Class_gen.Swich_generator(Settings_is=Settings_Textanzeiger_Top, Textanzeige="Liedvorschau", Text_datei_save=f"Liedvorschau", Text_hover="Diese Einstellung zeigt vor dem Gottesdienst die Lieder an", zise=text_size, ob_True=Liedvorschau, def_bei_offbutton=Test)
    Load_settings.Load_all_collor()
    Load_settings.Load_text_size(text_size)


def Load_SmarteSettings():
    global Settings_smarte_unterstüzung, Smarte_Verse, RichtigeVersereihenfolge, Smarte_vorschlage_Button, Smarte_vorschlage_Button_top
    hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
    Settings_smarte_unterstüzung = Toplevel()
    Settings_smarte_unterstüzung.geometry("500x800")
    Settings_smarte_unterstüzung.title("Einstellungen für Smarte Unterstüzung")
    Settings_smarte_unterstüzung.config(bg=hintergrund_farbe)
    Smarte_Verse = Class_gen.Swich_generator(Settings_is=Settings_smarte_unterstüzung, Textanzeige="Smarte Verse", Text_datei_save=f"Smarte_verse", Text_hover="Diese Einstellung schaltet Intiligente Verse ein, Falsche Verse werden gelöscht", zise=text_size, ob_True=Smarte_unterstüzung, def_bei_offbutton=Test)
    RichtigeVersereihenfolge = Class_gen.Swich_generator(Settings_is=Settings_smarte_unterstüzung, Textanzeige="Kronologische Vers Reihenfolge", Text_datei_save= f"kronologische_verse", Text_hover="Sortiert die Verse in die Richtige reihenfolge", zise=text_size, ob_True=Kronologische_Verse, def_bei_offbutton=Test)
    Smarte_vorschlage_Button = Class_gen.Swich_generator(Settings_is=Settings_smarte_unterstüzung, Textanzeige="Smarte Vorschläge", Text_datei_save= f"smarte_vorschläge", Text_hover="Lädt einprogrammierte ", zise=text_size, ob_True=Smarte_Vorschläge, def_bei_offbutton=Test)
    Smarte_vorschlage_Button_top = ResponsiveWidget(Button, Settings_smarte_unterstüzung, font=Textgröße_von_alle_Texte, text="Vorschläge Bearbeiten", command=Test, bd=0)
    Load_settings.Load_text_size(text_size)
    Load_settings.Load_all_collor()



def Info():
    global Info_manager
    try:
        hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        Info_manager.config(bg=hintergrund_farbe)
    except:
        Info_manager = Class_gen.Test_info()

