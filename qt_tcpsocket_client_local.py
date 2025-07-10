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
from PySide6.QtNetwork import (
    QHostAddress,
    QTcpSocket,
)


class TcpSocketClientLocal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.connected)
        self.socket.readyRead.connect(self.receive_message)

        # UI
        self.resize(400, 300)
        self.setWindowTitle("Client")

        base = QWidget()
        self.setCentralWidget(base)

        layout = QVBoxLayout()
        base.setLayout(layout)

        but_connect = QPushButton("Connect")
        but_connect.clicked.connect(self.connect_to_server)
        layout.addWidget(but_connect)

        self.tedit = tedit = QTextEdit(self)
        tedit.setStyleSheet("QTextEdit {font-family: monospace;}")
        tedit.setReadOnly(True)  # Set it to read-only for history
        layout.addWidget(tedit)

        self.ledit = ledit = QLineEdit(self)
        ledit.returnPressed.connect(self.send_message)  # Send when Return key is pressed
        form = QFormLayout()
        form.addRow("Message:", ledit)
        layout.addLayout(form)

    def connect_to_server(self):
        self.socket.connectToHost(QHostAddress.SpecialAddress.LocalHost, 12345)

    def connected(self):
        self.tedit.append("Connected to server.")

    def receive_message(self):
        msg = self.socket.readAll().data().decode()
        self.tedit.append(f"Received: {msg}")

    def send_message(self):
        msg = self.ledit.text()
        if msg:
            self.tedit.append(f"Sent: {msg}")
            self.socket.write(msg.encode())
            self.ledit.clear()  # Clear the input field after sending


def main():
    app = QApplication(sys.argv)
    win = TcpSocketClientLocal()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
