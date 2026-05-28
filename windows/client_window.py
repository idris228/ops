from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from db import get_products
from widgets.product_card import ProductCard


class ClientWindow(QMainWindow):

    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        self.setWindowTitle("Клиент")

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)

        logout_button = QPushButton("Выйти")
        logout_button.clicked.connect(self.logout)

        layout.addWidget(logout_button, alignment=Qt.AlignmentFlag.AlignRight)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.container_layout = QVBoxLayout(container)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.load_products()

    def load_products(self):

        rows = get_products()

        for row in rows:
            card = ProductCard(row)
            self.container_layout.addWidget(card)

        self.container_layout.addStretch()

    def logout(self):
        self.close()
        self.login_window.show()
