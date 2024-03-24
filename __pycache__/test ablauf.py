import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

Liste_der_Befehle = ["Textwort", "Lieder", "Kamera"]

def add_command():
    command_name = entry.get()
    selected_command = command_combobox.get()

    if command_name and selected_command:
        commands_list.insert(tk.END, f"Name: {command_name}, Befehl: {selected_command}")
        entry.delete(0, tk.END)

def move_up():
    selected_index = commands_list.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if selected_index > 0:
            command = commands_list.get(selected_index)
            commands_list.delete(selected_index)
            commands_list.insert(selected_index - 1, command)
            commands_list.select_clear(0, tk.END)
            commands_list.select_set(selected_index - 1)

def move_down():
    selected_index = commands_list.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if selected_index < commands_list.size() - 1:
            command = commands_list.get(selected_index)
            commands_list.delete(selected_index)
            commands_list.insert(selected_index + 1, command)
            commands_list.select_clear(0, tk.END)
            commands_list.select_set(selected_index + 1)

def on_key(event):
    if event.keysym == 'Up':
        move_up()
    elif event.keysym == 'Down':
        move_down()

def execute_command():
    global current_index
    selected_index = current_index
    if selected_index is not None:
        command = commands_list.get(selected_index)
        yes= command.split(",")
        no= yes[1].split(":")
        if no[1] == Liste_der_Befehle[0]:
            print("Befehl 1 wurde ausgeführt")
        elif no[1] == Liste_der_Befehle[1]:
            print("Befehl 2 wurde ausgeführt")
        elif no[1] == Liste_der_Befehle[2]:
            print("Befehl 3 wurde ausgeführt")


def confirm_commands():
    commands = list(commands_list.get(0, tk.END))

    if not commands:
        messagebox.showinfo("Bestätigte Befehle", "Keine Befehle zum Ausführen.")
    else:
        result_window = tk.Toplevel(root)
        result_window.title("Bestätigte Befehle")

        for command in commands:
            result_label = tk.Label(result_window, text=command)
            result_label.pack(fill='x')

        result_window.mainloop()

def navigate_commands(event):
    global current_index
    if event.keysym == 'Up':
        current_index = max(current_index - 1, 0)
    elif event.keysym == 'Down':
        current_index = min(current_index + 1, commands_list.size() - 1)
    elif event.keysym == 'Return':
        execute_command()
    update_display()

def update_display():
    selected_index = current_index
    selected_command = commands_list.get(selected_index)
    display_label.config(text=selected_command)

def inhalt_auslesen():
    for i in range (1, len(commands_list.get(0, tk.END))):
        if (inhalt[i-1][0]) == Liste_der_Befehle[1]:
            print(inhalt[i-1][1].get())
        if (inhalt[i-1][0]) == Liste_der_Befehle[0]:
            print("Textwort")
        if (inhalt[i-1][0]) == Liste_der_Befehle[2]:
            print("Kamera")


def switch_to_navigation():
    global inhalt 
    inhalt = []
    ablaufsteuerung = tk.Toplevel(root)
    ablaufsteuerung.title("Ablaufsteuerung")
    for i in range (1, len(commands_list.get(0, tk.END))):
        aufbau = []
        command = commands_list.get(i)
        command_split = command.split(",")
        comand_split = command_split[0].split(":")
        Befehl = command_split[1].split(":")
        lable_eingabe = tk.LabelFrame(ablaufsteuerung, background="black")
        lable_eingabe.pack()
        lable_name=tk.Label(lable_eingabe, text=comand_split[1])
        lable_name.pack()
        if Befehl[1] == Liste_der_Befehle[1]:
            aufbau.append(Liste_der_Befehle[1])
            liste = tk.StringVar()
            liste.set(Befehl[1])
            checkbutton_list = tk.OptionMenu(lable_eingabe, liste, *Liste_der_Befehle)
            checkbutton_list.pack()
            liednummer_lable=tk.Label(lable_eingabe,text="Liednummer")
            liednummer_lable.pack()
            entry_buch = tk.Entry(lable_eingabe)
            entry_buch.pack()
            tk.Label
            tk.Entry
            aufbau.append(entry_buch)

        elif Befehl[1] == Liste_der_Befehle[0]:
            aufbau.append(Liste_der_Befehle[0])
            lable_kamera = tk.Button(lable_eingabe, text="Textwort")
            lable_kamera.pack()
        elif Befehl[1] == Liste_der_Befehle[2]:
            aufbau.append(Liste_der_Befehle[2])
            lable_ka = tk.Label(lable_eingabe, text="Kamera")
            lable_ka.pack()
        button_abgabe = tk.Button(ablaufsteuerung,text="Ausgabe", command=inhalt_auslesen)
        button_abgabe.pack()
        inhalt.append(aufbau)

    global current_index
    current_index = 0
    update_display()
    root.unbind("<Key>")
    root.bind("<Key>", navigate_commands)
    switch_button.config(text="Zurück zu Bestätigen", command=switch_to_confirm)

def switch_to_confirm():
    root.unbind("<Key>")
    root.bind("<Key>", on_key)
    switch_button.config(text="Zurück zur Navigation", command=switch_to_navigation)

current_index = 0

root = tk.Tk()
root.title("Befehlssteuerung")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry_label = tk.Label(frame, text="Name eingeben:")
entry_label.pack(fill='x')

entry = tk.Entry(frame)
entry.pack(fill='x')

command_label = tk.Label(frame, text="Befehl auswählen:")
command_label.pack(fill='x')

command_combobox = ttk.Combobox(frame, values=Liste_der_Befehle)
command_combobox.pack(fill='x')

add_button = tk.Button(frame, text="Hinzufügen", command=add_command)
add_button.pack(fill='x')

commands_list = tk.Listbox(frame, selectmode=tk.SINGLE, width=35)
commands_list.pack(fill='both', expand=True)

commands_list.insert(tk.END, f"Name: Eingslied, Befehl:{Liste_der_Befehle[1]}")
commands_list.insert(tk.END, f"Name: Textwort, Befehl:{Liste_der_Befehle[1]}")
commands_list.insert(tk.END, f"Name: Amstwechsel, Befehl:{Liste_der_Befehle[2]}")
commands_list.insert(tk.END, f"Name: Bußlied,Befehl:{Liste_der_Befehle[0]}")
commands_list.insert(tk.END, f"Name: Abendmahlslied, Befehl:{Liste_der_Befehle[1]}")
commands_list.insert(tk.END, f"Name: Schlusslied, Befehl:{Liste_der_Befehle[1]}")

up_button = tk.Button(frame, text="Nach oben", command=move_up)
up_button.pack(fill='x')

down_button = tk.Button(frame, text="Nach unten", command=move_down)
down_button.pack(fill='x')

switch_button = tk.Button(root, text="Zur Navigation wechseln", command=switch_to_navigation)
switch_button.pack(pady=10)

display_label = tk.Label(root, text="")
display_label.pack()

root.bind("<Key>", on_key)

root.mainloop()
