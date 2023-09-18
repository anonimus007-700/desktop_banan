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
        self.current_x = 0
        self.current_y = 0
        self.in_work = False
        self.cords = []
        self.jail_objects = []

        self.sania_defoult_skin = QPixmap('../res/sania.png')
        self.sania_ult_1_skin = QPixmap('../res/sania_ult_1.png')
        self.sania_ult_2_skin = QPixmap('../res/sania_ult_2.png')
        
        self.stas_defoult_skin = QPixmap('../res/stas.png')
        self.stas_ult_1_skin = QPixmap('../res/stas_ult_1.png')
        self.stas_ult_2_skin = QPixmap('../res/stas_ult_2.png')

        # calling method
        self.UiComponents()
        self.mouse()

        self.show()

    def all_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_player)
        self.timer.start(random.randint(1200, 4000))
        
        self.random_choice = random.choice([self.sania_ult_1, self.sania_ult_2])

        self.ult_timer = QTimer(self)
        self.ult_timer.timeout.connect(self.stas_ult_1)
        self.ult_timer.start(random.randint(5000, 15000))

    def thread(func):
        def wrapper(*args, **kwargs):
            current_thread = threading.Thread(
                target=func, args=args, kwargs=kwargs)
            current_thread.start()

        return wrapper

    def UiComponents(self):
        self.player = QLabel(self)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.button_chose = QVBoxLayout()  # Вертикальний контейнер для розміщення
        self.central_widget.setLayout(self.button_chose)

        self.sania_but = QPushButton("Саня", self)
        self.sania_but.setIcon(QIcon(self.sania_defoult_skin))
        self.sania_but.setIconSize(self.sania_defoult_skin.size())
        self.sania_but.setStyleSheet("""
                                color: white;
                                background-color: transparent;
                                font-weight: bold;
                                """)
        self.sania_but.clicked.connect(lambda: self._chose_player('sania'))

        self.stas_but = QPushButton("Стас", self)
        self.stas_but.setIcon(QIcon(self.stas_defoult_skin))
        self.stas_but.setIconSize(self.stas_defoult_skin.size())
        self.stas_but.setStyleSheet("""
                                color: white;
                                background-color: transparent;
                                font-weight: bold;
                                """)
        self.stas_but.clicked.connect(lambda: self._chose_player('stas'))

        self.button_chose.addWidget(self.sania_but)
        self.button_chose.addWidget(self.stas_but)

        self.button_chose.setAlignment(Qt.AlignCenter)

        self.showFullScreen()

    def move_player(self):
        new_x = random.randint(0, self.width())
        new_y = random.randint(0, self.height())

        start_rect = QRect(self.player.x(),
                           self.player.y(),
                           self.sania_defoult_skin.width(),
                           self.sania_defoult_skin.height())
        end_rect = QRect(new_x,
                         new_y,
                         self.sania_defoult_skin.width(),
                         self.sania_defoult_skin.height())

        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        
        self.animation.start()
        
        self.timer.start(random.randint(1200, 4000))

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

        self.x_limit = (self.cords[0], self.cords[2])
        self.y_limit = (self.cords[1], self.cords[7])

        self.in_work = True

        self.jailMoveEvent()

        self.continue_timer = QTimer(self)
        self.continue_timer.timeout.connect(self._continue_sania)
        self.continue_timer.start(6000)

    def sania_ult_2(self):
        self.timer.stop()
        self.ult_timer.stop()
        
        self.player.setPixmap(self.sania_ult_2_skin)
        
        self.animation.setDuration(2000)

        self.in_work = True

        start_rect = QRect(self.player.x(),
                        self.player.y(),
                        self.sania_defoult_skin.width(),
                        self.sania_defoult_skin.height())
        end_rect = QRect(self.current_x,
                        self.current_y,
                        self.sania_defoult_skin.width(),
                        self.sania_defoult_skin.height())

        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)

        self.animation.start()

        self.going_cursor()
        
        ending_rect = QRect(0,
                            0,
                            self.sania_defoult_skin.width(),
                            self.sania_defoult_skin.height())
        
        self.animation.setStartValue(end_rect)
        self.animation.setEndValue(ending_rect)

        self.animation.start()

        self.continue_timer = QTimer(self)
        self.continue_timer.timeout.connect(self._continue_sania)
        self.continue_timer.start(2100)
    
    def stas_ult_1(self):
        self.timer.stop()
        self.ult_timer.stop()

        self.player.setPixmap(self.stas_ult_1_skin)
        
        self.sleeping = QLabel(self)
        self.sleeping.setGeometry(0, 0, self.width(), self.height())
        self.sleeping.setStyleSheet('background-color: black;')
        
        self.opacity_effect = QGraphicsOpacityEffect()
        self.sleeping.setGraphicsEffect(self.opacity_effect)
        
        self.sleep_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.sleep_anim.setDuration(2000)  # Тривалість анімації (2 секунди)
        self.sleep_anim.setStartValue(0.0)  # Початкова прозорість (0)
        self.sleep_anim.setEndValue(0.9)  # Кінцева прозорість (0.9)
        self.sleep_anim.setEasingCurve(QEasingCurve.OutQuad)  # Крива ефекту


        self.layout().addWidget(self.sleeping)
        self.player.raise_()
        
        self.sleeping_text = QLabel("дєтскій час", self)
        self.sleeping_text.setStyleSheet('color: white;')
        self.sleeping_text.setGeometry(int(self.width()/2), int(self.height()/2), 200, 50)
        
        font = QFont()
        font.setPointSize(16)  # Задаємо розмір шрифту 16
        self.sleeping_text.setFont(font)
        
        self.layout().addWidget(self.sleeping_text)
        
        self.sleep_anim.start()
        
        self.continue_timer = QTimer(self)
        self.continue_timer.timeout.connect(self._continue_stas)
        self.continue_timer.start(6000)


    @thread
    def mouse(self):
        with Listener(on_move=self.on_move) as listener:
            listener.join()

    def on_move(self, x, y):
        self.current_x = x
        self.current_y = y

    @thread
    def going_cursor(self):
        while self.in_work:
            pyautogui.moveTo(self.player.x()+30, self.player.y()+30)

    @thread
    def jailMoveEvent(self):
        while self.in_work:
            if self.current_x < self.x_limit[0] or self.current_x > self.x_limit[1] or self.current_y < self.y_limit[0] or self.current_y > self.y_limit[1]:
                # Перемістіть курсор миші в середину визначених обмежень
                new_x = max(self.x_limit[0], min(self.current_x, self.x_limit[1]))
                new_y = max(self.y_limit[0], min(self.current_y, self.y_limit[1]))
                pyautogui.moveTo(new_x, new_y)

    def _continue_sania(self):
        self.all_timer()

        self.continue_timer.stop()
        
        self.animation.setDuration(1000)

        if self.jail_objects:
            for obj in self.jail_objects:
                obj.deleteLater()
        
        self.cords.clear()
        self.jail_objects.clear()
        self.in_work = False

        self.player.setPixmap(self.sania_defoult_skin)
    
    def _continue_stas(self):
        self.all_timer()

        self.continue_timer.stop()
        
        self.sleeping.deleteLater()
        self.sleeping_text.deleteLater()
        
        self.player.setPixmap(self.stas_defoult_skin)
        
    
    def _chose_player(self, player_chose):
        if player_chose == 'sania':
            self.player.setPixmap(self.sania_defoult_skin)

            self.player.resize(self.sania_defoult_skin.width(),
                               self.sania_defoult_skin.height())
        else:
            self.player.setPixmap(self.stas_defoult_skin)

            self.player.resize(self.stas_defoult_skin.width(),
                               self.stas_defoult_skin.height())
            
        self.animation = QPropertyAnimation(self.player, b"geometry")
        self.animation.setDuration(1000)
        
        self.sania_but.deleteLater()
        self.stas_but.deleteLater()

        self.all_timer()

App = QApplication(sys.argv)

window = Window()
sys.exit(App.exec())
