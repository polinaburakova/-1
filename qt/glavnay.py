from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
import sys

from qt.registracia import RegWindow, LoginWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle('Ресторан "Мамука"')

        self.register_window = RegWindow()
        self.login_window = LoginWindow()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Добро пожаловать в ресторан Мамука! Для того, чтобы забронировать столик, пожалуйста, войдите или зарегистрируйтесь")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        layout.addWidget(self.label)

        button_reg = QPushButton("Зарегистрироваться")
        button_reg.clicked.connect(self.go_to_register)
        layout.addWidget(button_reg)

        button_login = QPushButton("Войти")
        button_login.clicked.connect(self.go_to_login)
        layout.addWidget(button_login)

    def go_to_register(self):
        self.register_window.show()
        self.close()

    def go_to_login(self):
        self.login_window.show()
        self.close()

    def update(self):
        self.label.setText("New and Updated Text")

    def get(self):
        print(self.label.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())