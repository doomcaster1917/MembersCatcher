from PyQt6.QtWidgets import QApplication
import sys
from Views.View import GeneralView


class GUI(GeneralView):
    def __init__(self):
        super().__init__()
        GeneralView()

app = QApplication(sys.argv)
window = GUI()
window.setFixedSize(1029, 519)
window.show()
sys.exit(app.exec())