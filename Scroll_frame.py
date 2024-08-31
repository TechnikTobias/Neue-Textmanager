import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        # Erstellen des Canvas-Objekts
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.config(style="TLabel")

        # Hinzufügen der vertikalen Scrollbar
        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.pack(side="bottom", fill="x")


        # Hinzufügen der horizontalen Scrollbar

        # Verknüpfen der Scrollbars mit dem Canvas
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Erstellen eines Frames im Canvas
        self.frame = ttk.Frame(self.canvas, style="TButton")
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Konfigurieren des Canvas, um seine Größe anzupassen
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        # Maus-Scrollrad konfigurieren
        self.frame.bind("<Enter>", lambda e: self._bind_mousewheel(self.canvas))
        self.frame.bind("<Leave>", lambda e: self._unbind_mousewheel(self.canvas))

    def frame_id_def(self, width, height):
        self.canvas.itemconfig(self.frame_id, width=width, height= height)

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



    

