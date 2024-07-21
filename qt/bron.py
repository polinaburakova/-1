import datetime
import sys

import requests
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMessageBox, \
    QDateTimeEdit

from qt.file import read_token


class BronWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("Бронирование столика")
        self.setLayout(layout)

        # Title Label
        title = QLabel("Введите данные")
        title.setProperty("class", "heading")
        layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        # user = QLabel("Количество гостей")
        # user.setProperty("class", "normal")
        # layout.addWidget(user, 1, 0)
        # self.input1 = QLineEdit()
        # self.input1.setValidator(QIntValidator())
        # layout.addWidget(self.input1, 1, 1, 1, 2)

        user = QLabel("Номер столика")
        user.setProperty("class", "normal")
        layout.addWidget(user, 2, 0)
        self.input2 = QLineEdit()
        self.input2.setValidator(QIntValidator())
        layout.addWidget(self.input2, 2, 1, 1, 2)

        # Время
        user = QLabel("Время")
        user.setProperty("class", "normal")
        layout.addWidget(user, 3, 0)
        self.time_edit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.time_edit.setDisplayFormat("hh:mm")
        layout.addWidget(self.time_edit, 3, 1, 1, 2)

        # Дата
        user = QLabel("Дата")
        user.setProperty("class", "normal")
        layout.addWidget(user, 4, 0)
        self.date_edit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        layout.addWidget(self.date_edit, 4, 1, 1, 2)

        button1 = QPushButton("Забронировать")
        button1.clicked.connect(self.bron)
        layout.addWidget(button1, 5, 1)

        self.token = read_token()

        self.message_box = None

    def get_datetime(self) -> datetime.datetime:
        selected_date = self.date_edit.date().toPyDate()
        selected_time = self.time_edit.time().toPyTime()
        return datetime.datetime.combine(selected_date, selected_time)

    def bron(self):
        date = self.get_datetime()

        if not self.token:
            self.message_box = QMessageBox(QMessageBox.Icon.Critical, "Ошибка", "Вы не авторизованы",
                                           QMessageBox.StandardButton.Yes)
            self.message_box.show()
            return

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        res = requests.get("http://127.0.0.1:8000/tables/all", headers=headers)

        if res.status_code == 200:
            data = res.json()
        else:
            self.message_box = QMessageBox(QMessageBox.Icon.Critical, "Ошибка", f"status code {res.status_code}",
                                           QMessageBox.StandardButton.Yes)
            self.message_box.show()
            return

        if not len(data):
            self.message_box = QMessageBox(QMessageBox.Icon.Critical, "Ошибка", f"Нет столиков",
                                           QMessageBox.StandardButton.Yes)
            self.message_box.show()
            return

        current_table = [el for el in data if el["table_number"] == int(self.input2.text())]

        if not current_table:
            self.message_box = QMessageBox(QMessageBox.Icon.Critical, "Ошибка", f"Нет Подходящего столика",
                                           QMessageBox.StandardButton.Yes)
            self.message_box.show()
            return

        current_table = current_table[0]

        res = requests.post("http://127.0.0.1:8000/order/create",
                            headers=headers,
                            json={
                                "table_id": current_table["id"],
                                "date": date.isoformat()
                            })

        if res.status_code == 200:
            self.message_box = QMessageBox(QMessageBox.Icon.Information, "Успех", f"Вы забронировали столик",
                                           QMessageBox.StandardButton.Yes)
            self.message_box.show()
            return
        elif res.status_code == 409:
            self.message_box = QMessageBox(QMessageBox.Icon.Warning, "Ошибка", f"Столик уже забронировае",
                                           QMessageBox.StandardButton.Yes)
            self.message_box.show()
            return
        else:
            self.message_box = QMessageBox(QMessageBox.Icon.Critical, "Ошибка", f"status code {res.status_code}",
                                           QMessageBox.StandardButton.Yes)
            self.message_box.show()
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BronWindow()
    window.show()
    sys.exit(app.exec())
