from PySide import QtGui

from PySide.QtGui import QDialog

from QtUi.loginwindow import Ui_Dialog as LoginDialog


class LoginWindow(QDialog, LoginDialog):

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)

    def connect_to_accept(self, slot):
        self.buttonBox.accepted.connect(slot)

    def get_account(self):
        return self.lineEmail.text()

    def get_password(self):
        return self.linePw.text()

    def set_account(self, account):
        self.lineEmail.setText(account)

    def set_password(self, pw):
        self.linePw.setText(pw)

    def disable(self):
        self.setDisabled(True)
        QtGui.qApp.processEvents()

    def enable(self):
        self.setEnabled(True)
        QtGui.qApp.processEvents()
