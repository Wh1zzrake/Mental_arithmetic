from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from screens.splash_screen import SplashScreen
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.menu_screen import MenuScreen
from screens.lesson_screen import LessonScreen
from screens.test_screen import TestScreen
from screens.result_screen import ResultScreen
from screens.trainer_screen import TrainerListScreen, TrainerWorkScreen
from screens.statistics_screen import OverallStatsScreen, PersonalStatsScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тренажёр устного счёта")
        self.current_user = None           # кто вошёл (заполняется после входа)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # создаём экраны и передаём им ссылку на себя
        self.splash = SplashScreen(self)
        self.login = LoginScreen(self)
        self.register = RegisterScreen(self)
        self.menu = MenuScreen(self)
        self.lesson = LessonScreen(self)
        self.test = TestScreen(self)
        self.result = ResultScreen(self)
        self.trainer_list = TrainerListScreen(self)
        self.trainer_work = TrainerWorkScreen(self)
        self.overall_stats = OverallStatsScreen(self)
        self.personal_stats = PersonalStatsScreen(self)

        for screen in (self.splash, self.login, self.register, self.menu,
                       self.lesson, self.test, self.result,
                       self.trainer_list, self.trainer_work,
                       self.overall_stats, self.personal_stats):
            self.stack.addWidget(screen)

        self.stack.setCurrentWidget(self.splash)

    def go_to(self, screen):
        # если у экрана есть метод refresh() — обновим данные перед показом
        if hasattr(screen, "refresh"):
            screen.refresh()
        self.stack.setCurrentWidget(screen)
