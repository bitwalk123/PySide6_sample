# Reference:
# https://github.com/bhowiebkr/client-server-socket-example/
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtNetwork import QHostAddress, QTcpSocket


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.connected)
        self.socket.readyRead.connect(self.receiveMessage)

        # UI
        self.setGeometry(600, 100, 400, 300)
        self.setWindowTitle("Client")

        # Layouts
        layout = QVBoxLayout()
        self.setLayout(layout)
        base = QWidget()
        base.setLayout(layout)
        self.setCentralWidget(base)
        form = QFormLayout()

        # Widgets
        but_connect = QPushButton("Connect")
        but_connect.clicked.connect(self.connect)

        self.tedit = QTextEdit(self)
        self.tedit.setReadOnly(True)  # Set it to read-only for history

        self.ledit = QLineEdit(self)
        self.ledit.returnPressed.connect(self.sendMessage)  # Send when Return key is pressed

        # Add Widgets
        form.addRow("Message:", self.ledit)
        layout.addWidget(self.tedit)
        layout.addLayout(form)
        layout.addWidget(but_connect)

    def connect(self):
        self.socket.connectToHost(QHostAddress.SpecialAddress.LocalHost, 12345)

    def connected(self):
        self.tedit.append("Connected to server.")

    def sendMessage(self):
        message = self.ledit.text()
        if message:
            self.tedit.append(f"Sent: {message}")
            self.socket.write(message.encode())
            self.ledit.clear()  # Clear the input field after sending

    def receiveMessage(self):
        message = self.socket.readAll().data().decode()
        self.tedit.append(f"Received: {message}")


def main():
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
