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


class Server(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server = QTcpServer(self)
        self.server.listen(QHostAddress.SpecialAddress.LocalHost, 12345)
        self.server.newConnection.connect(self.newConnection)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Server")
        self.tedit = QTextEdit(self)
        self.tedit.setReadOnly(True)  # Set it to read-only for history

        base = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tedit)
        base.setLayout(layout)
        self.setCentralWidget(base)

    def newConnection(self):
        self.client_connection = self.server.nextPendingConnection()
        self.client_connection.readyRead.connect(self.receiveMessage)

    def receiveMessage(self):
        message = self.client_connection.readAll().data().decode()
        self.tedit.append(f"Received: {message}")
        self.client_connection.write(f"Server received: {message}".encode())


def main():
    app = QApplication(sys.argv)
    server = Server()
    server.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
