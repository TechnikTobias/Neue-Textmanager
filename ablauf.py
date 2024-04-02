import Neue_Textmanager
import Load_settings

from tkinter import *
def Präsentation_starten():
    global alle_inhalt, button_liste
    alle_inhalt = []
    Neue_Textmanager.clear_window()
    über_inhalt = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("speichern",))[0].split("!")
    for i in über_inhalt:
        alle_inhalt.append(gegerator_lieder(i))
    Neue_Textmanager.Textmanager.bind("<Configure>", on_resize)
    Neue_Textmanager.Textmanager.bind("<Key>", on_key)
    button_liste = []
    button_liste.append(button_generator())
    anfang_ablauf()
    position_präsi()

def on_key(event):
        if event.keysym == 'Up':
            zurueck_lied()
        elif event.keysym == 'Down':
            weiter_lied()
        elif event.keysym == 'Right':
            weiter_vers()
        elif event.keysym == 'Left':
            zurueck_vers()


def button_generator():
    hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("Hintergrundfarbe",))
    text_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("Textfarbe",))
    rueckgabe = []
    weiter_button = Button(Neue_Textmanager.Textmanager, text="weiter", command=weiter_vers)
    rueckgabe.append(weiter_button)
    rueckgabe.append("Button")
    zrueck_button = Button(Neue_Textmanager.Textmanager, text="zurück", command=zurueck_vers)
    rueckgabe.append(zrueck_button)
    zrueck_button = Button(Neue_Textmanager.Textmanager, text="Text Eingaben", command=clear_window)
    rueckgabe.append(zrueck_button)
    zrueck_button = Button(Neue_Textmanager.Textmanager, text="zurück", command=zurueck_vers)
    rueckgabe.append(zrueck_button)
    for i in rueckgabe:
        if isinstance(i, Widget):
            i.config(bg=hintergrund_farbe, fg=text_farbe)
    return rueckgabe

def weiter_vers():
    ablauf_varables[1] += 1
    ablauf_aktualisieren_vers()

def weiter_lied():
    ablauf_varables[0] += 1
    ablauf_varables[1] = 0
    ablauf_aktualisieren_lied()


def zurueck_vers():
    if ablauf_varables[0] > 0 or ablauf_varables[0] == 0 and ablauf_varables[1]:
        ablauf_varables[1] -= 1
        ablauf_aktualisieren_vers()

def zurueck_lied():
    if ablauf_varables[0] >= 0:
        ablauf_varables[0] -= 1
        ablauf_varables[1] = 0
        ablauf_varables[2] = True
        ablauf_aktualisieren_lied()
        

def anfang_ablauf():
    global ablauf_varables
    ablauf_varables = []
    ablauf_varables.append(0) 
    ablauf_varables.append(0) 
    ablauf_varables.append(False) 

def clear_window():
    global ablauf_varables, alle_inhalt
    del ablauf_varables
    Neue_Textmanager.Textmanager.unbind("<Key>")
    Neue_Textmanager.Textmanager.unbind("<Configure>")
    for i in alle_inhalt:
        for i in i:
            if isinstance(i, Widget):
                i.destroy()
    del alle_inhalt
    Neue_Textmanager.start_anzeige_bildschirm()
    Neue_Textmanager.posistion()


def ablauf_aktualisieren_vers():
    übergabe = gesamt_verse()
    if ablauf_varables[1] >=1 and ablauf_varables[1] <= len(übergabe):
        alle_inhalt[ablauf_varables[0]][0].config(bg="green")
        vers_anzeigen()
    elif ablauf_varables[1] <= 0:
        if ablauf_varables[0] > 0:
            ablauf_varables[0] -= 1
            übergabe = gesamt_verse()
            ablauf_varables[1] = len(übergabe) +1
        grund_farbe()
        alle_inhalt[ablauf_varables[0]][0].config(bg="yellow")
        if ablauf_varables[2]:
            ablauf_varables[2] = False
            zurueck_vers()
    elif ablauf_varables [1] > len(übergabe):
        try:
            grund_farbe()
            alle_inhalt[ablauf_varables[0]+1][0].config(bg="yellow")
            ablauf_varables[0] += 1
            ablauf_varables[1] = 0
        except:
            alle_inhalt[ablauf_varables[0]][0].config(bg="pink")
            ablauf_varables[1] = len(übergabe) +1



def ablauf_aktualisieren_lied():
    ablauf_varables[1] = 0
    if ablauf_varables[0] >=0:
        try:
            grund_farbe()
            alle_inhalt[ablauf_varables[0]][0].config(bg="yellow")
        except:
            ablauf_varables[0] -= 1
            alle_inhalt[ablauf_varables[0]][0].config(bg="yellow")
    else:
            ablauf_varables[0] += 1
            alle_inhalt[ablauf_varables[0]][0].config(bg="yellow")


def vers_anzeigen():
    numbers = gesamt_verse()
    aktuelles_lied = alle_inhalt[ablauf_varables[0]]
    song_name = Neue_Textmanager.get_db_connection("SELECT verse_text FROM verses WHERE song_number = ? AND book_name = ? AND verse_number = ?", (str(aktuelles_lied[1][2]),aktuelles_lied[1][4], numbers[ablauf_varables[1]-1]))
    if song_name:
        Load_settings.Text_Anzeige_Label.config(text=song_name[0])



def gesamt_verse():
    aktuelles_lied = alle_inhalt[ablauf_varables[0]]
    if aktuelles_lied[1][2]:
        song_min_vers = Neue_Textmanager.get_db_connection("SELECT min_vers FROM songs WHERE song_number = ? AND book_name = ?", (str(aktuelles_lied[1][2]),str(aktuelles_lied[1][4])))
    else:
        song_min_vers = []
        song_min_vers.append(1)        
    if aktuelles_lied[1][3]:
        numbers = []
        parts = aktuelles_lied[1][3].split(',')  # Teile die Eingabe anhand des Kommas
        for part in parts:
            if '-' in part:  # Überprüfe, ob ein Bereich (z.B. 3-6) vorhanden ist
                start, end = map(int, part.split('-'))  # Teile den Bereich anhand des Bindestrichs
                numbers.extend(range(start, end + 1))  # Füge die Zahlen im Bereich zur Liste hinzu
            else:
                numbers.append(int(part))  # Füge einzelne Zahlen zur Liste hinzu
    else:
        numbers = list(range(1, song_min_vers[0] + 1))
    return numbers


def grund_farbe():
    for i in alle_inhalt:
        hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("Hintergrundfarbe",))
        i[0].config(bg=hintergrund_farbe)
    Load_settings.Text_Anzeige_Label.config(text="")


def on_resize(event):
    position_präsi(1)
    position_button()

def gegerator_lieder(input):
    hintergrund_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("Hintergrundfarbe",))
    text_farbe = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("Textfarbe",))
    ja = input.split(";")
    name_lied = ja[1]
    aktion = ja[0]
    Kamera = ja[2]
    Liednummer = ja[3]
    Buch = ja[5]
    Vers_nummer = ja[4]
    inhalt = []
    Lied_start = Label(Neue_Textmanager.Textmanager, text=name_lied)
    Lied_start.config(bg=hintergrund_farbe, fg=text_farbe)
    inhalt.append(Lied_start)
    inhalt.append([aktion, name_lied, Liednummer, Vers_nummer, Buch, Kamera])
    if aktion == " Textwort":
        pass
    elif aktion == " Lied":
        lable_Kamera = Button(Neue_Textmanager.Textmanager, text="Kamera", border=0)
        lable_Kamera.config(bg=hintergrund_farbe, fg=text_farbe)
        inhalt.append(lable_Kamera)
        text_lied_lable = Label(Neue_Textmanager.Textmanager)
        text_lied_lable.config(bg=hintergrund_farbe, fg=text_farbe)
        inhalt.append(text_lied_lable)
    elif aktion == " Kamera":
        lied_weiter = Button(Neue_Textmanager.Textmanager, text= "servus", border=0)
        lied_weiter.config(bg=hintergrund_farbe, fg=text_farbe)
        inhalt.append(lied_weiter)
    return inhalt


def position_präsi(factor= 1):
    for pos,i in enumerate(alle_inhalt):
        text_size = min( int(i[0].winfo_height()/3*factor), int(i[0].winfo_width()/8*factor))
        i[0].config(font=('Helvetica', text_size))
        if i[1][0] == " Lied":
            i[0].place(x= 0, y= pos*i[0].winfo_height()*2+pos*2,relwidth=0.3*factor, relheight=0.05*factor)
            i[2].place(x= 0, y= pos*(i[0].winfo_height()+1)*2+i[0].winfo_height()+1,relwidth=0.3*factor, relheight=0.05*factor)
            i[2].config(font=('Helvetica', text_size))
            i[3].place(x= (i[0].winfo_width()+1), y= pos*i[0].winfo_height()*2+pos*2,relwidth=0.5*factor, relheight=0.1*factor)
            i[3].config(font=('Helvetica', text_size))
            song = Neue_Textmanager.get_db_connection("SELECT song_name FROM songs WHERE song_number = ? AND book_name = ?", (str(i[1][2]),str(i[1][4])))
            if not i[1][3]:
                text_einfügen = ""
            elif len(i[1][3]) == 1:
                text_einfügen = f"Vers {i[1][3]}"
            elif len(i[1][3]) > 1:
                text_einfügen = f"Verse {i[1][3]}"
            if song:
                Text_speicher = f"{i[1][2]} {i[1][4]} {text_einfügen}\n{song[0]}"
                i[3].config(text= Text_speicher)
            else:
                i[3].config(text = "Bitte geben sie eine Nummer ein\n")
        elif i[1][0] == " Kamera":
            i[0].place(x= 0, y= pos*i[0].winfo_height()*2+pos*2,relwidth=0.3*factor, relheight=0.05*factor)
            i[2].place(x= 0, y= pos*(i[0].winfo_height()+1)*2+i[0].winfo_height()+1,relwidth=0.3*factor, relheight=0.05*factor)
            i[2].config(font=('Helvetica', text_size))
        elif i[1][0] == " Textwort":
            i[0].place(x= 0, y= pos*i[0].winfo_height()+pos*2,relwidth=0.4*factor, relheight=0.1*factor)



def position_button(factor = 1):
    fenster_width= Neue_Textmanager.Textmanager.winfo_width()
    text_size = min( int(button_liste[0][0].winfo_height()/3*factor), int(button_liste[0][0].winfo_width()/8*factor))
    button_liste[0][0].config(font=('Helvetica', text_size))
    button_liste[0][0].place(x=fenster_width-button_liste[0][0].winfo_width()-15, y=10, relwidth=0.12*factor, relheight=0.07*factor)
    button_liste[0][2].place(x=fenster_width-button_liste[0][2].winfo_width()-15, y=button_liste[0][0].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)
    button_liste[0][2].config(font=('Helvetica', text_size))
    button_liste[0][3].place(x=fenster_width-button_liste[0][0].winfo_width()-15, y=button_liste[0][0].winfo_height()+button_liste[0][2].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)
    button_liste[0][3].config(font=('Helvetica', text_size))
    button_liste[0][4].place(x=fenster_width-button_liste[0][0].winfo_width()-15, y=button_liste[0][0].winfo_height()+button_liste[0][2].winfo_height()+button_liste[0][3].winfo_height()+10, relwidth=0.12*factor, relheight=0.07*factor)
    button_liste[0][4].config(font=('Helvetica', text_size))