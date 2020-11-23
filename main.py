from PyQt5.QtGui import QIcon

from config import *
from PyQt5 import QtWidgets
import sys

import contracts as con
from models import Bill


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # шаблон окна
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

        # Вешаем на кнопку функцию "Spam"
        self.ui.pushButton.clicked.connect(self.spam)
        self.ui.listWidget.clicked.connect(self.contract_bills)

        # Заполняем listWidget договорами
        data = con.show_full_data()
        for agent, contract in data:
            self.ui.listWidget.addItem(f'{agent.id} : {agent.name}\tномер договора:  {contract.number}')

    def init_UI(self):
        self.setWindowTitle('Контракты')
        self.setWindowIcon(QIcon('ico/1.png'))

    def contract_bills(self):
        """вывод счетов по выбранному договору"""
        # TODO: переделать с принта на что-то нормальное

        for item in self.ui.listWidget.selectedItems():
            text = item.text().split()
            agent_id = text[0]
            agent_name = text[2]
            contract_number = text[5]

            bills = con.session.query(Bill).filter_by(agent_id=agent_id, contract_number=contract_number).all()
            print(f'Счета контрагента {agent_name} к договору № {contract_number}:')
            if bills:
                total_bills_sum = 0
                for bill in bills:
                    total_bills_sum += bill.bill_sum
                    print(f'Счет № {bill.bill_number}\tсумма = {bill.bill_sum}')
                print(f'На общую сумму: {total_bills_sum}\n')
            else:
                print('Счетов нет\n')

    # Описываем функцию
    def spam(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
