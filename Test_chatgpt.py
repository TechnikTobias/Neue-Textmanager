import tkinter as tk
from tkinter import ttk

class TextmanagerAPP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Textmanager")
        self.geometry("800x600")

        # Canvas für Scrollbars
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Vertikale Scrollbar
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")

        # Horizontale Scrollbar
        self.h_scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")

        # Verknüpfen der Scrollbars mit dem Canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        # Frame im Canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Frame-Konfiguration
        self.frame.bind("<Configure>", self.on_frame_configure)

        # Widgets registrieren
        self.register_widgets()

        # Slider und Button
        self.slider = ttk.Scale(self, from_=1, to=20, orient="horizontal")
        self.slider.pack(pady=20)
        self_button = tk.Button(self, text="aktualisieren", command=self.update_widget_positions)
        self_button.pack()

        

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def register_widgets(self):
        # Beispiel-Widgets hinzufügen
        self.widgets = []
        for i in range(20):
            label = tk.Label(self.frame, text=f"Widget {i+1}")
            label.grid(row=i, column=0, padx=10, pady=10)
            self.widgets.append(label)

    def update_widget_positions(self):
        scale_factor = self.slider.get()
        print(f"Skalierungsfaktor: {scale_factor}")
        for widget in self.widgets:
            # Schriftgröße skalieren
            font_size = int(10 * scale_factor)
            widget.config(font=("Arial", font_size))

            # Padding skalieren
            widget.grid_configure(padx=10 * scale_factor, pady=10 * scale_factor)

    # Beispiel einer Methode zur asynchronen Datenbankabfrage
    def db_connection_info_get_async(self, input_db, input_db_variabel, singel_or_multi, callback):
        def task():
            result = self.db_connection_info_get(input_db, input_db_variabel, singel_or_multi)
            self.after(0, callback, result)

        import threading
        threading.Thread(target=task).start()

    def db_connection_info_get(self, input_db, input_db_variabel, singel_or_multi):
        # Beispielhafte Implementierung einer Datenbankabfrage
        return "Mocked DB Result"

    def on_db_result(self, result):
        # Callback-Funktion zur Verarbeitung der Datenbankergebnisse
        print(f"Datenbankergebnis: {result}")

app = TextmanagerAPP()
app.mainloop()
