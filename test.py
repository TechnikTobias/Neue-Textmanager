from tkinter import * 
import traceback
import os

print(os.environ.get("PASS_CAM"))

test = Tk()

import tkinter as tk
from tkinter import ttk

def update_scale_label(value):
    scale_label.config(text=f"{value}%")

def update_button_size(value):
    update_scale_label(value)
    button.config(width=int(base_width * round(float(value)) / 100), )


# Basisgröße des Buttons
base_width = 100
base_height = 50

# ttk Scale für den prozentualen Faktor
scale = ttk.Scale(test, from_=10, to=200, orient=tk.HORIZONTAL, command=update_button_size)
scale.set(100)  # Startwert
scale.pack()

# Label zur Anzeige des aktuellen Wertes des Scales
scale_label = ttk.Label(test, text="100%")
scale_label.pack()

# Button, dessen Größe dynamisch angepasst wird
button = ttk.Button(test, text="Klick mich!", width=base_width, )
button.pack(pady=20)

# Funktion zum Aktualisieren des Labels
update_scale_label(100)



def ResponsiveWidget(widget, *args, **kwargs):
    bindings = {'<Enter>': {'state': 'active'},
                '<Leave>': {'state': 'normal'}}
    w = widget(*args, **kwargs)
    for (k, v) in bindings.items():
        w.bind(k, lambda e, kwarg=v: e.widget.config(**kwarg))
    return w

Button_test = ResponsiveWidget(Button, test)

if 6:
    print("ölichduild")


def settings1():
    Setting1.config(bg="red")

def settings():
    global Setting1
    Settings = Toplevel(test)
    Settings.geometry("400x300")
    Settings.title("Settings")
    Setting1 = Button(Settings, text="Setting", command=settings1)
    Setting1.pack()

def if_abfrage():
    b = False

    if b == False:
        print("b == False")
    if b:
        print("b")
    if not b:
        print("not b")



    print(traceback.format_exc())  # Drucken Sie den Fehlerstapel


def nothing(event=None):
    print("hi")

ko = [
    "lhjksdfvkl",
    "oöifwqalhfa"
]
test.geometry("600x400")
hi = Menu(test)
hi.add_command(label="Hi", command=nothing)
hi.add_command(label="settings", command=settings)
hi.add_checkbutton(label="test", command=if_abfrage)

test.config(menu=hi)
test.bind("<F11>", nothing)

nom = Button(test)
nom.config(text="moin")
nom.place(x=50,y=600)


koll = Scrollbar(test)

koll.pack()

mainloop()