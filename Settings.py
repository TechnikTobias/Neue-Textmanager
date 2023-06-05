import Neue_Textmanager

import os
from tkinter import *
from PIL import Image, ImageTk

Programm_ort = os.getlogin()



def Check_settings():
    global see_the_text, Textmanager_Hintergrund, Textmanager_Textfarbe, open_datei, Vers_kontroll
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










def make_settings():
    Check_settings()
    global Textanzeiger_setting_class, Datei_open_class, Vers_kontroll_class, Settings
    Settings = Toplevel(Neue_Textmanager.Textmanager)
    Settings.geometry("600x800")
    Settings.config(bg=Textmanager_Hintergrund)
    Textanzeiger_setting_class = Swich_generator(Settings, 10, 10, "Liedtextanzeige", 70, f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", see_the_text)
    Datei_open_class = Swich_generator(Settings, 10, 70, "Datei Öffnen", 70, f"Textmanager Daten\\Textmanager Daten\\open_text.txt", open_datei)
    Vers_kontroll_class = Swich_generator(Settings, 10, 130, "Vers Kontrolle", 70, f"Textmanager Daten\\Textmanager Daten\\Vers_kontroll.txt", Vers_kontroll)


class Swich_generator:
    def __init__(self, Settings_is, x_pos, y_pos, Textnazeige, x_pos_text, Text_datei_save, ob_True):
        self.Text_datei_save = Text_datei_save
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

    def switch_setting_on(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("True")
        self.Photo1 = Image.open("on-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command=self.switch_setting_off)




def Info():
    global Info_manager
    try:
        Info_manager.destroy()
    except:
        pass
    Info_manager = Toplevel(Neue_Textmanager.Textmanager)
    Info_manager.geometry("800x600")
    Info_manager.config(bg=Textmanager_Hintergrund)
    Text_für_Info = "Entwickler/ Uhrheber: Tobias Giebelhaus\nIn gedenken an meinen Geliebten Opa der bis zum Schluss Geistig fit war und sorgen kurz vor dem Tod im Internet war. Er war ein sehr lieber Opa"
    Info_zum_programm = Label(Info_manager, font=("Halvetica", 15), bg=Textmanager_Hintergrund, fg=Textmanager_Textfarbe, text=Text_für_Info, wraplength=800)
    Info_zum_programm["justify"] = "left"
    Info_zum_programm.place(x=0,y=0)
    Bild_für_opa1 = Image.open(f"Textmanager Daten\\Textmanager Daten\\Sterbe Anzeige Opa.jpg")
    Bild_für_opa = ImageTk.PhotoImage(image=Bild_für_opa1.resize((472,341))) 
    Bild_für_opa_Label = Label(Info_manager,image=Bild_für_opa)
    Bild_für_opa_Label.place(x=0,y=100)
    Bild_für_opa_Label.update()