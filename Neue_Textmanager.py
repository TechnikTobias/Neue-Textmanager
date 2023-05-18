from tkinter import *
import os


import Settings
import Kamera
import Lied_Kontrolle
import Help

Programm_ort = os.getlogin()


def Start():
    global Textmanager
    Settings.Check_settings()
    Textmanager = Tk()
    Textmanager.title("Textmanager")
    Textmanager.config(bg=Settings.Textmanager_Hintergrund)
    Textmanager.geometry("1040x800")
    Textmanager.minsize(width=1040, height=850)
    Textmanager.iconbitmap(f"C:\\Users\\{Programm_ort}\\Desktop\\Lieder\\picture_compress 1.ico")
    Menu_generator()
    Load_Setting()

def Menu_generator():
    Menu_Settings = Menu(Textmanager, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0)
    Menu_Info = Menu(Menu_Settings, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0)
    Menu_Kamera = Menu(Menu_Settings, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0)
    Menu_LiedKontrolle = Menu(Menu_Settings, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0)
    Menu_Help = Menu(Menu_Settings, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, border=0, borderwidth=0)
    Menu_Settings.add_cascade(label="Info", menu=Menu_Info)
    Menu_Settings.add_cascade(label="Kamera", menu=Menu_Kamera)
    Menu_Settings.add_cascade(label="Lied Kontrolle", menu=Menu_LiedKontrolle)
    Menu_Settings.add_cascade(label="Hilfe", menu=Menu_Help)
    Menu_Info.add_command(label="Einstellungen", command=Settings.make_settings)
    Menu_Info.add_command(label= "Info", command=Settings.Info)
    Menu_Kamera.add_command(label="Einstellungen", command=Kamera.Settings)
    Menu_Kamera.add_command(label="Position", command=Kamera.Position)
    Menu_LiedKontrolle.add_command(label="Einstellungen", command=Lied_Kontrolle.Settings)
    Menu_LiedKontrolle.add_command(label="Lied Kontrolieren", command=Lied_Kontrolle.controll)
    Menu_Help.add_command(label="Hilfe", command=Help.Help)
    Textmanager.config(menu=Menu_Settings)

def Load_Setting():
    if Settings.see_the_text:
        AnzeigeText = Toplevel(Textmanager)
        AnzeigeText.config(bg=Settings.Textmanager_Hintergrund)
        AnzeigeText.geometry("1920x1080+1920+0")
        AnzeigeText.overrideredirect(True)
        Text_Anzeige_Label = Label(AnzeigeText, font=("Helvetica", 60), fg="white", bg="black", wraplength=1920)
        Aktueller_Text = ""
        Text_Anzeige_Label.config(text=Aktueller_Text)
        Text_Anzeige_Label["justify"] = "left"
        Text_Anzeige_Label.place(x=0, y=0)





