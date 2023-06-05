import Neue_Textmanager
import Load_settings

import os
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor
from tkinter.colorchooser import ResponsiveWidget
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


def Check_settings():
    global see_the_text, Textmanager_Hintergrund, Textmanager_Textfarbe, Button_hervorheben, Vers_kontroll, Text_anzeiger_textgröße, Button_hervorheben_farbe
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
    with open(f"Textmanager Daten\\Textmanager Daten\\Button_hervorheben_farbe.txt", "r", encoding='utf8') as Text_anzeiger_textgröße1:
        Button_hervorheben_farbe = Text_anzeiger_textgröße1.read()


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
    


def on():
    print("on")
def off():
    print(Neue_Textmanager.Textmanager.winfo_screenheight())
    print(Neue_Textmanager.Textmanager.winfo_screenwidth())

def Text_size_def(var):
    Load_settings.Font1.config(size= var)
    with open(f"Textmanager Daten\\Textmanager Daten\\Text_anzeiger_textgröße.txt", "w", encoding='utf8') as Text_anzeiger_textgröße1:
        Text_anzeiger_textgröße1.write(var)

def make_settings():
    Check_settings()
    global Textanzeiger_setting_class, Button_hervorheben_class, Vers_kontroll_class, Settings_bildschirm, Bildschirm_opt, Bildschirm_opt1, Textfarbe_auswahl, Hintergrndfarbe_auswahl
    try: Settings_bildschirm.config(bg=Textmanager_Hintergrund)
    except:
        Settings_bildschirm = Toplevel(Neue_Textmanager.Textmanager)
        Settings_bildschirm.geometry("600x800")
        Settings_bildschirm.config(bg=Textmanager_Hintergrund)
        Textanzeiger_setting_class = Swich_generator(Settings_bildschirm, 10, 10, "Liedtextanzeige", 70, f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", see_the_text, Neue_Textmanager.Load_Setting, Neue_Textmanager.Load_Setting)
        try: 
            global Text_größe_Textanzeiger
            Load_settings.AnzeigeText.config(bg=Textmanager_Hintergrund)
            Text_größe_Textanzeiger = Scale(Settings_bildschirm, from_=0, to=100, orient= HORIZONTAL, background=Textmanager_Hintergrund, foreground=Textmanager_Textfarbe, bd=0,font=24, length=300, width=25, command=Text_size_def, tickinterval=25)
            Text_größe_Textanzeiger.set(Text_anzeiger_textgröße)
            Text_größe_Textanzeiger.place(y=10, x=250)
        except: pass


        Button_hervorheben_class = Swich_generator(Settings_bildschirm, 10, 70, "Button hervorheben", 70, f"Textmanager Daten\\Textmanager Daten\\Button_hervorheben.txt", Button_hervorheben, Neue_Textmanager.Load_Setting, Neue_Textmanager.Load_Setting)
        Vers_kontroll_class = Swich_generator(Settings_bildschirm, 10, 130, "Vers Kontrolle", 70, f"Textmanager Daten\\Textmanager Daten\\Vers_kontroll.txt", Vers_kontroll, off, on)
        Bildschirm_opt = Bild_schirm_größe_class(Settings_bildschirm, 10, 250, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten\\Textmanager Daten\\Auflösung", "Hauptbildschirm")
        Bildschirm_opt1 = Bild_schirm_größe_class(Settings_bildschirm, 240, 250, Bildschirm_auflösung_quere, Bildschirm_auflösung_hoch ,f"Textmanager Daten\\Textmanager Daten\\Auflösung2", "Textbildschirm")
        Textfarbe_auswahl = Button(Settings_bildschirm, font=("Helvetica", 20), fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, text="Textfarbe\nauswählen", command=Textfarbe_farbe_def, border=0, activebackground=Button_hervorheben_farbe)
        Textfarbe_auswahl.place(x=10, y=370)
        Hintergrndfarbe_auswahl = Button(Settings_bildschirm, font=("Helvetica", 20), fg=Textmanager_Textfarbe, bg=Textmanager_Hintergrund, text="Hintergrund Farbe\nauswählen", command=Hintergrundfarbe_farbe_def, border=0,activebackground=Button_hervorheben_farbe)
        Hintergrndfarbe_auswahl.place(x=220, y=370)


class Swich_generator:
    def __init__(self, Settings_is, x_pos, y_pos, Textnazeige, x_pos_text, Text_datei_save, ob_True, def_bei_offbutton, def_bei_onbutton):
        self.Text_datei_save = Text_datei_save
        self.def_bei_offbutton = def_bei_offbutton
        self.def_bei_onbutton = def_bei_onbutton
        self.is_switch = Button(Settings_is,activebackground=Button_hervorheben_farbe)
        self.switch_text = Label(Settings_is, font=("Helvetica", 12), bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe, text=Textnazeige)
        self.switch_text.place(x=x_pos_text, y=y_pos + 12)
        if not ob_True:
            self.Photo1 = Image.open("off-button.png")
            self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
            self.is_switch.config(image=self.Photo, bg=Textmanager_Hintergrund, border=0, command=self.switch_setting_on)
        else:
            self.Photo1 = Image.open("on-button.png")
            self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
            self.is_switch.config(image=self.Photo, bg=Textmanager_Hintergrund, border=0, command=self.switch_setting_off)
        self.is_switch.place(x=x_pos, y=y_pos)

    def Color(self):
        self.switch_text.config(bg=Textmanager_Hintergrund,fg=Textmanager_Textfarbe)
        self.is_switch.config(bg=Textmanager_Hintergrund)

    def switch_setting_off(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("False")
        self.Photo1 = Image.open("off-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command= self.switch_setting_on)
        self.def_bei_offbutton()
        self.Photo1 = Image.open("off-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command= self.switch_setting_on)

    def switch_setting_on(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("True")
        self.Photo1 = Image.open("on-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command=self.switch_setting_off)
        self.def_bei_onbutton()
        self.Photo1 = Image.open("on-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command=self.switch_setting_off)


class Bild_schirm_größe_class:
    def __init__(self, Seite, x_pos, y_pos, bildschirm_große_quere, bilschirm_größe_hoch,  speicherort, Bildschirm):
        self.speicherort = speicherort
        self.Hauptbildschirm = Label(Seite, font=("Helvetica", 20), text=Bildschirm, bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe)
        self.Hauptbildschirm.place(x=x_pos , y=y_pos-50)
        with open(f"{speicherort}quere.txt", "r", encoding="utf8") as speicherort1:
            self.bildschirm_pos = speicherort1.read()
        self.Bild_größe_stringvar_quere = StringVar()
        self.Bild_größe_stringvar_quere.set(self.bildschirm_pos)
        self.Bildschirm_größe_quere_menü = OptionMenu(Seite, self.Bild_größe_stringvar_quere, *bildschirm_große_quere)
        self.Bildschirm_größe_quere_menü.place(x=x_pos, y=y_pos)
        with open(f"{speicherort}hoch.txt", "r", encoding="utf8") as speicherort1:
            self.bildschirm_pos1 = speicherort1.read()
        self.Bild_größe_stringvar_hoch = StringVar()
        self.Bild_größe_stringvar_hoch.set(self.bildschirm_pos1)
        self.Bildschirm_größe_hoch_menü = OptionMenu(Seite, self.Bild_größe_stringvar_hoch, *bilschirm_größe_hoch)
        self.Bildschirm_größe_hoch_menü.place(x=100+x_pos, y=y_pos)
        self.Bildschirm_bestätigen = Button(Seite, font=("Helvetica", 20), bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe, text="Bestätigen", command=self.Bildgröße_bestatigen, border=0, activebackground=Button_hervorheben_farbe)
        self.Bildschirm_bestätigen.place(x=x_pos, y=y_pos+50)
        self.X_bildschirm = Label(Seite, font=("Helvetica", 20),bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe, text="X")
        self.X_bildschirm.place(x=x_pos+75, y=y_pos)
    def Bildgröße_bestatigen(self):
        with open(f"{self.speicherort}hoch.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(self.Bild_größe_stringvar_hoch.get())
        with open(f"{self.speicherort}quere.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(self.Bild_größe_stringvar_quere.get())
    def color(self):
        self.Bildschirm_bestätigen.config(bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe)
        self.X_bildschirm.config(bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe)
        self.Hauptbildschirm.config(bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe)


def Info():
    global Info_manager
    try:
        Info_manager.config(bg=Textmanager_Hintergrund)
    except:
        Info_manager = Test_info()

class Test_info:
    def __init__(self):
        self.Info_manager = Toplevel(Neue_Textmanager.Textmanager)
        self.Info_manager.geometry("800x600")
        self.Info_manager.config(bg=Textmanager_Hintergrund)
        self.Text_für_Info = "Entwickler/ Uhrheber: Tobias Giebelhaus\nIn gedenken an meinen Geliebten Opa der bis zum Schluss Geistig fit war und sorgen kurz vor dem Tod im Internet war. Er war ein sehr lieber Opa"
        self.Info_zum_programm = Label(self.Info_manager, font=("Halvetica", 15), bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe, text=self.Text_für_Info, wraplength=800)
        self.Info_zum_programm["justify"] = "left"
        self.Info_zum_programm.place(x=0,y=0)
        self.Bild_für_opa1 = Image.open(f"Textmanager Daten\\Textmanager Daten\\Sterbe Anzeige Opa.jpg")
        self.Bild_für_opa = ImageTk.PhotoImage(image=self.Bild_für_opa1.resize((472,341))) 
        self.Bild_für_opa_Label = Label(self.Info_manager,image=self.Bild_für_opa)
        self.Bild_für_opa_Label.place(x=0,y=100)
