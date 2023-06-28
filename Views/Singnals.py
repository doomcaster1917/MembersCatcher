from PyQt6.QtCore import *
from controller import TelegramApi
from multiprocessing import Process
from .MessageBoxView import TelegramMessages
import socket
TelegramApi = TelegramApi()



class SignalSender(QObject):
    listView_message = pyqtSignal(str)
    messages_count = pyqtSignal(int)
    process_state = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.process = None
        self.sock = socket.socket()
        self.conn = None
        self.pause = False
        self.stop = False
    @pyqtSlot()
    def download_from_history_sig(self, chat_name=None):
        try:
            self.process = Process(target=TelegramApi.download_from_history, args=(chat_name,))
            self.process.start()
            self.sock.bind(('', 9090))
            self.sock.listen(1)
            self.conn, _ = self.sock.accept()
            self.process_state.emit("Загружается")
            while True:
                data = self.conn.recv(1024)
                text = data.decode("utf-8", "ignore")
                if text.isdigit():
                    self.messages_count.emit(int(text))
                elif text == 'Done':
                    break
                else:
                    self.listView_message.emit(f'.{text}')

                if self.pause:
                    self.conn.send(b'pause')
                elif self.stop:
                    self.conn.send(b'stop')
                else:
                    self.conn.send(b'ok')
                if not data:
                    break

            self.process.join()
            print('Загрузка завершена')
        except Exception as err:
            if err.ID == 'USERNAME_NOT_OCCUPIED':
                TelegramMessages.telegram_wrong_user_fields_inserted(err.ID)

    @pyqtSlot()
    def download_finished(self):
        self.process_state.emit('Загрузка завершена')

    @pyqtSlot()
    def set_pause(self):
        print(self.pause)
        self.pause = not self.pause
        if self.pause and self.conn:
            self.process_state.emit('Пауза')
        if not self.pause and self.conn:
            self.conn.send(b'resume')
            self.process_state.emit("Загружается")
            print('resumed')

    def set_stop(self):
        self.stop = True