from .raw_ui import Ui_MainWindow
from PyQt6.QtWidgets import *
from PyQt6 import uic, QtCore, QtGui, QtWidgets
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import *
from controller import *
from .Singnals import SignalSender
from functools import partial

TelegramApi = TelegramApi()
class GeneralView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.signal_sender = SignalSender()

        # placeholders settings
        self.ui.authentication_api_id.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите значение api_id", None))
        self.ui.authentication_api_hash.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите значение api_hash", None))

        self.ui.authentication_username.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите имя аккаунта telegram", None))
        self.ui.authentication_phone_number.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Введите телефонный номер аккаунта", None))

        #buttons connections
        self.ui.authentication_submit_button.clicked.connect(self.make_telegram_session)
        self.ui.set_mode_get_history_button.clicked.connect(self.open_process_widget_from_history)
        self.ui.set_mode_monitorin_button.clicked.connect(self.open_process_widget_monitoring)



        #edit_connections
        self.ui.process_page_chat_name_line_edit.textChanged.connect(self.chat_label_value_handler)

        #signals_connections
        self.signal_sender.print_browser_message.connect(self.textBrowser_and_pb_handler, Qt.QueuedConnection)

        self.textBrowser_text = ''
        self.progress_bar_value = 0
        self.displayed_page = None
        self.thread = QThread()
        self.signal_sender.moveToThread(self.thread)
        self.on_open()

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
        self.displayed_page = self.ui.process_page
        self.ui.process_page_chosen_mode_label.setText("Скачивание из истории")
        self.ui.process_page_progressBar.setMinimum(0)
        self.ui.process_page_progressBar.setMaximum(100000)
        self.ui.process_page_start_button.clicked.connect(self.start_download_from_history)
        self.displayed_page.show()

    def open_process_widget_monitoring(self):
        self.clear_stacked_widget()
        self.displayed_page = self.ui.process_page
        self.ui.process_page_chosen_mode_label.setText("Мониторинг сообщений")
        self.ui.process_page_progressBar.setMinimum(0)
        self.ui.process_page_progressBar.setMaximum(100000)
        self.ui.process_page_start_button.clicked.connect(self.start_monitoring)
        self.displayed_page.show()

    def start_download_from_history(self):
        try:
            chat_name = self.ui.process_page_chat_name_line_edit.text()
            # func = partial(self.signal_sender.download_from_history_sig, chat_name=chat_name)
            # self.thread.started.connect(func)
            # self.thread.start()
            self.signal_sender.download_from_history_sig(chat_name=chat_name)
            TelegramApi.download_from_history(chat_name=chat_name)
        except Exception as err:
            if err.ID == 'USERNAME_NOT_OCCUPIED':
                TelegramMessages.telegram_wrong_user_fields_inserted(err.ID)

    def start_monitoring(self):
        ...

    def chat_label_value_handler(self, chat_id):
        chat_name = TelegramApi.get_chat_name(chat_id)
        self.ui.process_page_chosen_chat.setText(chat_name)


    def textBrowser_and_pb_handler(self, text):
        self.textBrowser_text += text
        self.progress_bar_value += 1
        self.ui.process_page_textBrowser.setText(self.textBrowser_text)
        self.ui.process_page_progressBar.setValue(self.progress_bar_value)
