from qtpy.QtCore import QUrl
from qtpy.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QMessageBox
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtNetwork import QNetworkAccessManager, QNetworkRequest

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView(self)
        self.browser.load(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        back_button = QAction("Back", self)
        back_button.triggered.connect(self.browser.back)
        toolbar.addAction(back_button)

        forward_button = QAction("Forward", self)
        forward_button.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_button)

        refresh_button = QAction("Refresh", self)
        refresh_button.triggered.connect(self.browser.reload)
        toolbar.addAction(refresh_button)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        self.network_manager = QNetworkAccessManager(self)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.load(QUrl(url))

    def download_file(self, url, file_path):
        request = QNetworkRequest(QUrl(url))
        reply = self.network_manager.get(request)

        def handle_download_complete():
            if reply.error() == QNetworkAccessManager.NoError:
                with open(file_path, 'wb') as f:
                    f.write(reply.readAll())
                QMessageBox.information(self, "Download Completed", "File downloaded successfully.")
            else:
                QMessageBox.warning(self, "Download Failed", "Error downloading file.")

            reply.deleteLater()

        reply.finished.connect(handle_download_complete)

if __name__ == "__main__":
    app = QApplication([])
    browser = Browser()
    browser.show()
    app.exec_()








