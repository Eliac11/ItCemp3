import sys
import os

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Window(QMainWindow):
    def __init__(self, width, height):
        super().__init__()

        self.setWindowTitle("AI Generation Karelia")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(width, height)

        generate = QPushButton("Generate", self)
        generate.move(round(width*0.5-100),round(height*0.5-100))
        generate.resize(200, 100)

        combobox = QComboBox(self)
        combobox.addItem("Realisitic")
        combobox.addItem("Realisitic")
        combobox.addItem("Realisitic")
        combobox.addItem("Realisitic")
        combobox.addItem("Realisitic")

        combobox.move(round(width*0.5-100), round(height*0.5+50))
        combobox.resize(200, 50)

        pixmap = QPixmap(768,1024)
        pixmap.fill(Qt.red)
        label_gen = QLabel(self)
        label_gen.setPixmap(pixmap)
        label_gen.move(round(width*0.57),round(height*0.1))
        label_gen.resize(768,1024)

        canvas = QPixmap(768, 1024)
        canvas.fill(Qt.white)
        label_paint = QLabel(self)
        label_paint.setPixmap(canvas)
        label_paint.move(round(width*0.1),round(height*0.1))
        label_paint.resize(768,1024)




  

app = QApplication(sys.argv)
desktop = QApplication.desktop()

width = round(desktop.width()*0.6)
height = round(desktop.height()*0.6)

print(width, height)
wnd = Window(width, height)

wnd.show()

sys.exit(app.exec_())