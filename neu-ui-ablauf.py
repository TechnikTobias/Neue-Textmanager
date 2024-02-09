from PySide6 import QtWidgets as QTwg
import sys 

class MyWindow(QTwg.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mein Ablauf")

        label_text_inputline = QTwg.QLabel("Hallo Welt!")
        top_line_edit = QTwg.QLineEdit(parent=self)
        label_text_menue = QTwg.QLabel("Hallo Welt!")
        dropmenü = QTwg.QComboBox()
        dropmenü.addItems(["Textwort","Lieder","Kamera"])

