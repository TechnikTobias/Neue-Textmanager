import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import os
import sqlite3
import json

import ablauf
import Settings
import Kamera
import datenverarbeiten
import Load_settings
import Scroll_frame
from screeninfo import get_monitors

widget_info = {}

def get_db_connection():
    """
    Diese Funktion verbindet mich mit der Datenbank Lieder_Datenbank

    Parameter:
    Keine

    Rückgabewert:
    conn: verbindung zur datenbank
    """
    db_filename = "Lieder_Datenbank.db"
    db_path = os.path.join(os.path.dirname(__file__), db_filename)
    conn = sqlite3.connect(db_path)
    return conn

def db_connection_info_write(input_db :str = "input", input_db_variabel :tuple = ()):
    """
    Diese Funktion schreibt daten in die Datenbank

    Parameter:
    input_db: Befehl eingabe wie INSERT INTO Ablaufverwaltung (Position)
    input_db_variabel: eingabe in dem fall für Position (1), wichtig tupel
    
    Rückgabewert: 
    Keinen
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if len(input_db_variabel) > 1:
        cursor.execute(input_db, input_db_variabel)
    else:
        cursor.execute(input_db)
    conn.commit()
    conn.close()


def db_connection_info_get( input_db :str = "input", input_db_variabel :tuple = (), singel_or_multi :bool = False):
    """
    Diese Funktion liest Info aus einer Datenbank aus

    Parameter:
    input_db: eingabe wie "SELECT verse_text FROM verses WHERE song_id = ? AND verse_number = ?"
    input_db_variabel: eingabe wie (liednummer, Versnummer)
    singel_or_multi: Eingabe standart wert False ausgabe ist ein str oder int, bei True ist ausgabe eine list.

    Rückgabewert: 
    bei singel_or_multi == True: list
    bei singel_or_multi == False: str or int
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(input_db, input_db_variabel)
    Ausgabe = cursor.fetchall()
    conn.close()
    if Ausgabe: 
        if singel_or_multi:
            return [item[0] for item in Ausgabe]
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
        widget: tk.Widget = None, 
        relheight: int = 0.1, 
        relwidth : int = 0.11,
        relx: int = None, 
        rely: int = None,
        get_position: bool = False,
        position : int = 0,
        ):
    """Registriert ein Widget und speichert seine Informationen
    Hier werden die Info für die Widget übergeben damit sie an einer zentrallen stelle placiert werden und deren größe angepasst wird."""
    widget_info[name] = {
        "widget": widget,
        "relheight": relheight,
        "relwidth": relwidth,
        "relx": relx,
        "rely": rely, 
        "get_position": get_position,
        "position" : position,
    }

def update_widget_positions():
    min_rely = 0.00  # Minimum Y-Position
    max_rely = 1  # Maximum Y-Position
    """Aktualisiert die Positionen und Größen aller Widgets basierend auf dem Skalierungsfaktor."""
    try:
        factor = int(db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",))) / 100
    except Exception as e:
        print(f"Error retrieving scaling factor: {e}")
        return

    widgets_to_remove = []
    all_positions = []
    
    # Sammle alle Positionen, die berücksichtigt werden sollen
    for name, info in widget_info.items():
        if info.get("get_position", False):
            all_positions.append(float(info["position"]))
    
    # Sortiere die Positionen numerisch
    all_positions.sort()

    num_widgets = len(all_positions)


    # Berechne die Y-Positionen basierend auf der Anzahl der Widgets
    for idx, position in enumerate(all_positions):
        corresponding_info = next((info for info in widget_info.values() if float(info["position"]) == position), None)
        if corresponding_info:
            corresponding_info["rely"] = min_rely + ((max_rely - min_rely) / (len(all_positions))) * idx
            relheight = (max_rely - min_rely) / num_widgets  # Gleichmäßige Verteilung der Höhe
            corresponding_info["relheight"] = relheight  # Setze die berechnete Höhe

    for name, info in widget_info.items():
        try:
            widget = info["widget"]
            relwidth = info["relwidth"]
            relx = info["relx"]
            
            # Überprüfe, ob rely und relheight gesetzt werden müssen
            if info.get("get_position", False):
                rely = info["rely"]
                relheight = info["relheight"]
            else:
                rely = info.get("rely", 0)
                relheight = info.get("relheight", 0)
            
            # Platziere das Widget
            widget.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely)
        except Exception as e:
            widgets_to_remove.append(name)
            print(f"Error updating widget {name}: {e}")
    
    # Entferne die fehlerhaften Widgets aus widget_info
    for name in widgets_to_remove:
        del widget_info[name]


class TextmanagerAPP(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hintergrund_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("textanzeiger_hintergrund",))
        self.geometry("1040x800")
        self.title("Textmanager")
        self.config(bg=self.hintergrund_farbe)
        self.widget_info_liedauswahl = {}
        self.position_anzahl = 0
        self.all_widget = 0
        self.Menu_generator()


        # Verknüpfen der Scrollbars mit dem Canvas

        # Erstellen eines Frames im Canvas
        self.frame = Scroll_frame.ScrollableFrame(self)
        self.frame.pack(fill="both", expand=True)


        # Konfigurieren des Canvas, um seine Größe anzupassen

        self.start_programm_laden()
        self.bind("<Configure>", self.one_resize)
        update_widget_positions()



    def start_programm_laden(self):
        self.unbind("<Left>")
        self.unbind("<Right>")
        self.unbind("<Up>")
        self.unbind("<Down>")
        self.widget_delite()
        entries = fetch_all_program_info("Ablaufaufbau", "Reihenfolge")
        for position_amzahl, entry in enumerate(entries):
            self.all_widget += 1
        for position_amzahl, entry in enumerate(entries):
            self.position_anzahl = position_amzahl
            self.gegerator_lieder(entry[0]+1,entry[2], entry[1], self.all_widget)
        self.button_generator()
        update_widget_positions()
        self.liedanzeige_aktualisieren("hallo")


    def one_resize(self,event):
        Load_settings.Textmanager_größen(self, self.get_window_size())
        factor = int(db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("scalierung",)))/100
        self.all_widget = 0
        for name, info in widget_info.items():
            try:
                get_position = info["get_position"]
                if get_position:
                    self.all_widget += 1
            except:
                pass
        self.frame.frame_id_def(height=self.get_window_size()[1]/12*self.all_widget*factor, width=self.get_window_size()[0]*factor)


    def get_window_size(self):
        return self.winfo_width(), self.winfo_height()

    def festgröße_bestimmen(self):
        Load_settings.Textmanager_größen(self.get_window_size())



    def register_widegets_liedaktualisieren(self,
                             name: str = None,
                             name_datenbank: str = None,
                             liednummer: tk.Widget = None,
                             versnummer: tk.Widget = None,
                             widget: tk.Widget = None,
                             buchauswahl: tk.Widget = None,
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
                             liedanzeige: tk.Widget = None,
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
                             widget: tk.Widget = None,
                             pos: int = 0,
                             text : str = ""):
        """Regestiert die Liedauwahl und lasst das richtige lied erscheinen"""
        self.verse_widgets[name] = {
            "widget": widget,
            "pos": pos,
            "text": text
        }
    

    def text_fits_in_widget(self, widget, text):
        monitors = get_monitors()
        widget_font = font.Font(font=widget.cget("font"))
        text_width = widget_font.measure(text)
        text_height = widget_font.metrics("linespace") * (text.count("\n") + 1)  # Zeilenhöhe mal Anzahl der Zeilen
        widget_width = monitors[0].width
        widget_height = monitors[0].height
        return text_width <= widget_width and text_height <= widget_height

    def split_text_into_pages(self, widget, text, max_page_height=None):
        widget_font = font.Font(font=widget.cget("font"))
        line_height = widget_font.metrics("linespace")
        monitors = get_monitors()
        
        # Setze die maximale Seitenhöhe auf die Höhe des Bildschirms oder auf einen spezifischen Wert
        if max_page_height is None:
            max_page_height = monitors[0].height
        
        lines = text.splitlines()  # Teilt den Text in Zeilen
        current_page = []
        pages = []
        current_height = 0

        for line in lines:
            words = line.split()
            current_line = ""
            for word in words:
                # Überprüfe, ob die aktuelle Zeile + das neue Wort in den Bildschirm passt
                if self.text_fits_in_widget(widget, current_line + word + " "):
                    current_line += word + " "
                else:
                    current_page.append(current_line.strip())
                    current_height += line_height
                    current_line = word + " "
                
                # Falls die Höhe die maximale Seitenhöhe erreicht, speichere die aktuelle Seite und beginne eine neue
                if current_height + line_height > max_page_height:
                    pages.append(current_page)
                    current_page = []
                    current_height = 0
            
            # Füge die verbleibende Zeile zur aktuellen Seite hinzu
            current_page.append(current_line.strip())
            current_height += line_height

            # Wenn die Seite die maximale Höhe erreicht, speichere sie und beginne eine neue Seite
            if current_height > max_page_height:
                pages.append(current_page)
                current_page = []
                current_height = 0

        # Füge die letzte Seite hinzu, falls sie nicht leer ist
        if current_page:
            pages.append(current_page)
        
        num_pages = len(pages)

        return num_pages, pages


    def all_vers_exist(self):
            song = fetch_all_program_info("Ablaufverwaltung", "Position")
            #song = db_connection_info_get("SELECT * FROM Ablaufverwaltung" ( ))
            for singel_song in song:
                zusatz = 1
                all_vers = []
                versübergabeunfertig = (singel_song[4])
                versübergabe_ready = []
                versübergabe = []
                übergabe_allvers = []
                if versübergabeunfertig:
                    parts = str(versübergabeunfertig).split(',')  # Teile die Eingabe anhand des Kommas
                    for part in parts:
                        if '-' in part:  # Überprüfe, ob ein Bereich (z.B. 3-6) vorhanden ist
                            start, end = map(int, part.split('-'))  # Teile den Bereich anhand des Bindestrichs
                            versübergabe.extend(range(start, end + 1))  # Füge die Zahlen im Bereich zur Liste hinzu
                        else:
                            versübergabe.append(int(part))  # Füge einzelne Zahlen zur Liste hinzu
                vers_number = db_connection_info_get("SELECT verse_number FROM verses WHERE song_id = ?", (singel_song[2],),singel_or_multi=True)
                if not vers_number:
                    vers_number = [1]
                if not versübergabe and vers_number:
                    versübergabe = vers_number
                if singel_song[1] == "Lied":
                    for vers_zahl, vers in enumerate(vers_number):
                        text = db_connection_info_get("SELECT verse_text FROM verses WHERE song_id = ? AND verse_number = ?", (singel_song[2], vers))
                        if not text:
                            text = ""
                        page = (self.split_text_into_pages(textanzeiger, text=text))
                        if page[0] > 1:
                            for o in  range(0, page[0]):
                                if o > 0:
                                    zusatz +=1
                                if vers_zahl+1 in versübergabe:
                                    versübergabe_ready.append(vers_zahl+zusatz)
                                vers_singel = [vers_zahl+zusatz, page[1][o], f"{vers_zahl+1} teil {o+1}"]
                                all_vers.append(vers_singel)
                                
                        else:
                            if vers_zahl+1 in versübergabe:
                                versübergabe_ready.append(vers_zahl+zusatz)
                            vers_singel = [vers_zahl+zusatz, page[1], f"{vers_zahl+1}"]
                            all_vers.append(vers_singel)
                    übergabe_allvers.append(versübergabe_ready)
                elif singel_song[1] == "Textwort":
                    übergabe_allvers.append([1])
                    vers_singel = [1, "übergabe", f"Textwort"]
                    all_vers.append(vers_singel)
                elif singel_song[1] == "Kamera":
                    übergabe_allvers.append([1])
                    vers_singel = [1, "", f"Kamera"]
                    all_vers.append(vers_singel)
                for i in all_vers:
                    übergabe_allvers.append(i)
                self.all_info_vers.append(übergabe_allvers)


    def Menu_generator(self):
        hintergrund_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("hintergrundfarbe",))
        text_farbe = db_connection_info_get("SELECT supjekt FROM Einstellungen WHERE name = ?", ("text_farbe",))

        # Erstellen und Konfigurieren der Comboboxes
        self.menu_info_main = ttk.Combobox(self, values=["Einstellungen", "Info"], style='custom.TCombobox')
        self.menu_info_main.current(0)  # Standardwert festlegen
        self.menu_info_main.bind("<<ComboboxSelected>>", self.on_menu_info_selected)
        self.menu_info_main.pack(side=tk.LEFT, anchor=tk.NW)

        self.menu_kamera_main = ttk.Combobox(self, values=["Einstellungen", "Position"], style='custom.TCombobox')
        self.menu_kamera_main.current(0)
        self.menu_kamera_main.bind("<<ComboboxSelected>>", self.on_menu_kamera_selected)
        self.menu_kamera_main.pack(side=tk.LEFT, anchor=tk.NW)

        self.menu_liedkontrolle_main = ttk.Combobox(self, values=["Einstellungen", "Lied Kontrollieren"], style='custom.TCombobox')
        self.menu_liedkontrolle_main.current(0)
        self.menu_liedkontrolle_main.bind("<<ComboboxSelected>>", self.on_menu_liedkontrolle_selected)
        self.menu_liedkontrolle_main.pack(side=tk.LEFT, anchor=tk.NW)

        self.menu_help_main = ttk.Combobox(self, values=["Hilfe"], style='custom.TCombobox')
        self.menu_help_main.current(0)
        self.menu_help_main.bind("<<ComboboxSelected>>", self.on_menu_help_selected)
        self.menu_help_main.pack(side=tk.LEFT, anchor=tk.NW)
        self.menu_info_main.place(relheight=0.05, relwidth=0.2, relx=0, rely=0)
        self.menu_kamera_main.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0)
        self.menu_liedkontrolle_main.place(relheight=0.05, relwidth=0.2, relx=0.4, rely=0)
        # self.menu_help_main.place(relheight=0.05, relwidth=0.2, relx=0.6, rely=0)
        register_widget("Immer_anwesend", widget=self.menu_help_main, relheight=0.05, relwidth=0.2, relx=0.6, rely=0, get_position=True)
        self.space_lable = ttk.Label(self)

        self.space_lable.pack(pady=15)
    def on_menu_info_selected(self, event):
        selection = self.menu_info_main.get()
        if selection == "Einstellungen":
            self.settings_window()
        elif selection == "Info":
            Settings.Info()

    def on_menu_kamera_selected(self, event):
        selection = self.menu_kamera_main.get()
        if selection == "Einstellungen":
            Kamera.Settings()
        elif selection == "Position":
            Kamera.Position()

    def on_menu_liedkontrolle_selected(self, event):
        selection = self.menu_liedkontrolle_main.get()
        if selection == "Einstellungen":
            pass  # Platzhalter für die Einstellungen
        elif selection == "Lied Kontrollieren":
            datenverarbeiten.setup_ui()

    def on_menu_help_selected(self, event):
        selection = self.menu_help_main.get()
        if selection == "Hilfe":
            pass  # Platzhalter für die Hilfe

    def settings_window(self):
        print("Settings window opened")

    def settings_window(self):
        Settings.Settings_window(self)

    def gegerator_lieder(self, widget_position, name_lied, aktion, total_widgets):
        min_rely = 0.03
        max_rely = 1
        available_space = max_rely - min_rely

        # Position innerhalb des verfügbaren Bereichs berechnen
        rely = min_rely + (widget_position - 1) * (available_space / (total_widgets - 1))
        relhight = 0.95 /(total_widgets) 
        self.lied_frame = ttk.Frame(self.frame.frame, style="TButton")
        register_widget(f"frame_lied{widget_position}", self.lied_frame, relheight=relhight, relwidth=0.85, rely=rely-0.01, relx=0.0, get_position=True, position=widget_position)
        self.Lied_start = ttk.Label(self.lied_frame, text=name_lied, style='TLabel')
        register_widget(f"Lied_start{widget_position}", self.Lied_start, relheight=0.5, relwidth=0.25, rely=0, relx=0.0)
        if aktion == "Textwort":
            self.Button_Textwort = ttk.Button(self.lied_frame, text="Textwort", style='TButton')
            register_widget(f"Button_textwort{widget_position}", self.Button_Textwort, relheight=0.5, relwidth=0.25, rely=0, relx=0.25)
            self.register_widegets_liedaktualisieren(name=f"Textwort{widget_position}", name_datenbank=name_lied, befehl=aktion, pos=widget_position-1)
        elif aktion == "Lied":
            self.Button_Kamera = ttk.Button(self.lied_frame, text="Kamera", style='TButton')
            register_widget(f"Button_Kamera{widget_position}", self.Button_Kamera, relheight=0.5, relwidth=0.25, rely=0.5, relx=0)
            #befehle_kamera = ["Kamera", "Textwort", "Lied"]
            #clicked_kamera = StringVar()
            #clicked_kamera.set(befehle_kamera[0])
            #opt_kamera = ttk.OptionMenu(self, clicked_kamera, *befehle_kamera, style='custom.TMenubutton')
            #register_widget(f"clicked_kamera{widget_position}",opt_kamera, relheight=0.05, relwidth=0.1, rely=rely, relx=0.3)
            #inhalt.append(clicked_kamera)
            #inhalt.append(opt_kamera)
            self.eingabe_lied = ttk.Entry(self.lied_frame, style='TEntry')
            self.eingabe_lied.bind("<KeyRelease>", self.liedanzeige_aktualisieren)
            register_widget(name=f"eingabe_lieder{widget_position}",widget=self.eingabe_lied, relheight=0.5, relwidth=0.05, relx=0.55, rely=0)
            self.eingabe_vers = ttk.Entry(self.lied_frame, style='TEntry')
            self.eingabe_vers.bind("<KeyRelease>", self.liedanzeige_aktualisieren)
            register_widget(name=f"eingabe_verse{widget_position}", widget=self.eingabe_vers, relheight=0.5, relwidth=0.05, relx=0.55, rely=0.5)
            self.befehle_buch = ["Gesangbuch", "Chorbuch", "Jugendliederbuch"]
            self.clicked_buch = tk.StringVar()
            self.clicked_buch.set(self.befehle_buch[0])
            self.opt_buch = ttk.OptionMenu(self.lied_frame, self.clicked_buch, *self.befehle_buch, command=self.liedanzeige_aktualisieren)
            register_widget(name=f"opt_buch{widget_position}", widget=self.opt_buch, relheight=0.5, relwidth=0.2, relx=0.25, rely=0)
            self.liednummer_lable = ttk.Label(self.lied_frame, style='TLabel', text="Liednummer  -->")
            register_widget(name=f"liednummer_lable{widget_position}", widget=self.liednummer_lable, relheight=0.5, relwidth=0.15, relx=0.4, rely=0)
            self.versnummer_lable = ttk.Label(self.lied_frame, style='TLabel', text="Versnummer  -->")
            register_widget(name=f"versnummer_lable{widget_position}", widget=self.versnummer_lable, relheight=0.5, relwidth=0.15, relx=0.4, rely=0.5)
            self.text_lied_lable = ttk.Label(self.lied_frame, style='TLabel')
            register_widget(name=f"text_lied_lable{widget_position}", widget=self.text_lied_lable, relheight=1, relwidth=0.4, relx=0.6, rely=0)
            self.register_widegets_liedaktualisieren(name=f"liedanzeiger{widget_position}",name_datenbank = name_lied,liednummer=self.eingabe_lied, versnummer=self.eingabe_vers, befehl=aktion, pos=widget_position-1, widget=self.text_lied_lable, buchauswahl=self.clicked_buch)
        elif aktion == "Kamera":
            self.Button_Kamera = ttk.Button(self.lied_frame, text="Kamera", style='TButton')
            register_widget(f"Button_Kamera{widget_position}", self.Button_Kamera, relheight=1, relwidth=0.15, rely=0, relx=0.3)
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
        wiederherstellen = ttk.Button(self.frame.frame, text="Wiederherstellen", style='TButton')
        register_widget("widerherstell_button", widget=wiederherstellen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.1)
        loeschen = ttk.Button(self.frame.frame, text="Löschen", style='TButton')
        register_widget("löeschen_button", widget=loeschen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.2)
        preasentation = ttk.Button(self.frame.frame, text="Präsentation", command=self.Ablaufsteuerung, style='TButton')
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
        self.vers_position :int = 0
        self.lied_position :int = 0
        self.verse_widgets = {}
        self.all_info_vers :list = []  
        """Die Vareable info_all_vers ist erste klammer [] ist die Position 
        in der ablauf was über die Vareable self.lied_position gesteuert wird
        """
        self.bind("<Configure>", self.one_resize)
        self.bind("<Left>", self.trigger_command_with_param)
        self.bind("<Right>", self.trigger_command_with_param)
        self.bind("<Up>", self.trigger_command_with_param)
        self.bind("<Down>", self.trigger_command_with_param)
        self.button_aktivitat = 0
        self.all_vers_exist()
        self.ablauf_steuerung(0,0, button_press=True)

    def button_ablauf_steuerung(self):
        global textanzeiger
        """wiederherstellen = ttk.Button(self, text="Wiederherstellen", style='TButton')
        register_widget("widerherstell_button", widget=wiederherstellen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.1)
        loeschen = ttk.Button(self, text="Löschen", style='TButton')
        register_widget("löeschen_button", widget=loeschen, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.2)"""
        eingabe = ttk.Button(self.frame.frame, text="Eingabe", command=self.start_programm_laden, style='TButton')
        register_widget("presentation_button", widget=eingabe, relheight=0.1, relwidth=0.2, relx=0.8, rely=0.3)
        textanzeiger = tk.Label(self.frame.frame, font=('Helvetica', 60))
        textanzeiger.place(relheight=0.1, relwidth=0.2, relx=0.8, rely=0.5)


    def gegerator_lieder_ablauf(self, widget_position, name_lied, aktion, liednummer, versnummer, buch):
        self.frame1 = ttk.Button(self.frame.frame, style='TLabel', command=lambda l= widget_position: self.lied_vers_button_command(l, 0))
        register_widget(name=f"frame{widget_position}", widget=self.frame1, relheight=0.1, relwidth=0.7, relx=0, rely=0.1*(widget_position+1)-0.05, get_position=True, position=widget_position)
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
            self.text_lied_lable = ttk.Button(self.frame1, style='TLabel', text=Text_speicher, command=lambda l= widget_position: self.lied_vers_button_command(l, 0))
            register_widget(name=f"text_lied_lable{widget_position}", widget=self.text_lied_lable, relheight=1, relwidth=0.4, relx=0.405, rely=0)
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
            for x in (lst):
                if x > num:
                    return x
            return None
        
        # Funktion zur Suche der nächsten kleineren Zahl in der Liste
        def next_lower(num, lst):
            for x in reversed(list(lst)):
                if x < num:
                    return x
            return None
        if number in comparison_list:
            # Wenn die Zahl in der Liste ist, übernehmen wir sie
            widget_position = comparison_list.index(number)
            return number, widget_position, None
        else:
            # Wenn die Zahl nicht in der Liste ist, bearbeiten wir sie
            if change > 0:
                # Positive Änderungszahl
                next_num = next_higher(number, comparison_list)
                if next_num is not None:
                    return next_num, None
                else:
                    # Wenn keine nächsthöhere Zahl vorhanden ist
                    return None, "up"
            elif change < 0:
                # Negative Änderungszahl
                next_num = next_lower(number, comparison_list)
                if next_num is not None:
                    return next_num, None
                else:
                    # Wenn keine nächstkleinere Zahl vorhanden ist
                    return None, "down"
            else:
                print("Keine Änderung erforderlich.")
                return number



    def ablauf_steuerung(self, über_lied = 0, über_vers = 0, button_press = False):
        if button_press:
            self.command_button_press(über_lied, über_vers)

        elif über_vers:
            if not self.lied_position +über_lied < 0 or not self.vers_position + über_vers < 0:
                self.command_über_vers(über_vers)
    
        elif über_lied:
            if not self.lied_position + über_lied < 0 and self.lied_position + über_lied < len(self.all_info_vers) :
                self.command_button_press(self.lied_position+über_lied, über_vers)

    def command_button_press(self, über_lied, über_vers):
        self.vers_position = über_vers
        self.lied_position = über_lied
        self.ablauf_steuerung_versposition()

    def command_über_vers(self, über_vers):
        self.vers_position += über_vers
        if self.vers_position < 0 and self.lied_position > 0:
            self.lied_position -= 1
            self.vers_position = self.all_info_vers[self.lied_position][0][-1]
            self.command_button_press(über_lied=self.lied_position, über_vers=self.vers_position)
            

        elif self.vers_position < 0 and self.lied_position == 0 :
            self.vers_position = 0
            return
        elif self.lied_position == len(self.all_info_vers) -1 and len(self.all_info_vers[self.lied_position]) <= self.vers_position:
            if len(self.all_info_vers[self.lied_position]) < self.vers_position:
                self.vers_position -= 1
            for name, info in self.verse_widgets.items():
                widget = info["widget"]
                position_vers = info["pos"]
                if position_vers == self.vers_position-1:
                    widget.config(style='end.TFrame')
                    self.command_last_lied()
                else:
                    widget.config(style="TLabel")
            return
        elif not self.vers_position == 0:
            vers_über = (self.adjust_number(self.vers_position, self.all_info_vers[self.lied_position][0], über_vers))
            self.vers_position = vers_über[0]
            if self.vers_position == None:
                self.vers_position = 0
            if vers_über[1] == "up":
                self.command_button_press(über_lied=self.lied_position + 1, über_vers=0)
                vers_über = 0
            

        for name, info in self.widget_info_liedauswahl_aublauf.items():
            liednummer = info["liednummer"]
            versnummer = info["versnummer"]
            widget_liedanzeige = info["liedanzeige"]
            buchauswahl = info["buchauswahl"]
            befehl = info["befehl"]
            position_lied = info["pos"]
            if position_lied == self.lied_position:
                if self.vers_position > 0:
                    widget_liedanzeige.config(style='aktive.TLabel')
                else:
                    widget_liedanzeige.config(style='vorbereitung.TFrame')
                for name, info in self.verse_widgets.items():
                    widget = info["widget"]
                    position_vers = info["pos"]
                    if position_vers == self.vers_position:
                        widget.config(style='aktive.TLabel')
                        self.command_aktive_lied_vers()
                    else:
                        widget.config(style="TLabel")





    def ablauf_steuerung_versposition(self):

        for self.name, info in self.widget_info_liedauswahl_aublauf.items():
            liednummer = info["liednummer"]
            versnummer = info["versnummer"]
            widget_liedanzeige = info["liedanzeige"]
            buchauswahl = info["buchauswahl"]
            befehl = info["befehl"]
            position = info["pos"]
            widget_liedanzeige.config(style='TLabel')
            if position == self.lied_position:
                self.clear_verse_widgets()
                aktuelle_lieder = self.all_info_vers[self.lied_position]
                for o, i in enumerate(aktuelle_lieder):
                    if o > 0:
                        verse_num = i[0]
                        text = i[1]
                        text_label = i[2]
                        verse_widget = ttk.Button(self.frame.frame, text=f"{text_label}", style='TButton', command=lambda v=verse_num, l= self.lied_position: self.lied_vers_button_command(l, v))
                        verse_rel_y = 0.1 * (position + 1 + o)  # Berechnet die y-Position des Widgets
                        register_widget(name=f"verse_{position}_{verse_num}", widget=verse_widget, relheight=0.05, relwidth=0.7, relx=0, rely=verse_rel_y, get_position=True, position=float(f"{position}.{verse_num}"))
                        self.register_vers_widegt(name=f"verse_{position}_{verse_num}", widget=verse_widget, pos=o, text=text)
                        if self.vers_position == o:
                            verse_widget.config(style='aktive.TLabel')
                        if self.vers_position > 0:
                            widget_liedanzeige.config(style='aktive.TLabel')
                        else:
                            widget_liedanzeige.config(style='vorbereitung.TFrame')
                update_widget_positions()     








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
            self.versübergabe = 0
        elif key_pressed == 'Down':
            self.liedübergabe = 1
            self.versübergabe = 0
        self.ablauf_steuerung(self.liedübergabe, self.versübergabe)


    def lied_vers_button_command(self, position_lied, position_vers):
        self.ablauf_steuerung(über_lied=position_lied, über_vers=position_vers, button_press=True)

    def command_last_lied(self):
        pass

    def command_aktive_lied_vers(self):
        text = self.all_info_vers[self.lied_position][self.vers_position][1]
        print(f"{text}erste anzeige")
        for name, info in self.verse_widgets.items():
            text = info["text"]
            position_vers = info["pos"]
            if self.vers_position == position_vers:
                print(f"{text}zweite anzeige")
                break
    def command_vorbereitung_lied_vers(self):
        pass