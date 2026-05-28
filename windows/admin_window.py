from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from db import *
from widgets.product_card import ProductCard
from widgets.order_card import OrderCard


class AdminWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        self.product_cards = []
        self.order_cards = []

        self.setWindowTitle("Админ")
        self.resize(1200, 700)

        tabs = QTabWidget()
        tabs.addTab(self.products_tab(), "Товары")
        tabs.addTab(self.orders_tab(), "Заказы")

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.logout)

        main_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(tabs)

        self.setCentralWidget(main_widget)

    def logout(self):
        self.close()
        self.login_window.show()

    def products_tab(self):

        widget = QWidget()
        layout = QVBoxLayout(widget)

        tools = QHBoxLayout()

        self.add_product_btn = QPushButton("Добавить")
        self.edit_product_btn = QPushButton("Изменить")
        self.delete_product_btn = QPushButton("Удалить")

        self.add_product_btn.clicked.connect(self.add_product)
        self.edit_product_btn.clicked.connect(self.edit_product)
        self.delete_product_btn.clicked.connect(self.delete_product)

        tools.addWidget(self.add_product_btn)
        tools.addWidget(self.edit_product_btn)
        tools.addWidget(self.delete_product_btn)

        layout.addLayout(tools)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.products_layout = QVBoxLayout(container)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.load_products()

        return widget

    def load_products(self):

        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.product_cards.clear()

        rows = get_products()

        for row in rows:
            card = ProductCard(row, clickable=True)
            self.product_cards.append(card)
            self.products_layout.addWidget(card)

        self.products_layout.addStretch()

    def get_selected_product(self):

        for card in self.product_cards:
            if card.selected:
                return card.item
        return None

    def product_dialog(self, item=None):

        dialog = QDialog(self)
        dialog.setWindowTitle("Товар")

        layout = QFormLayout(dialog)

        category = QLineEdit(item["category"] if item else "")
        name = QLineEdit(item["name"] if item else "")
        description = QLineEdit(item["description"] if item else "")
        manufacturer = QLineEdit(item["manufacturer"] if item else "")
        supplier = QLineEdit(item["supplier"] if item else "")

        price = QSpinBox()
        stock = QSpinBox()
        discount = QSpinBox()

        image = QLineEdit(item["image_path"] if item else "")

        price.setMaximum(10**9)
        stock.setMaximum(10**6)
        discount.setMaximum(100)

        if item:
            price.setValue(item["price"])
            stock.setValue(item["stock_quantity"])
            discount.setValue(item["discount"])

        layout.addRow("Категория", category)
        layout.addRow("Название", name)
        layout.addRow("Описание", description)
        layout.addRow("Производитель", manufacturer)
        layout.addRow("Поставщик", supplier)
        layout.addRow("Цена", price)
        layout.addRow("Остаток", stock)
        layout.addRow("Скидка", discount)
        layout.addRow("Картинка", image)

        save_btn = QPushButton("Сохранить")
        layout.addRow(save_btn)

        data = {}

        def save():
            data.update({
                "category": category.text(),
                "name": name.text(),
                "description": description.text(),
                "manufacturer": manufacturer.text(),
                "supplier": supplier.text(),
                "price": price.value(),
                "stock_quantity": stock.value(),
                "discount": discount.value(),
                "image_path": image.text()
            })
            dialog.accept()

        save_btn.clicked.connect(save)

        if dialog.exec():
            return data

        return None

    def add_product(self):

        data = self.product_dialog()
        if not data:
            return

        add_product(data)
        self.load_products()

    def edit_product(self):

        item = self.get_selected_product()

        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите товар")
            return

        data = self.product_dialog(item)

        if not data:
            return

        update_product(item["id"], data)
        self.load_products()

    def delete_product(self):

        item = self.get_selected_product()

        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите товар")
            return

        delete_product(item["id"])
        self.load_products()

    def orders_tab(self):

        widget = QWidget()
        layout = QVBoxLayout(widget)

        tools = QHBoxLayout()

        self.add_order_btn = QPushButton("Добавить")
        self.edit_order_btn = QPushButton("Изменить")
        self.delete_order_btn = QPushButton("Удалить")

        self.add_order_btn.clicked.connect(self.add_order)
        self.edit_order_btn.clicked.connect(self.edit_order)
        self.delete_order_btn.clicked.connect(self.delete_order)

        tools.addWidget(self.add_order_btn)
        tools.addWidget(self.edit_order_btn)
        tools.addWidget(self.delete_order_btn)

        layout.addLayout(tools)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.orders_layout = QVBoxLayout(container)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.load_orders()

        return widget

    def load_orders(self):

        while self.orders_layout.count():
            item = self.orders_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.order_cards.clear()

        rows = get_orders()

        for row in rows:
            card = OrderCard(row, clickable=True)
            self.order_cards.append(card)
            self.orders_layout.addWidget(card)

        self.orders_layout.addStretch()

    def get_selected_order(self):

        for card in self.order_cards:
            if card.selected:
                return card.item
        return None

    def order_dialog(self, item=None):

        dialog = QDialog(self)
        dialog.setWindowTitle("Заказ")

        layout = QFormLayout(dialog)

        user_id = QSpinBox()
        product_id = QSpinBox()
        quantity = QSpinBox()
        total_price = QSpinBox()
        status = QLineEdit()

        user_id.setMaximum(10**9)
        product_id.setMaximum(10**9)
        quantity.setMaximum(10**6)
        total_price.setMaximum(10**9)

        if item:
            user_id.setValue(item["user_id"])
            product_id.setValue(item["product_id"])
            quantity.setValue(item["quantity"])
            total_price.setValue(item["total_price"])
            status.setText(item["status"])

        layout.addRow("User ID", user_id)
        layout.addRow("Product ID", product_id)
        layout.addRow("Количество", quantity)
        layout.addRow("Сумма", total_price)
        layout.addRow("Статус", status)

        save_btn = QPushButton("Сохранить")
        layout.addRow(save_btn)

        data = {}

        def save():
            data.update({
                "user_id": user_id.value(),
                "product_id": product_id.value(),
                "quantity": quantity.value(),
                "total_price": total_price.value(),
                "status": status.text()
            })
            dialog.accept()

        save_btn.clicked.connect(save)

        if dialog.exec():
            return data

        return None

    def add_order(self):

        data = self.order_dialog()
        if not data:
            return

        add_order(data)
        self.load_orders()

    def edit_order(self):

        item = self.get_selected_order()

        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return

        data = self.order_dialog(item)

        if not data:
            return

        update_order(item["id"], data)
        self.load_orders()

    def delete_order(self):

        item = self.get_selected_order()

        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return

        delete_order(item["id"])
        self.load_orders()
