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


widget_info = {}


def get_db_connection():
    db_filename = "Lieder_Datenbank.db"
    db_path = os.path.join(os.path.dirname(__file__), db_filename)
    conn = sqlite3.connect(db_path)
    return conn

def db_connection_info_write(input_db, input_db_variabel):
    conn = get_db_connection()
    cursor = conn.cursor()
    if len(input_db_variabel) > 1:
        cursor.execute(input_db, input_db_variabel)
    else:
        cursor.execute(input_db)
    conn.commit()
    conn.close()


def db_connection_info_get( input_db, input_db_variabel, singel_or_multi = FALSE):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(input_db, input_db_variabel)
    Ausgabe = cursor.fetchall()
    conn.close()
    if Ausgabe: 
        if singel_or_multi:
            return Ausgabe
        else:
            return Ausgabe[0][0]


def fetch_all_program_info(input_db, input, auswahl= "*"):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(f'SELECT {auswahl} FROM {input_db} ORDER BY {input}')
    all_entries = c.fetchall()
    conn.close()
    return all_entries


def register_widget(
        name: str, 
        widget: Widget = None, 
        relheight: int = 0.1, 
        relwidth : int = 0.11,
        relx: int = None, 
        rely: int = None):
    """Registriert ein Widget und speichert seine Informationen
    Hier werden die Info für die Widget übergeben damit sie an einer zentrallen stelle placiert werden und deren größe angepasst wird."""
    widget_info[name] = {
        "widget": widget,
        "relheight": relheight,
        "relwidth": relwidth,
        "relx": relx,
        "rely": rely
    }

def update_widget_positions():
    """Aktualisiert die Positionen und Größen aller Widgets basierend auf dem Skalierungsfaktor"""
    factor = int(db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",)))/100
    widgets_to_remove = []
    
    for name, info in widget_info.items():
        try:
            widget = info["widget"]
            relheight = info["relheight"] * factor
            relwidth = info["relwidth"] * factor
            relx = info["relx"] * factor
            rely = info["rely"]
            widget.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)
        except Exception as e:
            widgets_to_remove.append(name)
            print(f"Error updating widget {name}: {e}")
    
    # Entferne die fehlerhaften Widgets aus widget_info
    for name in widgets_to_remove:
        del widget_info[name]


class TextmanagerAPP(Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hintergrund_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("textanzeiger_hintergrund",))
        self.geometry("1040x800")
        self.config(bg=self.hintergrund_farbe)
        self.widget_info_liedauswahl = {}
        self.position_anzahl = 0

        # Erstellen des Canvas-Objekts
        self.canvas = Canvas(self, bg=self.hintergrund_farbe)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Hinzufügen der vertikalen Scrollbar
        self.v_scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")

        # Hinzufügen der horizontalen Scrollbar

        # Verknüpfen der Scrollbars mit dem Canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Erstellen eines Frames im Canvas
        self.frame = Frame(self.canvas, bg="red")
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Konfigurieren des Canvas, um seine Größe anzupassen
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)



        # Frame-Konfiguration
        self.Menu_generator()
        self.start_programm_laden()
        self.bind("<Configure>", self.one_resize)
        update_widget_positions()
        self.mainloop()


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def start_programm_laden(self):
        self.unbind("<Left>")
        self.unbind("<Right>")
        self.unbind("<Up>")
        self.unbind("<Down>")
        self.widget_delite()
        entries = fetch_all_program_info("Ablaufaufbau", "Reihenfolge")
        all_sum = 0
        for position_amzahl, entry in enumerate(entries):
            all_sum += 1
        for position_amzahl, entry in enumerate(entries):
            self.position_anzahl = position_amzahl
            self.gegerator_lieder(entry[0]+1,entry[2], entry[1], all_sum)
        self.button_generator()
        update_widget_positions()



    def one_resize(self,event):
        Load_settings.Textmanager_größen(self, self.get_window_size())
        factor = int(db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",)))/100
        self.canvas.itemconfig(self.frame_id, height= 120*self.position_anzahl*factor, width= self.get_window_size()[0]-20)



    def get_window_size(self):
        return self.winfo_width(), self.winfo_height()

    def festgröße_bestimmen(self):
        Load_settings.Textmanager_größen(self.get_window_size())



    def register_widegets_liedaktualisieren(self,
                             name: str = None,
                             name_datenbank: str = None,
                             liednummer: Widget = None,
                             versnummer: Widget = None,
                             widget: Widget = None,
                             buchauswahl: Widget = None,
                             befehl: str = None,
                             pos: int = 0):
        """Regestiert die Liedauwahl und lasst das richtige lied erscheinen"""
        self.widget_info_liedauswahl[name] = {
            "name_datenbank": name_datenbank,
            "liednummer": liednummer,
            "versnummer": versnummer,
            "widget": widget,
            "buchauswahl": buchauswahl,
            "befehl": befehl,
            "pos": pos
        }


    def register_widegets_liedaktualisieren_ablauf(self,
                             name: str = None,
                             liednummer: int = None,
                             versnummer: int = None,
                             liedanzeige: Widget = None,
                             buchauswahl: str = None,
                             befehl: str = None,
                             pos: int = 0):
        """Regestiert die Liedauwahl und lasst das richtige lied erscheinen"""
        self.widget_info_liedauswahl_aublauf[name] = {
            "liednummer": liednummer,
            "versnummer": versnummer,
            "liedanzeige": liedanzeige,
            "buchauswahl": buchauswahl,
            "befehl": befehl,
            "pos": pos
        }


    def register_vers_widegt(self,
                             name: str = None,
                             widget: Widget = None,
                             pos: int = 0):
        """Regestiert die Liedauwahl und lasst das richtige lied erscheinen"""
        self.verse_widgets[name] = {
            "widget": widget,
            "pos": pos
        }
    

    def Menu_generator(self):
        hintergrund_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        text_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))
        self.menu_info_main = ttk.Menubutton(self.frame, text='Info', style='custom.TMenubutton')
        menu_info = Menu(self.menu_info_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_kamera_main = ttk.Menubutton(self.frame, text="Kamera", style='custom.TMenubutton')
        menu_kamera = Menu(self.menu_kamera_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_liedkontrolle_main = ttk.Menubutton(self.frame, text="Liedkontrolle", style='custom.TMenubutton')
        menu_liedkontrolle = Menu(self.menu_liedkontrolle_main, bg=hintergrund_farbe, fg=text_farbe, border=0, borderwidth=0, tearoff=False)
        self.menu_help_main = ttk.Menubutton(self.frame, text="Hilfe", style='custom.TMenubutton')
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
        Settings.Settings_window(self)

    def gegerator_lieder(self, widget_position, name_lied, aktion, total_widgets):
        self.Lied_start = ttk.Label(self.frame, text=name_lied, style='TLabel')
        rely = (widget_position - 1) / total_widgets
        register_widget(f"Lied_start{widget_position}", self.Lied_start, relheight=0.05, relwidth=0.15, rely=rely-0.05, relx=0.0)
        if aktion == "Textwort":
            self.Button_Textwort = ttk.Button(self.frame, text="Textwort", style='TButton')
            register_widget(f"Button_textwort{widget_position}", self.Button_Textwort, relheight=0.1, relwidth=0.15, rely=rely-0.05, relx=0.15)
            self.register_widegets_liedaktualisieren(name=f"Textwort{widget_position}", name_datenbank=name_lied, befehl=aktion, pos=widget_position-1)
        elif aktion == "Lied":
            self.Button_Kamera = ttk.Button(self.frame, text="Kamera", style='TButton')
            register_widget(f"Button_Kamera{widget_position}", self.Button_Kamera, relheight=0.05, relwidth=0.15, rely=rely, relx=0)
            #befehle_kamera = ["Kamera", "Textwort", "Lied"]
            #clicked_kamera = StringVar()
            #clicked_kamera.set(befehle_kamera[0])
            #opt_kamera = ttk.OptionMenu(self, clicked_kamera, *befehle_kamera, style='custom.TMenubutton')
            #register_widget(f"clicked_kamera{widget_position}",opt_kamera, relheight=0.05, relwidth=0.1, rely=rely, relx=0.3)
            #inhalt.append(clicked_kamera)
            #inhalt.append(opt_kamera)
            self.eingabe_lied = ttk.Entry(self.frame, style='TEntry')
            self.eingabe_lied.bind("<KeyRelease>", self.liedanzeige_aktualisieren)
            register_widget(name=f"eingabe_lieder{widget_position}",widget=self.eingabe_lied, relheight=0.05, relwidth=0.05, relx=0.35, rely=rely-0.05)
            self.eingabe_vers = ttk.Entry(self.frame, style='TEntry')
            self.eingabe_vers.bind("<KeyRelease>", self.liedanzeige_aktualisieren)
            register_widget(name=f"eingabe_verse{widget_position}", widget=self.eingabe_vers, relheight=0.05, relwidth=0.05, relx=0.35, rely=rely)
            self.befehle_buch = ["Gesangbuch", "Chorbuch", "Jugendliederbuch"]
            self.clicked_buch = StringVar()
            self.clicked_buch.set(self.befehle_buch[0])
            self.opt_buch = ttk.OptionMenu(self.frame, self.clicked_buch, *self.befehle_buch, command=self.liedanzeige_aktualisieren)
            register_widget(name=f"opt_buch{widget_position}", widget=self.opt_buch, relheight=0.05, relwidth=0.2, relx=0.15, rely=rely-0.05)
            self.text_lied_lable = ttk.Label(self.frame)
            register_widget(name=f"text_lied_lable{widget_position}", widget=self.text_lied_lable, relheight=0.1, relwidth=0.3, relx=0.405, rely=rely-0.05)
            self.register_widegets_liedaktualisieren(name=f"liedanzeiger{widget_position}",name_datenbank = name_lied,liednummer=self.eingabe_lied, versnummer=self.eingabe_vers, befehl=aktion, pos=widget_position-1, widget=self.text_lied_lable, buchauswahl=self.clicked_buch)
        elif aktion == "Kamera":
            self.Button_Kamera = ttk.Button(self.frame, text="Kamera", style='TButton')
            register_widget(f"Button_Kamera{widget_position}", self.Button_Kamera, relheight=0.05, relwidth=0.15, rely=rely, relx=0)
            self.register_widegets_liedaktualisieren(name=f"Kamera{widget_position}", name_datenbank=name_lied, befehl=aktion, pos=widget_position-1)    
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
        wiederherstellen = ttk.Button(self.frame, text="Wiederherstellen", style='TButton')
        register_widget("widerherstell_button", widget=wiederherstellen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.1)
        loeschen = ttk.Button(self.frame, text="Löschen", style='TButton')
        register_widget("löeschen_button", widget=loeschen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.2)
        preasentation = ttk.Button(self.frame, text="Präsentation", command=self.Ablaufsteuerung, style='TButton')
        register_widget("presentation_button", widget=preasentation, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.3)




    def liedanzeige_aktualisieren(self, event):
        self.widgets_to_remove = []
        db_connection_info_write('DELETE FROM Ablaufverwaltung', ())
        
        for name, info in self.widget_info_liedauswahl.items():
            name_datenbank = info["name_datenbank"]
            liednummer = info["liednummer"]
            versnummer = info["versnummer"]
            widget = info["widget"]
            buchauswahl = info["buchauswahl"]
            befehl = info["befehl"]
            widget_position = info["pos"]
            
            if liednummer and buchauswahl:
                song = db_connection_info_get(
                    "SELECT song_name FROM songs WHERE song_number = ? AND book_name = ?", 
                    (liednummer.get(), buchauswahl.get())
                )

                vers_info = versnummer.get()
                if not vers_info:
                    text_einfügen = ""
                elif len(vers_info) == 1:
                    text_einfügen = f"Vers {vers_info}"
                else:
                    text_einfügen = f"Verse {vers_info}"
                    
                if song:
                    text_speicher = f"{buchauswahl.get()} {liednummer.get()} {text_einfügen}\n{song}"
                    widget.config(text=text_speicher)
                else:
                    widget.config(text="Bitte geben Sie eine Nummer ein\n")
                
                db_connection_info_write(
                    'INSERT INTO Ablaufverwaltung (Position, Comand, Liednummer, Name, Versnummer, Buch) VALUES (?, ?, ?, ?, ?, ?)', 
                    (widget_position, befehl, liednummer.get(), name_datenbank, vers_info, buchauswahl.get())
                )
            else:
                db_connection_info_write(
                    'INSERT INTO Ablaufverwaltung (Position, Comand, Liednummer, Name, Versnummer, Buch) VALUES (?, ?, ?, ?, ?, ?)', 
                    (widget_position, befehl, "", name_datenbank, 1, "")
                )

        # Entferne die fehlerhaften Widgets aus widget_info
        for name in self.widgets_to_remove:
            del self.widget_info_liedauswahl[name]






    def widget_delite(self):
        # Entferne und zerstöre alle Widgets aus widget_info
        for name, info in widget_info.items():
            widget = info.get("widget")
            if widget:
                widget.destroy()
        widget_info.clear()

        # Entferne und zerstöre alle Widgets aus widget_info_liedauswahl
        for name, info in self.widget_info_liedauswahl.items():
            widget = info.get("widget")
            if widget:
                widget.destroy()
        self.widget_info_liedauswahl.clear()



    def Ablaufsteuerung(self):
        self.widget_delite()
        self.widget_info_liedauswahl_aublauf = {}
        entries = fetch_all_program_info("Ablaufverwaltung", "Position")
        for entry in entries:
            self.gegerator_lieder_ablauf(entry[0],entry[3], entry[1], liednummer=entry[2], versnummer=entry[4], buch=entry[5])
        self.button_ablauf_steuerung()
        update_widget_positions()
        self.vers_postion = 0
        self.lied_position = 0
        self.verse_widgets = {}
        self.bind("<Configure>", self.one_resize)
        self.bind("<Left>", self.trigger_command_with_param)
        self.bind("<Right>", self.trigger_command_with_param)
        self.bind("<Up>", self.trigger_command_with_param)
        self.bind("<Down>", self.trigger_command_with_param)
        self.button_aktivitat = 0
        self.ablauf_sterung(0,0)

    def button_ablauf_steuerung(self):
        """wiederherstellen = ttk.Button(self, text="Wiederherstellen", style='TButton')
        register_widget("widerherstell_button", widget=wiederherstellen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.1)
        loeschen = ttk.Button(self, text="Löschen", style='TButton')
        register_widget("löeschen_button", widget=loeschen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.2)"""
        eingabe = ttk.Button(self.frame, text="Eingabe", command=self.start_programm_laden, style='TButton')
        register_widget("presentation_button", widget=eingabe, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.3)


    def gegerator_lieder_ablauf(self, widget_position, name_lied, aktion, liednummer, versnummer, buch):
        self.frame1 = ttk.Frame(self.frame, style='TLabel')
        register_widget(name=f"frame{widget_position}", widget=self.frame1, relheight=0.1, relwidth=0.7, relx=0, rely=0.1*(widget_position+1)-0.05)
        self.Lied_start = ttk.Button(self.frame1, text=name_lied, style='TButton', command=lambda l= widget_position: self.lied_vers_button_command(l, 0))
        register_widget(name=f"Liedstart{widget_position}", widget=self.Lied_start, relheight=0.5, relwidth=0.2, relx=0, rely=0)
        self.register_widegets_liedaktualisieren_ablauf(name=f"{name_lied}{widget_position}", liednummer=liednummer, versnummer=versnummer, buchauswahl=buch, liedanzeige=self.frame1, befehl=aktion, pos=widget_position)
        if aktion == "Textwort":
            pass
        elif aktion == "Lied":
            self.lable_Kamera = ttk.Button(self.frame1, text="Kamera", style='TButton')
            register_widget(name=f"lablekamera{widget_position}", widget=self.lable_Kamera, relheight=0.5, relwidth=0.15, relx=0.2, rely=0)
            song = db_connection_info_get("SELECT song_name FROM songs WHERE song_number = ? AND book_name = ?", (liednummer, buch))
            if not versnummer:
                text_einfügen = ""
            elif len(str(versnummer)) == 1:
                text_einfügen = f"Vers {versnummer}"
            elif len(versnummer) > 1:
                text_einfügen = f"Verse {versnummer}"
            if song:
                Text_speicher = f"{buch} {liednummer} {text_einfügen}\n{song}"
            else:
                Text_speicher = ""
            self.text_lied_lable = ttk.Label(self.frame1, style='TLabel', text=Text_speicher)
            register_widget(name=f"text_lied_lable{widget_position}", widget=self.text_lied_lable, relheight=0.5, relwidth=0.4, relx=0.405, rely=0)
        elif aktion == "Kamera":
            self.lied_weiter = ttk.Button(self.frame1, text= "servus", style='TButton')
            register_widget(name=f"text_lied_lable{widget_position}", widget=self.lied_weiter, relheight=0.5, relwidth=0.15, relx=0.20, rely=0)


    def clear_verse_widgets(self):
        try:
            """Löscht alle Widgets der Verse"""
            widget_keys = list(self.verse_widgets.keys())
            for name in widget_keys:
                if name in self.verse_widgets:
                    widget = self.verse_widgets[name]["widget"]
                    widget.destroy()
                    del widget_info[name]
            self.verse_widgets.clear()
        except Exception as e:
            print(f"beim widegt {e} konnte nicht ordentlich gelöscht werden")


    def adjust_number(self, number, comparison_list, change):
        
        # Funktion zur Suche der nächsten größeren Zahl in der Liste
        def next_higher(num, lst):
            for index, x in enumerate(lst):
                if x > num:
                    return x, index
            return None, None
        
        # Funktion zur Suche der nächsten kleineren Zahl in der Liste
        def next_lower(num, lst):
            for index, x in reversed(list(enumerate(lst))):
                if x < num:
                    return x, index
            return None, None
        
        if number in comparison_list:
            # Wenn die Zahl in der Liste ist, übernehmen wir sie
            widget_position = comparison_list.index(number)
            return number, widget_position, None
        else:
            # Wenn die Zahl nicht in der Liste ist, bearbeiten wir sie
            if change > 0:
                # Positive Änderungszahl
                next_num, index = next_higher(number, comparison_list)
                if next_num is not None:
                    return next_num, index, None
                else:
                    # Wenn keine nächsthöhere Zahl vorhanden ist
                    return None, None, "up"
            elif change < 0:
                # Negative Änderungszahl
                next_num, index = next_lower(number, comparison_list)
                if next_num is not None:
                    return next_num, index, None
                else:
                    # Wenn keine nächstkleinere Zahl vorhanden ist
                    return None, None, "down"
            else:
                print("Keine Änderung erforderlich.")
                return number, None




    def ablauf_sterung(self, übergabe_postion_lied, übergabe_postion_vers, button_or_normal = False):
        #Logig der Nummern
        if not button_or_normal and not self.button_aktivitat:
            self.vers_postion += übergabe_postion_vers
            self.lied_position += übergabe_postion_lied
            if self.vers_postion < 0 and self.lied_position > 0:
                self.lied_position -= 1
                self.vers_postion = 999
            elif self.vers_postion < 0 and self.lied_position == 0 or self.vers_postion ==0 and self.lied_position < 0:
                self.lied_position = 0
                self.vers_postion = 0
                return
            if self.lied_position < 0:
                self.lied_position = 0
        elif button_or_normal:
            self.lied_position = übergabe_postion_lied
            self.vers_postion = übergabe_postion_vers

        # Letztes lied deakteviert Lied + 1 eingabe 
        if self.lied_position > len(self.widget_info_liedauswahl_aublauf)-2:
            self.unbind("<Down>")
        else:
            self.bind("<Down>", self.trigger_command_with_param)


        self.clear_verse_widgets()
        for self.name, self.info in self.widget_info_liedauswahl_aublauf.items():
            self.liednummer = self.info["liednummer"]
            self.versnummer = self.info["versnummer"]
            widget_liedanzeige = self.info["liedanzeige"]
            self.buchauswahl = self.info["buchauswahl"]
            self.befehl = self.info["befehl"]
            self.position = self.info["pos"]
            if self.lied_position == self.position:
                numbers = []
                if self.versnummer:
                    parts = str(self.versnummer).split(',')  # Teile die Eingabe anhand des Kommas
                    for part in parts:
                        if '-' in part:  # Überprüfe, ob ein Bereich (z.B. 3-6) vorhanden ist
                            start, end = map(int, part.split('-'))  # Teile den Bereich anhand des Bindestrichs
                            numbers.extend(range(start, end + 1))  # Füge die Zahlen im Bereich zur Liste hinzu
                        else:
                            numbers.append(int(part))  # Füge einzelne Zahlen zur Liste hinzu
                else:
                    vers_number = db_connection_info_get("SELECT verse_number FROM verses WHERE song_id = ?", (self.liednummer,),singel_or_multi=True)
                    if vers_number:
                        for vers in vers_number:
                            numbers += vers
                    else:
                        numbers.append(1)
                numbers_all = []
                vers_number = db_connection_info_get("SELECT verse_number FROM verses WHERE song_id = ?", (self.liednummer,),singel_or_multi=True)
                if not button_or_normal:
                    if self.button_aktivitat:
                        ver_ausführen = self.adjust_number(self.vers_postion+übergabe_postion_vers, numbers, übergabe_postion_vers)
                        if not ver_ausführen[2]:
                            self.vers_postion =  ver_ausführen[1]+1
                        elif ver_ausführen[2] == "up":
                            self.vers_postion = 0
                            self.lied_position += 1
                            widget_liedanzeige.config(style='vorbereitung.TFrame')
                            self.command_vorbereitung_lied_vers()
                            self.clear_verse_widgets()
                            self.ablauf_sterung(übergabe_postion_vers=self.vers_postion, übergabe_postion_lied=self.lied_position, button_or_normal=True)
                            return
                        elif ver_ausführen[2] == "down":
                            self.vers_postion = 0
                        widget_liedanzeige.config(style='TButton')
                    self.button_aktivitat = False
                    if self.vers_postion == 999:
                        self.vers_postion = len(numbers)
                    if self.vers_postion > 1000:
                        self.vers_postion = 0
                else:
                    self.button_aktivitat = True
                if vers_number:
                    for vers in vers_number:
                        numbers_all += vers
                if not numbers_all:
                    for number in numbers:
                        numbers_all.append(number)
                for i, verse_num in enumerate(numbers_all):
                    verse_widget = ttk.Button(self.frame, text=f"Vers {verse_num}", style='TButton', command=lambda v=verse_num, l= self.lied_position: self.lied_vers_button_command(l, v))
                    verse_rel_y = 0.1 * (self.position + 1 + i)  # Berechnet die y-Position des Widgets
                    register_widget(name=f"verse_{self.position}_{verse_num}", widget=verse_widget, relheight=0.05, relwidth=0.7, relx=0, rely=verse_rel_y)
                    self.register_vers_widegt(name=f"verse_{self.position}_{verse_num}", widget=verse_widget, pos=i+1)
                    self.update_widget_positions()                

                for name, info in self.widget_info_liedauswahl_aublauf.items():
                    if info["pos"] > self.position:
                        info["liedanzeige"].place_configure(rely=0.1 * (info["pos"] + len(numbers_all)))
                
                #Letzes vers deakteviert tasteneingabe vers + 1
                if self.lied_position > len(self.widget_info_liedauswahl_aublauf)-2 and self.vers_postion > len(numbers):
                    self.unbind("<Right>")
                    self.unbind("<Up>")
                    self.bind("<Up>", self.trigger_command_with_param_last)
                    self.command_last_lied()
                    return
                else:
                    self.bind("<Right>", self.trigger_command_with_param)
                    self.unbind("<Up>")
                    self.bind("<Up>", self.trigger_command_with_param)

                if not button_or_normal:

                    if self.vers_postion > len(numbers):
                        self.vers_postion = 0
                        self.lied_position += 1
                        widget_liedanzeige.config(style='TButton')
                        self.clear_verse_widgets()
                        self.update_widget_positions()
                    elif self.vers_postion == 0 and self.lied_position == self.position:
                        widget_liedanzeige.config(style='vorbereitung.TFrame')
                        self.command_vorbereitung_lied_vers()
                    else:
                        widget_liedanzeige.config(style='aktive.TFrame')
                        self.command_aktive_lied_vers(vers_position=self.vers_postion, liedenummer=self.liednummer)
                        for name, info in self.verse_widgets.items():
                            widget = info["widget"]
                            position = info["pos"]
                            if position == numbers[self.vers_postion-1]:
                                widget.config(style='aktive.TLabel')
                else:
                    if self.vers_postion == 0:
                        widget_liedanzeige.config(style='vorbereitung.TFrame')
                        self.command_vorbereitung_lied_vers()
                    else:
                        widget_liedanzeige.config(style='aktive.TFrame')
                        self.command_aktive_lied_vers(vers_position=self.vers_postion, liedenummer=self.liednummer)
                        for name, info in self.verse_widgets.items():
                            widget = info["widget"]
                            position = info["pos"]
                            if position == self.vers_postion:
                                widget.config(style='aktive.TLabel')
            else:
                widget_liedanzeige.config(style='TButton')






    def trigger_command_with_param_last(self, event):
        self.ablauf_sterung(-1, 10000)



    def trigger_command_with_param(self, event):
        key_pressed = event.keysym
        if key_pressed == 'Left':
            self.liedübergabe = 0
            self.versübergabe = -1
        elif key_pressed == 'Right':
            self.liedübergabe = 0
            self.versübergabe = 1
        elif key_pressed == 'Up':
            self.liedübergabe = -1
            self.versübergabe = 1500
        elif key_pressed == 'Down':
            self.liedübergabe = 1
            self.versübergabe = 1500
        self.ablauf_sterung(self.liedübergabe, self.versübergabe)


    def lied_vers_button_command(self, position_lied, position_vers):
        self.ablauf_sterung(übergabe_postion_lied=position_lied, übergabe_postion_vers=position_vers, button_or_normal=True)

    def command_last_lied(self):
        pass

    def command_aktive_lied_vers(self, liedenummer, vers_position):
        vers_number = db_connection_info_get("SELECT verse_text FROM verses WHERE song_id = ? AND verse_number = ?", (liedenummer, vers_position))


    def command_vorbereitung_lied_vers(self):
        pass