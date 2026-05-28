from PyQt6.QtWidgets import *

from styles import CARD_STYLE, SELECTED_CARD_STYLE


class OrderCard(QFrame):

    def __init__(self, item, clickable=False):
        super().__init__()

        self.item = item
        self.selected = False
        self.clickable = clickable

        self.setStyleSheet(CARD_STYLE)
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Клиент: {item['client_name']}"))
        layout.addWidget(QLabel(f"Товар: {item['product_name']}"))
        layout.addWidget(QLabel(f"Количество: {item['quantity']}"))
        layout.addWidget(QLabel(f"Сумма: {item['total_price']}"))
        layout.addWidget(QLabel(f"Статус: {item['status']}"))

    def mousePressEvent(self, event):
        if self.clickable:
            self.selected = not self.selected
            if self.selected:
                self.setStyleSheet(SELECTED_CARD_STYLE)
            else:
                self.setStyleSheet(CARD_STYLE)
