#!/usr/bin/python

import sys

from PySide.QtGui import QApplication, QMessageBox

from Google.GoogleApi import GoogleApi
from Norton.PQS import PQS
from UI.LoginWindow import LoginWindow
from UI.MainWindow import MainWindow

from Google.GoogleApi import LOGIN_FAILURE
from Google.GoogleApi import LOGIN_SUCCESS
from Google.GoogleApi import LOGIN_NEED_PIN_VERIFICATION

DEFAULT_ACCOUNT = "symantec.device@gmail.com"
DEFAULT_PW = "Symantec123$"

google = GoogleApi()
pqs = PQS()


def _handle_login():
    loginWindow.disable()
    login_result = google.login(loginWindow.get_account(), loginWindow.get_password())
    if LOGIN_SUCCESS == login_result :
        loginWindow.close()
        _open_scan_window()
    elif LOGIN_NEED_PIN_VERIFICATION == login_result :
        QMessageBox.about(loginWindow, "ATTENTION", "SMS code requested")
        loginWindow.enable()
    else:
        QMessageBox.about(loginWindow, "ERROR", "Login failed! Please retry")
        loginWindow.enable()


def _handle_device_selection(index):
    mainWindow.disable()
    device_id = devices[index].get_web_id()
    mainWindow.set_results_list(_scan_device(device_id))
    mainWindow.enable()


def _open_scan_window():
    mainWindow.display()
    _prepare_devices()
    mainWindow.set_device_list([device.get_display_name() for device in devices])


def _prepare_devices():
    global devices
    devices = google.get_device_list()


def _scan_device(device_id):
    raw_result = pqs.batch_scan(google.get_apps_by_device_web_id(device_id))
    result = []

    if raw_result:
        for reputation in raw_result:
            result.append(reputation.get_rating_name() + " [" + reputation.get_app().get_name() + "]")

    return result


if __name__ == '__main__':
    ############ init first ############
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    loginWindow.connect_to_accept(_handle_login)
    loginWindow.set_account(DEFAULT_ACCOUNT)
    loginWindow.set_password(DEFAULT_PW)

    mainWindow = MainWindow()
    mainWindow.connect_to_change_device(_handle_device_selection)

    devices = []
    ############ end of init ############

    loginWindow.show()

    app.exec_()
