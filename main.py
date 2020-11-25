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
        self.ui.tableWidget.setRowCount(len(self.data))

        # сначала создаем необходимое кол-во рядов согласно кол-ву полученных данных
        for i in range(len(self.data)):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget.setItem(i, 3, item)

        # теперь добавляем в каждую стоку полученные ранее данные
        row_number = 0
        for agent, contract in self.data:
            item = self.ui.tableWidget.item(row_number, 0)
            item.setText(str(agent.id))
            item = self.ui.tableWidget.item(row_number, 1)
            item.setText(agent.name)
            item = self.ui.tableWidget.item(row_number, 2)
            item.setText(contract.number)
            item = self.ui.tableWidget.item(row_number, 3)
            item.setText(contract.description)
            row_number += 1




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWindow()
    myapp.show()
    sys.exit(app.exec_())
