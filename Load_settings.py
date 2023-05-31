import Settings
import Neue_Textmanager
from tkinter import *
import tkinter.font as tkFont
def Load_Text_anzeiger():
    if Settings.see_the_text:
        global AnzeigeText, Font1
        try: AnzeigeText.config(bg="black")
        except:
            Font1 = tkFont.Font(family="Helvetica",size= Settings.Text_anzeiger_textgröße)
            AnzeigeText = Toplevel(Neue_Textmanager.Textmanager)
            AnzeigeText.config(bg=Settings.Textmanager_Hintergrund)
            AnzeigeText.geometry(f"100x100+{Neue_Textmanager.Textmanager.winfo_screenwidth()}+0")
            AnzeigeText.overrideredirect(True)
            Text_Anzeige_Label = Label(AnzeigeText, font=Font1, fg="white", bg="black", wraplength=1920)
            Text_Anzeige_Label.config(text="")
            Text_Anzeige_Label["justify"] = "left"
            Text_Anzeige_Label.place(x=0, y=0)
            AnzeigeText.geometry(f"{AnzeigeText.winfo_screenwidth()}x{AnzeigeText.winfo_screenheight()}")
            try:
                Settings.Text_größe_Textanzeiger = Scale(Settings.Settings, from_=1, to=200, orient= HORIZONTAL, background=Settings.Textmanager_Hintergrund, foreground=Settings.Textmanager_Textfarbe, bd=0,font=24, length=300, width=25, command=Settings.Text_size_def)
                Settings.Text_größe_Textanzeiger.set(Settings.Text_anzeiger_textgröße)
                Settings.Text_größe_Textanzeiger.place(y=10, x=250)
            except: pass
    else: 
        try:
            AnzeigeText.destroy()
            Settings.Text_größe_Textanzeiger.destroy()
        except: pass


