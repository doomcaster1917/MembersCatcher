import requests
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox, QLineEdit
import os
import sys
class TelegramMessages():
    @staticmethod
    def telegram_auth_code(two_factor=None):
        msg = QMessageBox()
        key_line_edit = QLineEdit(msg)

        if two_factor:
            msg.setWindowTitle(f'Двухфакторная идентификация')
            msg.setText(f'   Введите код из смс \n от администрации месседжера')
        else:
            msg.setWindowTitle(f'Код подтверждения')
            msg.setText(f'   Введите код из смс \n   или сообщения в telegram  \n   от администрации месседжера')

        msg.setStyleSheet("QLabel{min-width: 300px; min-height: 300px}")
        key_line_edit.setGeometry(QtCore.QRect(60, 200, 150, 50))
        msg.setStandardButtons(QMessageBox.StandardButton.Yes)

        msg.exec()

        if msg.clickedButton():
            key = key_line_edit.text()
            print(key)
            return key

    @staticmethod
    def telegram_wrong_auth_code_inserted():
        msg = QMessageBox()

        msg.setWindowTitle(f'Введён неверный код')
        msg.setText(f'   Введён неверный код подтверждения.\n Приложение перезапустится,'
                    f' \n попробуйте авторизоваться заново')
        msg.setStyleSheet("QLabel{min-width: 300px; min-height: 300px}")
        msg.setGeometry(QtCore.QRect(60, 170, 300, 300))
        msg.setStandardButtons(QMessageBox.StandardButton.Yes)

        msg.exec()

        if msg.clickedButton():
            os.execv(sys.executable, ['python'] + sys.argv)

    @staticmethod
    def telegram_wrong_user_fields_inserted(err_text):
        msg = QMessageBox()

        msg.setWindowTitle(f'Введены неверные данные')
        msg.setText(f'   Введены неверные данные. \n {err_text}')
        msg.setStyleSheet("QLabel{min-width: 300px; min-height: 300px}")
        msg.setGeometry(QtCore.QRect(60, 170, 300, 300))
        msg.setStandardButtons(QMessageBox.StandardButton.Yes)

        msg.exec()

        if msg.clickedButton():
            pass