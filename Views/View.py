from .raw_ui import Ui_MainWindow
from PyQt6.QtWidgets import *
from PyQt6 import uic, QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtCore import *
from controller import *
from thread import HistoryThread, MonitoringThread, Signals
import re

TelegramApi = TelegramApi()
class GeneralView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.signal_sender = None
        self.thread = None
        self.ui.process_page.setGeometry(QtCore.QRect(0, 0, 711, 461))

        # placeholders settings
        self.ui.authentication_api_id.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите значение api_id", None))
        self.ui.authentication_api_hash.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите значение api_hash", None))

        self.ui.authentication_username.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите имя аккаунта telegram", None))
        self.ui.authentication_phone_number.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите телефонный номер аккаунта", None))
        self.ui.process_page_chat_name_line_edit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите @ чата", None))

        #buttons connections
        self.ui.authentication_submit_button.clicked.connect(self.make_telegram_session)
        self.ui.set_mode_get_history_button.clicked.connect(self.open_process_widget_from_history)
        self.ui.set_mode_monitoring_button.clicked.connect(self.open_process_widget_monitoring)



        #edit_connections
        self.ui.process_page_chat_name_line_edit.textChanged.connect(self.chat_label_value_handler)

        self.model = QtGui.QStandardItemModel()
        self.ui.process_page_listView.setModel(self.model)
        self.downloaded_value = 0
        self.displayed_page = None
        self.on_open()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
    def clear_stacked_widget(self):
        objects = [self.ui.set_mode, self.ui.process_page, self.ui.authentication]
        for obj in objects:
            obj.hide()


    def on_open(self):
        self.clear_stacked_widget()

        if check_session_exists():
            self.displayed_page = self.ui.set_mode
        else:
            self.displayed_page = self.ui.authentication

        self.displayed_page.show()

    def make_telegram_session(self):
        print('Authorisation is started')
        api_id = self.ui.authentication_api_id.text()
        api_hash = self.ui.authentication_api_hash.text()
        phone_number = self.ui.authentication_phone_number.text()
        account_name = self.ui.authentication_username.text()
        try:
            telegram_sign_in(api_id=api_id, api_hash=api_hash,
                             phone=phone_number, account_name=account_name)
            self.displayed_page = self.ui.set_mode
            self.clear_stacked_widget()
            self.displayed_page.show()
        except Exception as err:
            err_text = err.ID
            if err.CODE == 400 and err_text == 'PHONE_CODE_INVALID':
                TelegramMessages.telegram_wrong_auth_code_inserted()
            else:
                TelegramMessages.telegram_wrong_user_fields_inserted(err_text)

    def open_process_widget_from_history(self):
        self.clear_stacked_widget()
        self.clear_process_widget()
        self.displayed_page = self.ui.process_page
        self.ui.process_page_stop_button.setText("Остановить")
        self.ui.process_page_pause_button.setText("Пауза")
        self.ui.process_page_chosen_mode_label.setText("Скачивание из истории")
        self.ui.process_page_start_button.clicked.connect(self.start_download_from_history)
        self.ui.process_page_pause_button.clicked.connect(self.pause_button_handler)
        self.ui.process_page_stop_button.clicked.connect(self.stop_button_handler)
        self.displayed_page.show()

    def open_process_widget_monitoring(self):
        self.clear_stacked_widget()
        self.clear_process_widget()
        self.displayed_page = self.ui.process_page
        self.ui.process_page_stop_button.setText("Остановить")
        self.ui.process_page_pause_button.hide()
        self.ui.process_page_chosen_mode_label.setText("Мониторинг сообщений")
        self.ui.process_page_start_button.clicked.connect(self.start_monitoring)
        self.ui.process_page_stop_button.clicked.connect(self.stop_button_handler)
        self.displayed_page.show()

    def clear_process_widget(self):
        self.model.clear()
        labels = [self.ui.process_page_state_label, self.ui.process_page_downloaded_sum_label,
                  self.ui.process_page_chosen_chat, self.ui.process_page_messages_sum_label,
                  self.ui.process_page_chosen_mode_label]
        for label in labels:
            label.setText('')
        self.ui.process_page_chat_name_line_edit.setText('')

    @pyqtSlot()
    def start_download_from_history(self):
        print(self.thread)
        try:
            if not self.ui.process_page_chosen_chat.text():
                TelegramMessages.telegram_wrong_user_fields_inserted('Неправильное название чата')
            else:
                raw_chat_name = self.ui.process_page_chat_name_line_edit.text()
                chat_name = re.sub(r'@', r'', raw_chat_name)
                self.thread = HistoryThread(chat_name=chat_name)
                self.signal_sender = self.thread.signals
                self.signal_sender.listView_message.connect(self.listView_and_downloaded_label_handler)
                self.signal_sender.messages_count.connect(self.messages_count_label_handler)
                self.signal_sender.process_state.connect(self.state_label_handler)
                self.thread.finished.connect(self.signal_sender.download_finished)
                self.thread.start()

        except Exception as err:
            print(err)
            if err.ID == 'USERNAME_NOT_OCCUPIED':
                TelegramMessages.telegram_wrong_user_fields_inserted(err.ID)

    def start_monitoring(self):
        if not self.ui.process_page_chosen_chat.text():
            TelegramMessages.telegram_wrong_user_fields_inserted('Неправильное название чата')
        else:
            raw_chat_name = self.ui.process_page_chat_name_line_edit.text()
            chat_name = re.sub(r'@', r'', raw_chat_name)
            self.thread = MonitoringThread(chat_name=chat_name)
            self.signal_sender = self.thread.signals
            self.signal_sender.listView_message.connect(self.listView_and_downloaded_label_handler)
            self.signal_sender.messages_count.connect(self.messages_count_label_handler)
            self.signal_sender.process_state.connect(self.state_label_handler)
            self.thread.finished.connect(self.signal_sender.download_finished)
            self.thread.start()


    def pause_button_handler(self):
        self.thread.set_pause()
        if self.thread.pause:
            self.ui.process_page_pause_button.setText("Продолжить")
        else:
            self.ui.process_page_pause_button.setText("Пауза")

    def stop_button_handler(self):
        try:
            if self.thread:
                self.thread.set_stop()

                self.ui.process_page_start_button.clicked.disconnect()
                self.ui.process_page_stop_button.clicked.disconnect()

                if self.ui.process_page_chosen_mode_label.text() == 'Скачивание из истории':
                    self.ui.process_page_pause_button.clicked.disconnect()

            self.displayed_page = self.ui.set_mode
            self.clear_stacked_widget()
            self.displayed_page.show()
        except Exception as e:
            print(e)

    def chat_label_value_handler(self, chat_name):
        data = TelegramApi.get_chat_info(chat_name=chat_name)
        if data:
            chat_title = data['title']
            self.ui.process_page_chosen_chat.setText(chat_title)
        else:
            self.ui.process_page_chosen_chat.setText('')

    def messages_count_label_handler(self, count):
        self.ui.process_page_messages_sum_label.setText(f'Проверено {count} сообщений')

    def state_label_handler(self, text):
        self.ui.process_page_state_label.setText(text)
        if text == 'Загрузка завершена':
            self.ui.process_page_stop_button.setText("Закрыть")

    def listView_and_downloaded_label_handler(self, text):
        item = QtGui.QStandardItem(text)
        self.model.appendRow(item)
        self.downloaded_value += 1
        self.ui.process_page_downloaded_sum_label.setText(f'Загружено {self.downloaded_value} участников')


    def closeEvent(self, *args, **kwargs):
        print(111)
        try:
            if self.thread.process:
                self.thread.sock.close()
                if isinstance(self.thread.process, HistoryThread):
                    self.thread.set_stop()
                    self.thread.process.terminate()
                else:
                    self.thread.set_stop()
                print(222)
        except Exception as err:
            print(err)
        self.close()


