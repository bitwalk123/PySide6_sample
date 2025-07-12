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
from PySide6.QtNetwork import (
    QHostAddress,
    QTcpServer,
    QTcpSocket,
)


class TcpSocketServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client: QTcpSocket | None = None
        self.server = QTcpServer(self)
        self.server.listen(QHostAddress.SpecialAddress.Any, 12345)
        self.server.newConnection.connect(self.new_connection)

        self.resize(400, 300)
        self.setWindowTitle("Server")

        base = QWidget()
        self.setCentralWidget(base)

        layout = QVBoxLayout()
        base.setLayout(layout)

        self.tedit = tedit = QTextEdit(self)
        tedit.setStyleSheet("QTextEdit {font-family: monospace;}")
        tedit.setReadOnly(True)  # Set it to read-only for history
        layout.addWidget(tedit)

    def new_connection(self):
        self.client = self.server.nextPendingConnection()
        peerAddress = self.client.peerAddress()
        peerPort = self.client.peerPort()
        self.tedit.append(f"Connected from {peerAddress.toString()}:{peerPort}.")
        self.client.readyRead.connect(self.receive_message)

    def receive_message(self):
        msg = self.client.readAll().data().decode()
        self.tedit.append(f"Received: {msg}")
        # just for verification
        self.client.write(f"Server received: {msg}".encode())


def main():
    app = QApplication(sys.argv)
    win = TcpSocketServer()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
