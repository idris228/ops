from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from db import get_products, get_orders
from widgets.product_card import ProductCard
from widgets.order_card import OrderCard


class ManagerWindow(QMainWindow):

    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        self.setWindowTitle("Менеджер")

        tabs = QTabWidget()

        tabs.addTab(self.create_products_tab(), "Товары")
        tabs.addTab(self.create_orders_tab(), "Заказы")

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        self.setCentralWidget(main_widget)

        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.logout)

        main_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(tabs)

    def logout(self):
        self.close()
        self.login_window.show()

    def create_products_tab(self):

        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск")

        self.sort_box = QComboBox()
        self.sort_box.addItems([
            "Без сортировки",
            "Цена по возрастанию",
            "Цена по убыванию"
        ])

        btn = QPushButton("Найти")
        btn.clicked.connect(self.load_products)

        top = QHBoxLayout()
        top.addWidget(self.search_edit)
        top.addWidget(self.sort_box)
        top.addWidget(btn)

        layout.addLayout(top)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.products_container = QWidget()
        self.products_layout = QVBoxLayout(
            self.products_container
        )

        scroll.setWidget(self.products_container)

        layout.addWidget(scroll)

        self.load_products()

        return widget

    def load_products(self):

        while self.products_layout.count():
            child = self.products_layout.takeAt(0)

            if child.widget():
                child.widget().deleteLater()

        sort = ""

        if self.sort_box.currentIndex() == 1:
            sort = "price_asc"

        elif self.sort_box.currentIndex() == 2:
            sort = "price_desc"

        rows = get_products(
            self.search_edit.text(),
            sort
        )

        for row in rows:
            self.products_layout.addWidget(
                ProductCard(row)
            )

    def create_orders_tab(self):

        widget = QWidget()

        layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()

        cards_layout = QVBoxLayout(container)

        rows = get_orders()

        for row in rows:
            cards_layout.addWidget(
                OrderCard(row)
            )

        scroll.setWidget(container)

        layout.addWidget(scroll)

        return widget
