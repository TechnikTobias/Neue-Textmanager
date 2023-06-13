import Settings
import Load_settings
import Neue_Textmanager

from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont




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

    def __init__(self, Seite, x_pos, y_pos, bildschirm_große_quere, bilschirm_größe_hoch,  speicherort, Bildschirm):
        self.speicherort = speicherort
        self.Hauptbildschirm = Label(Seite, font=("Helvetica", 20), text=Bildschirm, bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
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
        self.Bildschirm_bestätigen = ResponsiveWidget(Button, Seite, activebackground=Settings.Button_hervorheben_farbe, font=("Helvetica", 20), fg=Settings.Textmanager_Textfarbe, bg=Settings.Textmanager_Hintergrund, bd=0, text="Bestätigen", command=self.Bildgröße_bestatigen, activeforeground=Settings.Button_hervorheben_farbe)
        self.Bildschirm_bestätigen.place(x=x_pos, y=y_pos+50)
        self.X_bildschirm = Label(Seite, font=("Helvetica", 20),bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, text="X")
        self.X_bildschirm.place(x=x_pos+75, y=y_pos)


    def Bildgröße_bestatigen(self):
        with open(f"{self.speicherort}hoch.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(self.Bild_größe_stringvar_hoch.get())
        with open(f"{self.speicherort}quere.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(self.Bild_größe_stringvar_quere.get())

    def Auto_auflösung(self, Screen):
        with open(f"{self.speicherort}hoch.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(str(Screen.winfo_screenheight()))
        self.Bild_größe_stringvar_hoch.set(Screen.winfo_screenheight())
        with open(f"{self.speicherort}quere.txt", "w", encoding="utf8") as speicherort1:
            speicherort1.write(str(Screen.winfo_screenwidth()))
        self.Bild_größe_stringvar_quere.set(Screen.winfo_screenwidth())


    def color(self):
        self.Bildschirm_bestätigen.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
        self.X_bildschirm.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)
        self.Hauptbildschirm.config(bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe)

def Text_scalierung():
    Settings.Text_größe_Textanzeiger = Scale(Settings.Settings_bildschirm, from_=0, to=100, orient= HORIZONTAL, background=Settings.Textmanager_Hintergrund, foreground=Settings.Textmanager_Textfarbe, bd=0,font=24, length=300, width=25, command=Settings.Text_size_def, tickinterval=25)
    Settings.Text_größe_Textanzeiger.set(Settings.Text_anzeiger_textgröße)
    Settings.Text_größe_Textanzeiger.place(y=10, x=250)


class Swich_generator:
    def __init__(self, Settings_is, x_pos, y_pos, Textnazeige, x_pos_text, Text_datei_save, ob_True, def_bei_offbutton, def_bei_onbutton):
        self.Text_datei_save = Text_datei_save
        self.def_bei_offbutton = def_bei_offbutton
        self.def_bei_onbutton = def_bei_onbutton
        self.is_switch = ResponsiveWidget(Button, Settings_is, activebackground=Settings.Textmanager_Hintergrund)
        self.switch_text = Label(Settings_is, font=("Helvetica", 12), bg=Settings.Textmanager_Hintergrund, fg=Settings.Textmanager_Textfarbe, text=Textnazeige)
        self.switch_text.place(x=x_pos_text, y=y_pos + 12)
        if not ob_True:
            self.Photo1 = Image.open("off-button.png")
            self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
            self.is_switch.config(image=self.Photo, bg=Settings.Textmanager_Hintergrund, border=0, command=self.switch_setting_on)
        else:
            self.Photo1 = Image.open("on-button.png")
            self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
            self.is_switch.config(image=self.Photo, bg=Settings.Textmanager_Hintergrund, border=0, command=self.switch_setting_off)
        self.is_switch.place(x=x_pos, y=y_pos)


    def Color(self):
        self.switch_text.config(bg=Settings.Textmanager_Hintergrund,fg=Settings.Textmanager_Textfarbe)
        self.is_switch.config(bg=Settings.Textmanager_Hintergrund)


    def switch_setting_off(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("False")
        self.Photo1 = Image.open("off-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command= self.switch_setting_on)
        self.def_bei_offbutton()
        self.Photo1 = Image.open("off-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command= self.switch_setting_on)


    def switch_setting_on(self):
        with open(f"{self.Text_datei_save}", "w", encoding='utf8') as see_the_textinfo:
            see_the_textinfo.write("True")
        self.Photo1 = Image.open("on-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command=self.switch_setting_off)
        self.def_bei_onbutton()
        self.Photo1 = Image.open("on-button.png")
        self.Photo = ImageTk.PhotoImage(self.Photo1.resize((50,50)))
        self.is_switch.configure(image=self.Photo, command=self.switch_setting_off)
