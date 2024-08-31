import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Canvas erstellen, Rand und Highlighting entfernen
        canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.config(style="")

        # Scrollbars erstellen
        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)

        # Innerer Frame für den scrollbaren Bereich
        self.scrollable_frame = ttk.Frame(canvas, padding=(0, 0), style="TLabel")

        # Bindung, um die Größe des scrollbaren Bereichs zu ändern
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Platzierung des inneren Frames in der Canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Scrollbars konfigurieren
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set, bg="black")

        # Platzierung der Scrollbars und der Canvas
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        # Maus-Scrollen ermöglichen
        self.scrollable_frame.bind("<Enter>", lambda e: self._bind_mousewheel(canvas))
        self.scrollable_frame.bind("<Leave>", lambda e: self._unbind_mousewheel(canvas))

    def _bind_mousewheel(self, canvas):
        canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, canvas))
        canvas.bind_all("<Shift-MouseWheel>", lambda event: self._on_shift_mousewheel(event, canvas))

    def _unbind_mousewheel(self, canvas):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Shift-MouseWheel>")

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_shift_mousewheel(self, event, canvas):
        canvas.xview_scroll(-1 * (event.delta // 120), "units")

class TextmanagerAPP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Textmanager")
        self.geometry("800x600")
        self.config(bg="black")
        style = ttk.Style()
        style.configure('TLabel', relief='flat', borderwidth=0, font=('Helvetica', 10), background="black", foreground="white")


        # Statische Inhalte außerhalb des scrollbaren Bereichs
        self.menu_info_main = ttk.Label(self, style='TLabel')
        self.menu_info_main.pack(pady=10)
        self.Menu_generator()

        def callback(event):
            print("Selected:", combo.get())

        combo = ttk.Combobox(self, values=["Option 1", "Option 2", "Option 3"])
        combo.current(0)  # Set default value
        combo.bind("<<ComboboxSelected>>", callback)
        combo.pack(pady=20)


        # Erstelle den scrollbaren Frame
        scrollable_frame = ScrollableFrame(self)
        scrollable_frame.pack(fill="both", expand=True)
        # Beispiel-Widgets hinzufügen
        for i in range(20):
            # Scrollbare Inhalte innerhalb des Canvas
            ttk.Label(scrollable_frame.scrollable_frame, text=f"Label {i}", style="TLabel").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            ttk.Entry(scrollable_frame.scrollable_frame, style="TLabel").grid(row=i, column=1, padx=5, pady=2, sticky="w")
            ttk.Button(scrollable_frame.scrollable_frame, text="Button", style="TLabel").grid(row=i, column=2, padx=5, pady=2, sticky="w")
            
            # Labels außerhalb des sichtbaren Bereichs, um das Scrollen zu testen
            ttk.Label(scrollable_frame.scrollable_frame, text=f"Extra Label {i}", style="TLabel").grid(row=i, column=3, padx=(400, 5), pady=2, sticky="w")

    def Menu_generator(self):
        hintergrund_farbe = "black"
        text_farbe = "withe"
        # Hintergrundfarbe und Textfarbe aus der Datenbank holen
        # Erstellen und Konfigurieren der Comboboxes
        self.menu_info_main = ttk.Combobox(self, values=["Einstellungen", "Info"], style='custom.TCombobox')
        self.menu_info_main.current(0)  # Standardwert festlegen
        self.menu_info_main.bind("<<ComboboxSelected>>", )
        # self.menu_info_main.pack(side=tk.LEFT, anchor=tk.NW)

        self.menu_kamera_main = ttk.Combobox(self, values=["Einstellungen", "Position"], style='custom.TCombobox')
        self.menu_kamera_main.current(0)
        self.menu_kamera_main.bind("<<ComboboxSelected>>", )
#
        self.menu_liedkontrolle_main = ttk.Combobox(self, values=["Einstellungen", "Lied Kontrollieren"], style='custom.TCombobox')
        self.menu_liedkontrolle_main.current(0)
        self.menu_liedkontrolle_main.bind("<<ComboboxSelected>>", )
#
        self.menu_help_main = ttk.Combobox(self, values=["Hilfe"], style='custom.TCombobox')
        self.menu_help_main.current(0)
        self.menu_help_main.bind("<<ComboboxSelected>>", )
        # self.menu_help_main.pack(side=tk.LEFT, anchor=tk.NW)
        self.menu_info_main.place(relheight=0.05, relwidth=0.2, relx=0, rely=0)
        self.menu_kamera_main.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0)
        self.menu_liedkontrolle_main.place(relheight=0.05, relwidth=0.2, relx=0.4, rely=0)
        self.menu_help_main.place(relheight=0.05, relwidth=0.2, relx=0.6, rely=0)

if __name__ == "__main__":
    app = TextmanagerAPP()
    app.mainloop()
