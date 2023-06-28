from PyQt6.QtWidgets import QApplication
import sys
from Views.View import GeneralView
from multiprocessing import freeze_support

class GUI(GeneralView):
    def __init__(self):
        super().__init__()
        GeneralView()

if __name__ == '__main__':
    freeze_support()
    app = QApplication(sys.argv)
    window = GUI()
    window.setFixedSize(1029, 519)
    window.show()
    sys.exit(app.exec())