import Settings
import Neue_Textmanager
import Class_gen

from tkinter import *
import tkinter.font as tkFont

def Load_Text_anzeiger():
    if Settings.see_the_text:
        global AnzeigeText, Font1, Text_Anzeige_Label
        try: AnzeigeText.config(bg="black")
        except:
            with open (f"Textmanager Daten\\Textmanager Daten\\Auflösungquere.txt", "r", encoding='utf8') as Hoch_auflösung:
                Quere_auflösung = Hoch_auflösung.read()
            with open (f"Textmanager Daten\\Textmanager Daten\\Auflösung2hoch.txt", "r", encoding='utf8') as Hoch_auflösung:
                Hoch_auflösung1 = Hoch_auflösung.read()
            with open (f"Textmanager Daten\\Textmanager Daten\\Auflösung2quere.txt", "r", encoding='utf8') as Hoch_auflösung:
                Quere_auflösung1 = Hoch_auflösung.read()
            with open (f"Textmanager Daten\\Textmanager Daten\\AuflösungSkalierung.txt", "r", encoding='utf8') as Hoch_auflösung:
                Skalierung = Hoch_auflösung.read()
            with open (f"Textmanager Daten\\Textmanager Daten\\Auflösung2Skalierung.txt", "r", encoding='utf8') as Hoch_auflösung:
                Skalierung1 = Hoch_auflösung.read()
            if Settings.Bildschirm_ausrichtung:
                Plusor_muínus = + int(int(Quere_auflösung)/int(Skalierung)*100)
            else:
                Plusor_muínus = - int(int(Quere_auflösung1)/int(Skalierung1)*100)
            Font1 = tkFont.Font(family="Helvetica",size= Settings.Text_anzeiger_textgröße)
            AnzeigeText = Toplevel(Neue_Textmanager.Textmanager)
            AnzeigeText.config(bg=Settings.Textmanager_Hintergrund)
            AnzeigeText.geometry(f"100x100+{Plusor_muínus}+0")
            AnzeigeText.overrideredirect(True)
            Text_Anzeige_Label = Label(AnzeigeText, font=Font1, fg="white", bg="black", wraplength=int(int(Quere_auflösung1)/int(Skalierung1)*100))
            Text_Anzeige_Label.config(text="Hallo Welt, wie gehts euch, das ist ein test text, der text soll normal angezeigt werden")
            Text_Anzeige_Label["justify"] = "left"
            Text_Anzeige_Label.place(x=0, y=0)
            AnzeigeText.geometry(f"{int(int(Quere_auflösung1)/int(Skalierung1)*100)}x{int(int(Hoch_auflösung1)/int(Skalierung1)*100)}+{Plusor_muínus}+0")
    else: 
        try:
            AnzeigeText.destroy()
        except: pass




def Load_all_collor():
    Settings.Check_settings()
    Hintergrund = Settings.Textmanager_Hintergrund
    Textfarbe = Settings.Textmanager_Textfarbe
    if Settings.Button_hervorheben:
        Aufleuchtfarbe_Hintergrund = Settings.Button_hervorheben_farbe
        Aufleuchtfarbe_Textfarbe = Settings.Button_Textfarbe
    else:
        Aufleuchtfarbe_Hintergrund = Settings.Textmanager_Hintergrund
        Aufleuchtfarbe_Textfarbe = Settings.Textmanager_Textfarbe
    if Settings.see_the_text:
        AnzeigeText.config(bg=Settings.Textanzeiger_Hintergrund)
        Text_Anzeige_Label.config(bg=Settings.Textanzeiger_Hintergrund, fg=Settings.Textanzeiger_Textfarbe)
    try: 
        Class_gen.Text_größe_ändern.color_farb(backgrund=Hintergrund, foregrund=Textfarbe, active_vorgrund=Aufleuchtfarbe_Hintergrund)
        Class_gen.Bildschirm_opt1.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Class_gen.Bildschirm_ausrichtung_button.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
        Class_gen.Textanzeiger_Hintergrund.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Class_gen.Textanzeiger_Textfarbe.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
    except: pass
    Neue_Textmanager.Menu_Settings.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
    Neue_Textmanager.Menu_Info.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
    Neue_Textmanager.Menu_LiedKontrolle.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
    Neue_Textmanager.Menu_Help.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
    Neue_Textmanager.Menu_Kamera.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
    Neue_Textmanager.Textmanager.config(bg=Hintergrund)
    try:
        Settings.Graphig_bildschirm.config(bg=Hintergrund)
        Settings.Hintergrndfarbe_auswahl.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Textfarbe_auswahl.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Button_Textfarbe_Button.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Button_Hintergrndfarbe_auswahl.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Text_größe_anpassen.color_farb(backgrund=Hintergrund, foregrund=Textfarbe, active_vorgrund=Aufleuchtfarbe_Hintergrund)
    except:
        pass
    try:
        Settings.Settings_bildschirm.config(bg=Hintergrund)
        Settings.Setings_Textanzeiger.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
        Settings.Settings_Graphig_option.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
        Class_gen.Textanzeiger_setting_class.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Bildschirm_opt.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Button_hervorheben_class.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
    except: pass


def Load_text_size(Text_größe_übergabe):
    Settings.Textgröße_von_alle_Texte.config(size=Text_größe_übergabe)
    with open(f"Textmanager Daten\\Textmanager Daten\\text_size.txt", "w", encoding='utf8') as text_size:
        text_size.write(Text_größe_übergabe)
    Settings.Hintergrndfarbe_auswahl.Text_size(Settings.Textgröße_von_alle_Texte)
    Settings.text_size = Text_größe_übergabe
    try:
        Class_gen.Textanzeiger_setting_class.Text_size(Settings.Textgröße_von_alle_Texte, int(Text_größe_übergabe))
        Class_gen.Textanzeiger_Hintergrund.Text_size(Settings.Text_anzeiger_textgröße)
        Class_gen.Textanzeiger_Textfarbe.Text_size(Settings.Textgröße_von_alle_Texte)
        Class_gen.Bildschirm_opt1.Text_size(Settings.Textgröße_von_alle_Texte)
    except:
        pass
    try:
        Settings.Hintergrndfarbe_auswahl.Place_def(Factor_y=18,Factor_x=0)
        Settings.Textfarbe_auswahl.Place_def(Factor_x=13, Factor_y=18)
        Settings.Button_Textfarbe_Button.Place_def(Factor_x=0, Factor_y=22)
        Settings.Button_Hintergrndfarbe_auswahl.Place_def(Factor_x=13, Factor_y=22)
    except:
        pass