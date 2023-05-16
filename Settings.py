import Neue_Textmanager

import os
from tkinter import *
from PIL import Image, ImageTk

Programm_ort = os.getlogin()

if __name__ == "__main__":
    pass




def Check_settings():
    global see_the_text, Textmanager_Hintergrund, Textmanager_Textfarbe
    with open(f"C:\\Users\\{Programm_ort}\\Desktop\\Textmanager Daten\\Textmanager Daten\\see_the_text.txt") as see_the_textinfo:
        see_the_text = see_the_textinfo.read()
    with open(f"C:\\Users\\{Programm_ort}\\Desktop\\Textmanager Daten\\Textmanager Daten\\Hintergrund.txt") as Neue_Texmanager_Hinregrund:
        Textmanager_Hintergrund = Neue_Texmanager_Hinregrund.read()
    with open(f"C:\\Users\\{Programm_ort}\\Desktop\\Textmanager Daten\\Textmanager Daten\\Textfarbe.txt") as Neue_Texmanager_Textfarbe:
        Textmanager_Textfarbe = Neue_Texmanager_Textfarbe.read()


def make_settings():
    Settings = Toplevel(Neue_Textmanager.Textmanager)
    Settings.geometry("600x800")
    Settings.config(bg=Textmanager_Hintergrund)


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