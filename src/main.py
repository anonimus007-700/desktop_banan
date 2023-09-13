import sys
import random
import pyautogui
import threading

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.acceptDrops()

        self.setWindowTitle("Python ")
        
        self.setGeometry(QDesktopWidget().availableGeometry())

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Qt.FramelessWindowHint | 
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.speed = 15
        self.cords = []

        self.defoult_skin = QPixmap('../res/sania.png')
        self.sania_ult_1_skin = QPixmap('../res/sania_ult_1.png')

        # calling method
        self.UiComponents()

        self.show()
        
        self.jail_event = threading.Thread(target=self.mouseMoveEvent)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_player)
        self.timer.start(random.randint(1200, 4000))
        
        self.ult_timer = QTimer(self)
        self.ult_timer.timeout.connect(self.sania_ult_1)
        self.ult_timer.start(random.randint(5000, 15000))

    def UiComponents(self):
        self.player = QLabel(self)

        self.player.setPixmap(self.defoult_skin)

        self.player.resize(self.defoult_skin.width(),
                           self.defoult_skin.height())

        self.animation = QPropertyAnimation(self.player, b"geometry")
        self.animation.setDuration(1000)
        
        self.label = QLabel(self)
        self.label.resize(200, 40)
        
        self.showFullScreen()

    def move_player(self):
        new_x = random.randint(0, self.width())
        new_y = random.randint(0, self.height())

        start_rect = QRect(self.player.x(),
                           self.player.y(),
                           self.defoult_skin.width(),
                           self.defoult_skin.height())
        end_rect = QRect(new_x,
                         new_y,
                         self.defoult_skin.width(),
                         self.defoult_skin.height())

        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        
        self.animation.start()
        
        # self.timer.stop()
        # self.timer.start(random.randint(1200, 4000))

        # self.player.move(new_x, new_y)

    def calling_ult(self):
        self.ult_timer = QTimer(self)
        self.ult_timer.timeout.connect(self.sania_ult_1)
        self.ult_timer.start(random.randint(5000, 15000))

    def sania_ult_1(self):
        self.timer.stop()
        self.ult_timer.stop()

        self.jail_event.start()

        self.player.setPixmap(self.sania_ult_1_skin)

        jail_x = [self.curentx - 40, self.curentx + 40]
        jail_y = [self.curenty - 40, self.curenty + 40]
        
        for i in jail_x:
            self.wall = QLabel(self)
            self.wall.setGeometry(i,
                             self.y-30,
                             20,
                             80)
            self.wall.setStyleSheet('''background-color: black;
                                border:3px solid white;
                                border-radius: 10px;''')
            self.layout().addWidget(self.wall)

            self.cords.append(self.wall.x())
            self.cords.append(self.wall.y())

        for i in jail_y:
            self.wall = QLabel(self)
            self.wall.setGeometry(self.x-30,
                             i,
                             80,
                             20)
            self.wall.setStyleSheet('''background-color: black;
                                border:3px solid white;
                                border-radius: 10px;''')
            self.layout().addWidget(self.wall)

            self.cords.append(self.wall.x())
            self.cords.append(self.wall.y())

        print(self.cords)

        self.x_limit = (self.cords[0], self.cords[4])  # Приклад обмежень по осі X
        self.y_limit = (self.cords[1], self.cords[5])  # Приклад обмежень по осі Y

        self.jail_timer = QTimer(self)
        self.jail_timer.timeout.connect(self.jailMoveEvent)
        self.jail_timer.start(4000)
        
        self.jail_event.join()

        self.continue_timer = QTimer(self)
        self.continue_timer.timeout.connect(self._continue)
        self.continue_timer.start(5000)

    def jailMoveEvent(self):
        while True:
            self.curentx, self.curenty = pyautogui.position()
            
            if self.curentx < self.x_limit[0] or self.curentx > self.x_limit[1] or self.curenty < self.y_limit[0] or self.curenty > self.y_limit[1]:
                # Перемістіть курсор миші в середину визначених обмежень
                new_x = max(self.x_limit[0], min(self.curentx, self.x_limit[1]))
                new_y = max(self.y_limit[0], min(self.curenty, self.y_limit[1]))
                pyautogui.moveTo(new_x, new_y)

    def _continue(self):
        self.timer.start(random.randint(1200, 4000))
        self.ult_timer.start(random.randint(5000, 15000))
        
        self.continue_timer.stop()
        
        self.cords.clear()
        self.setMouseTracking(False)

        self.player.setPixmap(self.defoult_skin)

App = QApplication(sys.argv)

window = Window()
# print(window.size().height())
sys.exit(App.exec())
