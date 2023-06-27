from PyQt6.QtCore import *
from controller import TelegramApi
import traceback, sys
TelegramApi = TelegramApi()
#init this class in GeneralView to allow all Views Classes inherit one and the same instance


class Signals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    print_browser_message = pyqtSignal(str)
class SignalSender(QRunnable):
    print_browser_message = pyqtSignal(str)

    def __init__(self, fn, *args, **kwargs):
        super(SignalSender, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    @pyqtSlot()
    def run(self):
 
        try:
            result = self.fn(
                *self.args, **self.kwargs
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

    @pyqtSlot()
    def download_from_history_sig(self, chat_name=None):
        try:
            for message in TelegramApi.download_from_history(chat_name=chat_name):
                self.print_browser_message.emit(message)
        except Exception as e:
            print(e)