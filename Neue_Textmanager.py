from tkinter import *
import tkinter.ttk as ttk
import os
import sqlite3
import json

import ablauf
import Settings
import Kamera
import datenverarbeiten
import Load_settings


def get_db_connection():
    db_filename = "Lieder_Datenbank.db"
    db_path = os.path.join(os.path.dirname(__file__), db_filename)
    conn = sqlite3.connect(db_path)
    return conn

def db_connection_info_write(input_db, input_db_variabel):
    conn = get_db_connection()
    cursor = conn.cursor()
    if len(input_db_variabel) > 2:
        cursor.execute(input_db, input_db_variabel)
    else:
        cursor.execute(input_db)
    conn.commit()
    conn.close()


def db_connection_info_get( input_db, input_db_variabel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(input_db, input_db_variabel)
    Ausgabe = cursor.fetchall()
    conn.close()
    if Ausgabe: return Ausgabe[0][0]


def fetch_all_program_info(input_db, input):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(f'SELECT * FROM {input_db} ORDER BY {input}')
    all_entries = c.fetchall()
    conn.close()
    return all_entries



class TextmanagerAPP(Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hintergrund_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("textanzeiger_hintergrund",))
        self.geometry("1040x800")
        self.config(bg=self.hintergrund_farbe)
        self.widget_info = {}
        self.widget_info_liedauswahl = {}
        self.Menu_generator()
        self.start_programm_laden()
        self.bind("<Configure>", self.one_resize)
        self.update_widget_positions()
        self.mainloop()

    def start_programm_laden(self):
        self.widget_delite()
        entries = fetch_all_program_info("Ablaufaufbau", "Reihenfolge")
        for entry in entries:
            self.gegerator_lieder(entry[0]+1,entry[2], entry[1])
        self.button_generator()

    def one_resize(self,event):
        Load_settings.Textmanager_größen(self, self.get_window_size())


    def get_window_size(self):
        return self.winfo_width(), self.winfo_height()

    def festgröße_bestimmen(self):
        Load_settings.Textmanager_größen(self.get_window_size())

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
                             name: str = None,
                             name_datenbank: str = None,
                             liednummer: Widget = None,
                             versnummer: Widget = None,
                             liedanzeige: Widget = None,
                             buchauswahl: Widget = None,
                             befehl: str = None,
                             pos: int = 0):
        """Regestiert die Liedauwahl und lasst das richtige lied erscheinen"""
        self.widget_info_liedauswahl[name] = {
            "name_datenbank": name_datenbank,
            "liednummer": liednummer,
            "versnummer": versnummer,
            "liedanzeige": liedanzeige,
            "buchauswahl": buchauswahl,
            "befehl": befehl,
            "pos": pos
        }




        
    

    def Menu_generator(self):
        hintergrund_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        text_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
        self.menu_info_main = ttk.Menubutton(self, text='Info', style='custom.TMenubutton')
        menu_info = Menu(self.menu_info_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_kamera_main = ttk.Menubutton(self, text="Kamera", style='custom.TMenubutton')
        menu_kamera = Menu(self.menu_kamera_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_liedkontrolle_main = ttk.Menubutton(self, text="Liedkontrolle", style='custom.TMenubutton')
        menu_liedkontrolle = Menu(self.menu_liedkontrolle_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_help_main = ttk.Menubutton(self, text="Hilfe", style='custom.TMenubutton')
        menu_help = Menu(self.menu_help_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        menu_info.add_radiobutton(label="Einstellungen", command=self.settings_window)
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
    
    def settings_window(self):
        Settingswindow = Settings.Settings_window(self)

    def gegerator_lieder(self, position, name_lied, aktion):
        self.Lied_start = ttk.Label(self, text=name_lied, style='TLabel')
        self.register_widget(f"Lied_start{position}", self.Lied_start, relheight=0.05, relwidth=0.15, rely=0.1*position-0.05, relx=0.0)
        if aktion == " Textwort":
            self.Button_Textwort = ttk.Button(self, text="Textwort", style='TButton')
            self.register_widget(f"Button_textwort{position}", self.Button_Textwort, relheight=0.1, relwidth=0.15, rely=0.1*position-0.05, relx=0.15)
            self.register_widegets_liedaktualisieren(name=f"Textwort{position}", name_datenbank=name_lied, befehl=aktion, pos=position-1)
        elif aktion == " Lied":
            self.Button_Kamera = ttk.Button(self, text="Kamera", style='TButton')
            self.register_widget(f"Button_Kamera{position}", self.Button_Kamera, relheight=0.05, relwidth=0.15, rely=0.1*position, relx=0)
            #befehle_kamera = ["Kamera", "Textwort", "Lied"]
            #clicked_kamera = StringVar()
            #clicked_kamera.set(befehle_kamera[0])
            #opt_kamera = ttk.OptionMenu(self, clicked_kamera, *befehle_kamera, style='custom.TMenubutton')
            #self.register_widget(f"clicked_kamera{position}",opt_kamera, relheight=0.05, relwidth=0.1, rely=0.1*position, relx=0.3)
            #inhalt.append(clicked_kamera)
            #inhalt.append(opt_kamera)
            self.eingabe_lied = ttk.Entry(self, style='TEntry')
            self.eingabe_lied.bind("<KeyRelease>", self.liedanzeige_aktualisieren)
            self.register_widget(name=f"eingabe_lieder{position}",widget=self.eingabe_lied, relheight=0.05, relwidth=0.05, relx=0.35, rely=0.1*position-0.05)
            self.eingabe_vers = ttk.Entry(self, style='TEntry')
            self.eingabe_vers.bind("<KeyRelease>", self.liedanzeige_aktualisieren)
            self.register_widget(name=f"eingabe_verse{position}", widget=self.eingabe_vers, relheight=0.05, relwidth=0.05, relx=0.35, rely=0.1*position)
            self.befehle_buch = ["Gesangbuch", "Chorbuch", "Jugendliederbuch"]
            self.clicked_buch = StringVar()
            self.clicked_buch.set(self.befehle_buch[0])
            self.opt_buch = ttk.OptionMenu(self, self.clicked_buch, *self.befehle_buch, command=self.liedanzeige_aktualisieren)
            self.register_widget(name=f"opt_buch{position}", widget=self.opt_buch, relheight=0.05, relwidth=0.2, relx=0.15, rely=0.1*position-0.05)
            self.text_lied_lable = ttk.Label(self)
            self.register_widget(name=f"text_lied_lable{position}", widget=self.text_lied_lable, relheight=0.1, relwidth=0.3, relx=0.405, rely=0.1*position-0.05)
            self.register_widegets_liedaktualisieren(name=f"liedanzeiger{position}",name_datenbank = name_lied,liednummer=self.eingabe_lied, versnummer=self.eingabe_vers, befehl=aktion, pos=position-1, liedanzeige=self.text_lied_lable, buchauswahl=self.clicked_buch)
        elif aktion == " Kamera":
            self.Button_Kamera = ttk.Button(self, text="Kamera", style='TButton')
            self.register_widget(f"Button_Kamera{position}", self.Button_Kamera, relheight=0.05, relwidth=0.15, rely=0.1*position, relx=0)
            self.register_widegets_liedaktualisieren(name=f"Kamera{position}", name_datenbank=name_lied, befehl=aktion, pos=position-1)    
            #lied_weiter = ttk.Button(self, text= "servus", style='TButton')
            #inhalt.append(lied_weiter)
            #befehle = ["Kamera", "Textwort", "Lied"]
            #clicked = StringVar()
            #clicked.set(befehle[0])
            #inhalt.append(clicked)
            #opt = ttk.OptionMenu(self, clicked, *befehle)
            #opt.config(style='custom.TMenubutton')
            #inhalt.append(opt)

    def button_generator(self):
        bestaetigen = ttk.Button(self, text="Bestätigen", command=bestätigen, style='TButton')
        self.register_widget("rueckgabe_button", widget=bestaetigen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0)
        wiederherstellen = ttk.Button(self, text="Wiederherstellen", style='TButton')
        self.register_widget("widerherstell_button", widget=wiederherstellen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.1)
        loeschen = ttk.Button(self, text="Löschen", command=self.Ablaufsteuerung, style='TButton')
        self.register_widget("löeschen_button", widget=loeschen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.2)
        preasentation = ttk.Button(self, text="Präsentation", command=ablauf.Präsentation_starten, style='TButton')
        self.register_widget("presentation_button", widget=preasentation, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.3)



    def liedanzeige_aktualisieren(self, event):
        self.widgets_to_remove = []
        db_connection_info_write('DELETE FROM Ablaufverwaltung', ())
        for self.name, self.info in self.widget_info_liedauswahl.items():
                self.name_datenbank = self.info["name_datenbank"]
                self.liednummer = self.info["liednummer"]
                self.versnummer = self.info["versnummer"]
                self.liedanzeige = self.info["liedanzeige"]
                self.buchauswahl = self.info["buchauswahl"]
                self.befehl = self.info["befehl"]
                self.position = self.info["pos"]
                if self.liednummer and self.buchauswahl:
                    song = db_connection_info_get("SELECT song_name FROM songs WHERE song_number = ? AND book_name = ?", (self.liednummer.get(),self.buchauswahl.get()))

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
                    informationen_json = json.dumps([self.buchauswahl.get(), self.liednummer.get(), self.versnummer.get()])
                else:
                    informationen_json = None
                db_connection_info_write(
                'INSERT INTO Ablaufverwaltung (Position, Comand, Informationen, Name) VALUES (?, ?, ?, ?)', 
                (self.position, self.befehl, informationen_json, self.name_datenbank)
                )


        # Entferne die fehlerhaften Widgets aus widget_info
        for self.name in self.widgets_to_remove:
            del self.widget_info_liedauswahl[self.name]
            print(f"Widget {self.name} aus widget_info entfernt")

    def update_widget_positions(self):
        """Aktualisiert die Positionen und Größen aller Widgets basierend auf dem Skalierungsfaktor"""
        self.factor = int(db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",)))/100
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


    def widget_delite(self):
        try:
            # Erstelle eine Liste der Schlüssel, um Änderungen an widget_info während der Iteration zu vermeiden
            widget_keys = list(self.widget_info.keys())
            for name in widget_keys:
                widget = self.widget_info[name]["widget"]
                widget.destroy()
                del self.widget_info[name]
            widget_keys = list(self.widget_info_liedauswahl.keys())
            for name in widget_keys:
                del self.widget_info[name]
        except Exception as e:
            print(f"Fehler beim Löschen der Widgets: {e}")



    def Ablaufsteuerung(self):
        self.widget_delite()
        entries = fetch_all_program_info("Ablaufverwaltung", "Position")
        print(entries)
        for entry in entries:
            print(f"ID: {entry[0]}, Befehl: {entry[1]}, Name: {entry[2]}")        
            self.gegerator_lieder_ablauf(entry[0]+1,entry[3], entry[1], informationen=entry[2])
        self.button_generator()
        self.update_widget_positions()
        
    def gegerator_lieder_ablauf(self, position, name_lied, aktion, informationen):
        print(position)
        self.Lied_start = ttk.Label(self, text=name_lied, style='TLabel')
        self.register_widget(name=f"Liedstart{position}", widget=self.Lied_start, relheight=0.05, relwidth=0.3, relx=0, rely=0.1*position-0.05)
        if aktion == " Textwort":
            pass
        elif aktion == " Lied":
            self.lable_Kamera = ttk.Button(self, text="Kamera", style='TButton')
            self.register_widget(name=f"lablekamera{position}", widget=self.lable_Kamera, relheight=0.05, relwidth=0.15, relx=0.15, rely=0.1*position-0.05)
            self.text_lied_lable = ttk.Label(self, style='TLabel', text="Lied")
            self.register_widget(name=f"text_lied_lable{position}", widget=self.text_lied_lable, relheight=0.05, relwidth=0.15, relx=0.405, rely=0.1*position-0.05)
        elif aktion == " Kamera":
            self.lied_weiter = ttk.Button(self, text= "servus", style='TButton')
            self.register_widget(name=f"text_lied_lable{position}", widget=self.lied_weiter, relheight=0.05, relwidth=0.15, relx=0.205, rely=0.1*position-0.05)















def delete():
    for i in alle_inhalt:
        if i[0][0] == " Lied":
            i[5].delete(0, "end")
            i[6].delete(0, "end")
    eingabe_änderung("")




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


