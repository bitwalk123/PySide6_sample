#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://doc.qt.io/qtforpython-6.2/examples/example_widgets__codeeditor.html

import sys

from PySide6.QtCore import (
    QRect,
    QSize,
    Qt,
    Slot,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QTextFormat, QFontDatabase, QFontMetricsF,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPlainTextEdit,
    QTextEdit,
    QWidget,
)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self._editor = editor

    def sizeHint(self):
        return QSize(self._editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self._editor.lineNumberAreaPaintEvent(event)


class PlainTextEdit(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('QPlainTextEdit {background-color: white;}')
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setFontConfig()
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged[int].connect(self.updateLineNumberAreaWidth)
        self.updateRequest[QRect, int].connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    @Slot()
    def highlightCurrentLine(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)

            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def lineNumberAreaWidth(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.GlobalColor.white)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                width = self.lineNumberArea.width()
                height = self.fontMetrics().height()
                painter.drawText(0, top, width, height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

        # QPainter needs an explicit end().
        painter.end()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.lineNumberAreaWidth()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.lineNumberArea.setGeometry(rect)

    @Slot()
    def setFontConfig(self):
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.setFont(font)

        fm = QFontMetricsF(font)
        spaceWidth = fm.horizontalAdvance(' ')
        self.setTabStopDistance(spaceWidth * 4)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            width = self.lineNumberArea.width()
            self.lineNumberArea.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    @Slot()
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Simple Editor')

    def initUI(self):
        tedit = PlainTextEdit()
        self.setCentralWidget(tedit)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
