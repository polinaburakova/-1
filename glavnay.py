from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle('Ресторан "Мамука"')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Добро пожаловать в ресторан Мамука! Для того, чтобы забронировать столик, пожалуйста, войдите или зарегистрируйтесь")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        layout.addWidget(self.label)

        button = QPushButton("Зарегистрироваться")
        button.clicked.connect(self.update)
        layout.addWidget(button)

        button = QPushButton("Войти")
        button.clicked.connect(self.get)
        layout.addWidget(button)

    def update(self):
        self.label.setText("New and Updated Text")

    def get(self):
        print(self.label.text())

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())