from tkinter import *
import tkinter.ttk as ttk
import os
import sqlite3

import ablauf
import Settings
import Kamera
import datenverarbeiten
import Load_settings


class TextmanagerAPP:
    def __init__(self) -> None:
        self.hintergrund_farbe = self.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("textanzeiger_hintergrund",))
        self.Textmanager = Tk()
        self.Textmanager.title("Textmanager")
        self.Textmanager.geometry("1040x800")
        self.Textmanager.config(bg=self.hintergrund_farbe)
        self.widget_info = {}
        self.widget_info_liedauswahl = {}
        self.Menu_generator()
        verses = self.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("Ablauf",))
        input_lieder = (str(verses).split("!"))
        for pos, i in enumerate (input_lieder):
            self.gegerator_lieder(i, power_range=pos+1)
        self.Textmanager.bind("<Configure>", self.one_resize)
        self.update_widget_positions()
        self.Textmanager.mainloop()


    def one_resize(self,event):
        Load_settings.Textmanager_größen(self)


    def get_window_size(self):
        return self.Textmanager.winfo_width(), self.Textmanager.winfo_height()

    def festgröße_bestimmen(self):
        Load_settings.Textmanager_größen(self)

    def register_widget(self,
            name: str, 
            widget: Widget = None, 
            relheight: int = 0.1, 
            relwidth : int = 0.11,
            relx: int = None, 
            rely: int = None):
        """Registriert ein Widget und speichert seine Informationen
        Hier werden die Info für die Widget übergeben damit sie an einer zentrallen stelle placiert werden und deren größe angepasst wird."""
        self.widget_info[name] = {
            "widget": widget,
            "relheight": relheight,
            "relwidth": relwidth,
            "relx": relx,
            "rely": rely
        }

    def register_widegets_liedaktualisieren(self,
                             name,
                             liednummer,
                             versnummer,
                             liedanzeige,
                             buchauswahl):
        """Regestiert die Liedauwahl und lasst das richtige lied erscheinen"""
        self.widget_info_liedauswahl[name] = {
            "liednummer": liednummer,
            "versnummer": versnummer,
            "liedanzeige": liedanzeige,
            "buchauswahl": buchauswahl
        }



    def get_db_connection(self):
        self.db_filename = "Lieder_Datenbank.db"
        self.db_path = os.path.join(os.path.dirname(__file__), self.db_filename)
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def db_connection_info_write(self, input_db, input_db_variabel):
        self.conn = self.get_db_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute(input_db, input_db_variabel)
        self.conn.commit()
        self.conn.close()


    def db_connection_info_get(self, input_db, input_db_variabel):
        self.conn = self.get_db_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute(input_db, input_db_variabel)
        self.Ausgabe = self.cursor.fetchall()
        self.conn.close()
        if self.Ausgabe: return self.Ausgabe[0][0]
        
    

    def Menu_generator(self):
        hintergrund_farbe = self.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        text_farbe = self.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
        self.menu_info_main = ttk.Menubutton(self.Textmanager, text='Info', style='custom.TMenubutton')
        menu_info = Menu(self.menu_info_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_kamera_main = ttk.Menubutton(self.Textmanager, text="Kamera", style='custom.TMenubutton')
        menu_kamera = Menu(self.menu_kamera_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_liedkontrolle_main = ttk.Menubutton(self.Textmanager, text="Liedkontrolle", style='custom.TMenubutton')
        menu_liedkontrolle = Menu(self.menu_liedkontrolle_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_help_main = ttk.Menubutton(self.Textmanager, text="Hilfe", style='custom.TMenubutton')
        menu_help = Menu(self.menu_help_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        menu_info.add_radiobutton(label="Einstellungen", command=Load_settings.Textmanager_größen(self))
        menu_info.add_radiobutton(label="Info", command=Settings.Info)
        menu_kamera.add_command(label="Einstellungen", command=Kamera.Settings)
        menu_kamera.add_command(label="Position", command=Kamera.Position)
        menu_liedkontrolle.add_command(label="Einstellungen")
        menu_liedkontrolle.add_command(label="Lied Kontrolieren", command=datenverarbeiten.setup_ui)
        menu_help.add_command(label="Hilfe")
        self.menu_info_main['menu'] = menu_info
        self.menu_kamera_main['menu'] = menu_kamera
        self.menu_help_main["menu"] = menu_help
        self.menu_liedkontrolle_main["menu"] = menu_liedkontrolle
        self.menu_info_main.pack(side=LEFT, anchor=NW)
        self.menu_kamera_main.pack(side=LEFT, anchor=NW)
        self.menu_liedkontrolle_main.pack(side=LEFT, anchor=NW)
        self.menu_help_main.pack(side=LEFT, anchor=NW)
        


    def gegerator_lieder(self, input, power_range):
        ja = input.split(",")
        name_lied = ja[0].split(":")
        aktion = ja[1].split(":")
        inhalt = []
        inhalt.append([aktion[1], name_lied[1]])
        self.Lied_start = ttk.Label(self.Textmanager, text=name_lied[1], style='TLabel')
        self.register_widget(f"Lied_start{power_range}", self.Lied_start, relheight=0.05, relwidth=0.15, rely=0.1*power_range-0.05, relx=0.0)
        if aktion[1] == " Textwort":
            self.Button_Textwort = ttk.Button(self.Textmanager, text="Textwort", style='TButton')
            self.register_widget(f"Button_textwort{power_range}", self.Button_Textwort, relheight=0.1, relwidth=0.15, rely=0.1*power_range-0.05, relx=0.15)
        elif aktion[1] == " Lied":
            self.Button_Kamera = ttk.Button(self.Textmanager, text="Kamera", style='TButton')
            self.register_widget(f"Button_Kamera{power_range}", self.Button_Kamera, relheight=0.05, relwidth=0.15, rely=0.1*power_range, relx=0)
            befehle = ["Kamera", "Textwort", "Lied"]
            clicked = StringVar()
            clicked.set(befehle[0])
            opt = ttk.OptionMenu(self.Textmanager, clicked, *befehle, style='custom.TMenubutton')
            inhalt.append(clicked)
            inhalt.append(opt)
            self.eingabe_lied = ttk.Entry(self.Textmanager, style='TEntry')
            self.eingabe_lied.bind("<KeyRelease>", self.liedanzeige_aktualisieren)
            self.register_widget(name=f"eingabe_lieder{power_range}",widget=self.eingabe_lied, relheight=0.05, relwidth=0.05, relx=0.35, rely=0.1*power_range-0.05)
            self.eingabe_vers = ttk.Entry(self.Textmanager, style='TEntry')
            self.eingabe_vers.bind("<KeyRelease>", self.liedanzeige_aktualisieren)
            self.register_widget(name=f"eingabe_verse{power_range}", widget=self.eingabe_vers, relheight=0.05, relwidth=0.05, relx=0.35, rely=0.1*power_range)
            self.befehle_buch = ["Gesangbuch", "Chorbuch", "Jugendliederbuch"]
            self.clicked_buch = StringVar()
            self.clicked_buch.set(self.befehle_buch[0])
            self.opt_buch = ttk.OptionMenu(self.Textmanager, self.clicked_buch, *self.befehle_buch, command=self.liedanzeige_aktualisieren)
            self.register_widget(name=f"opt_buch{power_range}", widget=self.opt_buch, relheight=0.05, relwidth=0.2, relx=0.15, rely=0.1*power_range-0.05)
            self.text_lied_lable = ttk.Label(self.Textmanager)
            self.register_widget(name=f"text_lied_lable{power_range}", widget=self.text_lied_lable, relheight=0.1, relwidth=0.2, relx=0.405, rely=0.1*power_range-0.05)
            self.register_widegets_liedaktualisieren(name=f"liedanzeiger{power_range}",liednummer=self.eingabe_lied, versnummer=self.eingabe_vers, liedanzeige=self.text_lied_lable, buchauswahl=self.clicked_buch)
        elif aktion[1] == " Kamera":
            lied_weiter = ttk.Button(self.Textmanager, text= "servus", style='TButton')
            inhalt.append(lied_weiter)
            befehle = ["Kamera", "Textwort", "Lied"]
            clicked = StringVar()
            clicked.set(befehle[0])
            inhalt.append(clicked)
            opt = ttk.OptionMenu(self.Textmanager, clicked, *befehle)
            opt.config(style='custom.TMenubutton')
            inhalt.append(opt)
        return inhalt



    def liedanzeige_aktualisieren(self, event):
        self.widgets_to_remove = []
        for self.name, self.info in self.widget_info_liedauswahl.items():
                self.liednummer = self.info["liednummer"]
                self.versnummer = self.info["versnummer"]
                self.liedanzeige = self.info["liedanzeige"]
                self.buchauswahl = self.info["buchauswahl"]
                print(self.liednummer)
                print(self.liednummer.get())
                song = self.db_connection_info_get("SELECT song_name FROM songs WHERE song_number = ? AND book_name = ?", (self.liednummer.get(),self.buchauswahl.get()))
                self.vers_info = self.versnummer.get()
                if not self.vers_info:
                    text_einfügen = ""
                elif len(self.vers_info) == 1:
                    text_einfügen = f"Vers {self.vers_info}"
                elif len(self.vers_info) > 1:
                    text_einfügen = f"Verse {self.vers_info}"
                if song:
                    Text_speicher = f"{self.buchauswahl.get()} {self.liednummer.get()} {text_einfügen}\n{song}"
                    self.liedanzeige.config(text=Text_speicher)
                else:
                    self.liedanzeige.config(text = "Bitte geben sie eine Nummer ein\n")


        # Entferne die fehlerhaften Widgets aus widget_info
        for self.name in self.widgets_to_remove:
            del self.widget_info_liedauswahl[self.name]
            print(f"Widget {self.name} aus widget_info entfernt")

    def update_widget_positions(self):
        """Aktualisiert die Positionen und Größen aller Widgets basierend auf dem Skalierungsfaktor"""
        self.factor = int(self.db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",)))/100
        self.widgets_to_remove = []
        for self.name, self.info in self.widget_info.items():
            try:
                self.widget = self.info["widget"]
                self.relheight = self.info["relheight"] * self.factor
                self.relwidth = self.info["relwidth"] * self.factor
                self.relx = self.info["relx"] * self.factor
                self.rely = self.info["rely"] * self.factor
                self.widget.place(relwidth=self.relwidth, relheight=self.relheight, relx=self.relx, rely=self.rely)
            except:
                self.widgets_to_remove.append(self.name)

        # Entferne die fehlerhaften Widgets aus widget_info
        for self.name in self.widgets_to_remove:
            del self.widget_info[self.name]
            print(f"Widget {self.name} aus widget_info entfernt")






















Speicherort = os.path.dirname(os.path.abspath(__file__))

def Einstellung_laden(Einstellugen_name):
    verses = get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", (Einstellugen_name,), True)
    input_lieder = (str(verses[0]).split("!"))
    return input_lieder



def get_db_connection(input_db, input_db_variabel, get_output = True):
    db_filename = "Lieder_Datenbank.db"
    db_path = os.path.join(os.path.dirname(__file__), db_filename)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(input_db, input_db_variabel)
    Ausgabe = cursor.fetchall()
    conn.close()
    return Ausgabe[0]



def andere_info_db_conection():    
    db_filename = "Lieder_Datenbank.db"
    db_path = os.path.join(os.path.dirname(__file__), db_filename)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    Ausgabe = cursor.fetchall()
    zeichen_zum_entfernen = "'()"
    cleaned_verses = []
    conn.commit()
    conn.close()
    for element in Ausgabe:
        if not isinstance(element[0], int):
            cleaned_verses.append(element[0].translate({ord(zeichen): None for zeichen in zeichen_zum_entfernen}))
        else:
            cleaned_verses.append(element[0])
    if cleaned_verses == ['True']:
        cleaned_verses = True
    elif cleaned_verses == ['False']:
        cleaned_verses = False
    return cleaned_verses


def Start():
    global Textmanager
    hintergrund_farbe = get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
    Settings.Check_settings(Tkfont=False)
    Textmanager = Tk()
    Textmanager.title("Textmanager")
    Textmanager.config(bg=hintergrund_farbe)
    Textmanager.geometry("1040x800")
    Menu_generator()
    Load_settings.Load_Text_anzeiger()
    start_anzeige_bildschirm()


def start_anzeige_bildschirm():
    global alle_inhalt
    alle_inhalt = []
    for i in Einstellung_laden("Ablauf"):
        alle_inhalt.append(gegerator_lieder(i))
    eingabe_änderung("hallo")
    alle_inhalt.append(button_generator())
    Textmanager.bind("<Configure>", on_resize)


def on_resize(event):
    posistion()
    Load_settings.Textmanager_größen()


def Menu_generator():
    global menu_info_main
    Load_settings.Textmanager_größen()
    hintergrund_farbe = get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
    text_farbe = get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
    menu_info_main = ttk.Menubutton(Textmanager, text='Info', style='custom.TMenubutton')
    menu_info = Menu(menu_info_main, bg=hintergrund_farbe, fg= text_farbe, border=0, borderwidth=0, tearoff=False, )
    menu_kamera_main = ttk.Menubutton(Textmanager, text = "Kamera", style='custom.TMenubutton')
    menu_kamera = Menu(menu_kamera_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
    menu_liedkontrolle_main = ttk.Menubutton(Textmanager, text = "Liedkontrolle", style='custom.TMenubutton')
    menu_liedkontrolle = Menu(menu_liedkontrolle_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
    menu_help_main = ttk.Menubutton(Textmanager, text = "Hilfe", style='custom.TMenubutton')
    menu_help = Menu(menu_help_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
    menu_info.add_radiobutton(label="Einstellungen", command=Settings.make_settings)
    menu_info.add_radiobutton(label= "Info", command=Settings.Info)
    menu_kamera.add_command(label="Einstellungen", command=Kamera.Settings)
    menu_kamera.add_command(label="Position", command=Kamera.Position)
    menu_liedkontrolle.add_command(label="Einstellungen")
    menu_liedkontrolle.add_command(label="Lied Kontrolieren", command=datenverarbeiten.setup_ui)
    menu_help.add_command(label="Hilfe")
    menu_info_main['menu'] = menu_info
    menu_kamera_main['menu'] = menu_kamera
    menu_help_main["menu"] = menu_help
    menu_liedkontrolle_main["menu"] = menu_liedkontrolle
    menu_info_main.pack(side=LEFT, anchor=NW)
    menu_kamera_main.pack(side=LEFT, anchor=NW)
    menu_liedkontrolle_main.pack(side=LEFT, anchor=NW)
    menu_help_main.pack(side=LEFT, anchor=NW)


def Load_Setting():
    Settings.Check_settings()
    Load_settings.Load_Text_anzeiger()
    Load_settings.Load_all_collor()


def button_generator():
    rueckgabe = []
    rueckgabe.append("Button")
    Bestätigen = ttk.Button(Textmanager, text="Bestätigen", command=bestätigen, style='TButton')
    rueckgabe.append(Bestätigen)
    Wiederherstellen = ttk.Button(Textmanager, text="Wiederherstellen", style='TButton')
    rueckgabe.append(Wiederherstellen)
    Löschen = ttk.Button(Textmanager, text="Löschen", command=delete, style='TButton')
    rueckgabe.append(Löschen)
    Präsentation = ttk.Button(Textmanager, text="Präsentation", command=ablauf.Präsentation_starten, style='TButton')
    rueckgabe.append(Präsentation)
    return rueckgabe


def gegerator_lieder(input):
    ja = input.split(",")
    name_lied = ja[0].split(":")
    aktion = ja[1].split(":")
    inhalt = []
    inhalt.append([aktion[1], name_lied[1]])
    Lied_start = ttk.Label(Textmanager, text=name_lied[1], style='TLabel')
    inhalt.append(Lied_start)
    if aktion[1] == " Textwort":
        Button_Textwrt = ttk.Button(Textmanager, text="Textwort", style='TButton')
        inhalt.append(Button_Textwrt)
    elif aktion[1] == " Lied":
        Lable_Kamera = ttk.Button(Textmanager, text="Kamera", style='TButton')
        inhalt.append(Lable_Kamera)
        befehle = ["Kamera", "Textwort", "Lied"]
        clicked = StringVar()
        clicked.set(befehle[0])
        opt = ttk.OptionMenu(Textmanager, clicked, *befehle, style='custom.TMenubutton')
        inhalt.append(clicked)
        inhalt.append(opt)
        eingabe_Lied = ttk.Entry(Textmanager, style='TEntry')
        eingabe_Lied.bind("<KeyRelease>", eingabe_änderung)
        inhalt.append(eingabe_Lied)
        eingabe_Vers = ttk.Entry(Textmanager, style='TEntry')
        eingabe_Vers.bind("<KeyRelease>", eingabe_änderung)
        inhalt.append(eingabe_Vers)
        befehle_buch = ["Gesangbuch", "Chorbuch", "Jugendliederbuch"]
        clicked_buch = StringVar()
        clicked_buch.set(befehle_buch[0])
        opt_buch = ttk.OptionMenu(Textmanager, clicked_buch, *befehle_buch, command=eingabe_änderung)
        inhalt.append(clicked_buch)
        inhalt.append(opt_buch)
        Tex_lied_lable = ttk.Label(Textmanager)
        inhalt.append(Tex_lied_lable)
    elif aktion[1] == " Kamera":
        lied_weiter = ttk.Button(Textmanager, text= "servus", style='TButton')
        inhalt.append(lied_weiter)
        befehle = ["Kamera", "Textwort", "Lied"]
        clicked = StringVar()
        clicked.set(befehle[0])
        inhalt.append(clicked)
        opt = ttk.OptionMenu(Textmanager, clicked, *befehle)
        opt.config(style='custom.TMenubutton')
        inhalt.append(opt)
    return inhalt



def delete():
    for i in alle_inhalt:
        if i[0][0] == " Lied":
            i[5].delete(0, "end")
            i[6].delete(0, "end")
    eingabe_änderung("")


def clear_window():
    global alle_inhalt
    Textmanager.unbind("<Configure>")
    for i in alle_inhalt:
        for i in i:
            if isinstance(i, Widget):
                i.destroy()
    del alle_inhalt


def bestätigen():
    data = []
    for i in alle_inhalt:
        if i[0][0] == " Lied":
            data.append(f"{i[0][0]};{i[0][1]};{i[3].get()};{i[5].get()};{i[6].get()};{i[7].get()}")
        elif i[0][0] == " Kamera":
            data.append(f"{i[0][0]};{i[0][1]};{i[3].get()};0;1;0")
        elif i[0][0] == " Textwort":
            data.append(f"{i[0][0]};{i[0][1]};0;0;1;0")
    data_ready = "!".join(data,)
    get_db_connection("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", (data_ready, "speichern"), False)

def eingabe_änderung(event):
    for i in alle_inhalt:
        if i[0][0] == " Lied":
            song = get_db_connection("SELECT song_name FROM songs WHERE song_number = ? AND book_name = ?", (i[5].get(),i[7].get()))
            Vers_info = i[6].get()
            if not Vers_info:
                text_einfügen = ""
            elif len(Vers_info) == 1:
                text_einfügen = f"Vers {Vers_info}"
            elif len(Vers_info) > 1:
                text_einfügen = f"Verse {Vers_info}"
            if song:
                Text_speicher = f"{i[7].get()} {i[5].get()} {text_einfügen}\n{song[0]}"
                i[9].config(text= Text_speicher)
            else:
                i[9].config(text = "Bitte geben sie eine Nummer ein\n")
        elif i[0][0] == " Kamera":
            pass



def posistion():
    for pos, i in enumerate (alle_inhalt):
        factor = int(get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",))[0])/100
        if i[0][0] == " Textwort":
            i[1].place(x= 0, y= menu_info_main.winfo_height()+1+pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].place(x= (i[1].winfo_width()+1), y= menu_info_main.winfo_height()+1+pos*i[1].winfo_height()*2+pos*2,relwidth=0.3*factor, relheight=0.1*factor)
        elif i[0][0] == " Lied":
            i[1].place(x= 0, y= menu_info_main.winfo_height()+1+pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].place(x= 0, y= menu_info_main.winfo_height()+1+pos*(i[1].winfo_height()+1)*2+i[1].winfo_height()+1,relwidth=0.15*factor, relheight=0.05*factor)
            i[4].place(x= (i[1].winfo_width()+1), y= menu_info_main.winfo_height()+1+pos*i[1].winfo_height()*2+pos*2,relwidth=0.1*factor, relheight=0.05*factor)
            i[5].place(x= (i[1].winfo_width()+2+i[4].winfo_width()), y= menu_info_main.winfo_height()+1+pos*i[1].winfo_height()*2+pos*2-1,relwidth=0.1*factor, relheight=0.05*factor)
            i[6].place(x= (i[1].winfo_width()+2+i[4].winfo_width()), y= menu_info_main.winfo_height()+1+pos*(i[1].winfo_height()+1)*2+i[1].winfo_height(),relwidth=0.1*factor, relheight=0.05*factor)
            i[8].place(x= i[1].winfo_width()+2+i[4].winfo_width()+2+i[5].winfo_width(), y= menu_info_main.winfo_height()+1+pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[9].place(x= i[1].winfo_width()+2+i[4].winfo_width()+2+i[5].winfo_width()+2+i[8].winfo_width(), y= menu_info_main.winfo_height()+1+pos*(i[1].winfo_height()+1)*2,relwidth=0.3*factor, relheight=0.1*factor)
        elif i[0][0] == " Kamera":
            i[1].place(x= 0, y= menu_info_main.winfo_height()+1+pos*i[1].winfo_height()*2+pos*2,relwidth=0.15*factor, relheight=0.05*factor)
            i[2].place(x= 0, y= menu_info_main.winfo_height()+1+pos*(i[1].winfo_height()+1)*2+i[1].winfo_height()+1,relwidth=0.15*factor, relheight=0.05*factor)
            i[4].place(x= (i[1].winfo_width()+1), y= menu_info_main.winfo_height()+1+pos*i[1].winfo_height()*2+pos*2,relwidth=0.1*factor, relheight=0.05*factor)
        elif i[0] == "Button":
            fenster_width= Textmanager.winfo_width()
            i[1].place(x=fenster_width-i[1].winfo_width()-15, y=menu_info_main.winfo_height()+1+10, relwidth=0.12*factor, relheight=0.07*factor)
            i[2].place(x=fenster_width-i[2].winfo_width()-15, y=menu_info_main.winfo_height()+1+i[1].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)
            i[3].place(x=fenster_width-i[1].winfo_width()-15, y=menu_info_main.winfo_height()+1+i[1].winfo_height()+i[2].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)
            i[4].place(x=fenster_width-i[1].winfo_width()-15, y=menu_info_main.winfo_height()+1+i[1].winfo_height()+i[2].winfo_height()+i[3].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)

