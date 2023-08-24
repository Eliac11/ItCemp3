import sys
import os
import threading
from moduleReplicateApi import ReplicateInterface, paint_style

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
        generate.move(round(width*0.55-round(width*0.1)),round(height*0.5-round(height*0.1)))
        generate.resize(round(width*0.1), round(height*0.1))
        generate.clicked.connect(self.save_paint)
        generate.setStyleSheet("background-color: #5ea668; color: #ffffff")

        clear = QPushButton("Clear", self)
        clear.move(round(width*0.55-round(width*0.1)),round(height*0.5+round(height*0.1*0.5)))
        clear.resize(round(width*0.1), round(height*0.1))
        clear.clicked.connect(self.clear_paint)
        clear.setStyleSheet("background-color: #5ea668; color: #ffffff")

        self.combobox = QComboBox(self)
        for i in paint_style.keys():
            self.combobox.addItem(i)

        self.combobox.move(round(width*0.55-round(width*0.15)),round(height- height*0.97))
        self.combobox.resize(round(width*0.2), round(height*0.05))
        self.combobox.setStyleSheet("background-color: #5ea668; color: #ffffff")

        self.combobox.currentTextChanged.connect(self.text_changed)

        pixmap = QPixmap(QSize(round(width*0.35), round(height*0.8)))
        pixmap.fill(Qt.white)
        self.label_gen = QLabel(self)
        self.label_gen.setPixmap(pixmap)
        self.label_gen.move(round(width*0.58),round(height*0.1))
        self.label_gen.resize(QSize(round(width*0.35), round(height*0.8)))

        self.canvas = QPixmap(QSize(round(width*0.35), round(height*0.8)))
        self.canvas.fill(Qt.white)
        self.label_paint = QLabel(self)
        self.label_paint.move(round(width*0.07),round(height*0.1))
        self.label_paint.setPixmap(self.canvas)
        self.label_paint.resize(round(width*0.35),round(height*0.8))

        self.last_x, self.last_y = None, None

        self.now_changetstyle = "Realism"
        
        

    def mouseMoveEvent(self, e):
        mouse_x = e.x()-round(width*0.07)
        mouse_y = e.y()-round(height*0.1)
        if self.last_x is None:
            self.last_x = mouse_x
            self.last_y = mouse_y
            return
            
        painter = QPainter(self.label_paint.pixmap())
        p = painter.pen()
        p.setWidth(12)
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
        self.label_paint.move(round(width*0.07),round(height*0.1))
        
        self.genImage()

    def genImage(self):
        gen = ReplicateInterface("r8_5DHHGh72D2WeQjtERBDmyc8mwt8iiv339O4qL")
        newimg = gen.imageInpaiting(paint_style[self.now_changetstyle], "temp.png")
        gen_paint = QPixmap(newimg)
        gen_paint = gen_paint.scaled(round(width*0.35),round(height*0.8))
        self.label_gen.setPixmap(gen_paint)

    def clear_paint(self):
        painter = QPainter(self.label_paint.pixmap())
        p = painter.pen()
        p.setColor(Qt.white)
        painter.fillRect(0,0,round(width*0.35),round(height*0.8), Qt.white)
        painter.end()
        self.update()

    def text_changed(self,s):
        self.now_changetstyle = s

app = QApplication(sys.argv)
desktop = QApplication.desktop()

width = round(desktop.width()*0.6)
height = round(desktop.height()*0.6)
# width = round(1920*0.6)
# height = round(1080*0.6)
wnd = Window(width, height)

wnd.show()

sys.exit(app.exec_())