import tkinter as tk


class AblaufSteuerung:
    def __init__(self, root):
        self.root = root
        self.bausteine = []
        self.ablauf = []
        self.current_step = 0

        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()

        self.root.bind("<Left>", self.previous_step)
        self.root.bind("<Right>", self.next_step)

        self.execute_button = tk.Button(root, text="Befehl ausführen", command=self.execute_current_step)
        self.execute_button.pack()

        self.animation_speed = 1000  # Geschwindigkeit der Balken-Animation in Millisekunden
        self.animation_balken = None

        self.drag_data = {'x': 0, 'y': 0, 'item': None}

        self.create_text_bausteine()  # Erzeugt die Textbausteine beim Programmstart

        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

        # Erzeugt den Balken
        self.animation_balken = self.canvas.create_rectangle(750, 50, 800, 400, fill='green', outline='green')

    def create_text_bausteine(self):
        bausteine = ["Kamera", "Lied", "Einblendung"]
        x = 50
        y = 50
        for text in bausteine:
            box = self.create_box(x, y, text)
            self.bausteine.append(box)
            x += 150

    def create_box(self, x, y, text):
        box = self.canvas.create_rectangle(x, y, x + 100, y + 50, fill='lightblue')
        label = self.canvas.create_text(x + 50, y + 25, text=text)
        self.canvas.tag_bind(box, "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind(box, "<B1-Motion>", self.on_drag_motion)
        self.canvas.tag_bind(box, "<ButtonRelease-1>", self.on_drag_release)
        return (box, label)

    def on_drag_start(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self.drag_data['item'] = item[0]
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y

    def on_drag_motion(self, event):
        if self.drag_data['item']:
            x, y = event.x, event.y
            self.canvas.move(self.drag_data['item'], x - self.drag_data['x'], y - self.drag_data['y'])
            self.drag_data['x'] = x
            self.drag_data['y'] = y

    def on_drag_release(self, event):
        if self.drag_data['item']:
            item_x, item_y, _, _ = self.canvas.coords(self.drag_data['item'])
            if 750 < item_x < 800:  # Überprüfen, ob der Kasten im Balken ist
                label = self.canvas.itemcget(self.drag_data['item'], "text")
                self.ablauf.append(label)
                self.canvas.delete(self.drag_data['item'])
            self.drag_data['item'] = None

    def on_drop(self, event):
        for box, label in self.bausteine:
            item_x, item_y, _, _ = self.canvas.coords(box)
            if item_x < event.x < item_x + 100 and item_y < event.y < item_y + 50:
                self.ablauf.append(self.canvas.itemcget(label, "text"))
                break

    def previous_step(self, event):
        if self.current_step > 0:
            self.current_step -= 1

    def next_step(self, event):
        if self.current_step < len(self.ablauf):
            self.current_step += 1

    def execute_current_step(self):
        if 0 <= self.current_step < len(self.ablauf):
            command = self.ablauf[self.current_step]
            print(f"Ausführen von Befehl: {command}")

    def start_balken_animation(self):
        self.stop_balken_animation()
        self.animate_balken()

    def animate_balken(self):
        if self.current_step < len(self.ablauf):
            self.canvas.move(self.animation_balken, 0, 10)  # Bewegung um 10 Pixel nach unten
            self.root.after(self.animation_speed, self.animate_balken)
        else:
            self.stop_balken_animation()
            self.current_step = 0  # Zurücksetzen auf den Anfang

    def stop_balken_animation(self):
        if self.animation_balken:
            self.canvas.delete(self.animation_balken)

if __name__ == "__main__":
    root = tk.Tk()
    app = AblaufSteuerung(root)
    root.mainloop()
