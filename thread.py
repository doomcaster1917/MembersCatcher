from PyQt6.QtCore import *
from PyQt6.QtCore import *
from controller import TelegramApi
from multiprocessing import Process
from Views.MessageBoxView import TelegramMessages
import socket


class HistoryThread(QThread):
    def __init__(self, chat_name, parent=None):
        QThread.__init__(self, parent)
        self.telegram_api = TelegramApi()
        self.chat_name = chat_name
        self.signals = Signals()
        self.process = None
        self.sock = socket.socket()
        self.conn = None
        self.pause = False
        self.stop = False

    def run(self):
        try:
            self.process = Process(target=self.telegram_api.download_from_history, args=(self.chat_name,))
            self.process.start()
            self.sock.bind(('', 9090))
            self.sock.listen(1)
            self.conn, _ = self.sock.accept()
            self.signals.process_state.emit("Загружается")
            while True:
                data = self.conn.recv(1024)
                text = data.decode("utf-8", "ignore")
                if text.isdigit():
                    self.signals.messages_count.emit(int(text))
                elif text == 'Done':
                    break
                else:
                    self.signals.listView_message.emit(f'.{text}')

                if self.pause:
                    self.conn.send(b'pause')
                elif self.stop:
                    self.conn.send(b'stop')
                else:
                    self.conn.send(b'ok')
                if not data:
                    break

            self.process.join()
            self.sock.close()
            print('Загрузка завершена')
        except Exception as err:
            if err.ID == 'USERNAME_NOT_OCCUPIED':
                TelegramMessages.telegram_wrong_user_fields_inserted(err.ID)

    @pyqtSlot()
    def set_pause(self):

        self.pause = not self.pause
        if self.pause and self.conn:
            self.signals.process_state.emit('Пауза')
        if not self.pause and self.conn:
            self.conn.send(b'resume')
            self.signals.process_state.emit("Загружается")
            print('resumed')

    def set_stop(self):
        if not self.pause:
            self.stop = True
        else:
            self.conn.send(b'stop')

class MonitoringThread(QThread):
    def __init__(self, chat_name, parent=None):
        QThread.__init__(self, parent)
        self.telegram_api = TelegramApi()
        self.chat_name = chat_name
        self.signals = Signals()
        self.process = None
        self.sock = socket.socket()
        self.conn = None
        self.stop = False

    def run(self):
        try:
            self.process = Process(target=self.telegram_api.monitoring_chat, args=(self.chat_name,))
            self.process.start()
            self.sock.bind(('', 9090))
            self.sock.listen(1)
            self.conn, _ = self.sock.accept()
            self.signals.process_state.emit("Мониторится")
            while True:
                data = self.conn.recv(1024)
                text = data.decode("utf-8", "ignore")
                if text.isdigit():
                    self.signals.messages_count.emit(int(text))
                else:
                    self.signals.listView_message.emit(f'.{text}')

                if self.stop:
                    break

            print('Загрузка завершена')
        except Exception as err:
            print(err)

    def set_stop(self):
            self.stop = True
            self.process.terminate()
            self.sock.close()

class Signals(QObject):
    listView_message = pyqtSignal(str)
    messages_count = pyqtSignal(int)
    process_state = pyqtSignal(str)

    @pyqtSlot()
    def download_finished(self):
        self.process_state.emit('Загрузка завершена')