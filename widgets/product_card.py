from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from styles import CARD_STYLE, SELECTED_CARD_STYLE


class ProductCard(QFrame):

    def __init__(self, item, clickable=False):
        super().__init__()

        self.item = item
        self.selected = False
        self.clickable = clickable

        self.setStyleSheet(CARD_STYLE)
        self.setMinimumHeight(170)

        main_layout = QHBoxLayout(self)

        image_label = QLabel()
        image_label.setFixedSize(140, 120)

        pixmap = QPixmap(item.get("image_path"))

        if pixmap.isNull():
            pixmap = QPixmap("images/no_image.png")

        image_label.setPixmap(
            pixmap.scaled(
                120,
                140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        info_layout = QVBoxLayout()

        title = QLabel(
            f"{item['category']} | {item['name']}"
        )

        description = QLabel(item["description"])
        description.setWordWrap(True)

        price = QLabel(f"Цена: {item['price']}")

        stock = QLabel(
            f"Остаток: {item['stock_quantity']}"
        )

        discount = QLabel(
            f"Скидка: {item['discount']}%"
        )

        info_layout.addWidget(title)
        info_layout.addWidget(description)
        info_layout.addWidget(price)
        info_layout.addWidget(stock)
        info_layout.addWidget(discount)

        main_layout.addWidget(image_label)
        main_layout.addLayout(info_layout)

    def mousePressEvent(self, event):
        if self.clickable:
            self.selected = not self.selected
            if self.selected:
                self.setStyleSheet(SELECTED_CARD_STYLE)
            else:
                self.setStyleSheet(CARD_STYLE)
