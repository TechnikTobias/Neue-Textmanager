import Neue_Textmanager

import os
from tkinter import *
from PIL import Image, ImageTk

Programm_ort = os.getlogin()

if __name__ == "__main__":
    pass




def Check_settings():
    global see_the_text
    with open(f"C:\\Users\\{Programm_ort}\\Desktop\\Textmanager Daten\\Textmanager Zwischenspeicher\\see_the_text.txt") as see_the_textinfo:
        see_the_text = see_the_textinfo.read()
    Neue_Textmanager.Load_Setting()


def make_settings():
    Settings = Toplevel(Neue_Textmanager.Textmanager)

def Info():
    global Info_manager
    try:
        Info_manager.destroy()
    except:
        pass
    Info_manager = Toplevel(Neue_Textmanager.Textmanager)
    Info_manager.geometry("800x600")
    Info_manager.config(bg="black")
    Text_für_Info = "Entwickler/ Uhrheber: Tobias Giebelhaus\nIn gedenken an meinen Geliebten Opa der bis zum Schluss Geistig fit war und sorgen kurz vor dem Tod im Internet war. Er war ein sehr lieber Opa"
    Info_zum_programm = Label(Info_manager, font=("Halvetica", 15), bg="black", fg="green", text=Text_für_Info, wraplength=800)
    Info_zum_programm["justify"] = "left"
    Info_zum_programm.place(x=0,y=0)
    Bild_für_opa1 = Image.open(f"C:\\Users\\{Programm_ort}\\Desktop\\Textmanager Daten\\Textmanager Daten\\Sterbe Anzeige Opa.jpg")
    Bild_für_opa = ImageTk.PhotoImage(image=Bild_für_opa1.resize((472,341))) 
    Bild_für_opa_Label = Label(Info_manager,image=Bild_für_opa)
    Bild_für_opa_Label.place(x=0,y=100)
    Bild_für_opa_Label.draw()