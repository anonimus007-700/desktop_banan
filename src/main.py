import sys
import random
import pyautogui
import threading

from pynput.mouse import Listener

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.acceptDrops()

        self.setWindowTitle("Python ")
        
        self.setGeometry(QDesktopWidget().availableGeometry())
        self.setMouseTracking(True)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Qt.FramelessWindowHint | 
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.speed = 15
        self.jail_work = False
        self.cords = []
        self.jail_objects = []

        self.defoult_skin = QPixmap('../res/sania.png')
        self.sania_ult_1_skin = QPixmap('../res/sania_ult_1.png')

        # calling method
        self.UiComponents()

        self.show()
        
        self.mouse()
        # self.mous = threading.Thread(target=self.mouse)
        # self.jail_thread = threading.Thread(target=self.jailMoveEvent)
        
        # self.mous.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_player)
        self.timer.start(random.randint(1200, 4000))
        
        self.ult_timer = QTimer(self)
        self.ult_timer.timeout.connect(self.sania_ult_1)
        self.ult_timer.start(random.randint(5000, 15000))
        
    def thread(func):
        def wrapper(*args, **kwargs):
            current_thread = threading.Thread(
                target=func, args=args, kwargs=kwargs)
            current_thread.start()

        return wrapper

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

        self.player.setPixmap(self.sania_ult_1_skin)

        jail_x = [self.current_x - 40, self.current_x + 40]
        jail_y = [self.current_y - 40, self.current_y + 40]
        
        for i in jail_x:
            self.wall = QLabel(self)
            self.wall.setGeometry(i,
                             self.current_y-30,
                             20,
                             80)
            self.wall.setStyleSheet('''background-color: black;
                                border:3px solid white;
                                border-radius: 10px;''')
            self.layout().addWidget(self.wall)
            
            self.jail_objects.append(self.wall)

            self.cords.append(self.wall.x())
            self.cords.append(self.wall.y())

        for i in jail_y:
            self.wall = QLabel(self)
            self.wall.setGeometry(self.current_x-30,
                             i,
                             80,
                             20)
            self.wall.setStyleSheet('''background-color: black;
                                border:3px solid white;
                                border-radius: 10px;''')
            self.layout().addWidget(self.wall)
            
            self.jail_objects.append(self.wall)

            self.cords.append(self.wall.x())
            self.cords.append(self.wall.y())

        print(self.cords)

        self.x_limit = (self.cords[0], self.cords[2])
        self.y_limit = (self.cords[1], self.cords[7])

        self.jail_work = True

        self.jailMoveEvent()

        self.continue_timer = QTimer(self)
        self.continue_timer.timeout.connect(self._continue)
        self.continue_timer.start(5000)
    
    @thread
    def mouse(self):
        with Listener(on_move=self.on_move) as listener:
            listener.join()

    def on_move(self, x, y):
        self.current_x = x
        self.current_y = y

    @thread
    def jailMoveEvent(self):
        while self.jail_work:
            if self.current_x < self.x_limit[0] or self.current_x > self.x_limit[1] or self.current_y < self.y_limit[0] or self.current_y > self.y_limit[1]:
                # Перемістіть курсор миші в середину визначених обмежень
                new_x = max(self.x_limit[0], min(self.current_x, self.x_limit[1]))
                new_y = max(self.y_limit[0], min(self.current_y, self.y_limit[1]))
                pyautogui.moveTo(new_x, new_y)

    def _continue(self):
        self.timer.start(random.randint(1200, 4000))
        self.ult_timer.start(random.randint(5000, 15000))

        self.continue_timer.stop()

        for obj in self.jail_objects:
            obj.deleteLater()
        
        self.cords.clear()
        self.jail_objects.clear()
        self.jail_work = False

        self.player.setPixmap(self.defoult_skin)

App = QApplication(sys.argv)

window = Window()
# print(window.size().height())
sys.exit(App.exec())
