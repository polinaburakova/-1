import sys

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMainWindow, QMessageBox

from qt.bron import BronWindow
from qt.file import write_token, read_token


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("Вход в систему")
        self.setLayout(layout)

        self.bron_window = BronWindow()

        # Title Label
        title = QLabel("Вход")
        title.setProperty("class", "heading")
        layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        # Username Label and Input
        user = QLabel("Email:")
        user.setProperty("class", "normal")
        layout.addWidget(user, 1, 0)
        self.input1 = QLineEdit()
        layout.addWidget(self.input1, 1, 1, 1, 2)

        # Password Label and Input
        pwd = QLabel("Password")
        pwd.setProperty("class", "normal")
        layout.addWidget(pwd, 2, 0)
        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input2, 2, 1, 1, 2)

        button2 = QPushButton("Login")
        button2.clicked.connect(self.login_user)
        layout.addWidget(button2, 4, 2)

        self.message_box = None

    def login_user(self):
        payload_data = {
            "username": self.input1.text(),
            "password": self.input2.text()
        }

        res = requests.post(
            "http://127.0.0.1:8000/auth/jwt/login",
            data=payload_data
        )

        data = res.json()

        if res.status_code == 200:
            write_token(data["access_token"])
            self.go_to_bron()
        elif res.status_code == 400:
            self.message_box = QMessageBox(QMessageBox.Icon.Warning, "Bad request", f"Status code: {res.status_code}")
            self.message_box.show()
        elif res.status_code == 422:
            self.message_box = QMessageBox(QMessageBox.Icon.Warning, "Ошибка валидации", f"Status code: {res.status_code}", QMessageBox.StandardButton.Yes)
            self.message_box.show()
        else:
            self.message_box = QMessageBox(QMessageBox.Icon.Critical, "Ошибка сервера", f"Status code: {res.status_code}")
            self.message_box.show()

    def go_to_bron(self):
        self.bron_window.show()
        self.bron_window.token = read_token()
        self.close()


class RegWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("Регистрация")
        self.setLayout(layout)

        self.login_window = LoginWindow()

        # Title Label
        title = QLabel("Регистрация")
        title.setProperty("class", "heading")
        layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        # Username Label and Input
        user = QLabel("Email:")
        user.setProperty("class", "normal")
        layout.addWidget(user, 1, 0)
        self.input1 = QLineEdit()
        layout.addWidget(self.input1, 1, 1, 1, 2)

        # Password Label and Input
        pwd = QLabel("Password")
        pwd.setProperty("class", "normal")
        layout.addWidget(pwd, 2, 0)
        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input2, 2, 1, 1, 2)

        # Phone number
        phone = QLabel("Phone number")
        phone.setProperty("class", "normal")
        layout.addWidget(phone, 3, 0)
        self.input3 = QLineEdit()
        self.input3.setText("+7")
        layout.addWidget(self.input3, 3, 1, 1, 2)

        # Register and Login Buttons
        button1 = QPushButton("Register")
        button1.clicked.connect(self.register_user)
        layout.addWidget(button1, 4, 1)

    def go_to_login(self):
        self.login_window.show()
        self.close()

    def register_user(self):
        payload_data = {
            "phone_number": self.input3.text(),
            "role": "guest",
            "email": self.input1.text(),
            "password": self.input2.text(),
            "is_active": True,
            "is_superuser": False,
            "is_verified": False
        }

        res = requests.post(
            "http://127.0.0.1:8000/auth/register",
            json=payload_data
        )

        if res.status_code == 201:
            self.go_to_login()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
