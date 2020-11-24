from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt

# Наследуемся от QMainWindow

import contracts


class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1200, 400))  # Устанавливаем размеры
        self.setWindowTitle("Работа с QTableWidget")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        data = contracts.show_full_data()  # получаем данные из БД
        table = QTableWidget(self)  # Создаём таблицу
        table.setColumnCount(4)  # Устанавливаем 4 колонки
        table.setRowCount(len(data))  # строки в соответствии с кол-вом данных

        # Устанавливаем заголовки таблицы
        table.setHorizontalHeaderLabels(["id", "Названиве", "№ договора", "Описание"])

        # Устанавливаем всплывающие подсказки на заголовки
        table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        table.horizontalHeaderItem(2).setToolTip("Column 3 ")
        table.horizontalHeaderItem(3).setToolTip("Column 4 ")

        # Устанавливаем выравнивание на заголовки
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)

        # заполняем строки
        row = 0
        for agent, contract in data:
            print(agent, contract)
            table.setItem(row, 0, QTableWidgetItem(str(agent.id)))
            table.setItem(row, 1, QTableWidgetItem(agent.name))
            table.setItem(row, 2, QTableWidgetItem(contract.number))
            table.setItem(row, 3, QTableWidgetItem(contract.description))
            row += 1

        # делаем ресайз колонок по содержимому
        table.resizeColumnsToContents()

        grid_layout.addWidget(table, 0, 0)  # Добавляем таблицу в сетку


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
