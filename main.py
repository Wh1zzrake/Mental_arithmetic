import sys

from PyQt6.QtWidgets import QApplication

from core.main_window import MainWindow
from core import styles

app = QApplication(sys.argv)
styles.apply(app)
window = MainWindow()
window.resize(900, 600)
window.show()
sys.exit(app.exec())
