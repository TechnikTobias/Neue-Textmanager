import Neue_Textmanager
import Load_settings

import os
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont

Programm_ort = os.getlogin()



def Check_settings():
    global see_the_text, Textmanager_Hintergrund, Textmanager_Textfarbe, open_datei, Vers_kontroll, Text_anzeiger_textgröße
    with open(f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", "r", encoding='utf8') as see_the_textinfo:
        see_the_text = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\open_text.txt", "r", encoding='utf8') as see_the_textinfo:
        open_datei = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\Vers_kontroll.txt", "r", encoding='utf8') as see_the_textinfo:
        Vers_kontroll = see_the_textinfo.read() == "True"
    with open(f"Textmanager Daten\\Textmanager Daten\\Hintergrund.txt", "r", encoding='utf8') as Neue_Texmanager_Hinregrund:
        Textmanager_Hintergrund = Neue_Texmanager_Hinregrund.read()
    with open(f"Textmanager Daten\\Textmanager Daten\\Textfarbe.txt", "r", encoding='utf8') as Neue_Texmanager_Textfarbe:
        Textmanager_Textfarbe = Neue_Texmanager_Textfarbe.read()    
    with open(f"Textmanager Daten\\Textmanager Daten\\Text_anzeiger_textgröße.txt", "r", encoding='utf8') as Text_anzeiger_textgröße1:
        Text_anzeiger_textgröße = Text_anzeiger_textgröße1.read()




def on():
    print("on")
def off():
    print(Neue_Textmanager.Textmanager.winfo_screenheight())
    print(Neue_Textmanager.Textmanager.winfo_screenwidth())

def Text_size_def(var):
    Load_settings.Font1.config(family="Helvetica", size= var)
    with open(f"Textmanager Daten\\Textmanager Daten\\Text_anzeiger_textgröße.txt", "w", encoding='utf8') as Text_anzeiger_textgröße1:
        Text_anzeiger_textgröße1.write(var)

def make_settings():
    Check_settings()
    global Textanzeiger_setting_class, Datei_open_class, Vers_kontroll_class, Settings
    Settings = Toplevel(Neue_Textmanager.Textmanager)
    Settings.geometry("600x800")
    Settings.config(bg=Textmanager_Hintergrund)
    Textanzeiger_setting_class = Swich_generator(Settings, 10, 10, "Liedtextanzeige", 70, f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", see_the_text, Neue_Textmanager.Load_Setting, Neue_Textmanager.Load_Setting)
    try: 
        global Text_größe_Textanzeiger
        Load_settings.AnzeigeText.config(bg=Textmanager_Hintergrund)
        Text_größe_Textanzeiger = Scale(Settings, from_=1, to=200, orient= HORIZONTAL, background=Textmanager_Hintergrund, foreground=Textmanager_Textfarbe, bd=0,font=24, length=300, width=25, command=Text_size_def)
        Text_größe_Textanzeiger.set(Text_anzeiger_textgröße)
        Text_größe_Textanzeiger.place(y=10, x=250)
    except: pass

    Datei_open_class = Swich_generator(Settings, 10, 70, "Datei Öffnen", 70, f"Textmanager Daten\\Textmanager Daten\\open_text.txt", open_datei, off, on)
    Vers_kontroll_class = Swich_generator(Settings, 10, 130, "Vers Kontrolle", 70, f"Textmanager Daten\\Textmanager Daten\\Vers_kontroll.txt", Vers_kontroll, off, on)


class Swich_generator:
    def __init__(self, Settings_is, x_pos, y_pos, Textnazeige, x_pos_text, Text_datei_save, ob_True, def_bei_offbutton, def_bei_onbutton):
        self.Text_datei_save = Text_datei_save
        self.def_bei_offbutton = def_bei_offbutton
        self.def_bei_onbutton = def_bei_onbutton
        self.is_switch = Button(Settings_is)
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

    def switch_setting_off(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("False")
        self.Photo1 = Image.open("off-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command= self.switch_setting_on)
        self.def_bei_offbutton()

    def switch_setting_on(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("True")
        self.Photo1 = Image.open("on-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command=self.switch_setting_off)
        self.def_bei_onbutton()



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
