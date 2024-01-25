import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def add_command():
    command_name = entry.get()
    selected_command = command_combobox.get()

    if command_name and selected_command:
        commands_list.insert(tk.END, f"Name: {command_name}, Befehl: {selected_command}")
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
    if event.keysym == 'Up':
        move_up()
    elif event.keysym == 'Down':
        move_down()


def execute_command():
    selected_index = commands_list.curselection()
    if selected_index:
        selected_index = selected_index[0]
        command = commands_list.get(selected_index)
        print("Executing command:", command)
        # Hier können Sie den Befehl ausführen oder andere Aktionen durchführen

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


def switch_to_navigation():
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

commands = ["Befehl 1", "Befehl 2", "Befehl 3"]  # Hier können Sie Ihre Befehle hinzufügen
command_combobox = ttk.Combobox(frame, values=commands)
command_combobox.pack(fill='x')

add_button = tk.Button(frame, text="Hinzufügen", command=add_command)
add_button.pack(fill='x')

delete_button = tk.Button(frame, text="Löschen", command=delete_command)
delete_button.pack(fill='x')

commands_list = tk.Listbox(frame, selectmode=tk.SINGLE)
commands_list.pack(fill='both', expand=True)

commands_list.insert(tk.END, f"Name: Eingslied, Befehl: Befehl 1")
commands_list.insert(tk.END, f"Name: Textwort, Befehl: Befehl 1")
commands_list.insert(tk.END, f"Name: Amstwechsel, Befehl: Befehl 3")
commands_list.insert(tk.END, f"Name: Bußlied <,Befehl: Befehl 1")
commands_list.insert(tk.END, f"Name: Abendmahlslied, Befehl: Befehl 2")
commands_list.insert(tk.END, f"Name: Schlusslied, Befehl: Befehl 1")

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
