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


class TcpSocketClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.connected)
        self.socket.readyRead.connect(self.receive_message)

        # UI
        # self.setGeometry(600, 100, 400, 300)
        self.resize(400, 300)
        self.setWindowTitle("Client")

        # Layouts
        base = QWidget()
        self.setCentralWidget(base)

        layout = QVBoxLayout()
        base.setLayout(layout)

        but_connect = QPushButton("Connect")
        but_connect.clicked.connect(self.connect_to_server)
        layout.addWidget(but_connect)

        self.tedit = QTextEdit(self)
        self.tedit.setReadOnly(True)  # Set it to read-only for history
        layout.addWidget(self.tedit)

        self.ledit = QLineEdit(self)
        self.ledit.returnPressed.connect(self.send_message)  # Send when Return key is pressed
        form = QFormLayout()
        form.addRow("Message:", self.ledit)
        layout.addLayout(form)

    def connect_to_server(self):
        self.socket.connectToHost(QHostAddress.SpecialAddress.LocalHost, 12345)

    def connected(self):
        self.tedit.append("Connected to server.")

    def send_message(self):
        msg = self.ledit.text()
        if msg:
            self.tedit.append(f"Sent: {msg}")
            self.socket.write(msg.encode())
            self.ledit.clear()  # Clear the input field after sending

    def receive_message(self):
        msg = self.socket.readAll().data().decode()
        self.tedit.append(f"Received: {msg}")


def main():
    app = QApplication(sys.argv)
    win = TcpSocketClient()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
