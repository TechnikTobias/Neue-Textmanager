import tkinter as tk
import sqlite3
import os

import Neue_Textmanager
#neu überarbeiten und verschönern

Speicherort = os.path.dirname(os.path.abspath(__file__))

def add_command():
    command_name = entry.get()
    commands_list.insert(tk.END, f"Name: {command_name}, Befehl: {clicked.get()}")
    entry.delete(0, tk.END)

def delete_command():
    selected_index = commands_list.curselection()
    if selected_index:
        selected_index = selected_index[0]
        commands_list.delete(selected_index)

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
    if switch_button.cget("text"):
        if event.keysym == 'Up':
            move_up()
        elif event.keysym == 'Down':
            move_down()
        elif event.keysym == 'Return':
            execute_command()
        elif event.keysym == 'Left':
            delete_command()

def bestätigen():
    db_filename = "Lieder_Datenbank.db"
    db_path = os.path.join(os.path.dirname(__file__), db_filename)
    conn = sqlite3.connect(db_path)            
    c = conn.cursor()
    c.execute('DELETE FROM Ablaufaufbau')
    for pos,comnd in enumerate(commands_list.get(0, tk.END)):
        final =[]
        halbe_daten = comnd.split(",")
        for daten in halbe_daten:
            daten_to_remove_space = daten.split(":")[1]
            daten_to_remove_space.replace(" ", "")
            final.append(daten_to_remove_space.replace(" ", ""))
            

        c.execute('''INSERT INTO Ablaufaufbau (Reihenfolge, Name, Comand) VALUES (?, ?, ?)''', (pos, final[0], final[1]))
        conn.commit()
    conn.close()


def execute_command():
    selected_index = commands_list.curselection()
    if selected_index:
        selected_index = selected_index[0]
        command = commands_list.get(selected_index)

def switch_to_navigation():
    update_display()
    root.bind("<Key>", on_key)
    switch_button.config(text="Zurück zur Bestätigung", command=switch_to_confirm)

def switch_to_confirm():
    root.unbind("<Key>")
    switch_button.config(text="Zurück zur Navigation", command=switch_to_navigation)

def update_display():
    selected_index = commands_list.curselection()
    if selected_index:
        selected_index = selected_index[0]
        selected_command = commands_list.get(selected_index)
        display_label.config(text=selected_command)

root = tk.Tk()
root.title("Befehlssteuerung")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry_label = tk.Label(frame, text="Name eingeben:")
entry_label.pack(fill='x')

entry = tk.Entry(frame)
entry.pack(fill='x')

befehle = ["Kamera", "Textwort", "Lied"]

clicked = tk.StringVar()
clicked.set(befehle[0])
opt = tk.OptionMenu(frame, clicked, *befehle)
opt.config(font=('Helvetica', 12), fg="black", bg="white")
opt.pack()

button_bestätigen = tk.Button(frame, text="Bestätigen", command=add_command)
button_bestätigen.pack()

command_label = tk.Label(frame, text="Befehl auswählen:")
command_label.pack(fill='x')

commands_list = tk.Listbox(frame, selectmode=tk.SINGLE, width=40)
commands_list.pack(fill='both', expand=True)

entries = Neue_Textmanager.fetch_all_program_info("Ablaufaufbau", "Reihenfolge")
for entry in entries:
    commands_list.insert(tk.END, f"Name: {entry[2]}, Befehl: {entry[1]}")
    


up_button = tk.Button(frame, text="Nach oben", command=move_up)
up_button.pack(fill='x')

down_button = tk.Button(frame, text="Nach unten", command=move_down)
down_button.pack(fill='x')

switch_button = tk.Button(root, text="Zurück zur Navigation", command=bestätigen)
switch_button.pack(pady=10)

display_label = tk.Label(root, text="")
display_label.pack()

root.bind("<Key>", on_key)

root.mainloop()
