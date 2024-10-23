import Settings
import Load_settings
import Neue_Textmanager

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont
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
        hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        text_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
        self.Info_manager = Toplevel(Neue_Textmanager.Textmanager)
        self.Info_manager.geometry("800x600")
        self.Info_manager.config(bg=hintergrund_farbe)
        self.Text_für_Info = "Entwickler/ Uhrheber: Tobias Giebelhaus\nIn gedenken an meinen Geliebten Opa der bis zum Schluss Geistig fit war und sorgen kurz vor dem Tod im Internet war. Er war ein sehr lieber Opa"
        self.Info_zum_programm = Label(self.Info_manager, font=("Halvetica", 15), bg=hintergrund_farbe, fg=text_farbe, text=self.Text_für_Info, wraplength=800)
        self.Info_zum_programm["justify"] = "left"
        self.Info_zum_programm.place(x=0,y=0)
        self.Bild_für_opa1 = Image.open(f"Textmanager Daten/Textmanager Daten/Sterbe Anzeige Opa.jpg")
        self.Bild_für_opa = ImageTk.PhotoImage(image=self.Bild_für_opa1.resize((472,341))) 
        self.Bild_für_opa_Label = Label(self.Info_manager,image=self.Bild_für_opa)
        self.Bild_für_opa_Label.place(x=0,y=100)




class Bild_schirm_größe_class:

    def __init__(self, Seite, bildschirm_große_quere, bilschirm_größe_hoch,  speicherort, Bildschirm, skalierung_list, Text_hover = ""):
        hintergrund_farbe = Neue_Textmanager.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        text_farbe = Neue_Textmanager.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
        self.speicherort = speicherort
        self.Hauptbildschirm = Label(Seite, font=Settings.Textgröße_von_alle_Texte, text=Bildschirm, bg=hintergrund_farbe, fg=text_farbe)
        with open(f"{speicherort}quere.txt", "r", encoding="utf8") as speicherort1:
            self.bildschirm_pos = speicherort1.read()
        self.Bild_größe_stringvar_quere = StringVar()
        self.Bild_größe_stringvar_quere.set(self.bildschirm_pos)
        self.Bildschirm_größe_quere_menü = OptionMenu(Seite, self.Bild_größe_stringvar_quere, *bildschirm_große_quere)
        self.Bildschirm_größe_quere_menü.config(font=Settings.Textgröße_von_alle_Texte)
        with open(f"{speicherort}hoch.txt", "r", encoding="utf8") as speicherort1:
            self.bildschirm_pos1 = speicherort1.read()
        self.Bild_größe_stringvar_hoch = StringVar()
        self.Bild_größe_stringvar_hoch.set(self.bildschirm_pos1)
        self.Bildschirm_größe_hoch_menü = OptionMenu(Seite, self.Bild_größe_stringvar_hoch, *bilschirm_größe_hoch)
        self.Bildschirm_größe_hoch_menü.config(font=Settings.Textgröße_von_alle_Texte)
        self.Bildschirm_bestätigen = ResponsiveWidget(Button, Seite, activebackground=Settings.Button_hervorheben_farbe, font=Settings.Textgröße_von_alle_Texte, fg=text_farbe, bg=hintergrund_farbe, bd=0, text="Bestätigen", command=self.Bildgröße_bestatigen, activeforeground=Settings.Button_hervorheben_farbe)
        self.X_bildschirm = Label(Seite, font=Settings.Textgröße_von_alle_Texte,bg=hintergrund_farbe, fg=text_farbe, text="X")
        with open(f"{speicherort}Skalierung.txt", "r", encoding="utf8") as Skalierung:
            self.Skalierung = Skalierung.read()
        self.Bildschirm_Skalierung_stringvar_quere = StringVar()
        self.Bildschirm_Skalierung_stringvar_quere.set(self.Skalierung)
        self.Bildschirm_skalierung_quere_menü = OptionMenu(Seite, self.Bildschirm_Skalierung_stringvar_quere, *skalierung_list)
        self.Bildschirm_skalierung_quere_menü.config(font=Settings.Textgröße_von_alle_Texte)


    def Text_size(self, Font_, size=10, x_pos = 20, y_pos= 50):
        self.Hauptbildschirm.config(font=Font_)
        self.Bildschirm_größe_quere_menü.config(font=Font_)
        self.Bildschirm_größe_hoch_menü.config(font=Font_)
        self.Bildschirm_bestätigen.config(font=Font_)
        self.X_bildschirm.config(font=Font_)
        self.Bildschirm_skalierung_quere_menü.config(font=Font_)
        self.Hauptbildschirm.place(x=x_pos, y=y_pos-int(Settings.text_size)*2.5)
        self.Bildschirm_größe_hoch_menü.place(x=40+float(Settings.text_size)*4.4+x_pos, y=y_pos)
        self.X_bildschirm.place(x=40+x_pos+int(Settings.text_size)*3.2, y=y_pos)
        self.Bildschirm_größe_quere_menü.place(x=x_pos, y=y_pos)
        self.Bildschirm_bestätigen.place(x=x_pos, y=y_pos+25+int(Settings.text_size)*5)
        self.Bildschirm_skalierung_quere_menü.place(x=x_pos, y=y_pos+10+int(Settings.text_size)*2.7)


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





class Text_scalierung():
    def __init__(self, Anzeige_ort, command_, from__ = 10, to_= 200, orient_ = HORIZONTAL, backgrund= "Black", foregrund = "blue", font_ = 24, lengt = 300, with_ = 300, aktuelle_zahl = 10, size= 10,tickinterval = 25):
        self.Text_größe_Textanzeiger = Scale(Anzeige_ort, from_=from__, to=to_, orient= orient_, background=backgrund, foreground=foregrund, bd=0,font=font_,  command=command_, tickinterval=tickinterval)
        self.Text_größe_Textanzeiger.set(aktuelle_zahl)
        Load_settings.Load_all_collor()
    
    def color_farb(self,  active_vorgrund, backgrund, foregrund = "green"):
        self.Text_größe_Textanzeiger.config(activebackground=active_vorgrund, bg=backgrund, fg=foregrund)

    def Text_size(self, font_ = 10, size= 10, Y_ground = 10, Y_factor = 5):
        factor = int(Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",))[0])/100
        self.Text_größe_Textanzeiger.config(font=font_, length=size*15, width=size*2)
        self.Text_größe_Textanzeiger.place(y=Y_ground+Y_factor*size, relheight=0.15*factor, relwidth=0.8*factor)


class Swich_generator:
    def __init__(self, Settings_is, Textanzeige, Text_datei_save, ob_True, def_bei_offbutton, Text_hover = "", zise = 10):
        hintergrund_farbe = Neue_Textmanager.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        text_farbe = Neue_Textmanager.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
        self.Text_datei_save = Text_datei_save
        self.def_bei_offbutton = def_bei_offbutton
        self.zise = int(Settings.text_size)
        self.is_switch = ResponsiveWidget(Button, self, activebackground=hintergrund_farbe)
        self.switch_text = Label(self, font=("Helvetica", zise), bg=hintergrund_farbe, fg=text_farbe, text=Textanzeige)
        if not ob_True:
            self.Photo1 = Image.open("off-button.png")
            self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*int(Settings.text_size),3*int(Settings.text_size))))
            self.is_switch.config(image=self.Photo, bg=hintergrund_farbe, border=0, command=self.switch_setting_on)
        else:
            self.Photo1 = Image.open("on-button.png")
            self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*int(Settings.text_size),3*int(Settings.text_size))))
            self.is_switch.config(image=self.Photo, bg=hintergrund_farbe, border=0, command=self.switch_setting_off)



    def color(self, bg_color, fg_color, activ_bg, activ_fg):
        self.switch_text.config(bg=bg_color,fg=fg_color)
        hintergrund_farbe = Neue_Textmanager.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        self.is_switch.config(bg=bg_color, activebackground=hintergrund_farbe)

    def switch_setting_off(self):
        Neue_Textmanager.db_connection_info_write("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", ("False",f"{self.Text_datei_save}"))
        self.Photo1 = Image.open("off-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*int(Settings.text_size),3*int(Settings.text_size))))
        self.is_switch.configure(image=self.Photo, command= self.switch_setting_on)
        self.def_bei_offbutton()



    def switch_setting_on(self):
        Neue_Textmanager.db_connection_info_write("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", ("True",f"{self.Text_datei_save}"))
        self.Photo1 = Image.open("on-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*int(Settings.text_size),3*int(Settings.text_size))))
        self.is_switch.configure(image=self.Photo, command=self.switch_setting_off)
        self.def_bei_offbutton()

    def Text_size(self, Font_, size, x_ground = 10, x_factor = 0, y_ground = 10, y_factor = 0):
        self.switch_text.config(font=Font_)
        self.switch_text.place(y=y_ground+size*y_factor + 0.8*int(size)-4, x=x_ground+size*x_factor+size*3)
        self.is_switch.place(y=y_ground+size*y_factor, x=x_ground+size*x_factor)
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((3*size,3*size)))
        self.is_switch.configure(image=self.Photo)






