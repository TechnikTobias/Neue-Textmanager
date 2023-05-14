from tkinter import *
import os
import Settings


Programm_ort = os.getlogin()



Textmanager = Tk()
Textmanager.title("Textmanager")
Textmanager.geometry("1040x800")
Textmanager.minsize(width=1040, height=850)
Textmanager.iconbitmap(f"C:\\Users\\{Programm_ort}\\Desktop\\Lieder\\picture_compress 1.ico")
Settings.Check_settings()

if Settings.see_the_text:
    AnzeigeText = Toplevel(Textmanager)
    AnzeigeText.config(bg="black")
    AnzeigeText.geometry("1920x1080+1920+0")
    AnzeigeText.overrideredirect(True)
    Text_Anzeige_Label = Label(AnzeigeText, font=("Helvetica", 60), fg="white", bg="black", wraplength=1920)
    Aktueller_Text = ""
    Text_Anzeige_Label.config(text=Aktueller_Text)
    Text_Anzeige_Label["justify"] = "left"
    Text_Anzeige_Label.place(x=0, y=0)





