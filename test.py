from tkinter import * 
import traceback
import os

print(os.environ.get("PASS_CAM"))




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
test = Tk()
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