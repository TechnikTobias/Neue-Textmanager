import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors

# Monitor Klasse zur Darstellung der Bildschirme
class Monitor:
    def __init__(self, name, width, height, x, y):
        self.name = name
        self.width = width
        self.height = height
        self.x = x
        self.y = y

class ScreenSelectionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bildschirm Auswahl")
        self.geometry("1000x800")
        self.selected_screen = None
        
        # Echte Bildschirme erkennen
        self.screens = self.detect_screens()
        
        # Virtuelle Bildschirme Liste initialisieren
        self.virtual_screens = []
        
        # UI Komponenten erstellen
        self.create_widgets()
        
    def detect_screens(self):
        monitors = get_monitors()
        screens = []
        for i, monitor in enumerate(monitors):
            screens.append(Monitor(f"Echter Bildschirm {i+1}", monitor.width, monitor.height, monitor.x, monitor.y))
        return screens
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=1000, height=700, bg="white")
        self.canvas.pack(pady=20)
        
        self.status_label = ttk.Label(self, text="Kein zweiter Bildschirm ausgewählt")
        self.status_label.place(relheight=0.05, relwidth=1, relx=0, rely=0.75)

        self.recognize_button = ttk.Button(self, text="Erkennen", command=self.recognize_screens)
        self.recognize_button.place(relheight=0.05, relwidth=0.5, relx=0, rely=0.85)
        
        self.update_button = ttk.Button(self, text="Aktualisieren", command=self.update_screens)
        self.update_button.place(relheight=0.05, relwidth=0.5, relx=0.5, rely=0.85)

        self.screen_position_label = ttk.Label(self, text="")
        self.screen_position_label.place(relheight=0.05, relwidth=1, relx=0, rely=0.9)

        self.update_screen_display()
        self.update_screen_position()

    def update_screen_display(self):
        self.canvas.delete("all")
        all_screens = self.screens + self.virtual_screens

        if not all_screens:
            return

        min_x = min(screen.x for screen in all_screens)
        min_y = min(screen.y for screen in all_screens)
        
        # Verschiebung berechnen, um negative Positionen zu vermeiden
        offset_x = -min_x if min_x < 0 else 0
        offset_y = -min_y if min_y < 0 else 0
        
        max_width = max(screen.x + screen.width for screen in all_screens) + offset_x
        max_height = max(screen.y + screen.height for screen in all_screens) + offset_y
        scale_factor = min((900 / max_width), (600 / max_height))
        
        self.screen_rects = []
        
        for i, screen in enumerate(all_screens):
            x1 = (screen.x + offset_x) * scale_factor
            y1 = (screen.y + offset_y) * scale_factor
            x2 = x1 + screen.width * scale_factor
            y2 = y1 + screen.height * scale_factor
            
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="black")
            self.screen_rects.append(rect)
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(i + 1), font=("Arial", 24))
            self.canvas.create_text((x1 + x2) / 2, y1 - 10, text=screen.name)
            self.canvas.tag_bind(rect, '<Button-1>', lambda event, idx=i: self.select_screen(idx, self.canvas))

    def select_screen(self, index, canvas):
        if self.selected_screen is not None:
            canvas.itemconfig(self.screen_rects[self.selected_screen], fill="lightgray")
        
        self.selected_screen = index
        canvas.itemconfig(self.screen_rects[self.selected_screen], fill="lightblue")
        self.status_label.config(text=f"Der zweite Bildschirm ist jetzt: {self.screens[self.selected_screen].name}")
        
        # Ausgabe der Bildschirmgröße und Vollbildmodus-Information
        screen = self.screens[self.selected_screen]
        print(f"Ausgewählter Bildschirm: {screen.name}")
        print(f"Breite: {screen.width}, Höhe: {screen.height}")
        print(f"Um diesen Bildschirm im Vollbildmodus zu platzieren, verwenden Sie die folgenden Parameter:")
        print(f"x: {screen.x}, y: {screen.y}, Breite: {screen.width}, Höhe: {screen.height}")

    def recognize_screens(self):
        for i, screen in enumerate(self.screens):
            self.show_screen_number(i, screen)

    def show_screen_number(self, index, screen):
        recognize_window = tk.Toplevel(self)
        recognize_window.overrideredirect(1)
        recognize_window.geometry(f"100x70+{screen.x + screen.width - 130}+{screen.y + screen.height - 130}")
        label = tk.Label(recognize_window, text=f"{index + 1}", font=("Arial", 50))
        label.pack()
        
        # Fenster 5 Sekunden lang anzeigen und dann zerstören
        self.after(5000, recognize_window.destroy)
    
    def update_screens(self):
        self.screens = self.detect_screens()
        self.update_screen_display()
        self.update_screen_position()

    def add_virtual_screen(self, width=1920, height=1080, x=None, y=None):
        if x is None:
            x = 1920 * len(self.virtual_screens)
        if y is None:
            y = 0
        new_screen_id = len(self.screens) + len(self.virtual_screens) + 1
        new_virtual_screen = Monitor(f"Virtueller Bildschirm {new_screen_id}", width, height, x, y)
        self.virtual_screens.append(new_virtual_screen)
        self.update_screen_display()

    def remove_virtual_screen(self):
        if self.virtual_screens:
            self.virtual_screens.pop()
            self.update_screen_display()

    def update_screen_position(self):
        # Fensterposition und -größe abrufen
        self.update_idletasks()
        window_geometry = self.geometry()
        window_width, window_height, window_x, window_y = map(int, window_geometry.replace('x', '+').split('+'))
        
        for screen in self.screens:
            if screen.x <= window_x < screen.x + screen.width and screen.y <= window_y < screen.y + screen.height:
                self.screen_position_label.config(text=f"Das Programm befindet sich auf: {screen.name}")
                return
        
        for screen in self.virtual_screens:
            if screen.x <= window_x < screen.x + screen.width and screen.y <= window_y < screen.y + screen.height:
                self.screen_position_label.config(text=f"Das Programm befindet sich auf: {screen.name}")
                return

        self.screen_position_label.config(text="Das Programm befindet sich außerhalb bekannter Bildschirme")


# Hauptprogramm starten
if __name__ == "__main__":
    app = ScreenSelectionApp()
    
    # Virtuelle Bildschirme per Code hinzufügen
    app.add_virtual_screen(width=1920, height=1080, x=1920, y=0)  # Fügt einen weiteren virtuellen Bildschirm mit benutzerdefinierten Parametern hinzu

    app.mainloop()
