import sys
from PySide2 import QtWidgets

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Meine kleine UI")

        # Erstellen einer Label-Komponente
        label = QtWidgets.QLabel("Hallo Welt!")

        # Erstellen einer Button-Komponente
        button = QtWidgets.QPushButton("Klick mich!")

        insert = QtWidgets.QPlainTextEdit()
        input = QtWidgets.QMenuBar()
        menü = QtWidgets.QStyleOptionMenuItem()

        # Anordnen der Komponenten im Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        layout.addWidget(insert)
        layout.addWidget(input)
        input.addMenu("menü")

        # Setzen des Layouts für die Komponente
        self.setLayout(layout)

        # Anhängen eines Slots an den Button
        button.clicked.connect(self.handleButtonClick)

    def handleButtonClick(self):
        # Ausgabe einer Meldung in der Konsole
        print("Der Button wurde geklickt!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    my_window = MyWindow()
    my_window.show()

    sys.exit(app.exec_())
