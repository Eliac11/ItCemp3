import sys
import os

from moduleReplicateApi import ReplicateInterface

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
        generate.clicked.connect(self.save_paint)

        clear = QPushButton("Clear", self)
        clear.move(round(width*0.5-100),round(height*0.5-250))
        clear.resize(200, 100)
        clear.clicked.connect(self.clear_paint)

        combobox = QComboBox(self)
        combobox.addItem("Realism")
        combobox.addItem("Cubism")
        combobox.addItem("Oil")
        combobox.addItem("Watercolor")
        combobox.addItem("Color pencil")
        combobox.addItem("Black pencil")
        combobox.addItem("Charcoal")
        combobox.addItem("Kashtanov")
        combobox.addItem("Ivanenko")
        combobox.addItem("Embroidery")
        combobox.addItem("Anime")

        combobox.move(round(width*0.5-100), round(height*0.5+50))
        combobox.resize(200, 50)

        pixmap = QPixmap(768,1024)
        pixmap.fill(Qt.red)
        self.label_gen = QLabel(self)
        self.label_gen.setPixmap(pixmap)
        self.label_gen.move(round(width*0.57),round(height*0.1))
        self.label_gen.resize(768,1024)

        self.canvas = QPixmap(QSize(768, 1024))
        self.canvas.fill(Qt.white)
        self.label_paint = QLabel(self)
        self.label_paint.move(round(width*0.1),round(height*0.1))
        self.label_paint.setPixmap(self.canvas)
        self.label_paint.resize(768,1024)

        self.last_x, self.last_y = None, None

    def mouseMoveEvent(self, e):
        mouse_x = e.x()-round(width*0.1)
        mouse_y = e.y()-round(height*0.1)
        if self.last_x is None:
            self.last_x = mouse_x
            self.last_y = mouse_y
            return
            
        painter = QPainter(self.label_paint.pixmap())
        p = painter.pen()
        p.setWidth(16)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, mouse_x, mouse_y)
        painter.drawPoint
        painter.end()
        self.update()

        self.last_x = mouse_x
        self.last_y =  mouse_y

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
    
    def save_paint(self):
        self.label_paint.move(0,0)
        self.render(self.canvas)
        self.canvas.save("temp.png", "PNG")
        self.label_paint.move(round(width*0.1),round(height*0.1))
        
        self.genImage()

    def genImage(self):
        gen = ReplicateInterface("r8_7LQDYseC2kXuZYlhqpIEp3Kt7V4UXLH3M0Lxp")
        newimg = gen.imageInpaiting("realistic, forest, Russia", "temp.png")
        gen_paint = QPixmap(newimg)
        gen_paint = gen_paint.scaled(768,1024)
        self.label_gen.setPixmap(gen_paint)

    def clear_paint(self):
        painter = QPainter(self.label_paint.pixmap())
        p = painter.pen()
        p.setColor(Qt.white)
        painter.fillRect(0,0,768,1024, Qt.white)
        painter.end()
        self.update()

app = QApplication(sys.argv)
desktop = QApplication.desktop()

width = round(desktop.width()*0.6)
height = round(desktop.height()*0.6)

print(width, height)
wnd = Window(width, height)

wnd.show()

sys.exit(app.exec_())