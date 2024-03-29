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
        Settings.Text_größe_ändern.color_farb(backgrund=Hintergrund, foregrund=Textfarbe, active_vorgrund=Aufleuchtfarbe_Hintergrund)
        Settings.Bildschirm_opt1.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Bildschirm_ausrichtung_button.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
        Settings.Textanzeiger_Hintergrund_Button.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Textanzeiger_Textfarbe_button.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Textanzeiger_setting_class.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Liedvorschau.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
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
        Settings.Bildschirm_opt.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Button_hervorheben_class.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
    except:
        pass
    try:
        Settings.Settings_bildschirm.config(bg=Hintergrund)
        Settings.Setings_Textanzeiger.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
        Settings.Settings_Graphig_option.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
        Settings.Smarte_unterstüzung_button.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
    except: pass
    try:
        Settings.Settings_smarte_unterstüzung.config(bg=Settings.Textmanager_Hintergrund)
        Settings.RichtigeVersereihenfolge.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Smarte_Verse.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Smarte_vorschlage_Button.color(Hintergrund, Textfarbe, Aufleuchtfarbe_Hintergrund, Aufleuchtfarbe_Textfarbe)
        Settings.Smarte_vorschlage_Button_top.config(bg=Hintergrund, fg=Textfarbe, activebackground=Aufleuchtfarbe_Hintergrund, activeforeground=Aufleuchtfarbe_Textfarbe)
    except: pass

def Load_text_size(Text_größe_übergabe):
    Settings.Textgröße_von_alle_Texte.config(size=Text_größe_übergabe)
    with open(f"Textmanager Daten\\Textmanager Daten\\text_size.txt", "w", encoding='utf8') as text_size:
        text_size.write(Text_größe_übergabe)
    Settings.text_size = Text_größe_übergabe
    try:
        Settings.Textanzeiger_setting_class.Text_size(Settings.Textgröße_von_alle_Texte, int(Text_größe_übergabe))
        Settings.Textanzeiger_Hintergrund_Button.Text_size(Settings.Textgröße_von_alle_Texte, Factor_x=0, Factor_y=10)
        Settings.Textanzeiger_Textfarbe_button.Text_size(Settings.Textgröße_von_alle_Texte, Factor_x=11, Factor_y=10)
        Settings.Bildschirm_opt1.Text_size(Settings.Textgröße_von_alle_Texte, x_pos=10, y_pos=50+13*int(Settings.text_size))
        Settings.Bildschirm_ausrichtung_button.config(font=Settings.Textgröße_von_alle_Texte)
        Settings.Bildschirm_ausrichtung_button.place(x=50+int(Settings.text_size)*12,y=70+int(Settings.text_size)*11)
        Settings.Text_größe_ändern.Text_size(font_=Settings.Textgröße_von_alle_Texte, size=int(Settings.text_size), Y_factor=4, Y_ground=10)
        Settings.Liedvorschau_Button.Text_size(Font_=Settings.Textgröße_von_alle_Texte, size=int(Settings.text_size), y_factor=21, y_ground=70)
    except: pass
    try:
        Settings.Hintergrndfarbe_auswahl.Text_size(Settings.Textgröße_von_alle_Texte,Factor_y=19, Y_Start=70,Factor_x=0)
        Settings.Textfarbe_auswahl.Text_size(Settings.Textgröße_von_alle_Texte,Factor_x=13, Factor_y=19, Y_Start=70)
        Settings.Button_Textfarbe_Button.Text_size(Settings.Textgröße_von_alle_Texte,Factor_x=0, Factor_y=22,Y_Start=100)
        Settings.Button_Hintergrndfarbe_auswahl.Text_size(Settings.Textgröße_von_alle_Texte,Factor_x=13, Factor_y=22,Y_Start=100)
        Settings.Text_größe_anpassen.Text_size(font_=Settings.Textgröße_von_alle_Texte, size=int(Settings.text_size), Y_factor= 3, Y_ground=25)
        Settings.Bildschirm_opt.Text_size(Font_=Settings.Textgröße_von_alle_Texte, size=int(Settings.text_size), x_pos=10, y_pos=50+11*int(Settings.text_size))
        Settings.Button_hervorheben_class.Text_size(Font_=Settings.Textgröße_von_alle_Texte, size=int(Settings.text_size))
    except: pass
    try:
        Settings.Settings_Graphig_option.config(font=Settings.Textgröße_von_alle_Texte)
        Settings.Setings_Textanzeiger.config(font=Settings.Textgröße_von_alle_Texte)
        Settings.Settings_Graphig_option.place(x=10, y=20+4*int(Settings.text_size))
        Settings.Setings_Textanzeiger.place(y=10, x=10)
        Settings.Smarte_unterstüzung_button.place(x=10, y=40+8*int(Settings.text_size))
        Settings.Smarte_unterstüzung_button.config(font= Settings.Textgröße_von_alle_Texte)
    except: pass
    try:
        Settings.Smarte_Verse.Text_size(y_factor=0, x_factor=0, x_ground=10, y_ground=10, Font_=Settings.Textgröße_von_alle_Texte, size=int(Settings.text_size))
        Settings.RichtigeVersereihenfolge.Text_size(y_ground=20, y_factor=2, x_ground=10, x_factor=0, Font_=Settings.Textgröße_von_alle_Texte, size=int(Settings.text_size))
        Settings.Smarte_vorschlage_Button.Text_size(y_ground=30, y_factor=4, x_ground=10, x_factor=0, Font_=Settings.Textgröße_von_alle_Texte, size=int(Settings.text_size))
        Settings.Smarte_vorschlage_Button_top.place(x=10, y=40+6*int(Settings.text_size))
        Settings.Smarte_vorschlage_Button_top.config(font= Settings.Textgröße_von_alle_Texte)
    except: pass