import Neue_Textmanager
import Load_settings
import Class_gen
import tkinter.ttk as ttk
from typing import Optional

import os
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tktooltip import *
from tkinter.colorchooser import askcolor
Programm_ort = os.getlogin()

#alles noch mal anschauen 
widget_info = {}
def register_widget(
        name: str, 
        widget_place, 
        einstellungs_leiste: Optional[Widget] = None, 
        widget: Widget = None, 
        relheight: int = 0.1, 
        relwidth : int = .11,
        relx: int = 0, 
        rely: int = 0):
    """Registriert ein Widget und speichert seine Informationen
    Hier werden die Info für die Widget übergeben damit sie an einer zentrallen stelle placiert werden und deren größe angepasst wird."""
    widget_info[name] = {
        "widget_place" : widget_place,
        "Einstellugs_leiste" : einstellungs_leiste,
        "widget": widget,
        "relheight": relheight,
        "relwidth": relwidth,
        "relx": relx,
        "rely": rely
    }




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

#checksetting kann weg aber ert wenn alles verbessert wurde
def Check_settings(Tkfont = True):
    global Button_hervorheben, Vers_kontroll, Text_anzeiger_textgröße, Button_hervorheben_farbe, Button_Textfarbe, Bildschirm_ausrichtung, Textanzeiger_Hintergrund, Textanzeiger_Textfarbe, Textgröße_von_alle_Texte, text_size, Liedvorschau,Smarte_unterstüzung, Kronologische_Verse, Smarte_Vorschläge
    Button_hervorheben = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("button_hervorheben",))
    Vers_kontroll = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("vers_kontroll",))
    Textanzeiger_Textfarbe= Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("textanzeiger_textfarbe",))
    Textanzeiger_Hintergrund = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("textanzeiger_hintergrund",))
    Text_anzeiger_textgröße = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_anzeiger_textgröße",))
    Button_hervorheben_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("button_hintergrund",))
    Button_Textfarbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("button_textfarbe",))
    Bildschirm_ausrichtung = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("bildschirm_ausrichtung",))[0] == "Rechts"
    Liedvorschau = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("liedvorschau",))
    Smarte_unterstüzung = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("smarte_verse",))
    Kronologische_Verse = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("kronologische_verse",))
    Smarte_Vorschläge = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("smarte_vorschläge",))
    text_size1 = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_size",))
    text_size = text_size1
    if Tkfont:
        text_size1 = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_size",))
        text_size = int(text_size1[0])
        Textgröße_von_alle_Texte = tkFont.Font(family="Helvetica", size=text_size)





#kontrolieren
def Text_size_def(text_groeße):
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",), True)
    if see_the_text:
        Neue_Textmanager.get_db_connection("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", (text_groeße,"text_anzeiger_textgröße"), False)
        Load_settings.Font1.config(size= text_groeße)


#rechts links bildschirmausrichtung verbessern
def Rechts():
    Neue_Textmanager.get_db_connection("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", ("Rechts","bildschirm_ausrichtung"), False)
    Bildschirm_ausrichtung_button.config(text="Rechts", command=Links)
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",), True)
    if see_the_text:
        Textanzeiger_setting_class.switch_setting_off()
        Textanzeiger_setting_class.switch_setting_on()

def Links():
    Neue_Textmanager.get_db_connection("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", ("Links","bildschirm_ausrichtung"), False)
    Bildschirm_ausrichtung_button.config(text="Links", command=Rechts)
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",), True)
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
    Load_anzeige()

def Test(event=None):
    pass

def Load_anzeige():
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",))
    if see_the_text:
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
    factor = int(Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",))[0])/100
    skalierung = int(Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",))[0])
    def groese_plus():#
        nonlocal skalierung
        skalierung += 10
        Neue_Textmanager.get_db_connection("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", (skalierung,"scalierung"), False)
        Load_settings.Textmanager_größen()
        update_widget_positions()
    def groese_minus():
        nonlocal skalierung
        skalierung -= 10
        Neue_Textmanager.get_db_connection("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", (skalierung,"scalierung"), False)
        Load_settings.Textmanager_größen()
        update_widget_positions()
    global Textfarbe_auswahl, Hintergrndfarbe_auswahl, Button_Hintergrndfarbe_auswahl, Button_Textfarbe_Button,Text_größe_anpassen, Button_hervorheben_class, Graphig_bildschirm, Bildschirm_opt
    hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
    Graphig_bildschirm = Toplevel(Neue_Textmanager.Textmanager)
    Graphig_bildschirm.geometry("600x800")
    Graphig_bildschirm.config(bg=hintergrund_farbe)
    scale_label = ttk.Label(Graphig_bildschirm, text=skalierung)
    scale_label.config(text=skalierung)
    scale_label.place(relheight=0.12, relwidth=0.2)
    scale_button_plus = ttk.Button(Graphig_bildschirm, style='TButton', text="+10%", command=groese_plus)
    register_widget(name="Scale_button_plus", widget=scale_button_plus, einstellungs_leiste=scale_label, widget_place= Graphig_bildschirm, relheight=0.05, relwidth=0.1*factor, relx=0.1*factor, rely=0.1*factor)
    scale_button_minus = ttk.Button(Graphig_bildschirm, style='TButton', text="-10%", command=groese_minus)
    register_widget(name="scale_button_minus", widget=scale_button_minus, einstellungs_leiste=scale_label, widget_place= Graphig_bildschirm,  relheight=0.05, relwidth=0.1*factor, relx=0.2*factor, rely=0.1*factor)
    Hintergrndfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "Hintergrund", "Hintergrund Farbe\n auswählen", "Mit dem Button kann die Farbe des Hintergrund geändert werden")
    Textfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "text_farbe", "text_farbe\nauswählen", "Mit dem Button kann die text_farbe geändert werden")
    Button_Textfarbe_Button = Class_gen.Farben_class(Graphig_bildschirm, "button_Textfarbe", "Button text_farbe", "Mit dem Button kann die text_farbe der button geändert werden die angezeigt wird, wenn der Mauszeiger uber einen Button geht")
    Button_Hintergrndfarbe_auswahl = Class_gen.Farben_class(Graphig_bildschirm, "button_Hintergrund", "Button Hintergrund\nfarbe", "Mit dem Button kann die Hintergrund geändert der Button werden, die angezeigt wird wenn der Mauszeiger uber einen Button geht")
    #Class_gen.Text_scalierung(command_=Load_settings.Load_text_size, Anzeige_ort=Graphig_bildschirm, from__=5, to_=45, aktuelle_zahl=int(text_size), font_=Textgröße_von_alle_Texte, size=int(text_size), tickinterval=15)
    Bildschirm_opt = Class_gen.Bild_schirm_größe_class(Graphig_bildschirm, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten/Textmanager Daten/Auflösung", "Hauptbildschirm", Skalierung, "Bestätigt die eingegebene Bildschirmgröße und Bildschirm Skalierung von Hauptbildschirm von Windows")
    Auto_auflösung = ResponsiveWidget(Button,Graphig_bildschirm, font=Textgröße_von_alle_Texte, text="Auto Auflösung", command=Auto_auflösung_def, bd=0)
    Button_hervorheben_class = Class_gen.Swich_generator(Graphig_bildschirm, "Button hervorheben", f"button_hervorheben", Button_hervorheben, Neue_Textmanager.Load_Setting, Text_hover="Bringt die Butten in der eingestellte farbe zum Leuchten", zise=10)
    Neue_Textmanager.Load_Setting()
    Load_settings.Load_text_size(text_size)
    update_widget_positions()



def Settings_Textanzeiger_def():
    global Settings_Textanzeiger_Top, Textanzeiger_Textfarbe_button, Textanzeiger_Hintergrund_Button, Bildschirm_opt1, Bildschirm_ausrichtung_button, Text_größe_ändern, Textanzeiger_setting_class, Liedvorschau_Button
    see_the_text = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("see_the_text",), True)
    Settings_Textanzeiger_Top = Toplevel()
    Settings_Textanzeiger_Top.geometry("500x800")
    Settings_Textanzeiger_Top.title("Einstellungen für Textanzeiger")
    hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
    text_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
    Settings_Textanzeiger_Top.config(bg=hintergrund_farbe)
    Textanzeiger_setting_class = Class_gen.Swich_generator(Settings_Textanzeiger_Top, "Liedtextanzeige", f"see_the_text", see_the_text, Neue_Textmanager.Load_Setting, "Lädt die Textanzeige womit der Text an einem anderm Bildschirm", zise=text_size)
    Textanzeiger_Textfarbe_button = Class_gen.Farben_class(Settings_Textanzeiger_Top, "textanzeiger_textfarbe", "text_farbe")
    Textanzeiger_Hintergrund_Button = Class_gen.Farben_class(Settings_Textanzeiger_Top, "textanzeiger_hintergrund", "Hintergrund")
    Bildschirm_opt1 = Class_gen.Bild_schirm_größe_class(Settings_Textanzeiger_Top, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten/Textmanager Daten/Auflösung2", "Textbildschirm", Skalierung)
    if Bildschirm_ausrichtung:
        Bildschirm_ausrichtung_button = ResponsiveWidget(Button,Settings_Textanzeiger_Top, font=Textgröße_von_alle_Texte, text="Rechts", command=Links, bd=0)
    else:
        Bildschirm_ausrichtung_button = ResponsiveWidget(Button, Settings_Textanzeiger_Top, font=Textgröße_von_alle_Texte, text="Links", command=Rechts, bd=0)
    Text_größe_ändern = Class_gen.Text_scalierung(Settings_Textanzeiger_Top, Text_size_def, from__=0, to_=100, orient_=HORIZONTAL, backgrund=hintergrund_farbe, foregrund=text_farbe, aktuelle_zahl=int(Text_anzeiger_textgröße[0]), font_=Textgröße_von_alle_Texte, size=int(text_size))
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


def update_widget_positions():
    """Aktualisiert die Positionen und Größen aller Widgets basierend auf dem Skalierungsfaktor"""
    factor = int(Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",))[0])/100
    for info in widget_info.values():
        widget_place = info["widget_place"]
        print(f"{widget_place}info von toplevel")
        einstellungs_leiste = info["Einstellugs_leiste"]
        widget = info["widget"]
        relheight = max(info["relheight"] * widget_place.winfo_height(), einstellungs_leiste.winfo_height()) * factor
        relwidth = info["relwidth"] * factor
        relx = info["relx"] * factor
        rely = info["rely"] * factor
        widget.place( relwidth=relwidth, relx=relx, rely=rely)



