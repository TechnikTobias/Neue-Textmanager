import Neue_Textmanager

from tkinter import *
alle_inhalt = []
def Präsentation_starten():
    Neue_Textmanager.clear_window()
    über_inhalt = Neue_Textmanager.get_db_connection("SELECT supjekt FROM Einstellungen WHERE name = ?", ("speichern",), True)[0].split("!")
    for i in über_inhalt:
        alle_inhalt.append(gegerator_lieder(i))
        Position_präsi(1)
    Neue_Textmanager.Textmanager.bind("<Configure>", on_resize)
    Neue_Textmanager.Textmanager.bind("<Key>", on_key)
    anfang_ablauf()

def on_key(event):
        if event.keysym == 'Up':
            zurueck_lied()
        elif event.keysym == 'Down':
            weiter_lied()
        elif event.keysym == 'Right':
            weiter_vers()
        elif event.keysym == 'Left':
            zurueck_vers()


def weiter_vers():
    ablauf_varables[2] += 1
    ablauf_akualisieren()

def weiter_lied():
    ablauf_varables[1] += 1
    ablauf_akualisieren()


def zurueck_vers():
    ablauf_varables[2] -= 1
    ablauf_akualisieren()

def zurueck_lied():
    ablauf_varables[1] -= 1
    ablauf_akualisieren()

def anfang_ablauf():
    global ablauf_varables
    ablauf_varables = []
    ablauf_varables.append(alle_inhalt)
    ablauf_varables.append(0) 
    ablauf_varables.append(0) 

def ende_ablauf():
    global ablauf_varables
    del ablauf_varables


def ablauf_akualisieren():
    übergabe = alle_inhalt[ablauf_varables[1]][1][3].split(",")
    print(len(übergabe))
    if ablauf_varables[2] >=1 and ablauf_varables[2] < len(übergabe):
        print(übergabe[ablauf_varables[2]-1])
    elif ablauf_varables[2] <= 0:
        ablauf_varables[1] -= 1
        ablauf_varables[2] = 1
        print(True)
    elif ablauf_varables [2] > len(alle_inhalt[ablauf_varables[1]][1][3]):
        ablauf_varables[1] += 1
        ablauf_varables[2] = 1
        print(False)


def on_resize(event):
    Position_präsi(1)

def gegerator_lieder(input):
    ja = input.split(";")
    name_lied = ja[1]
    aktion = ja[0]
    Liednummer = ja[3]
    Buch = ja[5]
    Vers_nummer = ja[4]
    inhalt = []
    Lied_start = Label(Neue_Textmanager.Textmanager, text=name_lied)
    inhalt.append(Lied_start)
    if aktion == " Textwort":
        inhalt.append([aktion, name_lied])
    elif aktion == " Lied":
        inhalt.append([aktion, name_lied, Liednummer, Vers_nummer, Buch])
        Lable_Kamera = Button(Neue_Textmanager.Textmanager, text="Kamera", border=0)
        inhalt.append(Lable_Kamera)
        Tex_lied_lable = Label(Neue_Textmanager.Textmanager)
        inhalt.append(Tex_lied_lable)
    elif aktion == " Kamera":
        inhalt.append([aktion, name_lied])
        lied_weiter = Button(Neue_Textmanager.Textmanager, text= "servus", border=0)
        inhalt.append(lied_weiter)
    return inhalt


def Position_präsi(factor):
    for pos,i in enumerate(alle_inhalt):
        text_size = min( int(i[0].winfo_height()/3*factor), int(i[0].winfo_width()/8*factor))
        i[0].config(font=('Helvetica', text_size))
        if i[1][0] == " Textwort":
            i[0].place(x= 0, y= pos*i[0].winfo_height()+pos*2,relwidth=0.4*factor, relheight=0.1*factor)
        elif i[1][0] == " Lied":
            i[0].place(x= 0, y= pos*i[0].winfo_height()*2+pos*2,relwidth=0.3*factor, relheight=0.05*factor)
            i[2].place(x= 0, y= pos*(i[0].winfo_height()+1)*2+i[0].winfo_height()+1,relwidth=0.3*factor, relheight=0.05*factor)
            i[2].config(font=('Helvetica', text_size))
            i[3].place(x= (i[0].winfo_width()+1), y= pos*i[0].winfo_height()*2+pos*2,relwidth=0.4*factor, relheight=0.1*factor)
            i[3].config(font=('Helvetica', text_size))
            song = Neue_Textmanager.get_db_connection("SELECT song_name FROM songs WHERE song_number = ? AND book_name = ?", (str(i[1][2]),str(i[1][4])), True)
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
