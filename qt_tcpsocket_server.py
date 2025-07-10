# Reference:
# https://github.com/bhowiebkr/client-server-socket-example/
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtNetwork import QHostAddress, QTcpServer


class TcpSocketServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client_connection = None
        self.server = QTcpServer(self)
        self.server.listen(QHostAddress.SpecialAddress.LocalHost, 12345)
        self.server.newConnection.connect(self.new_connection)

        self.resize(400, 300)
        self.setWindowTitle("Server")

        base = QWidget()
        self.setCentralWidget(base)

        layout = QVBoxLayout()
        base.setLayout(layout)

        self.tedit = QTextEdit(self)
        self.tedit.setReadOnly(True)  # Set it to read-only for history
        layout.addWidget(self.tedit)

    def new_connection(self):
        self.client_connection = self.server.nextPendingConnection()
        self.client_connection.readyRead.connect(self.receive_message)

    def receive_message(self):
        msg = self.client_connection.readAll().data().decode()
        self.tedit.append(f"Received: {msg}")
        self.client_connection.write(f"Server received: {msg}".encode())


def main():
    app = QApplication(sys.argv)
    win = TcpSocketServer()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
