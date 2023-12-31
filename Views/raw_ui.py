# Form implementation generated from reading ui file 'MembersCatcher.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1029, 519)
        MainWindow.setStyleSheet("background: url(pictures/flag.jpg);\n"
"background-size: cover;\n"
"background-repeat: no-repeat; \n"
"background-position: center;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(280, 30, 711, 461))
        self.stackedWidget.setStyleSheet("background: rgb(47, 112, 157);\n"
"border-radius: 25px;")
        self.stackedWidget.setObjectName("stackedWidget")
        self.authentication = QtWidgets.QWidget()
        self.authentication.setObjectName("authentication")
        self.label = QtWidgets.QLabel(self.authentication)
        self.label.setGeometry(QtCore.QRect(212, 30, 294, 60))
        self.label.setStyleSheet("background:none;\n"
"color: white;\n"
"font-size: 50px;")
        self.label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label.setObjectName("label")
        self.authentication_api_id = QtWidgets.QLineEdit(self.authentication)
        self.authentication_api_id.setGeometry(QtCore.QRect(190, 120, 331, 41))
        self.authentication_api_id.setStyleSheet("background: white;\n"
"border-radius: 15%;")
        self.authentication_api_id.setObjectName("authentication_api_id")
        self.authentication_submit_button = QtWidgets.QPushButton(self.authentication)
        self.authentication_submit_button.setGeometry(QtCore.QRect(290, 390, 151, 41))
        self.authentication_submit_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.authentication_submit_button.setStyleSheet("background: green;\n"
"border-radius: 15%;\n"
"color: white;\n"
"font-size: 23px;")
        self.authentication_submit_button.setObjectName("authentication_submit_button")
        self.authentication_api_hash = QtWidgets.QLineEdit(self.authentication)
        self.authentication_api_hash.setGeometry(QtCore.QRect(190, 190, 331, 41))
        self.authentication_api_hash.setStyleSheet("background: white;\n"
"border-radius: 15%;")
        self.authentication_api_hash.setObjectName("authentication_api_hash")
        self.authentication_username = QtWidgets.QLineEdit(self.authentication)
        self.authentication_username.setGeometry(QtCore.QRect(190, 260, 331, 41))
        self.authentication_username.setStyleSheet("background: white;\n"
"border-radius: 15%;")
        self.authentication_username.setObjectName("authentication_username")
        self.authentication_phone_number = QtWidgets.QLineEdit(self.authentication)
        self.authentication_phone_number.setGeometry(QtCore.QRect(190, 330, 331, 41))
        self.authentication_phone_number.setStyleSheet("background: white;\n"
"border-radius: 15%;")
        self.authentication_phone_number.setObjectName("authentication_phone_number")
        self.stackedWidget.addWidget(self.authentication)
        self.set_mode = QtWidgets.QWidget()
        self.set_mode.setStyleSheet("border-image: url(pictures/choice_image.jpg);\n"
"")
        self.set_mode.setObjectName("set_mode")
        self.set_mode_monitoring_button = QtWidgets.QPushButton(self.set_mode)
        self.set_mode_monitoring_button.setGeometry(QtCore.QRect(480, 300, 141, 71))
        self.set_mode_monitoring_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.set_mode_monitoring_button.setStyleSheet("border-image: url(pictures/Rectangle 2.png);\n"
"border-radius: 15%;\n"
"color: white;\n"
"font-size: 13px;")
        self.set_mode_monitoring_button.setObjectName("set_mode_monitorin_button")
        self.set_mode_get_history_button = QtWidgets.QPushButton(self.set_mode)
        self.set_mode_get_history_button.setGeometry(QtCore.QRect(90, 290, 151, 71))
        self.set_mode_get_history_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.set_mode_get_history_button.setStyleSheet("border-image: url(pictures/Rectangle 1.png);\n"
"border-radius: 15%;\n"
"color: white;\n"
"font-size: 13px;")
        self.set_mode_get_history_button.setObjectName("set_mode_get_history_button")
        self.stackedWidget.addWidget(self.set_mode)
        self.process_page = QtWidgets.QWidget()
        self.process_page.setObjectName("process_page")
        self.process_page_chat_name_line_edit = QtWidgets.QLineEdit(self.process_page)
        self.process_page_chat_name_line_edit.setGeometry(QtCore.QRect(20, 130, 151, 41))
        self.process_page_chat_name_line_edit.setStyleSheet("background: white;\n"
"border-radius: 15%;")
        self.process_page_chat_name_line_edit.setObjectName("process_page_chat_name_line_edit")
        self.process_page_start_button = QtWidgets.QPushButton(self.process_page)
        self.process_page_start_button.setGeometry(QtCore.QRect(20, 190, 151, 41))
        self.process_page_start_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.process_page_start_button.setStyleSheet("background: black;\n"
"border-radius: 15%;\n"
"color: white;\n"
"font-size: 23px;")
        self.process_page_start_button.setObjectName("process_page_start_button")
        self.process_page_pause_button = QtWidgets.QPushButton(self.process_page)
        self.process_page_pause_button.setGeometry(QtCore.QRect(20, 260, 151, 41))
        self.process_page_pause_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.process_page_pause_button.setStyleSheet("background: black;\n"
"border-radius: 15%;\n"
"color: white;\n"
"font-size: 23px;")
        self.process_page_pause_button.setObjectName("process_page_pause_button")
        self.process_page_stop_button = QtWidgets.QPushButton(self.process_page)
        self.process_page_stop_button.setGeometry(QtCore.QRect(20, 330, 151, 41))
        self.process_page_stop_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.process_page_stop_button.setStyleSheet("background: black;\n"
"border-radius: 15%;\n"
"color: white;\n"
"font-size: 23px;")
        self.process_page_stop_button.setObjectName("process_page_stop_button")
        self.process_page_chosen_mode_label = QtWidgets.QLabel(self.process_page)
        self.process_page_chosen_mode_label.setGeometry(QtCore.QRect(20, 20, 151, 41))
        self.process_page_chosen_mode_label.setStyleSheet("border: 4px solid black;\n"
"border-radius: 10;\n"
"\n"
"background-color: rgb(119, 118, 123)")
        self.process_page_chosen_mode_label.setText("")
        self.process_page_chosen_mode_label.setObjectName("process_page_chosen_mode_label")
        self.process_page_chosen_chat = QtWidgets.QLabel(self.process_page)
        self.process_page_chosen_chat.setGeometry(QtCore.QRect(20, 70, 151, 41))
        self.process_page_chosen_chat.setStyleSheet("border: 4px solid black;\n"
"border-radius: 10;\n"
"\n"
"background-color: rgb(119, 118, 123)")
        self.process_page_chosen_chat.setText("")
        self.process_page_chosen_chat.setObjectName("process_page_chosen_chat")
        self.process_page_listView = QtWidgets.QListView(self.process_page)
        self.process_page_listView.setGeometry(QtCore.QRect(180, 20, 501, 371))
        self.process_page_listView.setStyleSheet("background: white;\n"
"border-radius: 0px;")
        self.process_page_listView.setObjectName("process_page_listView")
        self.process_page_downloaded_sum_label = QtWidgets.QLabel(self.process_page)
        self.process_page_downloaded_sum_label.setGeometry(QtCore.QRect(440, 400, 241, 41))
        self.process_page_downloaded_sum_label.setStyleSheet("border: 4px solid black;\n"
"border-radius: 10;\n"
"\n"
"background-color: #62A1CE;")
        self.process_page_downloaded_sum_label.setText("")
        self.process_page_downloaded_sum_label.setObjectName("process_page_downloaded_sum_label")
        self.process_page_state_label = QtWidgets.QLabel(self.process_page)
        self.process_page_state_label.setGeometry(QtCore.QRect(20, 400, 181, 41))
        self.process_page_state_label.setStyleSheet("border: 4px solid black;\n"
"border-radius: 10;\n"
"\n"
"background-color: #62A1CE;")
        self.process_page_state_label.setText("")
        self.process_page_state_label.setObjectName("process_page_state_label")
        self.process_page_messages_sum_label = QtWidgets.QLabel(self.process_page)
        self.process_page_messages_sum_label.setGeometry(QtCore.QRect(210, 400, 221, 41))
        self.process_page_messages_sum_label.setStyleSheet("border: 4px solid black;\n"
"border-radius: 10;\n"
"\n"
"background-color: #62A1CE;")
        self.process_page_messages_sum_label.setText("")
        self.process_page_messages_sum_label.setObjectName("process_page_messages_sum_label")
        self.stackedWidget.addWidget(self.process_page)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Авторизация"))
        self.authentication_submit_button.setText(_translate("MainWindow", "Войти"))
        self.set_mode_monitoring_button.setText(_translate("MainWindow", "Мониторить \n"
" новые сообщения"))
        self.set_mode_get_history_button.setText(_translate("MainWindow", "Скачать участников \n"
" из истории сообщений"))
        self.process_page_start_button.setText(_translate("MainWindow", "Начать"))
        self.process_page_pause_button.setText(_translate("MainWindow", "Пауза"))
        self.process_page_stop_button.setText(_translate("MainWindow", "Остановить"))
