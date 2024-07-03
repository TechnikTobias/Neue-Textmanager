import Neue_Textmanager
import Load_settings
import Class_gen
import tkinter.ttk as ttk
from typing import Optional

import os
from tkinter import *
from PIL import Image
import tkinter.font as tkFont
from tktooltip import *
from tkinter.colorchooser import askcolor

#alles noch mal anschauen 





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


class Settings_window(Toplevel):
    def __init__(self, parent, *args, **kwargs):
        hintergrund_farbe = Neue_Textmanager.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        self.widget_info = {}
        try: 
            self.config(bg=hintergrund_farbe)
        except:
            super().__init__(parent, *args, **kwargs)
            self.title("Einstellungen")
            self.geometry("600x800")
            self.config(bg=hintergrund_farbe)
            Settings_Graphig_option = ttk.Button(self, command=Load_graphig_settings, text= "Einstellung für\nGraphig", style="TButton")
            self.register_widget("Settings_Graphig_option", Settings_Graphig_option, relheight=0.05, relwidth=0.15, rely=0.05, relx=0)
            Setings_Textanzeiger = ttk.Button(self, text="Einstellungen für\nTextanzeiger",command=Settings_Textanzeiger_def, style="TButton")
            self.register_widget("Setings_Textanzeiger", Setings_Textanzeiger, relheight=0.05, relwidth=0.15, rely=0.15, relx=0)
            Smarte_unterstüzung_button = ttk.Button(self, command= Load_SmarteSettings, text= "Intelligente Unterstützung", style="TButton")
            self.register_widget("Smarte_unterstüzung_button", Smarte_unterstüzung_button, relheight=0.05, relwidth=0.15, rely=0.25, relx=0)
            ToolTip(Setings_Textanzeiger, msg="Lädt alle Einstellungen für den Textanzeiger", delay=2, follow=True)
            self.update_widget_positions()
    def register_widget(self,
        name: str, 
        widget: Widget = None, 
        relheight: int = 0.1, 
        relwidth : int = .11,
        relx: int = 0, 
        rely: int = 0):
        """Registriert ein Widget und speichert seine Informationen
        Hier werden die Info für die Widget übergeben damit sie an einer zentrallen stelle placiert werden und deren größe angepasst wird."""
        self.widget_info[name] = {
            "widget": widget,
            "relheight": relheight,
            "relwidth": relwidth,
            "relx": relx,
            "rely": rely
        }

    def update_widget_positions(self):
        """Aktualisiert die Positionen und Größen aller Widgets basierend auf dem Skalierungsfaktor"""
        self.factor = int(Neue_Textmanager.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",)))/100
        self.widgets_to_remove = []
        for self.name, self.info in self.widget_info.items():
            try:
                self.widget = self.info["widget"]
                self.relheight = self.info["relheight"] * self.factor
                self.relwidth = self.info["relwidth"] * self.factor
                self.relx = self.info["relx"] * self.factor
                self.rely = self.info["rely"] * self.factor
                self.widget.place(relwidth=self.relwidth, relheight=self.relheight, relx=self.relx, rely=self.rely)
            except:
                self.widgets_to_remove.append(self.name)

        # Entferne die fehlerhaften Widgets aus widget_info
        for self.name in self.widgets_to_remove:
            del self.widget_info[self.name]
            print(self.widget_info)
            print(f"Widget {self.name} aus widget_info entfernt")



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
    register_widget("Prozentanzeige der Skalierung", widget_place=Graphig_bildschirm,widget=scale_label,relheight=0.05, relwidth=0.1, relx=0.1, rely=0.1)
    scale_button_plus = ttk.Button(Graphig_bildschirm, style='TButton', text="+10%", command=groese_plus)
    register_widget(name="Scale_button_plus", widget=scale_button_plus, widget_place= Graphig_bildschirm, relheight=0.05, relwidth=0.1, relx=0.1, rely=0.15)
    scale_button_minus = ttk.Button(Graphig_bildschirm, style='TButton', text="-10%", command=groese_minus)
    register_widget(name="scale_button_minus", widget=scale_button_minus, widget_place= Graphig_bildschirm,  relheight=0.05, relwidth=0.1, relx=0.2, rely=0.15)
    Hintergrndfarbe_auswahl = ttk.Button(Graphig_bildschirm, text="Hintergrund",style='TButton')
    register_widget(name="Hintergrund Farben Button", widget_place=Graphig_bildschirm, widget=Hintergrndfarbe_auswahl,relheight=0.05, relwidth=0.2, relx=0.1,rely=0.25)
    Button_Textfarbe_Button = ttk.Button(Graphig_bildschirm, text="Button Text Farbe",style='TButton')
    register_widget(name="Text Farben Button", widget_place=Graphig_bildschirm, widget=Button_Textfarbe_Button,relheight=0.05, relwidth=0.3, relx=0.3,rely=0.25)
    Textfarbe_auswahl = ttk.Button(Graphig_bildschirm, text="Hintergrund",style='TButton')
    register_widget(name="Text Farben ", widget_place=Graphig_bildschirm, widget=Textfarbe_auswahl,relheight=0.05, relwidth=0.2, relx=0.1,rely=0.35)
    Button_Hintergrndfarbe_auswahl = ttk.Button(Graphig_bildschirm, text="Hintergrund",style='TButton')
    register_widget(name="Hintergrund Farben", widget_place=Graphig_bildschirm, widget=Button_Hintergrndfarbe_auswahl,relheight=0.05, relwidth=0.2, relx=0.3,rely=0.35)
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
    widgets_to_remove = []
    print(widget_info)
    for name, info in widget_info.items():
        try:
            print("erledigt")
            widget_place = info["widget_place"]
            widget = info["widget"]
            relheight = info["relheight"] * factor
            relwidth = info["relwidth"] * factor
            relx = info["relx"] * factor
            rely = info["rely"] * factor
            widget.place( relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)
        except:
            widgets_to_remove.append(name)
            print("fehler")

    # Entferne die fehlerhaften Widgets aus widget_info
    for name in widgets_to_remove:
        del widget_info[name]
        print(f"Widget {name} aus widget_info entfernt")


