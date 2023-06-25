import Settings
import Load_settings
import Neue_Textmanager

from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tktooltip import *
from tkinter.colorchooser import askcolor





def ResponsiveWidget(widget, *args, **kwargs):
    bindings = {'<Enter>': {'state': 'active'},
                '<Leave>': {'state': 'normal'}}

    w = widget(*args, **kwargs)

    for (k, v) in bindings.items():
        w.bind(k, lambda e, kwarg=v: e.widget.config(**kwarg))
    return w




class Test_info:

    def __init__(self):
        self.Info_manager = Toplevel(Settings.Neue_Textmanager.Textmanager)
        self.Info_manager.geometry("800x600")
        self.Info_manager.config(bg=Settings.Textmanager_Hintergrund)
        self.Text_für_Info = "Entwickler/ Uhrheber: Tobias Giebelhaus\nIn gedenken an meinen Geliebten Opa der bis zum Schluss Geistig fit war und sorgen kurz vor dem Tod im Internet war. Er war ein sehr lieber Opa"
        self.Info_zum_programm = Label(self.Info_manager, font=("Halvetica", 15), bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, text=self.Text_für_Info, wraplength=800)
        self.Info_zum_programm["justify"] = "left"
        self.Info_zum_programm.place(x=0,y=0)
        self.Bild_für_opa1 = Image.open(f"Textmanager Daten\\Textmanager Daten\\Sterbe Anzeige Opa.jpg")
        self.Bild_für_opa = ImageTk.PhotoImage(image=self.Bild_für_opa1.resize((472,341))) 
        self.Bild_für_opa_Label = Label(self.Info_manager,image=self.Bild_für_opa)
        self.Bild_für_opa_Label.place(x=0,y=100)




class Bild_schirm_größe_class:

    def __init__(self, Seite, x_pos, y_pos, bildschirm_große_quere, bilschirm_größe_hoch,  speicherort, Bildschirm, skalierung_list, Text_hover = ""):
        self.speicherort = speicherort
        self.Hauptbildschirm = Label(Seite, font=Settings.Textgröße_von_alle_Texte, text=Bildschirm, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
        self.Hauptbildschirm.place(x=x_pos , y=y_pos-50)
        with open(f"{speicherort}quere.txt", "r", encoding="utf8") as speicherort1:
            self.bildschirm_pos = speicherort1.read()
        self.Bild_größe_stringvar_quere = StringVar()
        self.Bild_größe_stringvar_quere.set(self.bildschirm_pos)
        self.Bildschirm_größe_quere_menü = OptionMenu(Seite, self.Bild_größe_stringvar_quere, *bildschirm_große_quere)
        self.Bildschirm_größe_quere_menü.place(x=x_pos, y=y_pos)
        with open(f"{speicherort}hoch.txt", "r", encoding="utf8") as speicherort1:
            self.bildschirm_pos1 = speicherort1.read()
        self.Bild_größe_stringvar_hoch = StringVar()
        self.Bild_größe_stringvar_hoch.set(self.bildschirm_pos1)
        self.Bildschirm_größe_hoch_menü = OptionMenu(Seite, self.Bild_größe_stringvar_hoch, *bilschirm_größe_hoch)
        self.Bildschirm_größe_hoch_menü.place(x=100+x_pos, y=y_pos)
        self.Bildschirm_bestätigen = ResponsiveWidget(Button, Seite, activebackground=Settings.Button_hervorheben_farbe, font=Settings.Textgröße_von_alle_Texte, fg=Settings.Textmanager_Textfarbe, bg=Settings.Textmanager_Hintergrund, bd=0, text="Bestätigen", command=self.Bildgröße_bestatigen, activeforeground=Settings.Button_hervorheben_farbe)
        self.Bildschirm_bestätigen.place(x=x_pos, y=y_pos+100)
        self.X_bildschirm = Label(Seite, font=Settings.Textgröße_von_alle_Texte,bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, text="X")
        self.X_bildschirm.place(x=x_pos+75, y=y_pos)
        with open(f"{speicherort}Skalierung.txt", "r", encoding="utf8") as Skalierung:
            self.Skalierung = Skalierung.read()
        self.Bildschirm_Skalierung_stringvar_quere = StringVar()
        self.Bildschirm_Skalierung_stringvar_quere.set(self.Skalierung)
        self.Bildschirm_skalierung_quere_menü = OptionMenu(Seite, self.Bildschirm_Skalierung_stringvar_quere, *skalierung_list)
        self.Bildschirm_skalierung_quere_menü.place(x=x_pos, y=y_pos+50)
        if len(Text_hover) > 0:
            self.Text_anzeiger = ToolTip(self.Bildschirm_bestätigen, msg=Text_hover, delay=2, follow=True)
    def Text_size(self, Font_):
        self.Hauptbildschirm.config(font=Font_)
        self.Bildschirm_größe_quere_menü.config(font=Font_)
        self.Bildschirm_größe_hoch_menü.config(font=Font_)
        self.Bildschirm_bestätigen.config(font=Font_)
        self.X_bildschirm.config(font=Font_)


    def Bildgröße_bestatigen(self):
        with open(f"{self.speicherort}hoch.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(self.Bild_größe_stringvar_hoch.get())
        with open(f"{self.speicherort}quere.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(self.Bild_größe_stringvar_quere.get())
        with open(f"{self.speicherort}Skalierung.txt", "w", encoding="utf8") as Skalierung:
            Skalierung.write(self.Bildschirm_Skalierung_stringvar_quere.get())
        Settings.Load_anzeige()

    def Auto_auflösung(self, Screen):
        with open(f"{self.speicherort}hoch.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(str(Screen.winfo_screenheight()))
        self.Bild_größe_stringvar_hoch.set(Screen.winfo_screenheight())
        with open(f"{self.speicherort}quere.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(str(Screen.winfo_screenwidth()))
        self.Bild_größe_stringvar_quere.set(Screen.winfo_screenwidth())
        Settings.Load_anzeige()


    def color(self, bg_color, fg_color, activ_bg, activ_fg):
        self.Bildschirm_bestätigen.config(bg=bg_color,fg=fg_color, activebackground=activ_bg, activeforeground=activ_fg)
        self.X_bildschirm.config(bg=bg_color, fg=fg_color)
        self.Hauptbildschirm.config(bg=bg_color, fg=fg_color)


def Settings_Textanzeiger_def():
    global Settings_Textanzeiger_Top, Textanzeiger_Textfarbe, Textanzeiger_Hintergrund, Bildschirm_opt1, Bildschirm_ausrichtung_button, Text_größe_ändern
    Settings_Textanzeiger_Top = Toplevel()
    Settings_Textanzeiger_Top.geometry("800x600")
    Settings_Textanzeiger_Top.title("Einstellungen für Textanzeiger")
    Settings_Textanzeiger_Top.config(bg=Settings.Textmanager_Hintergrund)
    Textanzeiger_Textfarbe = Farben_class(Settings_Textanzeiger_Top, "Textanzeiger_Textfarbe", 10, 100, "Textfarbe")
    Textanzeiger_Hintergrund = Farben_class(Settings_Textanzeiger_Top, "Textanzeiger_Hintergrund", 150, 100, "Hintergrund")
    Bildschirm_opt1 = Bild_schirm_größe_class(Settings_Textanzeiger_Top, 10, 220, Settings.Bildschirm_auflösung_quere, Settings.Bildschirm_auflösung_hoch ,f"Textmanager Daten\\Textmanager Daten\\Auflösung2", "Textbildschirm", Settings.Skalierung)
    if Settings.Bildschirm_ausrichtung:
        Bildschirm_ausrichtung_button = ResponsiveWidget(Button,Settings_Textanzeiger_Top, font=Settings.Textgröße_von_alle_Texte, text="Rechts", command=Settings.Links, bd=0)
    else:
        Bildschirm_ausrichtung_button = ResponsiveWidget(Button, Settings_Textanzeiger_Top, font=Settings.Textgröße_von_alle_Texte, text="Links", command=Settings.Rechts, bd=0)
    Bildschirm_ausrichtung_button.place(x=220,y=250)
    Text_größe_ändern = Text_scalierung(Settings_Textanzeiger_Top, Settings.Text_size_def, 10, 10, from__=0, to_=100, orient_=HORIZONTAL, backgrund=Settings.Textmanager_Hintergrund, foregrund=Settings.Textmanager_Textfarbe, aktuelle_zahl=Settings.Text_anzeiger_textgröße)
    Load_settings.Load_all_collor()


class Text_scalierung():
    def __init__(self, Anzeige_ort, command_, x_pos, y_pos, from__ = 0, to_= 100, orient_ = HORIZONTAL, backgrund= "Black", foregrund = "blue", font_ = 24, lengt = 300, with_ = 300, aktuelle_zahl = 10):
        self.Text_größe_Textanzeiger = Scale(Anzeige_ort, from_=from__, to=to_, orient= orient_, background=backgrund, foreground=foregrund, bd=0,font=font_, length=300, width=font_, command=command_, tickinterval=25)
        self.Text_größe_Textanzeiger.set(aktuelle_zahl)
        self.Text_größe_Textanzeiger.place(y=y_pos, x=x_pos)
        Load_settings.Load_all_collor()
    def color_farb(self,  active_vorgrund, backgrund, foregrund = "green"):
        self.Text_größe_Textanzeiger.config(activebackground=active_vorgrund, bg=backgrund, fg=foregrund)


class Swich_generator:
    def __init__(self, Settings_is, x_pos, y_pos, Textnazeige, x_pos_text, Text_datei_save, ob_True, def_bei_offbutton, Text_hover = "", zise = 10):
        self.Text_datei_save = Text_datei_save
        self.def_bei_offbutton = def_bei_offbutton
        self.zise = int(zise)
        self.is_switch = ResponsiveWidget(Button, Settings_is, activebackground=Settings.Textmanager_Hintergrund)
        self.switch_text = Label(Settings_is, font=("Helvetica", 12), bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, text=Textnazeige)
        self.switch_text.place(x=x_pos_text, y=y_pos + 12)
        if not ob_True:
            self.Photo1 = Image.open("off-button.png")
            self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*int(zise),3*int(zise))))
            self.is_switch.config(image=self.Photo, bg=Settings.Textmanager_Hintergrund, border=0, command=self.switch_setting_on)
        else:
            self.Photo1 = Image.open("on-button.png")
            self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*int(zise),3*int(zise))))
            self.is_switch.config(image=self.Photo, bg=Settings.Textmanager_Hintergrund, border=0, command=self.switch_setting_off)
        if len(Text_hover) > 0:
            self.Text_anzeiger = ToolTip(self.is_switch, msg=Text_hover, delay=2, follow=True)
        self.is_switch.place(x=x_pos, y=y_pos)


    def color(self, bg_color, fg_color, activ_bg, activ_fg):
        self.switch_text.config(bg=bg_color,fg=fg_color)
        self.is_switch.config(bg=bg_color)

    def switch_setting_off(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("False")
        self.Photo1 = Image.open("off-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*self.zise,3*self.zise)))
        self.is_switch.configure(image=self.Photo, command= self.switch_setting_on)
        self.def_bei_offbutton()



    def switch_setting_on(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("True")
        self.Photo1 = Image.open("on-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*self.zise,3*self.zise)))
        self.is_switch.configure(image=self.Photo, command=self.switch_setting_off)
        self.def_bei_offbutton()

    def Text_size(self, Font_, size):
        self.switch_text.config(font=Font_)
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*size,3*size)))
        self.is_switch.configure(image=self.Photo)
        self.is_switch.place()


class Farben_class:

    def __init__(self, Anzeigefenster, Farbe_ort, x_place, y_place, Name, Text_hover = ""):
        self.Farbe_ort = Farbe_ort
        self.Hintergrndfarbe_auswahl = ResponsiveWidget(Button, Anzeigefenster, font=Settings.Textgröße_von_alle_Texte, fg=Settings.Textmanager_Textfarbe, bg=Settings.Textmanager_Hintergrund, text=Name, command=self.Farbe_def, border=0)
        self.Hintergrndfarbe_auswahl.place(x= x_place, y= y_place)
        if len(Text_hover) > 0:
            self.Text_anzeiger = ToolTip(self.Hintergrndfarbe_auswahl, msg=Text_hover, delay=2, follow=True)


    def Farbe_def(self):
        color = askcolor()  
        if not (color[1]) == None:
            with open(f"Textmanager Daten\\Textmanager Daten\\{self.Farbe_ort}.txt", "w", encoding='utf8') as Neue_Texmanager_Textfarbe:
                Neue_Texmanager_Textfarbe.write(color[1])
        Load_settings.Load_all_collor()

    def color(self, bg_color, fg_color, activ_bg, activ_fg):
        self.Hintergrndfarbe_auswahl.config(bg=bg_color, fg=fg_color, activebackground=activ_bg, activeforeground=activ_fg)
    
    def Text_size(self, Font_):
        self.Hintergrndfarbe_auswahl.config(font= Font_)
