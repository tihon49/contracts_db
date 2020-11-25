import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from config import *
from contracts import show_full_data


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.setStyleSheet('border: 2 solid green; border-radius: 20px;')

        # получаем данные для вывода в таблице
        self.data = show_full_data()
        # устанавливаем кол-во строк в таблице
        self.ui.tableWidget.setRowCount(len(self.data))

        self.row_index = 0
        # теперь добавляем в каждую стоку полученные ранее данные
        for agent, contract in self.data:
            self.ui.tableWidget.setItem(self.row_index, 0, QtWidgets.QTableWidgetItem(str(agent.id)))
            self.ui.tableWidget.setItem(self.row_index, 1, QtWidgets.QTableWidgetItem(agent.name))
            self.ui.tableWidget.setItem(self.row_index, 2, QtWidgets.QTableWidgetItem(contract.number))
            self.ui.tableWidget.setItem(self.row_index, 3, QtWidgets.QTableWidgetItem(contract.description))
            self.row_index += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWindow()
    myapp.show()
    sys.exit(app.exec_())
