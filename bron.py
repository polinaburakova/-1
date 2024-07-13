import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit

class Window(QWidget):
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

        # Username Label and Input
        user = QLabel("Количество гостей")
        user.setProperty("class", "normal")
        layout.addWidget(user, 1, 0)
        self.input1 = QLineEdit()
        layout.addWidget(self.input1, 1, 1, 1, 2)

        user = QLabel("Время")
        user.setProperty("class", "normal")
        layout.addWidget(user, 2, 0)
        self.input2 = QLineEdit()
        layout.addWidget(self.input2, 2, 1, 1, 2)

        # Password Label and Input
        user = QLabel("Дата")
        user.setProperty("class", "normal")
        layout.addWidget(user, 3, 0)
        self.input3 = QLineEdit()
        layout.addWidget(self.input3, 3, 1, 1, 2)

        # Register and Login Buttons
        button1 = QPushButton("Забронировать")
        layout.addWidget(button1, 4, 1)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())