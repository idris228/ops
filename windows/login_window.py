from PyQt6.QtWidgets import *

from db import auth

from windows.client_window import ClientWindow
from windows.manager_window import ManagerWindow
from windows.admin_window import AdminWindow


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Логин")

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Пароль")
        self.password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        login_btn = QPushButton("Войти")
        guest_btn = QPushButton("Войти как гость")

        login_btn.clicked.connect(self.login)
        guest_btn.clicked.connect(self.guest_login)

        layout.addWidget(self.login_edit)
        layout.addWidget(self.password_edit)
        layout.addWidget(login_btn)
        layout.addWidget(guest_btn)

    def login(self):

        user = auth(
            self.login_edit.text(),
            self.password_edit.text()
        )

        if not user:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Неверный логин или пароль"
            )
            return

        role = user["role"]

        if role == "client":
            self.window = ClientWindow(self)
        elif role == "manager":
            self.window = ManagerWindow(self)
        elif role == "admin":
            self.window = AdminWindow(self)
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Некорректная роль"
            )
            return

        self.window.show()
        self.close()
        self.login_edit.clear()
        self.password_edit.clear()

    def guest_login(self):
        self.window = ClientWindow(self)
        self.window.show()
        self.close()
        self.login_edit.clear()
        self.password_edit.clear()
