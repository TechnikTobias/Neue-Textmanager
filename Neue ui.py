import sys
from PySide6 import QtWidgets
from PySide6 import QtGui

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Meine kleine UI")

        # Erstellen einer Label-Komponente
        label = QtWidgets.QLabel("Hallo Welt!")

        # Erstellen einer Button-Komponente
        button = QtWidgets.QPushButton("Klick mich!")

        insert = QtWidgets.QPlainTextEdit()
        top_line_edit = QtWidgets.QLineEdit(parent=self)
        button_set = QtGui.QAction(self,"&Hallo")
        button_set.setCheckable(True)
        toolbar = QtWidgets.QToolBar()

        input = QtWidgets.QMenuBar()
        # Anordnen der Komponenten im Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        layout.addWidget(insert)
        layout.addWidget(top_line_edit)
        
        menü = QtWidgets.QMenuBar()
        self.setLayout(layout)
        file_menu = menü.addMenu("&Fail")
        file_menu.addAction(button_set)
        # Setzen des Layouts für die Komponente

        # Anhängen eines Slots an den Button
        button.clicked.connect(self.handleButtonClick)

    def handleButtonClick(self):
        # Ausgabe einer Meldung in der Konsole
        print("Der Button wurde geklickt!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    my_window = MyWindow()
    my_window.show()

    sys.exit(app.exec())
