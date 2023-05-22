import Neue_Textmanager

import os
from tkinter import *
from PIL import Image, ImageTk

Programm_ort = os.getlogin()

if __name__ == "__main__":
    pass



def Check_settings():
    global see_the_text, Textmanager_Hintergrund, Textmanager_Textfarbe, sd
    with open(f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", "r", encoding='utf8') as see_the_textinfo:
        see_the_text = see_the_textinfo.read() == "True"
        print (see_the_text)
    with open(f"Textmanager Daten\\Textmanager Daten\\Hintergrund.txt", "r", encoding='utf8') as Neue_Texmanager_Hinregrund:
        Textmanager_Hintergrund = Neue_Texmanager_Hinregrund.read()
    with open(f"Textmanager Daten\\Textmanager Daten\\Textfarbe.txt", "r", encoding='utf8') as Neue_Texmanager_Textfarbe:
        Textmanager_Textfarbe = Neue_Texmanager_Textfarbe.read()

def switch():
    with open(f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", "w", encoding='utf8') as see_the_textinfo:
        see_the_textinfo.write("True")
    Photo1 = Image.open("on-button.png")
    Photo = ImageTk.PhotoImage(Photo1.resize((50,50)))
    Textanzeiger_setting.config(image=Photo, command=switch1)
    Textanzeiger_setting.m


def switch1():
    with open(f"Textmanager Daten\\Textmanager Daten\\see_the_text.txt", "w", encoding='utf8') as see_the_textinfo:
        see_the_textinfo.write("False")
    Photo1 = Image.open("off-button.png")
    Photo = ImageTk.PhotoImage(Photo1.resize((50,50)))
    Textanzeiger_setting.config(image=Photo, command=switch)
    Textanzeiger_setting.m

def make_settings():
    Check_settings()
    global Textanzeiger_setting
    Settings = Toplevel(Neue_Textmanager.Textmanager)
    Settings.geometry("600x800")
    Settings.config(bg=Textmanager_Hintergrund)
    if not see_the_text:
        Photo1 = Image.open("off-button.png")
        Photo = ImageTk.PhotoImage(Photo1.resize((50,50)))
        Textanzeiger_setting = Button(Settings, image=Photo, bg=Textmanager_Hintergrund, border=0, command=switch)
    else:
        Photo1 = Image.open("on-button.png")
        Photo = ImageTk.PhotoImage(Photo1.resize((50,50)))
        Textanzeiger_setting = Button(Settings, image=Photo, bg=Textmanager_Hintergrund, border=0, command=switch1)
    Textanzeiger_setting.pack()
    Textanzeiger_setting.m

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
    Bild_für_opa1 = Image.open(f"C:\\Users\\{Programm_ort}\\Desktop\\Textmanager Daten\\Textmanager Daten\\Sterbe Anzeige Opa.jpg")
    Bild_für_opa = ImageTk.PhotoImage(image=Bild_für_opa1.resize((472,341))) 
    Bild_für_opa_Label = Label(Info_manager,image=Bild_für_opa)
    Bild_für_opa_Label.place(x=0,y=100)
    Bild_für_opa_Label.draw()