import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import Neue_Textmanager

def create_rounded_rectangle(width, height, radius, color):
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Zeichnen Sie die vier Kreisbögen für die abgerundeten Ecken
    draw.pieslice((0, 0, 2*radius, 2*radius), 180, 270, fill=color)
    draw.pieslice((width-2*radius, 0, width-1, 2*radius), 270, 360, fill=color)
    draw.pieslice((width-2*radius, height-2*radius, width-1, height), 0, 90, fill=color)
    draw.pieslice((0, height-2*radius, 2*radius, height), 90, 180, fill=color)
    
    # Zeichnen Sie die vier Rechtecke, die die abgerundeten Ecken verbinden
    draw.rectangle((radius, 0, width-radius, height), fill=color)
    draw.rectangle((0, radius, width, height-radius), fill=color)
    
    return image

class Switch(ttk.Frame):
    def __init__(self, parent, text="", text_on="ON", text_off="OFF", command=None, text_on_pos=(45, 12), text_off_pos=(15, 12),
                 oval_pos_on=(37, 2, 58, 23), oval_pos_off=(2, 2, 23, 23), Skalierung=1, state=False, speicher_db=None,
                 switch_shape="oval", style="Switch.TFrame", *args, **kwargs):
        super().__init__(parent, style=style, *args, **kwargs)

        self.text_on_str = text_on
        self.text_off_str = text_off
        self.Skalierung = Skalierung

        self.text_on_pos = self.skalieren(text_on_pos, sklaierung=Skalierung)
        self.text_off_pos = self.skalieren(text_off_pos, sklaierung=Skalierung)
        self.oval_pos_on = self.skalieren(oval_pos_on, sklaierung=Skalierung)
        self.oval_pos_off = self.skalieren(oval_pos_off, sklaierung=Skalierung)
        self.switch_shape = switch_shape
        self.speicher_ort = speicher_db
        self.command = command
        self.var = tk.BooleanVar(value=state)

        self.style = ttk.Style()
        self.style.configure(style)

        self.bg_image = ImageTk.PhotoImage(create_rounded_rectangle(self.skalieren(60, sklaierung=Skalierung), self.skalieren(25, sklaierung=Skalierung), self.skalieren(12, sklaierung=Skalierung), self.style.lookup(style, "background", ("",))))

        self.canvas = tk.Canvas(self, width=self.skalieren(60, sklaierung=Skalierung), height=self.skalieren(25, sklaierung=Skalierung), bd=0, highlightthickness=0)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        self.canvas.pack()

        self.on_color = self.style.lookup(style, "onbackground", ("pressed", "focus"))
        self.off_color = self.style.lookup(style, "offbackground")
        self.mid_color = self.style.lookup(style, "zwischen_background")
        self.text_color = self.style.lookup(style, "foreground")
        self.background_color = self.style.lookup(style, "background")

        # Initiales Erstellen des Texts mit einer festen Größe
        self.text_on = self.canvas.create_text(*self.text_on_pos, text=self.text_on_str, anchor=tk.CENTER, state='hidden', fill=self.text_color, font=("Arial", self.skalieren(12, sklaierung=Skalierung)))
        self.text_off = self.canvas.create_text(*self.text_off_pos, text=self.text_off_str, anchor=tk.CENTER, fill=self.text_color, font=("Arial", self.skalieren(12, sklaierung=Skalierung)))
        
        if state:
            if self.switch_shape == "oval":
                self.oval = self.canvas.create_oval(*self.oval_pos_off, fill=self.on_color, outline="")
            elif self.switch_shape == "rectangle":
                self.oval = self.canvas.create_rectangle(*self.oval_pos_off, fill=self.on_color, outline="")
        else:
            if self.switch_shape == "oval":
                self.oval = self.canvas.create_oval(*self.oval_pos_on, fill=self.off_color, outline="")
            elif self.switch_shape == "rectangle":
                self.oval = self.canvas.create_rectangle(*self.oval_pos_on, fill=self.off_color, outline="")

        self.canvas.bind("<Button-1>", self.toggle)
        self.update_text_visibility()

    def skalieren(self, input, sklaierung):
        if isinstance(input, (list, tuple)):
            return type(input)(round(i * sklaierung) for i in input)
        else:
            return round(input * sklaierung)

    def update_scale(self):
        font_size = int(12 * self.Skalierung)
        self.canvas.itemconfig(self.text_on, font=("Arial", font_size))
        self.canvas.itemconfig(self.text_off, font=("Arial", font_size))

    def toggle(self, event=None):
        if self.var.get():
            self.animate(False)
        else:
            self.animate(True)
        self.var.set(not self.var.get())
        if self.command:
            self.command(self.var.get())
        Neue_Textmanager.db_connection_info_write("UPDATE Einstellungen SET supjekt = ? WHERE name = ?", (str(self.var.get()),self.speicher_ort))

    def animate(self, state):
        steps = 30
        mid_step = steps // 2
        if state:
            for i in range(steps):
                self.after(i * 20, self.move_oval, self.oval_pos_on, self.oval_pos_off, steps, i)
                self.after(i * 20, self.move_text, self.text_off_pos, self.text_on_pos, steps, i, True)
            self.fade_color(self.off_color, self.mid_color, self.on_color, steps, function_übergabe=self.update_color, übergabe_item=self.oval)
        else:
            for i in range(steps):
                self.after(i * 20, self.move_oval, self.oval_pos_off, self.oval_pos_on, steps, i)
                self.after(i * 20, self.move_text, self.text_on_pos, self.text_off_pos, steps, i, False)
            self.fade_color(self.on_color, self.mid_color, self.off_color, steps, function_übergabe=self.update_color, übergabe_item=self.oval)

    def move_oval(self, start_coords, end_coords, steps, step):
        new_coords = [
            start_coords[i] + (end_coords[i] - start_coords[i]) * step // steps
            for i in range(4)
        ]
        self.canvas.coords(self.oval, new_coords)

    def move_text(self, start_coords, end_coords, steps, step, state):
        if step == 16:
            self.fade_color(self.background_color, self.background_color, self.text_color, 20, function_übergabe=self.update_color, übergabe_item=self.text_on if state else self.text_off)
        if step >= 16:
            self.canvas.itemconfig(self.text_off if state else self.text_on, state='hidden')
            self.canvas.itemconfig(self.text_on if state else self.text_off, state='normal')
        elif step >= 15:
            self.canvas.itemconfig(self.text_off if state else self.text_on, state='hidden')
            self.canvas.itemconfig(self.text_on if state else self.text_off, state='hidden')
        elif step >= 0:
            self.canvas.itemconfig(self.text_off if state else self.text_on, state='normal')
            self.canvas.itemconfig(self.text_on if state else self.text_off, state='hidden')
        if step == 0:
            self.fade_color(self.text_color, self.background_color, self.background_color, 20, function_übergabe=self.update_color, übergabe_item=self.text_on if not state else self.text_off)

        new_coords = [
            start_coords[i] + (end_coords[i] - start_coords[i]) * step // steps
            for i in range(2)
        ]
        self.canvas.coords(self.text_off, new_coords)
        self.canvas.coords(self.text_on, new_coords)

    def fade_color(self, start_color, mid_color, end_color, steps, function_übergabe, übergabe_item):
        start_rgb = self.canvas.winfo_rgb(start_color)
        mid_rgb = self.canvas.winfo_rgb(mid_color)
        end_rgb = self.canvas.winfo_rgb(end_color)
        delta1 = [(mid_rgb[i] - start_rgb[i]) / (steps // 2) for i in range(3)]
        delta2 = [(end_rgb[i] - mid_rgb[i]) / (steps // 2) for i in range(3)]

        for step in range(steps + 1):
            if step <= steps // 2:
                new_color = "#%02x%02x%02x" % (
                    int(start_rgb[0] / 256 + delta1[0] / 256 * step),
                    int(start_rgb[1] / 256 + delta1[1] / 256 * step),
                    int(start_rgb[2] / 256 + delta1[2] / 256 * step),
                )
            else:
                new_color = "#%02x%02x%02x" % (
                    int(mid_rgb[0] / 256 + delta2[0] / 256 * (step - steps // 2)),
                    int(mid_rgb[1] / 256 + delta2[1] / 256 * (step - steps // 2)),
                    int(mid_rgb[2] / 256 + delta2[2] / 256 * (step - steps // 2)),
                )
            self.after(step * 20, function_übergabe, new_color, übergabe_item)

    def update_color(self, color, update_item):
        try:
            self.canvas.itemconfig(update_item, fill=color)
        except tk.TclError as e:
            print(f"Error updating color: {e}")

    def update_text_visibility(self):
        if self.var.get():
            self.canvas.itemconfig(self.text_on, state='normal')
            self.canvas.itemconfig(self.text_off, state='hidden')
        else:
            self.canvas.itemconfig(self.text_on, state='hidden')
            self.canvas.itemconfig(self.text_off, state='normal')

# Beispiel für die Verwendung der Switch-Klasse in einem Tkinter-Fenster
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Switch Example")
        self.geometry("700x500")

        # Erzeugung und Platzierung eines Switch-Widgets
        self.style = ttk.Style(self)
        self.style.configure("Switch.TFrame", background="#009ba6", onbackground="#3eee21", offbackground="#e01b24", foreground="#000000", zwischen_background="#8f8523")

        self.switch = Switch(self, text="Option", command=self.switch_command, style="Switch.TFrame", Skalierung=20, speicher_db="liedvorschau")
        self.switch.pack(pady=20)

    def switch_command(self, state):
        pass
        #print(f"Switch state: {'ON' if state else 'OFF'}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
