from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import QLabel


class RoundedImage(QLabel):
    def __init__(self, imagePath):
        super().__init__()
        # TODO: 圆角改成6好一些
        self.radius = 8
        self.updateImage(imagePath)

    def updateImage(self, imagePath):
        image = QPixmap(imagePath)
        width = image.width()
        height = image.height()

        ratio = height / width

        # 比例在范围内则固定长宽
        if 1.25 <= ratio <= 1.55:
            self.setFixedSize(150, 210)
        else:
            self.setFixedSize(width * 210 / height, 210)

        self.setPixmap(image)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        pixmap = self.pixmap().scaled(
            self.size() * self.devicePixelRatioF(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self.radius, self.radius)
        painter.setClipPath(path)
        painter.drawPixmap(self.rect(), pixmap)
