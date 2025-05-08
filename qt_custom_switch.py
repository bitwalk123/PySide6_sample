import sys

from PySide6.QtCore import (
    QByteArray,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    Property,
    Signal,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QPainter,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QVBoxLayout,
    QWidget,
)


# Reference:
# https://www.programcreek.com/python/?code=decred%2Ftinydecred%2Ftinydecred-master%2Ftinywallet%2Ftinywallet%2Fqutilities.py
class Switch(QAbstractButton):
    """Implementation of a clean looking toggle switch translated from
    https://stackoverflow.com/a/38102598/1124661
    QAbstractButton::setDisabled to disable
    """
    statusChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self.onBrush = QBrush(QColor("#569167"))
        self.slotBrush = QBrush(QColor("#999999"))
        self.switchBrush = self.slotBrush
        self.disabledBrush = QBrush(QColor("#666666"))
        self.on = False
        self.fullHeight = 18
        self.halfHeight = self.xPos = int(self.fullHeight / 2)
        self.fullWidth = 34
        self.setFixedWidth(self.fullWidth)
        self.slotMargin = 3
        self.slotHeight = self.fullHeight - 2 * self.slotMargin
        self.travel = self.fullWidth - self.fullHeight
        self.slotRect = QRect(
            self.slotMargin,
            self.slotMargin,
            self.fullWidth - 2 * self.slotMargin,
            self.slotHeight,
        )
        #self.animation = QPropertyAnimation(self, b'pqProp', self)
        self.animation = QPropertyAnimation(self, QByteArray(b'pqProp'), self)
        self.animation.setDuration(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def paintEvent(self, e):
        """QAbstractButton method. Paint the button.
        """
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.switchBrush if self.on else self.disabledBrush)
        painter.setOpacity(0.6)
        painter.drawRoundedRect(
            self.slotRect, self.slotHeight / 2, self.slotHeight / 2,
        )
        painter.setOpacity(1.0)
        painter.drawEllipse(
            QRect(self.xPos, 0, self.fullHeight, self.fullHeight, )
        )

    def mouseReleaseEvent(self, e):
        """Switch the button.
        """
        if e.button() == Qt.MouseButton.LeftButton:
            self.on = not self.on
            self.switchBrush = self.onBrush if self.on else self.slotBrush
            self.animation.setStartValue(self.xPos)
            self.animation.setEndValue(self.travel if self.on else 0)
            self.animation.start()
            self.statusChanged.emit(self.on)
        super().mouseReleaseEvent(e)

    def sizeHint(self):
        """Required to be implemented and return the size of the widget.
        """
        return QSize(self.fullWidth, self.fullHeight)

    def setOffset(self, o):
        """Setter for QPropertyAnimation.
        """
        self.xPos = o
        self.update()

    def getOffset(self):
        """Getter for QPropertyAnimation.
        """
        return self.xPos

    pqProp = Property(int, fget=getOffset, fset=setOffset)

    def set(self, on):
        """Set state to on, and trigger repaint.
        """
        self.on = on
        self.switchBrush = self.onBrush if on else self.slotBrush
        self.xPos = self.travel if on else 0
        self.update()


class Example(QWidget):
    """Example widget for demonstration
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Example for Switch')

        layout = QVBoxLayout()
        self.setLayout(layout)

        switch = Switch()
        switch.statusChanged.connect(self.switch_changed)
        layout.addWidget(switch)

    def switch_changed(self, status: bool):
        """for statusChanged signal
        """
        print('Switch is', status)


def main():
    """main event loop
    """
    app: QApplication = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
