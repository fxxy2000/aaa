from PySide import QtGui

from PySide.QtGui import QMainWindow

from QtUi.mainwindow import Ui_MainWindow as Main


class MainWindow(QMainWindow, Main):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    def display(self):
        self.show()

    def disable(self):
        self.setDisabled(True)
        QtGui.qApp.processEvents()

    def enable(self):
        self.setEnabled(True)
        QtGui.qApp.processEvents()

    def connect_to_change_device(self, slot):
        self.listDevice.currentRowChanged.connect(slot)

    def set_device_list(self, devices):
        self.listDevice.clear()
        self.listDevice.addItems(devices)

    def set_results_list(self, results):
        self.listResult.clear()
        self.listResult.addItems(results)
