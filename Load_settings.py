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
                Settings.Text_größe_Textanzeiger = Scale(Settings.Settings_bildschirm, from_=1, to=200, orient= HORIZONTAL, background=Settings.Textmanager_Hintergrund, foreground=Settings.Textmanager_Textfarbe, bd=0,font=24, length=300, width=25, command=Settings.Text_size_def)
                Settings.Text_größe_Textanzeiger.set(Settings.Text_anzeiger_textgröße)
                Settings.Text_größe_Textanzeiger.place(y=10, x=250)
            except: pass
    else: 
        try:
            AnzeigeText.destroy()
            Settings.Text_größe_Textanzeiger.destroy()
        except: pass
def Button_hervorhen_frabe():
    Settings.Check_settings()
    if Settings.Button_hervorheben:
        print("wahr")
        try:
            def change_selected_button(button):
                print("hhha")
                global selected_button
                if selected_button is not None:
                    selected_button.config(bg=Settings.Button_hervorheben_farbe)
                selected_button = button
                button.config(bg="orange")
            Settings.Hintergrndfarbe_auswahl.config(selectcolor=Settings.Button_hervorheben_farbe, activebackground=Settings.Button_hervorheben_farbe,relief=RAISED, cursor="arrow", command=lambda button=Settings.Hintergrndfarbe_auswahl: change_selected_button(button))
            Settings.Textfarbe_auswahl.config(selectcolor=Settings.Button_hervorheben_farbe)
            Settings.Bildschirm_opt.Bildschirm_bestätigen.config(activebackground=Settings.Button_hervorheben_farbe,relief=RAISED, cursor="arrow")
            Settings.Bildschirm_opt1.Bildschirm_bestätigen.config(activebackground=Settings.Button_hervorheben_farbe)
        except: pass
        Neue_Textmanager.Menu_Info.config(activebackground=Settings.Button_hervorheben_farbe)
        Neue_Textmanager.Menu_Help.config(activebackground=Settings.Button_hervorheben_farbe)
        Neue_Textmanager.Menu_Kamera.config(activebackground=Settings.Button_hervorheben_farbe)
        Neue_Textmanager.Menu_LiedKontrolle.config(activebackground=Settings.Button_hervorheben_farbe)
        Neue_Textmanager.Menu_Settings.config(activebackground=Settings.Button_hervorheben_farbe)
    else:
        try:
            Settings.Hintergrndfarbe_auswahl.config(activebackground=Settings.Textmanager_Hintergrund)
            Settings.Textfarbe_auswahl.config(activebackground=Settings.Textmanager_Hintergrund)
            Settings.Bildschirm_opt.Bildschirm_bestätigen.config(activebackground=Settings.Textmanager_Hintergrund)
            Settings.Bildschirm_opt1.Bildschirm_bestätigen.config(activebackground=Settings.Textmanager_Hintergrund)
        except: pass
        Neue_Textmanager.Menu_Info.config(activebackground=Settings.Textmanager_Hintergrund)
        Neue_Textmanager.Menu_Help.config(activebackground=Settings.Textmanager_Hintergrund)
        Neue_Textmanager.Menu_Kamera.config(activebackground=Settings.Textmanager_Hintergrund)
        Neue_Textmanager.Menu_LiedKontrolle.config(activebackground=Settings.Textmanager_Hintergrund)
        Neue_Textmanager.Menu_Settings.config(activebackground=Settings.Textmanager_Hintergrund)
        Settings.Check_settings()


def Load_all_collor():
    Settings.Check_settings()
    Neue_Textmanager.Menu_Settings.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
    Neue_Textmanager.Menu_Info.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
    Neue_Textmanager.Menu_LiedKontrolle.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
    Neue_Textmanager.Menu_Help.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
    Neue_Textmanager.Menu_Kamera.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
    Neue_Textmanager.Textmanager.config(bg=Settings.Textmanager_Hintergrund)
    Settings.Textanzeiger_setting_class.Color()
    Settings.Button_hervorheben_class.Color()
    Settings.Vers_kontroll_class.Color()
    Settings.Settings_bildschirm.config(bg=Settings.Textmanager_Hintergrund)
    Settings.Bildschirm_opt.color()
    Settings.Bildschirm_opt1.color()
    Settings.Hintergrndfarbe_auswahl.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
    Settings.Textfarbe_auswahl.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
    if Settings.see_the_text:
        Settings.Text_größe_Textanzeiger.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)